"""Workspace preparation: copy the task's given files into the agent
workspace and render the README prompt from the Jinja2 template.

The prompt README doubles as the task description returned to the
evaluator (the same pattern as ExploitGym: README == prompt). Solution
and ground-truth files never enter the workspace.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from tamaringym.task.metadata import TaskMeta, task_dir_for

__all__ = ["prepare_workspace"]

_TEMPLATES_DIR = Path(__file__).parent / "templates"


def prepare_workspace(meta: TaskMeta, workspace_dir: Path) -> str:
    """Populate *workspace_dir* for *meta*; return the README prompt text."""
    tdir = task_dir_for(meta.task_id)
    workspace_dir.mkdir(parents=True, exist_ok=True)

    has_theory = has_goals = has_spec = has_broken = False
    for fname in meta.given_files:
        src = tdir / fname
        if not src.is_file():
            raise FileNotFoundError(f"given file missing for {meta.task_id}: {src}")
        shutil.copy(src, workspace_dir / fname)
        if fname == "theory.spthy":
            has_theory = True
        elif fname == "goals.md":
            has_goals = True
        elif fname == "spec.md":
            has_spec = True
        elif fname == "broken.spthy":
            has_broken = True

    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATES_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    template = env.get_template("README.md.j2")
    level_titles = {
        "L1_verdict": "Level 1: Property Formulation & Verdict",
        "L2_form": "Level 2: Modeling from a Natural-Language Spec",
        "L3_repair": "Level 3: Theory Repair & Attack Discovery",
    }
    prompt = template.render(
        level=meta.level,
        level_title=level_titles.get(meta.level, meta.level),
        has_theory=has_theory,
        has_goals=has_goals,
        has_spec=has_spec,
        has_broken=has_broken,
        uses_diff=meta.uses_diff_terms,
        meta=meta,
    )
    (workspace_dir / "README.md").write_text(prompt, encoding="utf-8")
    return prompt
