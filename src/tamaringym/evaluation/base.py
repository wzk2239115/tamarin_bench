"""Base evaluator: the 8-step evaluation pipeline (adapted from ExploitGym).

1. Load task metadata + ground truth; prepare the workspace.
2. Start an agent container from the agent image (resource-limited).
3. Copy the workspace into the container at ``/workspace``.
4. (Optional install phase / firewall network switch.)
5. Run the CLI agent (Claude Code) with the README prompt.
6. Collect outputs (``final.spthy``, ``verdict.json``, ``attack_report.md``)
   and logs from the container.
7. Score: structural anti-cheat + clean-container Tamarin re-run vs ground
   truth (:class:`tamaringym.evaluation.tamarin_eval.TamarinScorer`).
8. Persist ``result.json``.
"""

from __future__ import annotations

import logging
import re
import time
from pathlib import Path
from uuid import uuid4

from docker.models.containers import Container

import docker
from tamaringym.evaluation.agents.base import Agent
from tamaringym.evaluation.tamarin_eval import TamarinScorer
from tamaringym.evaluation.types import (
    AgentFnArguments,
    CheckResult,
    EvalConfig,
    EvalResult,
)
from tamaringym.task.metadata import (
    GroundTruth,
    TaskMeta,
    load_task_registry,
    task_dir_for,
)
from tamaringym.task.workspace import prepare_workspace
from tamaringym.utils import (
    docker_cp_dir_from_container_filtered,
    docker_cp_from_container,
    docker_cp_to_container,
    get_docker_client,
    save_json,
)

logger = logging.getLogger(__name__)

_REGISTRY: dict[str, dict[str, TaskMeta]] | None = None


def get_task_meta(task_id: str) -> TaskMeta:
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = load_task_registry()
    level, _, name = task_id.partition(":")
    try:
        return _REGISTRY[level][name] if ":" in task_id else _REGISTRY[task_id][name]
    except KeyError:
        level_map = {"L1": "L1_verdict", "L2": "L2_form", "L3": "L3_repair"}
        return _REGISTRY[level_map.get(level, level)][name]


def load_ground_truth(meta: TaskMeta) -> GroundTruth:
    tdir = task_dir_for(meta.task_id)
    return GroundTruth.model_validate_json(
        (tdir / "solution" / "ground_truth.json").read_text()
    )


def _container_name_part(value: str, max_len: int = 32) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_.-]+", "-", value).strip("-").lower() or "unknown"
    return sanitized[:max_len].rstrip("-") or "unknown"


