#!/usr/bin/env python3
"""Interactive mode: a bash shell inside a prepared task container.

    python scripts/interactive.py --task L1:NSPK3 [--name myslot]

Starts an agent container with the task workspace at /workspace and the
runtime mounted at /data, then attaches an interactive bash. The container
is removed on exit unless --keep is given.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tamaringym.evaluation.base import TamarinEvaluator  # noqa: E402
from tamaringym.evaluation.types import EvalConfig  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--task", required=True, help="task id, e.g. L1:NSPK3")
    ap.add_argument("--name", default="interactive")
    ap.add_argument("--keep", action="store_true", help="keep the container on exit")
    args = ap.parse_args()

    out_dir = (
        REPO_ROOT / "out" / args.name / f"interactive_{args.task.replace(':', '_')}"
    )
    cfg = EvalConfig(
        task_id=args.task,
        out_dir=out_dir,
        keep_container=True,
        credential_path=Path("/dev/null"),
    )
    evaluator = TamarinEvaluator(cfg)
    workspace_dir = out_dir / "workspace"
    evaluator.prepare_workspace(workspace_dir)
    print(f"workspace ready: {workspace_dir}")

    from tamaringym.utils import docker_cp_to_container, get_docker_client

    client = get_docker_client()
    container = evaluator._start_container(client)
    container.exec_run(["mkdir", "-p", "/workspace", "/logs"])
    docker_cp_to_container(container.id, f"{workspace_dir}/.", "/workspace")

    print(f"container {container.name} ready; workspace at /workspace")
    print(
        "inside, run the agent manually, e.g.:\n"
        "  /data/node/bin/claude-code.sh --verbose "
        "--permission-mode=bypassPermissions --disallowed-tools WebSearch,WebFetch"
    )
    try:
        import subprocess

        subprocess.run(
            ["docker", "exec", "-it", "-w", "/workspace", container.id, "bash"]
        )
    finally:
        if not args.keep:
            container.remove(force=True)
            print("container removed")
        else:
            print(f"container kept: {container.id[:12]}")


if __name__ == "__main__":
    main()
