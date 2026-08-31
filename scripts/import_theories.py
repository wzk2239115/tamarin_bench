#!/usr/bin/env python3
"""Import Tamarin example theories into ProtocolBench task directories.

Generalizes ``convert_cfb.py``: walks a checkout of
https://github.com/tamarin-prover/tamarin-prover ``examples/`` (skipping the
regression/testParser suites) and produces L1 (lemma-stripped theories) and
L2 (natural-language modeling) tasks using the same layout, validation
pipeline, and scoring as the CrypFormBench-derived v0 corpus.

Per .spthy file:

* parse structurally (comment- and preprocessor-aware — several examples
  keep their interesting lemmas commented out or behind ``#ifdef``);
* skip files with no provable goals (unless they are diff theories);
* extract the leading block comment as the natural-language spec;
* L1 task: ``theory.spthy`` = lemmas stripped, ``goals.md`` = goal table +
  spec, plus the sibling ``.oracle`` heuristic file when present (copied as
  ``oracle`` into the workspace and the solution dir);
* L2 task (spec >= --min-spec-chars): ``spec.md`` only;
* ``solution/solution.spthy`` = the original theory; ground truth is seeded
  empty (``validated=false``) — run ``scripts/validate_tasks.py`` afterwards.

Task ids land in ``data/task_ids/imported_raw.txt``; after validation,
``v1.txt`` = v0 + validated imports (see ``--emit-v1``).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tamaringym.task.metadata import GroundTruth, TaskMeta  # noqa: E402
from tamaringym.task.spthy import parse_theory, strip_lemmas  # noqa: E402

SKIP_DIRS = {"regression", "testParser", ".git", "proofs"}
MAX_FILE_BYTES = 600_000
DEFAULT_MIN_SPEC_CHARS = 400

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
- {oracle_note}Some theories use `diff()` terms (observational equivalence):
  analyzing them requires `tamarin-prover --diff`.

## Goals to formalize

| # | Lemma name | Quantifier | Property |
|---|------------|------------|----------|
{goal_rows}

## Protocol description (natural language)

{logic}
"""

L2_SPEC_HEADER = """# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: {goals_hint}.

---

"""


def humanize(name: str) -> str:
    parts = re.split(r"[_\-\s]+", name)
    return " ".join(p for p in parts if p).lower()


def sanitize(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_-]+", "_", name).strip("_")
    return s or "unnamed"


def extract_spec(text: str) -> str:
    """Leading comment block(s) before the `theory` header, de-commented."""
    m = re.search(r"^\s*theory\s+", text, re.IGNORECASE | re.MULTILINE)
    prefix = text[: m.start()] if m else ""
    # strip comment markers
    prefix = re.sub(r"/\*", "", prefix)
    prefix = re.sub(r"\*/", "", prefix)
    prefix = re.sub(r"^\s*//", "", prefix, flags=re.MULTILINE)
    # collapse runs of blank lines
    prefix = re.sub(r"\n{3,}", "\n\n", prefix).strip()
    return prefix


