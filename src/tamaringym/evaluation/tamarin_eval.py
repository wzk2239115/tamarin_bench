"""The Tamarin task evaluator: scoring pipeline for all three levels.

Scoring stages (each a :class:`CheckResult` with an explicit weight):

==========================  ======  =========================================
check                       weight  meaning
==========================  ======  =========================================
outputs_present             0.05    final.spthy + verdict.json exist
parses                      0.10    Tamarin accepts the theory (summary found)
wellformed                  0.05    no wellformedness failures
given_rules_unchanged       0.15    L1/L3: given rules intact (L2: reference
                                    rule-name coverage)
lemma_coverage              0.10    every goal stated with the right name
lemma_fact_references       0.10    lemmas reference the reference facts
no_trivial_lemmas           0.05    no P ==> P style bodies
verdict_match               0.25    per-lemma verdicts vs ground truth
attack_trace_match          0.10    falsified lemma traces vs ground truth
                                    traces (multiset overlap)
attack_report_match         0.05    report cites the reference trace rules
==========================  ======  =========================================

The verdict/attack checks run against a **fresh Tamarin re-run of the
agent's final.spthy in the verifier container** — the agent's own claims
are never trusted.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from tamaringym.evaluation.anticheat import (
    check_given_rules_unchanged,
    check_lemma_coverage,
    check_lemma_fact_references,
    check_no_trivial_lemmas,
)
from tamaringym.evaluation.tamarin_runner import run_tamarin_in_docker
from tamaringym.evaluation.types import CheckResult, EvalConfig
from tamaringym.evaluation.verifier import trace_rule_multiset
from tamaringym.task.metadata import GroundTruth, TaskMeta, task_dir_for
from tamaringym.task.spthy import SpthyParseError, parse_theory

logger = logging.getLogger(__name__)


def _load_verdict_json(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            return data
    except (OSError, json.JSONDecodeError):
        return None
    return None


def _attack_report_rule_coverage(
    report_path: Path, reference_rules: list[str]
) -> float:
    """Fraction of reference trace rules cited in the attack report."""
    if not report_path.is_file() or not reference_rules:
        return 0.0
    text = report_path.read_text(errors="replace")
    hit = sum(1 for r in set(reference_rules) if r in text)
    return hit / len(set(reference_rules))


class TamarinScorer:
    """Pure scoring logic, separable from container orchestration."""

    def __init__(
        self, config: EvalConfig, meta: TaskMeta, ground_truth: GroundTruth
    ) -> None:
        self.config = config
        self.meta = meta
        self.gt = ground_truth

    def score(self, outputs_dir: Path) -> list[CheckResult]:
        checks: list[CheckResult] = []
        final_spthy = outputs_dir / "final.spthy"
        verdict_json = _load_verdict_json(outputs_dir / "verdict.json")
        attack_report = outputs_dir / "attack_report.md"
        tdir = task_dir_for(self.meta.task_id)

        # 1. outputs present
        checks.append(
            CheckResult(
                name="outputs_present",
                score=1.0
                if (final_spthy.is_file() and verdict_json is not None)
                else 0.0,
                weight=0.05,
                details={
                    "final_spthy": final_spthy.is_file(),
                    "verdict_json": verdict_json is not None,
                },
            )
        )
        if not final_spthy.is_file():
            return checks

        # structural parse of the agent's theory
        try:
            final_theory = parse_theory(final_spthy.read_text(errors="replace"))
        except SpthyParseError as e:
            final_theory = None
            logger.info("final.spthy failed structural parse: %s", e)

        # reference theory (solution) for structural checks
        solution_path = tdir / "solution" / "solution.spthy"
        ref_theory = parse_theory(solution_path.read_text(errors="replace"))

        # given theory (L1) or broken theory (L3)
        given_theory = None
        for fname, kind in (("theory.spthy", "L1"), ("broken.spthy", "L3")):
            p = tdir / fname
            if p.is_file() and self.meta.level.startswith(kind):
                given_theory = parse_theory(p.read_text(errors="replace"))
                break

        # 2/3. run Tamarin in a clean verifier container
        rerun = run_tamarin_in_docker(
            final_spthy,
            image=self.config.verifier_image,
            timeout_s=self.config.verify_timeout_seconds,
            known_lemma_names=[l.name for l in ref_theory.lemmas] or None,
        )
        checks.append(
            CheckResult(
                name="parses",
                score=1.0 if rerun.ok else 0.0,
                weight=0.10,
                details={"exit_code": rerun.exit_code, "timeout": rerun.timeout},
            )
        )
        # 3. wellformedness — compared against the reference state: several
        # corpus theories carry inherent derivation-check warnings that cannot
        # be fixed without modifying the (frozen) rules; reproducing the
        # reference's state is full credit.
        wf_ok = rerun.parsed.get("wellformedness_ok")
        if wf_ok is None:
            wf_score = 1.0  # tamarin emitted no signal — do not penalize
        elif wf_ok:
            wf_score = 1.0
        else:
            wf_score = 1.0 if self.gt.wellformedness_ok is False else 0.0
        checks.append(
            CheckResult(
                name="wellformed",
                score=wf_score,
                weight=0.05,
                details={
                    "wellformedness_ok": wf_ok,
                    "reference_ok": self.gt.wellformedness_ok,
                },
            )
        )

        # 4. structural anti-cheat
        if final_theory is not None:
            if given_theory is not None:
                # L1: given rules must survive unchanged in the final theory.
                # L3: the repair target is the REFERENCE rules — the final
                # theory must restore them.
                base = given_theory if self.meta.level == "L1_verdict" else ref_theory
                r = check_given_rules_unchanged(base, final_theory)
            else:
                # L2: structural fidelity = fraction of reference rule names
                # present in the agent's theory
                ref_names = {r.name for r in ref_theory.rules}
                got_names = {r.name for r in final_theory.rules}
                overlap = len(ref_names & got_names) / max(len(ref_names), 1)
                from tamaringym.evaluation.anticheat import AntiCheatResult

                r = AntiCheatResult(
                    name="given_rules_unchanged",
                    score=overlap,
                    details={
                        "reference_rules": len(ref_names),
                        "matched": len(ref_names & got_names),
                    },
                )
            checks.append(
                CheckResult(name=r.name, score=r.score, weight=0.15, details=r.details)
            )

            # 5-7. lemma checks
            cov = check_lemma_coverage(ref_theory.lemmas, final_theory)
            checks.append(
                CheckResult(
                    name=cov.name, score=cov.score, weight=0.10, details=cov.details
                )
            )
            facts = check_lemma_fact_references(ref_theory.lemmas, final_theory)
            checks.append(
                CheckResult(
                    name=facts.name,
                    score=facts.score,
                    weight=0.10,
                    details=facts.details,
                )
            )
            trivial = check_no_trivial_lemmas(final_theory)
            checks.append(
                CheckResult(
                    name=trivial.name,
                    score=trivial.score,
                    weight=0.05,
                    details=trivial.details,
                )
            )

        # 8. verdict match — re-run verdicts vs ground truth
        run_verdicts = {name: verdict for name, _q, verdict, _s in rerun.lemmas}
        gt_verdicts = {l.name: l.verdict for l in self.gt.lemmas}
        if gt_verdicts:
            matched = sum(
                1
                for name, expected in gt_verdicts.items()
                if run_verdicts.get(name) == expected
            )
            verdict_score = matched / len(gt_verdicts)
        else:
            verdict_score = 0.0
        checks.append(
            CheckResult(
                name="verdict_match",
                score=verdict_score,
                weight=0.25,
                details={
                    "ground_truth": gt_verdicts,
                    "rerun": run_verdicts,
                    "agent_claim": (verdict_json or {}).get("lemmas"),
                },
            )
        )

        # 9. attack trace match (only falsified-with-trace lemmas)
        falsified_gt = {
            l.name
            for l in self.gt.lemmas
            if l.verdict == "falsified" and l.name in self.gt.attack_traces
        }
        if falsified_gt:
            scores = []
            details = {}
            for lemma in falsified_gt:
                ref_ms = trace_rule_multiset(self.gt.attack_traces[lemma])
                got_traces = rerun.traces.get(lemma, [])
                got_ms = trace_rule_multiset(got_traces)
                if not ref_ms:
                    continue
                # multiset overlap ratio (Jaccard-style on counts)
                inter = sum(
                    (min(ref_ms[r], got_ms[r]) for r in ref_ms if r in got_ms),
                    start=0,
                )
                union = sum(
                    max(ref_ms[r], got_ms.get(r, 0)) for r in set(ref_ms) | set(got_ms)
                )
                scores.append(inter / union if union else 0.0)
                details[lemma] = {
                    "reference_rules": sorted(ref_ms),
                    "rerun_rules": sorted(got_ms),
                }
            attack_score = sum(scores) / len(scores) if scores else 0.0
            checks.append(
                CheckResult(
                    name="attack_trace_match",
                    score=attack_score,
                    weight=0.10,
                    details=details,
                )
            )
            # 10. attack report
            if self.gt.overall_verdict == "UNSAFE":
                all_ref_rules: list[str] = []
                for lemma in falsified_gt:
                    for seq in self.gt.attack_traces[lemma]:
                        all_ref_rules.extend(seq)
                report_score = _attack_report_rule_coverage(
                    attack_report, all_ref_rules
                )
                checks.append(
                    CheckResult(
                        name="attack_report_match",
                        score=report_score,
                        weight=0.05,
                        details={"report_exists": attack_report.is_file()},
                    )
                )

        # persist the re-run summary for debugging
        try:
            (outputs_dir / "rerun_summary.json").write_text(
                json.dumps(rerun.summary_dict(), indent=2), encoding="utf-8"
            )
        except OSError:
            logger.warning("could not write rerun summary")

        return checks
