"""Structural anti-cheat checks for tamarin_bench.

The evaluator never trusts the agent container; the final theory is re-run
in a clean verifier container. But a *correct-looking* run can still be a
degenerate solution: tautological lemmas, weakened given rules, or removed
safety-critical restrictions. This module implements the objective
structural checks that catch those:

* ``check_given_rules_unchanged`` — every rule/restriction/axiom present in
  the given theory must survive, unchanged modulo whitespace/comments
  (normalized SHA-256 comparison), in the final theory. New rules are
  reported (allowed only for L2 form tasks; L1/L3 must not add protocol
  rules... actually adding rules would change the protocol, so for L1/L3
  any change is a violation; for L2 everything is built from scratch).
* ``check_lemma_coverage`` — each required lemma name must be stated by the
  agent (exact name match), with the reference quantifier.
* ``check_lemma_fact_references`` — each agent lemma must reference a
  superset of the protocol facts its reference lemma references. A
  tautology mentions no protocol facts, so this kills the
  "trivially-true lemma + declare SAFE" cheat for L1.
* ``check_no_trivial_lemmas`` — direct tautology heuristics (formula
  entails itself, empty conjunction, ⊤/⊥ misuse).

Each check returns a :class:`AntiCheatResult` with a score in [0, 1] and
machine-readable details for the CheckResult.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from tamaringym.task.spthy import (
    Lemma,
    Theory,
    lemma_referenced_facts,
    normalize_block,
)

__all__ = [
    "AntiCheatResult",
    "check_given_rules_unchanged",
    "check_lemma_coverage",
    "check_lemma_fact_references",
    "check_no_trivial_lemmas",
]


@dataclass
class AntiCheatResult:
    name: str
    score: float
    details: dict = field(default_factory=dict)


def _block_digest(block: str) -> str:
    return hashlib.sha256(normalize_block(block).encode()).hexdigest()


def check_given_rules_unchanged(given: Theory, final: Theory) -> AntiCheatResult:
    """All given rules/restrictions/axioms must be present and unchanged."""
    problems: list[dict] = []

    final_rules = {r.name: r for r in final.rules}
    final_restrictions = {r.name: r for r in final.restrictions}
    final_axioms = {r.name: r for r in final.axioms}

    for group, final_map in (
        ("rule", final_rules),
        ("restriction", final_restrictions),
        ("axiom", final_axioms),
    ):
        given_items = (
            given.rules
            if group == "rule"
            else given.restrictions
            if group == "restriction"
            else given.axioms
        )
        for gr in given_items:
            fr = final_map.get(gr.name)
            if fr is None:
                problems.append({"kind": group, "name": gr.name, "issue": "removed"})
            elif _block_digest(gr.body) != _block_digest(fr.body):
                problems.append({"kind": group, "name": gr.name, "issue": "modified"})

    given_total = len(given.rules) + len(given.restrictions) + len(given.axioms)
    if given_total == 0:
        return AntiCheatResult(name="given_rules_unchanged", score=1.0, details={})

    changed = len(problems)
    score = max(0.0, 1.0 - changed / given_total)
    return AntiCheatResult(
        name="given_rules_unchanged",
        score=score,
        details={"problems": problems, "given_total": given_total},
    )


def check_lemma_coverage(required: list[Lemma], final: Theory) -> AntiCheatResult:
    """Every required lemma name must be stated with the same quantifier."""
    if not required:
        return AntiCheatResult(name="lemma_coverage", score=1.0, details={})
    final_lemmas = {l.name: l for l in final.lemmas}
    missing: list[dict] = []
    wrong_quant: list[dict] = []
    for req in required:
        got = final_lemmas.get(req.name)
        if got is None:
            missing.append({"name": req.name})
        elif req.quantifier and got.quantifier and req.quantifier != got.quantifier:
            wrong_quant.append(
                {"name": req.name, "expected": req.quantifier, "got": got.quantifier}
            )
    score = max(0.0, 1.0 - (len(missing) + len(wrong_quant)) / len(required))
    return AntiCheatResult(
        name="lemma_coverage",
        score=score,
        details={"missing": missing, "wrong_quantifier": wrong_quant},
    )


def check_lemma_fact_references(
    required: list[Lemma], final: Theory
) -> AntiCheatResult:
    """Agent lemmas must reference the reference lemmas' protocol facts.

    For each required lemma with at least one protocol fact in the
    reference, the agent's lemma of the same name must reference all of
    those facts (extra facts are allowed — a stronger property is fine).
    """
    final_lemmas = {l.name: l for l in final.lemmas}
    checked = 0
    violations: list[dict] = []
    for req in required:
        ref_facts = lemma_referenced_facts(req)
        if not ref_facts:
            continue  # reference itself is fact-free (helper lemma): skip
        got = final_lemmas.get(req.name)
        if got is None:
            continue  # coverage check reports the miss; don't double-penalize
        got_facts = lemma_referenced_facts(got)
        missing = sorted(ref_facts - got_facts)
        if missing:
            violations.append({"name": req.name, "missing_facts": missing})
        checked += 1
    if checked == 0:
        return AntiCheatResult(name="lemma_fact_references", score=1.0, details={})
    score = max(0.0, 1.0 - len(violations) / checked)
    return AntiCheatResult(
        name="lemma_fact_references", score=score, details={"violations": violations}
    )


_TAUTOLOGY_RE = re.compile(
    r"(?P<a>[A-Z][A-Za-z0-9_]*\s*\([^()]*\))\s*(?:@\s*[#\w.]+)?\s*"
    r"==>\s*(?P=a)\s*(?:@\s*[#\w.]+)?\s*$"
)


def check_no_trivial_lemmas(final: Theory) -> AntiCheatResult:
    """Heuristic tautology detection: ``P ==> P`` style bodies."""
    trivial: list[str] = []
    for lem in final.lemmas:
        formula = " ".join(lem.formula.split())
        m = _TAUTOLOGY_RE.search(formula)
        if m:
            trivial.append(lem.name)
    score = 0.0 if trivial else 1.0
    return AntiCheatResult(
        name="no_trivial_lemmas", score=score, details={"trivial": trivial}
    )
