#!/usr/bin/env python3
"""Aggregate batch results: summary.json + per-check breakdown + leaderboard.

Usage:
    python scripts/aggregate_results.py out/run1 [out/run2 ...]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

CHECK_ORDER = [
    "outputs_present",
    "parses",
    "wellformed",
    "given_rules_unchanged",
    "lemma_coverage",
    "lemma_fact_references",
    "no_trivial_lemmas",
    "verdict_match",
    "attack_trace_match",
    "attack_report_match",
]


def load_run(run_dir: Path) -> list[dict]:
    results = []
    for rj in sorted(run_dir.rglob("result.json")):
        try:
            data = json.loads(rj.read_text())
        except json.JSONDecodeError:
            continue
        checks = {c["name"]: c for c in data.get("checks", [])}
        total_w = sum(c["weight"] for c in data.get("checks", []))
        score = (
            sum(c["score"] * c["weight"] for c in data.get("checks", [])) / total_w
            if total_w
            else 0.0
        )
        level = data["task_id"].split(":")[0]
        results.append(
            {
                "task_id": data["task_id"],
                "level": level,
                "score": score,
                "elapsed": data.get("elapsed_time", 0.0),
                "checks": checks,
                "error": data.get("error"),
            }
        )
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run_dirs", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    report: dict = {}
    for run_dir in args.run_dirs:
        results = load_run(run_dir)
        if not results:
            print(f"{run_dir}: no results found", file=sys.stderr)
            continue
        by_level: dict[str, list[dict]] = defaultdict(list)
        for r in results:
            by_level[r["level"]].append(r)
        all_scores = [r["score"] for r in results]
        # solved = weighted score >= 0.9
        solved = [r for r in results if r["score"] >= 0.9]
        check_stats = {}
        for name in CHECK_ORDER:
            vals = [r["checks"][name]["score"] for r in results if name in r["checks"]]
            if vals:
                check_stats[name] = {
                    "mean": sum(vals) / len(vals),
                    "n": len(vals),
                }
        level_stats = {
            lvl: {
                "n": len(rs),
                "mean": sum(r["score"] for r in rs) / len(rs),
                "solved": sum(1 for r in rs if r["score"] >= 0.9),
            }
            for lvl, rs in sorted(by_level.items())
        }
        report[str(run_dir)] = {
            "tasks": len(results),
            "mean_score": sum(all_scores) / len(all_scores),
            "solved(>=0.9)": len(solved),
            "mean_elapsed_s": sum(r["elapsed"] for r in results) / len(results),
            "per_level": level_stats,
            "per_check": check_stats,
            "unsolved": sorted(
                (r["task_id"], round(r["score"], 3))
                for r in results
                if r["score"] < 0.9
            ),
        }

    if args.json:
        print(json.dumps(report, indent=2))
        return
    for run, stats in report.items():
        print(f"== {run}")
        print(
            f"   tasks={stats['tasks']} mean={stats['mean_score']:.3f} "
            f"solved={stats['solved(>=0.9)']} mean_time={stats['mean_elapsed_s']:.0f}s"
        )
        for lvl, s in stats["per_level"].items():
            print(f"   {lvl}: n={s['n']} mean={s['mean']:.3f} solved={s['solved']}")
        print("   checks:")
        for name, s in stats["per_check"].items():
            bar = "#" * int(s["mean"] * 20)
            print(f"     {name:26s} {s['mean']:.2f} {bar}")


if __name__ == "__main__":
    main()
