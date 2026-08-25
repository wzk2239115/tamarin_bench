"""Run Tamarin inside a clean Docker container.

Shared by ``scripts/validate_tasks.py`` (ground-truth generation) and the
evaluator (scoring): the *only* trusted execution environment is a fresh
``tamaringym/verifier`` container with the pinned Tamarin — nothing that
ran inside the agent container is ever trusted.
"""

from __future__ import annotations

import subprocess
import tempfile
import time
from pathlib import Path

from tamaringym.evaluation.verifier import parse_attack_traces, parse_prove_output

__all__ = ["TamarinRunResult", "run_tamarin_in_docker", "DEFAULT_VERIFIER_IMAGE"]

DEFAULT_VERIFIER_IMAGE = "tamaringym/verifier:1.12.0"


class TamarinRunResult:
    """Structured result of one Tamarin ``--prove`` run."""

    def __init__(
        self,
        *,
        ok: bool,
        stdout: str,
        stderr: str,
        exit_code: str | int | None,
        wall_seconds: float,
        requires_diff: bool,
        parsed: dict,
        traces: dict,
        error: str | None = None,
    ) -> None:
        self.ok = ok
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code
        self.wall_seconds = wall_seconds
        self.requires_diff = requires_diff
        self.parsed = parsed
        self.traces = traces
        self.error = error

    @property
    def lemmas(self) -> list[tuple[str, str, str, int | None]]:
        return self.parsed.get("lemmas", [])

    @property
    def timeout(self) -> bool:
        return bool(self.parsed.get("timeout"))

    def summary_dict(self) -> dict:
        return {
            "ok": self.ok,
            "exit_code": self.exit_code,
            "wall_seconds": round(self.wall_seconds, 2),
            "requires_diff": self.requires_diff,
            "wellformedness_ok": self.parsed.get("wellformedness_ok"),
            "tamarin_version": self.parsed.get("tamarin_version"),
            "lemmas": [
                {"name": n, "quantifier": q, "verdict": v, "steps": s}
                for n, q, v, s in self.lemmas
            ],
            "traces": self.traces,
            "timeout": self.timeout,
            "error": self.error,
        }


def _run_once(work: Path, image: str, timeout_s: int, diff: bool) -> dict:
    flag = "--diff " if diff else ""
    cmd = [
        "docker",
        "run",
        "--rm",
        "-e",
        "LANG=C.UTF-8",
        "-e",
        "LC_ALL=C.UTF-8",
        "-v",
        f"{work}:/verify",
        image,
        "bash",
        "-c",
        (
            f"cd /verify && timeout {timeout_s} "
            f"tamarin-prover final.spthy {flag}--prove "
            "--output-json=traces.json > prove.stdout 2> prove.stderr; "
            "echo $? > exit_code"
        ),
    ]
    t0 = time.monotonic()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s + 120)
    wall = time.monotonic() - t0
    if proc.returncode != 0:
        return {
            "status": "docker_error",
            "error": (proc.stderr or proc.stdout)[-2000:],
            "wall_seconds": wall,
        }
    exit_code = (
        (work / "exit_code").read_text().strip()
        if (work / "exit_code").exists()
        else "?"
    )
    stdout = (
        (work / "prove.stdout").read_text(errors="replace")
        if (work / "prove.stdout").exists()
        else ""
    )
    stderr = (
        (work / "prove.stderr").read_text(errors="replace")
        if (work / "prove.stderr").exists()
        else ""
    )
    traces_raw = (
        (work / "traces.json").read_text(errors="replace")
        if (work / "traces.json").exists()
        else ""
    )
    return {
        "status": "done",
        "exit_code": exit_code,
        "wall_seconds": wall,
        "stdout": stdout,
        "stderr": stderr,
        "traces_json": traces_raw,
        "requires_diff": diff,
    }


def run_tamarin_in_docker(
    spthy_path: Path,
    *,
    image: str = DEFAULT_VERIFIER_IMAGE,
    timeout_s: int = 600,
    known_lemma_names: list[str] | None = None,
    retry_diff: bool = True,
) -> TamarinRunResult:
    """Run ``tamarin-prover final.spthy --prove`` in a fresh container.

    The plain mode is tried first; on diff-signals (``flag diff not set`` or
    a failed parse) the run is retried with ``--diff``. Returns a
    :class:`TamarinRunResult` with parsed lemmas and attack traces.
    """
    with tempfile.TemporaryDirectory(prefix="tg-run-") as tmp:
        work = Path(tmp)
        (work / "final.spthy").write_bytes(Path(spthy_path).read_bytes())
        result = _run_once(work, image, timeout_s, diff=False)
        if result["status"] != "done":
            return TamarinRunResult(
                ok=False,
                stdout="",
                stderr=str(result.get("error")),
                exit_code=None,
                wall_seconds=result.get("wall_seconds", 0.0),
                requires_diff=False,
                parsed={
                    "lemmas": [],
                    "timeout": False,
                    "errors": [str(result.get("error"))],
                },
                traces={},
                error=result.get("error"),
            )

        stdout = result["stdout"]
        exit_code = result["exit_code"]
        if retry_diff:
            needs_diff = "flag diff not set" in stdout or (
                exit_code not in ("0", 0) and "summary of summaries" not in stdout
            )
            if needs_diff:
                # clear previous artifacts before retrying
                for f in ("traces.json", "prove.stdout", "prove.stderr", "exit_code"):
                    p = work / f
                    if p.exists():
                        p.unlink()
                retry = _run_once(work, image, timeout_s, diff=True)
                if retry["status"] == "done" and "summary of summaries" in retry.get(
                    "stdout", ""
                ):
                    result = retry

    parsed = parse_prove_output(result["stdout"], exit_code=result.get("exit_code"))
    traces = parse_attack_traces(result.get("traces_json", ""), known_lemma_names or [])
    return TamarinRunResult(
        ok="summary of summaries" in result.get("stdout", ""),
        stdout=result.get("stdout", ""),
        stderr=result.get("stderr", ""),
        exit_code=result.get("exit_code"),
        wall_seconds=result.get("wall_seconds", 0.0),
        requires_diff=bool(result.get("requires_diff")),
        parsed=parsed,
        traces=traces,
    )
