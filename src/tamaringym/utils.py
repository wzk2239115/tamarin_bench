"""Docker helpers and misc utilities (adapted from ExploitGym's utils)."""

from __future__ import annotations

import logging
import os
import subprocess
from functools import lru_cache
from pathlib import Path

from pydantic_core import to_json

import docker

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parents[2].absolute()
DATA_DIR = PROJECT_ROOT / "data"


@lru_cache(maxsize=1)
def get_docker_client() -> docker.DockerClient:
    """Process-local cached Docker client (warm connection pool)."""
    return docker.from_env(timeout=int(os.environ.get("DOCKER_CLIENT_TIMEOUT", "300")))


def save_json(obj, path, indent=None, **kwargs) -> None:
    with open(path, "wb") as f:
        f.write(to_json(obj, indent=indent, **kwargs))


def docker_cp_to_container(
    container_id: str, host_path: str | Path, container_path: str, check: bool = True
) -> None:
    proc = subprocess.run(
        ["docker", "cp", str(host_path), f"{container_id}:{container_path}"],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    logger.debug("docker cp output: %s", proc.stdout.decode(errors="replace").rstrip())


def docker_cp_from_container(
    container_id: str, container_path: str, host_path: str | Path, check: bool = True
) -> None:
    proc = subprocess.run(
        ["docker", "cp", f"{container_id}:{container_path}", str(host_path)],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    logger.debug("docker cp output: %s", proc.stdout.decode(errors="replace").rstrip())


def docker_cp_dir_from_container_filtered(
    container_id: str, container_path: str, host_path: str | Path, max_bytes: int
) -> bool:
    """Copy a directory out of a container, skipping files larger than
    *max_bytes*. Returns False when the in-container filter was unavailable
    (caller should fall back to a plain copy + host-side prune)."""
    host_path = Path(host_path)
    host_path.mkdir(parents=True, exist_ok=True)
    script = (
        f"cd {container_path} && find . -type f -size -{max_bytes}c -print0 "
        f"| tar --null -cf - --files-from -"
    )
    cmd = ["docker", "exec", container_id, "bash", "-c", script]
    tar = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if tar.returncode != 0:
        return False
    untar = subprocess.run(
        ["tar", "-xf", "-", "-C", str(host_path)],
        input=tar.stdout,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return untar.returncode == 0


def container_exec(
    container,
    cmd: list[str] | str,
    *,
    env: dict | None = None,
    workdir: str | None = None,
    check: bool = False,
):
    """Run a command inside a container via docker exec."""
    if isinstance(cmd, str):
        argv = ["bash", "-c", cmd]
    else:
        argv = cmd
    return container.exec_run(argv, environment=env, workdir=workdir, demux=False)
