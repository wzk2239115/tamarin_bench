"""Pluggable protocol verification backends.

Each verifier implements the ``run(model_path, timeout_s)`` interface,
returning a ``VerifyResult`` with the tool's verdict on the model.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["VerifyResult", "TamarinVerifier", "VerifpalVerifier", "run_in_docker"]


@dataclass
class VerifyResult:
    """Result of running a protocol verifier on a model file."""

    tool: str  # "tamarin" | "verifpal" | "proverif"
    ok: bool  # did the tool run without crashing?
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    # parsed verdicts: list of (query_name, verdict, detail)
    # verdict ∈ {"verified", "falsified", "cannot_prove", "unknown"}
    queries: list[tuple[str, str, str]] = field(default_factory=list)
    # for tamarin: wellformedness
    wellformed: bool | None = None
    # any attack trace found (raw text)
    attack_trace: str | None = None
    # json output if available (verifpal --format json)
    json_output: dict | None = None

    @property
    def has_attack(self) -> bool:
        return any(v == "falsified" for _, v, _ in self.queries)

    @property
    def all_verified(self) -> bool:
        return len(self.queries) > 0 and all(
            v == "verified" for _, v, _ in self.queries
        )

    @property
    def terminated(self) -> bool:
        return (
            all(v in ("verified", "falsified") for _, v, _ in self.queries)
            if self.queries
            else False
        )


def run_in_docker(
    model_path: Path,
    command: list[str],
    image: str,
    timeout_s: int,
    extra_volumes: dict[str, str] | None = None,
) -> tuple[int, str, str]:
    """Run a command in a throwaway container with the model mounted read-only."""
    docker_cmd = ["docker", "run", "--rm", "--memory=8g", "--cpus=4"]
    volumes = {str(model_path.absolute()): {"bind": "/model.vp", "mode": "ro"}}
    if extra_volumes:
        volumes.update(extra_volumes)
    for vol, opts in volumes.items():
        mode = "ro" if opts["mode"] == "ro" else "rw"
        docker_cmd.extend(["-v", f"{vol}:{opts['bind']}:{mode}"])
    docker_cmd.append(image)
    docker_cmd.extend(command)
    try:
        proc = subprocess.run(
            docker_cmd,
            capture_output=True,
            timeout=timeout_s,
        )
        return (
            proc.returncode,
            proc.stdout.decode(errors="replace"),
            proc.stderr.decode(errors="replace"),
        )
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    except Exception as e:
        return 1, "", str(e)


class TamarinVerifier:
    """Tamarin prover backend — already implemented via tamarin_runner.py."""

    IMAGE = "protocolbench/agent:latest"

    def run(self, model_path: Path, timeout_s: int = 600) -> VerifyResult:
        from tamaringym.evaluation.tamarin_runner import run_tamarin_in_docker

        r = run_tamarin_in_docker(model_path, image=self.IMAGE, timeout_s=timeout_s)
        queries = [(n, v, "") for n, _, v, _ in r.lemmas]
        return VerifyResult(
            tool="tamarin",
            ok=r.ok,
            exit_code=r.exit_code,
            stdout=r.stdout,
            stderr=r.stderr,
            queries=queries,
            wellformed=r.parsed.get("wellformedness_ok"),
            attack_trace=r.parsed.get("attack_trace"),
        )


class VerifpalVerifier:
    """Verifpal backend — parses text or JSON output."""

    IMAGE = "protocolbench/agent:latest"

    def run(self, model_path: Path, timeout_s: int = 300) -> VerifyResult:
        # verifpal requires .vp extension
        exit_code, stdout, stderr = run_in_docker(
            model_path,
            ["verifpal", "verify", "/model.vp", "--format", "json"],
            self.IMAGE,
            timeout_s,
        )
        result = VerifyResult(
            tool="verifpal",
            ok=exit_code == 0,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
        )
        # parse JSON output
        try:
            data = json.loads(stdout)
            result.json_output = data
            for model in data.get("models", []):
                analysis = model.get("analysis", {})
                for q in analysis.get("queries", []):
                    name = q.get("query", "")
                    summary = q.get("summary", "")
                    # attack if summary contains "Attack trace" or conclusion mentions "obtained"/"forged"
                    has_attack = (
                        "Attack trace" in summary
                        or "obtained by Attacker" in str(q.get("conclusion", ""))
                    )
                    if has_attack:
                        verdict = "falsified"
                        result.attack_trace = summary[:2000]
                    elif q.get("envelope", {}).get("exhausted"):
                        verdict = "verified"
                    else:
                        verdict = "unknown"
                    result.queries.append((name, verdict, summary[:200]))
        except (json.JSONDecodeError, KeyError):
            # fallback: parse text output
            for line in stdout.splitlines():
                m = re.match(r"\s*(FAIL|HOLD|OK)\s+(.+)", line)
                if m:
                    verdict = {
                        "FAIL": "falsified",
                        "HOLD": "verified",
                        "OK": "verified",
                    }.get(m.group(1), "unknown")
                    result.queries.append((m.group(2).strip(), verdict, ""))
            if "FAIL" in stdout:
                idx = stdout.find("Attack trace:")
                if idx >= 0:
                    result.attack_trace = stdout[idx:][:2000]

        return result
