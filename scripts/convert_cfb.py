#!/usr/bin/env python3
"""Convert CrypFormBench spthy datasets into ProtocolBench task directories.

Reads (from --cfb-dir, default ~/projects/CrypFormBench):

* datasets/completion/spthy_com_datasets_data_eng_100.json  (51 complete theories)
* datasets/generation/spthy_datasets_data_eng_100.json      (NL specs + verdict summaries)
* datasets/correction/spthy_corr_error_datasets_data_eng_100.json (broken theories)
* datasets/correction/spthy_corr_false_datasets_data_eng_100.json (falsely-passing theories)

Produces under data/tasks/:

* L1_verdict/<name>/  — theory.spthy (lemmas stripped) + goals.md + solution/
* L2_form/<name>/     — spec.md (NL only) + solution/   [10 attack-bearing protocols]
* L3_repair/<name>/   — broken.spthy + error_hint.txt + solution/ [10 chosen]

plus data/task_ids/v0.txt (all tasks) and sample.txt (smoke-test subset).

Ground-truth verdicts are seeded from CrypFormBench's stored summaries but
MUST be re-validated with scripts/validate_tasks.py (real Tamarin runs)
before any evaluation; the seeded entries are marked validated=false.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tamaringym.task.metadata import GroundTruth, LemmaTruth, TaskMeta  # noqa: E402
from tamaringym.task.spthy import (  # noqa: E402
    parse_theory,
    strip_lemmas,
)

_VERDICT_RE = re.compile(
    r"^\s+(?P<name>\S+)\s+\((?P<quant>all-traces|exists-trace|trace)\):\s+"
    r"(?P<verdict>verified|falsified - found trace|incomplete|processing error)"
    r"(?:\s+\((?P<steps>\d+) steps?\))?",
    re.M,
)


def _find_summary(obj) -> str | None:
    if isinstance(obj, str) and "analyzed:" in obj:
        return obj
    if isinstance(obj, list):
        for x in obj:
            found = _find_summary(x)
            if found:
                return found
    if isinstance(obj, dict):
        for x in obj.values():
            found = _find_summary(x)
            if found:
                return found
    return None


def parse_summary_verdicts(results) -> dict[str, dict]:
    summary = _find_summary(results)
    if not summary:
        return {}
    out: dict[str, dict] = {}
    for m in _VERDICT_RE.finditer(summary):
        out[m.group("name")] = {
            "quantifier": m.group("quant"),
            "verdict": m.group("verdict"),
            "steps": int(m.group("steps")) if m.group("steps") else None,
        }
    return out


def humanize(name: str) -> str:
    parts = re.split(r"[_\-\s]+", name)
    return " ".join(p for p in parts if p).lower()


def load_cfb(cfb_dir: Path) -> dict[str, dict]:
    """file -> {code, logic, results, source} with correction files merged in."""
    table: dict[str, dict] = {}

    gen = json.loads(
        (cfb_dir / "datasets/generation/spthy_datasets_data_eng_100.json").read_text()
    )
    for item in gen:
        table[item["file"]] = {
            "logic": item.get("logic", ""),
            "results": item.get("results"),
            "code": None,
            "source": "generation",
        }

    comp = json.loads(
        (
            cfb_dir / "datasets/completion/spthy_com_datasets_data_eng_100.json"
        ).read_text()
    )
    for item in comp:
        if item["file"] in table:
            table[item["file"]]["code"] = item["complete:"]
        else:
            table[item["file"]] = {
                "logic": "",
                "results": None,
                "code": item["complete:"],
                "source": "completion",
            }

    corr_variants: dict[str, dict] = {}
    for kind, fname, code_key in (
        ("error", "spthy_corr_error_datasets_data_eng_100.json", "errorcode"),
        ("false", "spthy_corr_false_datasets_data_eng_100.json", "falsecode"),
    ):
        data = json.loads((cfb_dir / "datasets/correction" / fname).read_text())
        for item in data:
            entry = corr_variants.setdefault(item["file"], {})
            entry[f"{kind}_code"] = item[code_key]
            entry[f"{kind}_info"] = item.get("errorinfo") or item.get("falseinfo") or ""
            if "logic" not in entry and item.get("logic"):
                entry["logic"] = item["logic"]
            if "code" not in entry and item.get("code"):
                entry["code"] = item["code"]
            if "results" not in entry and item.get("results"):
                entry["results"] = item["results"]

    for fname, entry in corr_variants.items():
        if fname not in table:
            table[fname] = {
                "logic": entry.get("logic", ""),
                "results": entry.get("results"),
                "code": entry.get("code"),
                "source": "correction",
                "corr": entry,
            }
        else:
            # generation/completion entry exists; merge correction extras
            table[fname]["corr"] = entry
            if not table[fname]["code"] and entry.get("code"):
                table[fname]["code"] = entry["code"]
            if not table[fname]["logic"] and entry.get("logic"):
                table[fname]["logic"] = entry["logic"]
            if not table[fname]["results"] and entry.get("results"):
                table[fname]["results"] = entry["results"]

    # resolve reference code: correction `code` field wins for its files
    for fname, entry in corr_variants.items():
        if entry.get("code"):
            table[fname]["code"] = entry["code"]
            table[fname]["source"] = "correction"
    return table


def seed_ground_truth(name: str, code: str, results) -> GroundTruth:
    """Build the pre-validation ground truth from CrypFormBench summaries."""
    theory = parse_theory(code)
    verdicts = parse_summary_verdicts(results) if results else {}
    lemmas = []
    any_falsified = False
    for lem in theory.lemmas:
        v = verdicts.get(lem.name, {})
        verdict = v.get("verdict", "unknown")
        if verdict == "falsified - found trace":
            any_falsified = True
        lemmas.append(
            LemmaTruth(
                name=lem.name,
                quantifier=lem.quantifier or "all-traces",
                verdict=verdict,
                steps=v.get("steps"),
            )
        )
    overall = "UNSAFE" if any_falsified else ("SAFE" if lemmas else "UNKNOWN")
    return GroundTruth(
        protocol=name,
        overall_verdict=overall,
        lemmas=lemmas,
        tamarin_version="seeded-from-crypformbench",
        validated=False,
    )


def write_task(
    *,
    level: str,
    name: str,
    meta: TaskMeta,
    workspace_files: dict[str, str],
    solution_spthy: str,
    ground_truth: GroundTruth,
    tasks_root: Path,
) -> Path:
    tdir = tasks_root / level / name
    if tdir.exists():
        raise FileExistsError(f"task dir already exists: {tdir} (use --force)")
    (tdir / "solution").mkdir(parents=True)
    for fname, content in workspace_files.items():
        (tdir / fname).write_text(content, encoding="utf-8")
    (tdir / "solution" / "solution.spthy").write_text(solution_spthy, encoding="utf-8")
    (tdir / "solution" / "ground_truth.json").write_text(
        ground_truth.model_dump_json(indent=2), encoding="utf-8"
    )
    (tdir / "task.json").write_text(meta.model_dump_json(indent=2), encoding="utf-8")
    return tdir


GOALS_TEMPLATE = """# Verification goals

