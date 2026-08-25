"""Task tokens and per-deployment secrets.

Mirrors ExploitGym's token design:

* ``generate_token`` / ``verify_token`` — HMAC-checksummed task tokens that
  bind an agent run to a task id (used by the controller when one exists).
* ``generate_verdict_key`` — a deterministic per-task key derived from the
  deployment's flag seed. It binds a recorded result to the deployment (a
  result produced against a different seed/ground-truth state cannot be
  replayed unnoticed) and serves as the tamarin-bench analog of the flag:
  the *expected verdict* is never stored anywhere the agent can reach.

Both the token salt and the flag seed are per-deployment secrets: they are
never hardcoded and must be passed in explicitly (the controller mints them
on startup, or ``scripts/setup/pre_run.py`` prints export lines).
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
from uuid import uuid4

__all__ = [
    "MAX_TASK_ID_LENGTH",
    "SALT_ENV_VAR",
    "FLAG_SEED_ENV_VAR",
    "API_KEY_ENV_VAR",
    "generate_secret",
    "require_secret",
    "resolve_secret",
    "generate_token",
    "verify_token",
    "generate_verdict_key",
]

MAX_TASK_ID_LENGTH = 63
TOKEN_BYTE_LENGTH = 96

SALT_ENV_VAR = "TAMARINGYM_SERVER_SALT"
FLAG_SEED_ENV_VAR = "TAMARINGYM_SERVER_FLAG_SEED"
API_KEY_ENV_VAR = "TAMARINGYM_SERVER_API_KEY"


def generate_secret(prefix: str) -> str:
    """Mint a fresh random secret, e.g. ``generate_secret("tg")`` → ``tg-<uuid4>``."""
    return f"{prefix}-{uuid4()}"


def require_secret(value: str | None, *, name: str, env_var: str) -> str:
    if not value:
        raise ValueError(
            f"{name} is not configured. It is a per-deployment secret: export "
            f"{env_var}=<value> (the controller / pre_run.py prints the values "
            "it generated at startup), or pass it explicitly."
        )
    return value


def resolve_secret(value: str | None, *, name: str, env_var: str) -> str:
    candidate = os.environ.get(env_var) if value is None else value
    return require_secret(candidate, name=name, env_var=env_var)


def generate_token(
    task_info: str, *, salt: str, agent_id: str | None = None
) -> tuple[str, str]:
    """Mint a task token: ``hex(len(task_info)) + task_info + checksum + pad``.

    The checksum is ``sha256(agent_id + task_info + salt)`` so a token is
    bound to both the run and the task.
    """
    task_info_len = len(task_info)
    if task_info_len > MAX_TASK_ID_LENGTH:
        raise ValueError("task_info is too long")
    if not salt:
        raise ValueError("salt must be a non-empty per-deployment secret")
    if agent_id is None:
        agent_id = uuid4().hex
    checksum = hashlib.sha256(f"{agent_id}{task_info}{salt}".encode()).digest()
    token_bytes = bytes([task_info_len]) + task_info.encode() + checksum
    token_bytes += uuid4().bytes
    token_bytes = token_bytes[:TOKEN_BYTE_LENGTH]
    token = base64.urlsafe_b64encode(token_bytes).decode()
    return agent_id, token


def verify_token(agent_id: str, token: str, *, salt: str) -> str | None:
    """Return the task_info if the token's checksum verifies, else None."""
    if not salt:
        raise ValueError("salt must be a non-empty per-deployment secret")
    try:
        token_bytes = base64.urlsafe_b64decode(token.encode())
        task_info_len = token_bytes[0]
        task_info = token_bytes[1 : 1 + task_info_len].decode()
        checksum = token_bytes[1 + task_info_len : 1 + task_info_len + 32]
        expected_checksum = hashlib.sha256(
            f"{agent_id}{task_info}{salt}".encode()
        ).digest()
        if hmac.compare_digest(checksum, expected_checksum):
            return task_info
    except Exception:
        pass
    return None


def generate_verdict_key(task_id: str, *, seed: str) -> str:
    """Derive the per-task verdict key from the deployment flag seed.

    This is the tamarin-bench analog of ExploitGym's ``flag{...}``: it
    identifies the expected-outcome state of a task within a deployment.
    Recorded in ``result.json`` so results are bound to the seed/ground
    truth they were produced against.
    """
    if not seed:
        raise ValueError("seed must be a non-empty per-deployment secret")
    mac = hmac.new(seed.encode(), task_id.encode(), hashlib.sha256).hexdigest()
    return f"tvk-{mac[:32]}"
