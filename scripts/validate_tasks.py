#!/usr/bin/env python3
"""Validate task ground truths by re-running Tamarin in the verifier container.

For every ``data/tasks/<level>/<name>/solution/solution.spthy``:

1. run ``tamarin-prover solution.spthy --prove --output-json=traces.json``
   inside a fresh ``tamaringym/verifier:<tag>`` container (pinned version),
   under a per-task timeout;
2. parse the summary (per-lemma verdicts), wellformedness status, runtime;
3. parse ``traces.json`` into per-lemma protocol-rule event multisets;
4. rewrite ``solution/ground_truth.json`` with ``validated=true``;
5. emit a global validation report (JSON + console).

Tasks whose reference does not terminate within the timeout are flagged; use
``--prune`` to drop them from ``data/task_ids/v0.txt``.
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tamaringym.evaluation.tamarin_runner import run_tamarin_in_docker  # noqa: E402
from tamaringym.evaluation.verifier import (  # noqa: E402
    parse_prove_output,
)
from tamaringym.task.metadata import (  # noqa: E402
    GroundTruth,
    LemmaTruth,
    load_task_registry,
    task_dir_for,
)

DEFAULT_IMAGE = "tamaringym/verifier:1.12.0"


def run_one(
    task_id: str,
    solution_spthy: Path,
    image: str,
    timeout_s: int,
    known_lemma_names: list[str] | None = None,
) -> dict:
    """Run Tamarin on one solution inside a fresh container; return raw results."""
    res = run_tamarin_in_docker(
        solution_spthy,
        image=image,
        timeout_s=timeout_s,
        retry_diff=True,
        known_lemma_names=known_lemma_names,
    )
    return {
        "task_id": task_id,
        "status": "done" if not res.error else "docker_error",
        "exit_code": res.exit_code,
        "wall_seconds": res.wall_seconds,
        "stdout": res.stdout,
        "stderr": res.stderr,
        "traces_json": "",  # traces already parsed inside the runner
        "_runner_traces": res.traces,
        "_runner_parsed": res.parsed,
        "requires_diff": res.requires_diff,
        "error": res.error,
    }


def build_ground_truth(
    task_id: str, result: dict, known_lemma_names: list[str]
) -> tuple[GroundTruth, dict]:
    parsed = result.get("_runner_parsed") or parse_prove_output(
        result.get("stdout", "")
    )
    traces = result.get("_runner_traces") or {}

    lemmas = [
        LemmaTruth(name=name, quantifier=quant, verdict=verdict, steps=steps)
        for name, quant, verdict, steps in parsed["lemmas"]
    ]
    any_falsified = any(l.verdict == "falsified" for l in lemmas)
    overall = (
        "UNSAFE"
        if any_falsified
        else (
            "SAFE"
            if lemmas and all(l.verdict == "verified" for l in lemmas)
            else "UNKNOWN"
        )
    )
    # --output-json also serializes witness traces of verified exists-trace
    # lemmas; only falsified lemmas' traces are attack traces.
    falsified_names = {l.name for l in lemmas if l.verdict == "falsified"}
    traces = {k: v for k, v in traces.items() if k in falsified_names}
    gt = GroundTruth(
        protocol=task_id.split("/")[-1],
        overall_verdict=overall,
        lemmas=lemmas,
        attack_traces=traces,
        tamarin_version=parsed["tamarin_version"],
        wellformedness_ok=parsed["wellformedness_ok"],
        runtime_seconds=parsed["processing_time"],
        requires_diff=bool(result.get("requires_diff")),
        validated=True,
    )
    summary = {
        "task_id": task_id,
        "status": result["status"],
        "exit_code": result.get("exit_code"),
        "wall_seconds": round(result.get("wall_seconds", 0.0), 1),
        "overall_verdict": overall,
        "wellformedness_ok": parsed["wellformedness_ok"],
        "tamarin_version": parsed["tamarin_version"],
        "requires_diff": bool(result.get("requires_diff")),
        "lemmas": [(l.name, l.verdict) for l in lemmas],
        "timeout": parsed["timeout"],
    }
    return gt, summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--image", default=DEFAULT_IMAGE)
    ap.add_argument(
        "--timeout", type=int, default=600, help="per-task tamarin timeout (s)"
    )
    ap.add_argument("--parallel", type=int, default=4, help="concurrent containers")
    ap.add_argument(
        "--tasks-file", type=Path, default=None, help="only validate ids from this file"
    )
    ap.add_argument(
        "--levels",
        nargs="*",
        default=["L1_verdict", "L2_form", "L3_repair"],
        help="task levels to validate (solutions are shared per protocol, so one "
        "pass over unique solution files is enough; levels filter which tasks "
        "get ground_truth updates)",
    )
    ap.add_argument(
        "--prune", action="store_true", help="drop broken tasks from v0.txt"
    )
    args = ap.parse_args()

    registry = load_task_registry()
    task_ids: list[str] = []
    for level in args.levels:
        for name, meta in sorted(registry[level].items()):
            task_ids.append(meta.task_id)
    if args.tasks_file:
        wanted = {
            line.strip()
            for line in args.tasks_file.read_text().splitlines()
            if line.strip()
        }
        task_ids = [t for t in task_ids if t in wanted]

    # unique solution files (same protocol appears in multiple levels)
    solutions: dict[Path, list[str]] = {}
    for tid in task_ids:
        tdir = task_dir_for(tid)
        sol = tdir / "solution" / "solution.spthy"
        solutions.setdefault(sol, []).append(tid)
    print(f"validating {len(solutions)} unique solutions ({len(task_ids)} tasks)")

    reports: list[dict] = []

    def _lemma_names_for(sol: Path) -> list[str]:
        meta_path = sol.parent.parent / "task.json"
        if meta_path.exists():
            return json.loads(meta_path.read_text()).get("lemma_names", [])
        return []

    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = {
            pool.submit(
                run_one, tids[0], sol, args.image, args.timeout, _lemma_names_for(sol)
            ): (sol, tids)
            for sol, tids in solutions.items()
        }
        for fut in as_completed(futures):
            sol, tids = futures[fut]
            try:
                result = fut.result()
            except Exception as e:  # noqa: BLE001
                result = {
                    "task_id": tids[0],
                    "status": "docker_error",
                    "error": str(e),
                    "stdout": "",
                    "traces_json": "",
                }
            known = _lemma_names_for(sol)
            if result["status"] != "done":
                print(
                    f"[{result['status']:>12}] {tids[0]}: {str(result.get('error'))[:120]}"
                )
                for tid in tids:
                    reports.append(
                        {
                            "task_id": tid,
                            "status": result["status"],
                            "error": str(result.get("error"))[:500],
                        }
                    )
                continue
            gt, summary = build_ground_truth(tids[0], result, known)
            for tid in tids:
                summary_t = dict(summary, task_id=tid)
                reports.append(summary_t)
                tdir = task_dir_for(tid)
                (tdir / "solution" / "ground_truth.json").write_text(
                    gt.model_dump_json(indent=2), encoding="utf-8"
                )
            flag = (
                "TIMEOUT"
                if summary["timeout"]
                else (
                    "UNSAFE"
                    if summary["overall_verdict"] == "UNSAFE"
                    else summary["overall_verdict"]
                )
            )
            print(
                f"[{flag:>12}] {tids[0]}: {summary['wall_seconds']:>7.1f}s "
                f"wf={'ok' if summary['wellformedness_ok'] else 'WARN'} "
                f"lemmas={summary['lemmas']}"
            )

    out_path = REPO_ROOT / "data" / "validation_report.json"
    out_path.write_text(json.dumps(reports, indent=2, default=str))
    print(f"\nwrote {out_path}")

    if args.prune:
        good = {
            r["task_id"]
            for r in reports
            if r.get("status") == "done" and not r.get("timeout")
        }
        ids_path = REPO_ROOT / "data" / "task_ids" / "v0.txt"
        ids = [line for line in ids_path.read_text().splitlines() if line.strip()]
        kept = [i for i in ids if i in good]
        dropped = [i for i in ids if i not in good]
        ids_path.write_text("\n".join(kept) + "\n")
        print(f"pruned {len(dropped)} tasks from v0.txt: {dropped}")


if __name__ == "__main__":
    main()
