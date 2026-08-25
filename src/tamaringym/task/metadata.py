"""Pydantic models for tamarin_bench task metadata and ground truth.

A task is a directory under ``data/tasks/<level>/<name>/`` containing:

* ``task.json``           — public metadata (safe to show the agent's harness)
* ``theory.spthy`` / ``spec.md`` / ``broken.spthy`` — the given inputs
* ``goals.md``            — NL description of what to verify (L1)
* ``solution/``           — reference solution + ``ground_truth.json``

``ground_truth.json`` is produced by ``scripts/validate_tasks.py`` (a real
Tamarin re-run in the verifier container) and never enters the agent
workspace.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

__all__ = [
    "TASK_LEVELS",
    "TaskMeta",
    "LemmaTruth",
    "GroundTruth",
    "load_task_registry",
]

TASK_LEVELS = ("L1_verdict", "L2_form", "L3_repair", "B1_attack")

DATA_DIR = Path(__file__).parents[3] / "data"
TASKS_DIR = DATA_DIR / "tasks"


class TaskMeta(BaseModel):
    task_id: str  # e.g. "L1:NSPK3" or "B1:kc_rs_basic"
    level: str  # L1_verdict | L2_form | L3_repair | B1_attack
    name: str  # sanitized protocol name (directory name)
    protocol: str  # original protocol name (theory name)
    source_file: str  # origin path, e.g. "SPTHY-1/NSPK3.spthy"
    source_dataset: str  # crypformbench | tamarin-examples | jwt_oidc | ...
    given_files: list[str] = Field(default_factory=list)
    # L1: lemma names the agent is asked to (re)formulate, in reference order.
    lemma_names: list[str] = Field(default_factory=list)
    # Theory uses diff() terms / observational equivalence (prompt hint).
    uses_diff_terms: bool = False
    # Evaluation family: "tamarin" (default) or a deployment family like
    # "jwt_oidc" (B1 tasks route to the family evaluator).
    family: str = "tamarin"
    # Deployment template for family tasks (directory under
    # data/deployments/<family>/).
    deployment: str | None = None
    # Reference solution needs a Tamarin oracle heuristic file (shipped as
    # solution/oracle and given to the agent as `oracle` in the workspace).
    oracle: bool = False
    description: str = ""


class LemmaTruth(BaseModel):
    name: str
    quantifier: str
    verdict: str  # "verified" | "falsified" | "incomplete" | "processing error"
    steps: int | None = None


class GroundTruth(BaseModel):
    protocol: str
    overall_verdict: str  # "SAFE" | "UNSAFE" | "UNKNOWN"
    lemmas: list[LemmaTruth] = Field(default_factory=list)
    # per falsified lemma: list of protocol-rule event sequences (one per trace)
    attack_traces: dict[str, list[list[str]]] = Field(default_factory=dict)
    tamarin_version: str | None = None
    wellformedness_ok: bool | None = None
    runtime_seconds: float | None = None
    # How the reference had to be run: False = plain --prove,
    # True = --diff --prove (theory needs observational-equivalence mode).
    requires_diff: bool = False
    validated: bool = False


def load_task_registry(tasks_dir: Path = TASKS_DIR) -> dict[str, dict[str, TaskMeta]]:
    """Load all task.json files.

    Returns ``{level: {name: TaskMeta}}``. Raises if a task directory is
    missing its task.json.
    """
    registry: dict[str, dict[str, TaskMeta]] = {lvl: {} for lvl in TASK_LEVELS}
    if not tasks_dir.is_dir():
        return registry
    for level_dir in sorted(tasks_dir.iterdir()):
        if not level_dir.is_dir() or level_dir.name not in TASK_LEVELS:
            continue
        for task_dir in sorted(level_dir.iterdir()):
            meta_path = task_dir / "task.json"
            if not meta_path.is_file():
                raise FileNotFoundError(f"task dir missing task.json: {task_dir}")
            meta = TaskMeta.model_validate(json.loads(meta_path.read_text()))
            registry[level_dir.name][task_dir.name] = meta
    return registry


def task_dir_for(task_id: str, tasks_dir: Path = TASKS_DIR) -> Path:
    """Resolve ``L1:NSPK3`` to its directory path."""
    level, _, name = task_id.partition(":")
    if not name:
        raise ValueError(f"malformed task id: {task_id!r} (expected 'L1:NAME')")
    level_map = {
        "L1": "L1_verdict",
        "L2": "L2_form",
        "L3": "L3_repair",
        "B1": "B1_attack",
    }
    level_dir = level_map.get(level, level)
    return tasks_dir / level_dir / name