class TamarinEvaluator:
    """Runs one task end-to-end against an agent."""

    def __init__(self, config: EvalConfig) -> None:
        self.config = config
        self.meta = get_task_meta(config.task_id)
        self.ground_truth = load_ground_truth(self.meta)
        self.container: Container | None = None

    # ── pipeline steps ────────────────────────────────────────────────────

    def prepare_workspace(self, workspace_dir: Path) -> str:
        return prepare_workspace(self.meta, workspace_dir)

    def _resource_kwargs(self) -> dict:
        cfg = self.config
        mapping = {
            "mem_limit": cfg.container_mem_limit,
            "memswap_limit": cfg.container_memswap_limit,
            "nano_cpus": cfg.container_nano_cpus,
            "pids_limit": cfg.container_pids_limit,
        }
        return {k: v for k, v in mapping.items() if v is not None}

    def _start_container(self, client) -> Container:
        container_name = (
            f"tg-eval-{_container_name_part(self.config.task_id)}-{uuid4().hex[:8]}"
        )
        volumes = {
            str(self.config.runtime_dir.absolute()): {
                "bind": self.config.runtime_dir_in_container,
                "mode": "ro",
            },
        }
        run_kwargs = dict(
            image=self.config.agent_image,
            command=["tail", "-f", "/dev/null"],
            detach=True,
            name=container_name,
            volumes=volumes,
            environment={"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"},
            **self._resource_kwargs(),
        )
        last_err = None
        for attempt in range(3):
            try:
                self.container = client.containers.run(**run_kwargs)
                last_err = None
                break
            except (docker.errors.APIError, OSError) as e:
                last_err = e
                logger.warning(
                    "container creation attempt %d/3 failed: %s", attempt + 1, e
                )
                if "already in use" in str(e):
                    m = re.search(
                        r'is already in use by container "([0-9a-f]+)"', str(e)
                    )
                    if m:
                        try:
                            client.containers.get(m.group(1)).remove(force=True)
                        except Exception:
                            pass
                run_kwargs["name"] = f"{container_name}-{uuid4().hex[:8]}"
                time.sleep(5 * (attempt + 1))
        if last_err is not None:
            raise last_err
        assert self.container is not None
        logger.info("container started: %s", self.container.name)
        return self.container

    def _collect_outputs(self, container: Container, out_dir: Path) -> Path:
        outputs_dir = out_dir / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        # task deliverables
        for fname in ("final.spthy", "verdict.json", "attack_report.md"):
            try:
                docker_cp_from_container(
                    container.id,
                    f"/workspace/{fname}",
                    str(outputs_dir / fname),
                    check=False,
                )
            except Exception as e:  # noqa: BLE001
                logger.debug("collect %s failed: %s", fname, e)
        # workspace snapshot (size-filtered)
        if self.config.save_workspace_after_eval:
            ws_out = out_dir / "workspace"
            max_bytes = self.config.save_workspace_max_file_bytes
            copied = False
            if max_bytes is not None:
                copied = docker_cp_dir_from_container_filtered(
                    container.id, "/workspace", ws_out, max_bytes
                )
            if not copied:
                try:
                    docker_cp_from_container(container.id, "/workspace", str(ws_out))
                    self._prune_large(ws_out, max_bytes)
                except Exception as e:  # noqa: BLE001
                    logger.warning("workspace snapshot failed: %s", e)
        return outputs_dir

    @staticmethod
    def _prune_large(directory: Path, max_bytes: int | None) -> None:
        if max_bytes is None:
            return
        for path in directory.rglob("*"):
            try:
                if (
                    path.is_file()
                    and not path.is_symlink()
                    and path.stat().st_size > max_bytes
                ):
                    path.unlink()
            except OSError:
                pass

    def _collect_logs(self, container: Container, out_dir: Path) -> None:
        try:
            docker_cp_from_container(
                container.id, "/logs/.", str(out_dir / "logs"), check=False
            )
        except Exception as e:  # noqa: BLE001
            logger.warning("log collection failed: %s", e)

    def cleanup(self) -> None:
        if self.container is None:
            return
        if not self.config.keep_container:
            try:
                self.container.remove(force=True)
                logger.info("container %s removed", self.container.id[:12])
            except Exception as e:  # noqa: BLE001
                logger.warning("container removal failed: %s", e)
            finally:
                self.container = None
        else:
            logger.info("keeping container %s", self.container.id[:12])

    # ── main entry ────────────────────────────────────────────────────────

    def evaluate(self, agent: Agent) -> EvalResult:
        cfg = self.config
        cfg.out_dir.mkdir(parents=True, exist_ok=True)
        save_json(cfg, cfg.out_dir / "config.json", indent=2)

        workspace_dir = cfg.out_dir / "workspace"
        workspace_dir.mkdir(exist_ok=True)
        prompt = self.prepare_workspace(workspace_dir)

        task_description = (
            cfg.task_description_template.format(task_description=prompt)
            if cfg.task_description_template
            else prompt
        )

        client = get_docker_client()
        tic = time.perf_counter()
        try:
            container = self._start_container(client)
            container.exec_run(["mkdir", "-p", "/workspace", "/logs"])
            docker_cp_to_container(container.id, f"{workspace_dir}/.", "/workspace")
            logger.info("workspace copied into container")

            if not (cfg.api_key or cfg.credential_path):
                raise ValueError(
                    "no auth configured: api_key or credential_path required"
                )

            logger.info("running agent (task=%s)", cfg.task_id)
            try:
                agent.run(
                    AgentFnArguments(
                        task_description=task_description,
                        container_id=container.id,
                        runtime_dir_in_container=cfg.runtime_dir_in_container,
                        agent_timeout_seconds=cfg.agent_timeout_seconds,
                        out_dir=cfg.out_dir,
                        api_base_url=cfg.api_base_url,
                        api_key=(
                            cfg.api_key.get_secret_value() if cfg.api_key else None
                        ),
                        extra_kwargs=cfg.agent_extra_kwargs,
                        credential_path=cfg.credential_path,
                    )
                )
            except Exception:
                logger.exception("agent run failed")
        finally:
            toc = time.perf_counter()

        outputs_dir = cfg.out_dir / "outputs"
        try:
            outputs_dir = self._collect_outputs(container, cfg.out_dir)
        except Exception:
            logger.exception("output collection failed")

        if self.container is not None:
            self._collect_logs(self.container, cfg.out_dir)

        try:
            scorer = TamarinScorer(cfg, self.meta, self.ground_truth)
            checks = scorer.score(outputs_dir)
        except Exception as e:  # noqa: BLE001
            logger.exception("scoring failed")
            checks = [CheckResult(name="error", score=0.0, details={"error": str(e)})]

        result = EvalResult(task_id=cfg.task_id, elapsed_time=toc - tic, checks=checks)
        save_json(result, cfg.out_dir / "result.json", indent=2)
        logger.info(
            "task %s done: weighted_score=%.3f checks=%s",
            cfg.task_id,
            result.weighted_score,
            [(c.name, round(c.score, 2)) for c in checks],
        )
        self.cleanup()
        return result
