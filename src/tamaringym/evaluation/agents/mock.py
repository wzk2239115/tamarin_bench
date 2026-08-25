"""Mock agents for pipeline testing without an LLM.

* :class:`MockPerfectAgent` — host-side; copies the reference solution into
  the container as the agent's outputs. Should score (near) perfectly.
* :class:`MockLazyAgent` — host-side; submits the given theory unchanged
  with a bogus verdict. Should score poorly.
* :class:`ScriptAgent` — runs a bash script inside the container (the
  realistic code path: work happens in /workspace inside the container).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from tamaringym.evaluation.agents.base import Agent
from tamaringym.evaluation.types import AgentFnArguments
from tamaringym.task.metadata import task_dir_for
from tamaringym.utils import docker_cp_to_container, get_docker_client

logger = logging.getLogger(__name__)


class MockPerfectAgent(Agent):
    """Copies the reference solution in as the agent's deliverables."""

    def run(self, args: AgentFnArguments) -> None:
        client = get_docker_client()
        container = client.containers.get(args.container_id)
        tdir = task_dir_for(args.extra_kwargs["task_id"])
        solution = tdir / "solution" / "solution.spthy"
        gt = json.loads((tdir / "solution" / "ground_truth.json").read_text())

        tmp = Path(args.out_dir) / "_mock"
        tmp.mkdir(parents=True, exist_ok=True)
        (tmp / "final.spthy").write_bytes(solution.read_bytes())
        lemmas = {l["name"]: l["verdict"] for l in gt["lemmas"]}
        attack_lemmas = [n for n, v in lemmas.items() if v == "falsified"]
        (tmp / "verdict.json").write_text(
            json.dumps(
                {
                    "overall": gt["overall_verdict"],
                    "lemmas": lemmas,
                    "attack_lemmas": attack_lemmas,
                    "notes": "mock perfect agent",
                },
                indent=2,
            )
        )
        if attack_lemmas:
            rules = []
            for lemma in attack_lemmas:
                for seq in gt.get("attack_traces", {}).get(lemma, []):
                    rules.extend(seq)
            (tmp / "attack_report.md").write_text(
                "# Attack report (mock)\n\nRules exercised:\n\n"
                + "\n".join(f"- {r}" for r in rules)
                + "\n"
            )
        for fname in ("final.spthy", "verdict.json", "attack_report.md"):
            p = tmp / fname
            if p.is_file():
                docker_cp_to_container(container.id, str(p), f"/workspace/{fname}")
        logger.info("MockPerfectAgent delivered reference solution")


class MockLazyAgent(Agent):
    """Submits the given theory unchanged with a bogus safe verdict."""

    def run(self, args: AgentFnArguments) -> None:
        client = get_docker_client()
        container = client.containers.get(args.container_id)
        src = "theory.spthy" if args.extra_kwargs.get("has_theory") else "broken.spthy"
        container.exec_run(
            [
                "bash",
                "-c",
                f"cp /workspace/{src} /workspace/final.spthy 2>/dev/null || true",
            ]
        )
        container.exec_run(
            [
                "bash",
                "-c",
                "cat > /workspace/verdict.json << 'EOF'\n"
                '{"overall": "SAFE", "lemmas": {}, "attack_lemmas": [], "notes": "lazy"}\n'
                "EOF",
            ]
        )
        logger.info("MockLazyAgent delivered lazy outputs")


class ScriptAgent(Agent):
    """Runs a bash script inside the container at /workspace."""

    def __init__(self, script: str) -> None:
        self.script = script

    def run(self, args: AgentFnArguments) -> None:
        client = get_docker_client()
        container = client.containers.get(args.container_id)
        logger.info("ScriptAgent running %d-byte script", len(self.script))
        exit_code, output = container.exec_run(
            ["bash", "-c", self.script], workdir="/workspace"
        )
        logger.info("ScriptAgent exit=%d", exit_code)