def find_oracle(spthy: Path) -> Path | None:
    """Sibling oracle heuristic for a theory (foo.oracle or ./oracle)."""
    cands = [
        spthy.with_suffix(".oracle"),
        spthy.parent / "oracle",
    ]
    for c in cands:
        if c.is_file():
            return c
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--examples-dir",
        type=Path,
        default=Path("/tmp/opencode/tamarin-src/tamarin-prover-1.12.0/examples"),
        help="tamarin-prover examples/ checkout",
    )
    ap.add_argument("--tasks-root", type=Path, default=REPO_ROOT / "data/tasks")
    ap.add_argument("--force", action="store_true", help="overwrite existing task dirs")
    ap.add_argument(
        "--min-spec-chars",
        type=int,
        default=DEFAULT_MIN_SPEC_CHARS,
        help="minimum natural-language spec length for L2 task generation",
    )
    ap.add_argument(
        "--emit-v1",
        action="store_true",
        help="after import, write data/task_ids/v1.txt = v0.txt + imported ids",
    )
    args = ap.parse_args()

    if not args.examples_dir.is_dir():
        sys.exit(f"examples dir not found: {args.examples_dir}")

    tasks_root = args.tasks_root
    existing: set[str] = set()
    for lvl in ("L1_verdict", "L2_form", "L3_repair", "B1_attack"):
        d = tasks_root / lvl
        if d.is_dir():
            existing.update(p.name for p in d.iterdir() if p.is_dir())

    created: list[tuple[str, str]] = []
    skipped: list[str] = []
    imported_ids: list[str] = []

    spthy_files = sorted(
        p
        for p in args.examples_dir.rglob("*.spthy")
        if p.is_file()
        and not any(
            part in SKIP_DIRS for part in p.relative_to(args.examples_dir).parts
        )
    )
    print(f"scanning {len(spthy_files)} .spthy files")

    for spthy in spthy_files:
        rel = spthy.relative_to(args.examples_dir)
        if spthy.stat().st_size > MAX_FILE_BYTES:
            skipped.append(f"{rel}: too large")
            continue
        text = spthy.read_text(errors="replace")
        try:
            theory = parse_theory(text)
        except Exception as e:  # noqa: BLE001
            skipped.append(f"{rel}: parse error ({e})")
            continue

        active = theory.lemmas
        uses_diff = bool(re.search(r"\bdiff\s*\(", text)) or any(
            l.quantifier == "diff" for l in active
        )
        if not active and not uses_diff:
            skipped.append(f"{rel}: no active lemmas")
            continue

        stem = sanitize(spthy.stem)
        rel_parts_no_ext = rel.with_suffix("").parts
        subdir = sanitize("__".join(rel_parts_no_ext[:-1]) or "root")
        name = f"{subdir}__{stem}" if subdir and subdir != "root" else stem
        if name in existing:
            skipped.append(f"{rel}: name collision with existing task {name}")
            continue
        existing.add(name)

        if args.force:
            import shutil

            shutil.rmtree(tasks_root / "L1_verdict" / name, ignore_errors=True)
            shutil.rmtree(tasks_root / "L2_form" / name, ignore_errors=True)

        spec = extract_spec(text)
        oracle_src = find_oracle(spthy)

        common = dict(
            name=name,
            protocol=theory.name,
            source_file=str(rel),
            source_dataset="tamarin-examples",
            oracle=oracle_src is not None,
        )

        # ── L1 ────────────────────────────────────────────────────────────
        if active:
            stripped = strip_lemmas(text)
            rows = [
                f"| {i + 1} | `{lem.name}` | {lem.quantifier} | {humanize(lem.name)} |"
                for i, lem in enumerate(active)
            ]
        else:
            stripped = text
            rows = [
                "| 1 | `Observational_equivalence` | diff | "
                "observational equivalence of the two diff-term sides |"
            ]
        oracle_note = (
            "An `oracle` proof-heuristic file is provided; keep it in the "
            "working directory when running tamarin (it guides proof search).\n"
            if oracle_src
            else ""
        )
        goals = GOALS_TEMPLATE.format(
            goal_rows="\n".join(rows),
            logic=spec or "(no description available; reconstruct from the theory)",
            oracle_note=oracle_note,
        )
        meta = TaskMeta(
            task_id=f"L1:{name}",
            level="L1_verdict",
            given_files=["theory.spthy", "goals.md"]
            + (["oracle"] if oracle_src else []),
            lemma_names=[l.name for l in active] or ["Observational_equivalence"],
            uses_diff_terms=uses_diff,
            description="Formulate the security lemmas, verify with Tamarin, give the verdict.",
            **common,
        )
        tdir = tasks_root / "L1_verdict" / name
        (tdir / "solution").mkdir(parents=True)
        (tdir / "theory.spthy").write_text(stripped, encoding="utf-8")
        (tdir / "goals.md").write_text(goals, encoding="utf-8")
        (tdir / "solution" / "solution.spthy").write_text(text, encoding="utf-8")
        (tdir / "solution" / "ground_truth.json").write_text(
            GroundTruth(
                protocol=theory.name,
                overall_verdict="UNKNOWN",
                tamarin_version=None,
                validated=False,
            ).model_dump_json(indent=2),
            encoding="utf-8",
        )
        if oracle_src:
            (tdir / "oracle").write_bytes(oracle_src.read_bytes())
            (tdir / "solution" / "oracle").write_bytes(oracle_src.read_bytes())
        (tdir / "task.json").write_text(
            meta.model_dump_json(indent=2), encoding="utf-8"
        )
        created.append(("L1_verdict", name))
        imported_ids.append(f"L1:{name}")

        # ── L2 ────────────────────────────────────────────────────────────
        if len(spec) >= args.min_spec_chars:
            goals_hint = ", ".join(humanize(l.name) for l in active[:6]) or (
                "observational equivalence"
            )
            meta2 = TaskMeta(
                task_id=f"L2:{name}",
                level="L2_form",
                given_files=["spec.md"] + (["oracle"] if oracle_src else []),
                lemma_names=[l.name for l in active] or ["Observational_equivalence"],
                uses_diff_terms=uses_diff,
                description="Model the protocol from the natural-language spec, verify, find attacks.",
                **common,
            )
            meta2.task_id = f"L2:{name}"
            tdir2 = tasks_root / "L2_form" / name
            (tdir2 / "solution").mkdir(parents=True)
            (tdir2 / "spec.md").write_text(
                L2_SPEC_HEADER.format(goals_hint=goals_hint) + spec + "\n",
                encoding="utf-8",
            )
            (tdir2 / "solution" / "solution.spthy").write_text(text, encoding="utf-8")
            (tdir2 / "solution" / "ground_truth.json").write_text(
                GroundTruth(
                    protocol=theory.name,
                    overall_verdict="UNKNOWN",
                    tamarin_version=None,
                    validated=False,
                ).model_dump_json(indent=2),
                encoding="utf-8",
            )
            if oracle_src:
                (tdir2 / "oracle").write_bytes(oracle_src.read_bytes())
                (tdir2 / "solution" / "oracle").write_bytes(oracle_src.read_bytes())
            (tdir2 / "task.json").write_text(
                meta2.model_dump_json(indent=2), encoding="utf-8"
            )
            created.append(("L2_form", name))
            imported_ids.append(f"L2:{name}")

    ids_path = tasks_root.parent / "task_ids" / "imported_raw.txt"
    ids_path.parent.mkdir(parents=True, exist_ok=True)
    ids_path.write_text("\n".join(imported_ids) + ("\n" if imported_ids else ""))

    if args.emit_v1:
        v0 = tasks_root.parent / "task_ids" / "v0.txt"
        v1 = tasks_root.parent / "task_ids" / "v1.txt"
        base = (
            [line for line in v0.read_text().splitlines() if line.strip()]
            if v0.is_file()
            else []
        )
        v1.write_text("\n".join(base + imported_ids) + "\n")

    n_l1 = sum(1 for lvl, _ in created if lvl == "L1_verdict")
    n_l2 = sum(1 for lvl, _ in created if lvl == "L2_form")
    print(f"created {len(created)} tasks (L1={n_l1}, L2={n_l2})")
    print(f"ids written to {ids_path}")
    print(f"skipped {len(skipped)} files:")
    from collections import Counter

    reasons = Counter(s.rsplit(": ", 1)[-1] for s in skipped)
    for reason, n in reasons.most_common():
        print(f"   {n:4d}  {reason}")


if __name__ == "__main__":
    main()