You are given the protocol theory in `theory.spthy`. The theory is complete
**except for its security lemmas**, which have been removed. Your job is to:

1. Formulate a security lemma for **each** goal listed below, using the given
   lemma names (Tamarin will match them when grading).
2. Run the Tamarin prover and drive the analysis to completion: every lemma
   must terminate with `verified` or `falsified - found trace`.
3. Produce the deliverables described in the task README
   (`final.spthy`, `verdict.json`, `attack_report.md` if unsafe).

Notes:

- Lemma statements are yours to write; the quantifier column is binding.
- Helper/source lemmas beyond the listed goals are allowed (and often
  needed to make the prover terminate).
- Some theories use `diff()` terms (observational equivalence): analyzing
  them requires `tamarin-prover --diff`; the default observational
  equivalence check covers theories with no explicit lemmas.

## Goals to formalize

| # | Lemma name | Quantifier | Property |
|---|------------|------------|----------|
{goal_rows}

## Protocol description (natural language)

{logic}
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--cfb-dir",
        type=Path,
        default=Path.home() / "projects/CrypFormBench",
        help="CrypFormBench checkout (default: ~/projects/CrypFormBench)",
    )
    ap.add_argument("--tasks-root", type=Path, default=REPO_ROOT / "data/tasks")
    ap.add_argument("--force", action="store_true", help="overwrite existing task dirs")
    args = ap.parse_args()

    table = load_cfb(args.cfb_dir)
    tasks_root = args.tasks_root
    tasks_root.mkdir(parents=True, exist_ok=True)

    # ── selection sets ────────────────────────────────────────────────────
    def is_attack(entry: dict) -> bool:
        if not entry.get("results"):
            return False
        return any(
            v["verdict"] == "falsified - found trace"
            for v in parse_summary_verdicts(entry["results"]).values()
        )

    attack_files = sorted(f for f, e in table.items() if e.get("code") and is_attack(e))
    l2_files = attack_files[:10]
    # L3: prefer the "falsely-passing" variants where they exist (they hide
    # real attacks), then error variants; keep verdict diversity with KAS1.
    l3_plan: list[tuple[str, str]] = []  # (file, variant)
    corr_false_used = set()
    for f in ["SPTHY-1/NSPK3.spthy", "SPTHY-1/RYY_PFS.spthy"]:
        if f in table and table[f].get("corr", {}).get("false_code"):
            l3_plan.append((f, "false"))
            corr_false_used.add(f)
    for f in [
        "SPTHY-1/BP_ABSTRACT_IBE_toyExample.spthy",
        "SPTHY-1/CCITT-X509-R.spthy",
        "SPTHY-1/CH07.spthy",
        "SPTHY-1/CHx.spthy",
        "SPTHY-1/dh_alternative.spthy",
        "SPTHY-1/exADH-kn.spthy",
        "SPTHY-1/Google2Step_MA.spthy",
        "SPTHY-1/KAS1.spthy",
    ]:
        if f in table and table[f].get("corr", {}).get("error_code"):
            l3_plan.append((f, "error"))

    created: list[tuple[str, str]] = []  # (level, name)
    skipped: list[str] = []

    for f, entry in sorted(table.items()):
        code = entry.get("code")
        if not code:
            skipped.append(f)
            continue
        name = Path(f).stem
        try:
            theory = parse_theory(code)
        except Exception as e:  # noqa: BLE001
            print(f"SKIP {f}: cannot parse ({e})")
            skipped.append(f)
            continue

        if args.force:
            import shutil

            for lvl in ("L1_verdict", "L2_form", "L3_repair"):
                shutil.rmtree(tasks_root / lvl / name, ignore_errors=True)

        gt = seed_ground_truth(name, code, entry.get("results"))
        common = dict(
            name=name,
            protocol=theory.name,
            source_file=f,
            source_dataset=entry["source"],
        )

        # ── L1: every protocol with provable goals ────────────────────────
        active_lemmas = theory.lemmas
        uses_diff = bool(re.search(r"\bdiff\s*\(", code))
        if not active_lemmas and not uses_diff:
            # no provable goals (all lemmas commented out / #ifdef'd away)
            print(f"SKIP L1 {f}: no active lemmas")
        else:
            if active_lemmas:
                stripped = strip_lemmas(code)
                rows = [
                    f"| {i + 1} | `{lem.name}` | {lem.quantifier} | {humanize(lem.name)} |"
                    for i, lem in enumerate(active_lemmas)
                ]
            else:
                # diff theory relying on the default observational-equivalence
                # check; the goal is the implicit DiffLemma
                stripped = code
                rows = [
                    "| 1 | `Observational_equivalence` | diff | observational equivalence of the two diff-term sides |"
                ]
            goals = GOALS_TEMPLATE.format(
                goal_rows="\n".join(rows),
                logic=(entry.get("logic") or "").strip()
                or "(no description available)",
            )
            meta = TaskMeta(
                task_id=f"L1:{name}",
                level="L1_verdict",
                given_files=["theory.spthy", "goals.md"],
                lemma_names=[l.name for l in active_lemmas]
                or ["Observational_equivalence"],
                uses_diff_terms=uses_diff,
                description="Formulate the security lemmas, verify with Tamarin, give the verdict.",
                **common,
            )
            write_task(
                level="L1_verdict",
                name=name,
                meta=meta,
                workspace_files={"theory.spthy": stripped, "goals.md": goals},
                solution_spthy=code,
                ground_truth=gt,
                tasks_root=tasks_root,
            )
            created.append(("L1_verdict", name))

        # ── L2: attack-bearing protocols from NL spec ─────────────────────
        if f in l2_files:
            logic = (entry.get("logic") or "").strip()
            if not logic:
                print(f"SKIP L2 {f}: no natural-language spec")
            else:
                meta = TaskMeta(
                    task_id=f"L2:{name}",
                    level="L2_form",
                    given_files=["spec.md"],
                    lemma_names=[l.name for l in theory.lemmas],
                    description=(
                        "Model the protocol from the natural-language spec in "
                        "Tamarin, verify it, and find the attack."
                    ),
                    **common,
                )
                write_task(
                    level="L2_form",
                    name=name,
                    meta=meta,
                    workspace_files={"spec.md": logic},
                    solution_spthy=code,
                    ground_truth=gt,
                    tasks_root=tasks_root,
                )
                created.append(("L2_form", name))

        # ── L3: repair tasks ──────────────────────────────────────────────
        for lf, variant in l3_plan:
            if lf != f:
                continue
            corr = entry.get("corr", {})
            broken = corr.get(f"{variant}_code", "")
            hint = corr.get(f"{variant}_info", "")
            if not broken:
                print(f"SKIP L3 {f}: no {variant} code")
                continue
            meta = TaskMeta(
                task_id=f"L3:{name}",
                level="L3_repair",
                given_files=["broken.spthy", "error_hint.txt"],
                lemma_names=[l.name for l in theory.lemmas],
                description=(
                    "Repair the broken theory, verify with Tamarin, and "
                    "determine whether the protocol satisfies its goals."
                ),
                **common,
            )
            write_task(
                level="L3_repair",
                name=name,
                meta=meta,
                workspace_files={
                    "broken.spthy": broken,
                    "error_hint.txt": hint,
                },
                solution_spthy=code,
                ground_truth=gt,
                tasks_root=tasks_root,
            )
            created.append(("L3_repair", name))

    # ── task id lists ──────────────────────────────────────────────────────
    ids = [
        {"L1_verdict": "L1:", "L2_form": "L2:", "L3_repair": "L3:"}[lvl] + name
        for lvl, name in created
    ]
    task_ids_dir = tasks_root.parent / "task_ids"
    task_ids_dir.mkdir(parents=True, exist_ok=True)
    (task_ids_dir / "v0.txt").write_text("\n".join(ids) + "\n")

    # sample.txt: small deterministic smoke set — 2 L1 (one safe one unsafe if
    # possible), 1 L2, 1 L3
    l1_ids = [i for i in ids if i.startswith("L1:")]
    sample = [i for i in l1_ids if "NSPK3" in i or "9.spthy".replace(".spthy", "") in i]
    sample = sample[:2] or l1_ids[:2]
    for prefix in ("L2:", "L3:"):
        m = [i for i in ids if i.startswith(prefix)]
        if m:
            sample.append(m[0])
    (task_ids_dir / "sample.txt").write_text("\n".join(sample) + "\n")

    print(
        f"created {len(created)} tasks "
        f"(L1={sum(1 for l, _ in created if l == 'L1_verdict')}, "
        f"L2={sum(1 for l, _ in created if l == 'L2_form')}, "
        f"L3={sum(1 for l, _ in created if l == 'L3_repair')})"
    )
    if skipped:
        print(f"skipped {len(skipped)} files: {skipped}")


if __name__ == "__main__":
    main()
