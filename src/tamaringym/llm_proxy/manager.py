"""LLM proxy management (LiteLLM-based, adapted from ExploitGym).

Runs a LiteLLM proxy as a host subprocess with a generated config:

* provider routes from environment keys (Anthropic/OpenAI/...), or a native
  Anthropic-protocol passthrough for custom endpoints (``GLM_PROVIDER=anthropic``,
  the 360/Z.AI/DeepSeek routing documented in ExploitGym's AGENTS.md that
  avoids LiteLLM's buggy chat/completions translation layer);
* per-task virtual keys with budgets and model scoping via LiteLLM's native
  ``/key/generate`` / ``/key/info`` / ``/key/delete`` endpoints;
* web search is blocked at two other layers already: the CLI
  (``--disallowed-tools WebSearch,WebFetch``) and the firewall allowlist
  (no general egress). The proxy exists for budgets + model pinning.

Usage::

    from tamaringym.llm_proxy import LLMProxyManager, ProxyKeyManager

    mgr = LLMProxyManager(port=4000)
    mgr.start()                      # generates config + spawns litellm
    keys = ProxyKeyManager(mgr.url, admin_key=mgr.master_key)
    key = keys.generate_api_key(max_budget=20.0)
    # agent uses api_base_url=mgr.url, api_key=key
"""

from __future__ import annotations

import logging
import os
import secrets
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

DEFAULT_PORT = 4000

_WILDCARD_PROVIDERS = ("anthropic", "openai", "gemini")


class LLMProxyManager:
    """Generates the LiteLLM config and runs the proxy as a subprocess."""

    def __init__(
        self,
        port: int = DEFAULT_PORT,
        workdir: str | Path | None = None,
        glm_provider: str | None = None,
        glm_model: str | None = None,
        glm_api_key: str | None = None,
        glm_api_base: str | None = None,
    ) -> None:
        self.port = port
        self.workdir = (
            Path(workdir)
            if workdir
            else Path(
                os.environ.get(
                    "TAMARINGYM_PROXY_DIR", Path.tempdir() / "tamaringym-proxy"
                )
            )
        )
        self.glm_provider = glm_provider or os.environ.get("GLM_PROVIDER")
        self.glm_model = glm_model or os.environ.get("GLM_MODEL")
        self.glm_api_key = glm_api_key or os.environ.get("GLM_API_KEY")
        self.glm_api_base = glm_api_base or os.environ.get("GLM_API_BASE")
        self.master_key = os.environ.get("TAMARINGYM_PROXY_MASTER_KEY") or (
            "tg-master-" + secrets.token_hex(16)
        )
        self._proc: subprocess.Popen | None = None

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    # ── config generation ──────────────────────────────────────────────────

    def _model_entries(self) -> list[dict]:
        entries: list[dict] = []
        if self.glm_provider == "anthropic" and self.glm_model:
            # native Anthropic-protocol passthrough: no chat/completions
            # translation (see ExploitGym AGENTS.md — the litellm translation
            # layer drops stream chunks / reasoning deltas)
            entries.append(
                {
                    "model_name": self.glm_model,
                    "litellm_params": {
                        "model": f"anthropic/{self.glm_model}",
                        "api_key": self.glm_api_key or "os.environ/GLM_API_KEY",
                        "api_base": self.glm_api_base or "os.environ/GLM_API_BASE",
                    },
                }
            )
            return entries
        # local claude-code-style envs: ANTHROPIC_AUTH_TOKEN + ANTHROPIC_BASE_URL
        # (e.g. Z.AI's native Anthropic endpoint) — route through litellm's
        # anthropic provider with the token as api_key (endpoint accepts both
        # x-api-key and Bearer).
        auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
        base_url = os.environ.get("ANTHROPIC_BASE_URL")
        if auth_token and base_url and base_url != "https://api.anthropic.com":
            model = os.environ.get("ANTHROPIC_MODEL", "glm-5.3")
            entries.append(
                {
                    "model_name": model,
                    "litellm_params": {
                        "model": f"anthropic/{model}",
                        "api_key": auth_token,
                        "api_base": base_url,
                    },
                }
            )
        for provider in _WILDCARD_PROVIDERS:
            env_key = f"{provider.upper()}_API_KEY"
            if os.environ.get(env_key):
                entries.append(
                    {
                        "model_name": f"{provider}/*",
                        "litellm_params": {
                            "model": f"{provider}/*",
                            "api_key": f"os.environ/{env_key}",
                        },
                    }
                )
        return entries

    def write_config(self) -> Path:
        import yaml

        self.workdir.mkdir(parents=True, exist_ok=True)
        cfg = {
            "model_list": self._model_entries(),
            "litellm_settings": {"drop_params": True},
            "general_settings": {"master_key": self.master_key},
        }
        if not cfg["model_list"]:
            logger.warning(
                "no provider keys found in env (ANTHROPIC_API_KEY / OPENAI_API_KEY / "
                "GLM_*); the proxy will start but route nothing"
            )
        path = self.workdir / "litellm_config.yaml"
        path.write_text(yaml.safe_dump(cfg, sort_keys=False))
        return path

    # ── database (litellm virtual keys need postgres) ──────────────────────

    POSTGRES_CONTAINER = "tamaringym-postgres"
    POSTGRES_IMAGE = "docker.m.daocloud.io/library/postgres:16-alpine"

    def _database_url(self) -> str | None:
        """Existing DATABASE_URL, else start (or reuse) the postgres container."""
        if os.environ.get("DATABASE_URL"):
            return os.environ["DATABASE_URL"]
        from docker.errors import NotFound

        import docker

        client = docker.from_env()
        password = os.environ.get("TAMARINGYM_PG_PASSWORD") or secrets.token_hex(12)
        try:
            container = client.containers.get(self.POSTGRES_CONTAINER)
            if container.status != "running":
                container.start()
        except NotFound:
            container = client.containers.run(
                self.POSTGRES_IMAGE,
                name=self.POSTGRES_CONTAINER,
                detach=True,
                environment={
                    "POSTGRES_USER": "litellm",
                    "POSTGRES_PASSWORD": password,
                    "POSTGRES_DB": "litellm",
                },
                labels={"tamaringym.owner": "proxy"},
            )
        # fixed host port keeps the URL stable across restarts
        host_port = int(os.environ.get("TAMARINGYM_PG_PORT", "45432"))
        try:
            client.networks.get("bridge").disconnect(container)
        except Exception:  # noqa: BLE001
            pass
        try:
            container.reload()
            ports = container.attrs.get("NetworkSettings", {}).get("Ports", {}) or {}
            if "5432/tcp" not in ports or not ports["5432/tcp"]:
                # (re)publish on the host port: requires recreate
                container.remove(force=True)
                container = client.containers.run(
                    self.POSTGRES_IMAGE,
                    name=self.POSTGRES_CONTAINER,
                    detach=True,
                    environment={
                        "POSTGRES_USER": "litellm",
                        "POSTGRES_PASSWORD": password,
                        "POSTGRES_DB": "litellm",
                    },
                    ports={"5432/tcp": ("127.0.0.1", host_port)},
                    labels={"tamaringym.owner": "proxy"},
                )
        except Exception as e:  # noqa: BLE001
            logger.warning("postgres port publish failed: %s", e)
        # wait for readiness
        for _ in range(60):
            res = container.exec_run(["pg_isready", "-U", "litellm", "-d", "litellm"])
            if res.exit_code == 0:
                logger.info("postgres ready on 127.0.0.1:%d", host_port)
                return f"postgresql://litellm:{password}@127.0.0.1:{host_port}/litellm"
            time.sleep(1)
        raise RuntimeError("postgres did not become ready within 60s")

    # ── lifecycle ──────────────────────────────────────────────────────────

    def is_running(self) -> bool:
        try:
            with httpx.Client(base_url=self.url, timeout=2) as c:
                r = c.get("/health/liveliness")
                return r.status_code == 200
        except httpx.HTTPError:
            return False

    def start(self, force: bool = False) -> None:
        if self.is_running():
            if not force:
                logger.info("proxy already running at %s", self.url)
                return
            self.stop()
        cfg_path = self.write_config()
        log_path = self.workdir / "litellm.log"
        log_f = log_path.open("ab")
        # litellm ships a console script (no __main__); prefer it, fall back
        # to the module entry point
        litellm_bin = Path(sys.executable).parent / "litellm"
        argv = (
            [str(litellm_bin)]
            if litellm_bin.is_file()
            else [sys.executable, "-m", "litellm"]
        )
        self._proc = subprocess.Popen(
            [
                *argv,
                "--config",
                str(cfg_path),
                "--port",
                str(self.port),
                "--host",
                "0.0.0.0",
                "--detailed_debug",
            ],
            stdout=log_f,
            stderr=subprocess.STDOUT,
            env={
                **os.environ,
                "LITELLM_MASTER_KEY": self.master_key,
                "DATABASE_URL": self._database_url() or "",
                "STORE_MODEL_IN_DB": "True",
            },
        )
        for _ in range(60):
            if self.is_running():
                logger.info("litellm proxy up at %s (config=%s)", self.url, cfg_path)
                return
            if self._proc.poll() is not None:
                raise RuntimeError(
                    f"litellm exited with {self._proc.returncode}; see {log_path}"
                )
            time.sleep(1)
        raise RuntimeError(f"proxy did not become healthy; see {log_path}")

    def stop(self) -> None:
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self._proc.kill()
            logger.info("proxy subprocess stopped")
        self._proc = None


class ProxyKeyManager:
    """Mint/inspect/delete virtual keys on the LiteLLM proxy."""

    def __init__(
        self,
        proxy_url: str,
        admin_key: str,
        default_max_budget: float = 20.0,
        default_allowed_models: list[str] | None = None,
    ) -> None:
        self.proxy_url = proxy_url.rstrip("/")
        self.admin_key = admin_key
        self.default_max_budget = default_max_budget
        self.default_allowed_models = default_allowed_models
        self._alive_keys: set[str] = set()

    @property
    def api_base_url(self) -> str:
        return self.proxy_url

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.admin_key}"}

    def generate_api_key(
        self, max_budget: float | None = None, allowed_models: list[str] | None = None
    ) -> str:
        budget = max_budget or self.default_max_budget
        models = (
            allowed_models
            if allowed_models is not None
            else self.default_allowed_models
        )
        payload: dict = {
            "max_budget": budget,
            "key_alias": f"tg-{secrets.token_hex(4)}",
        }
        if models:
            payload["models"] = list(models)
        with httpx.Client(
            base_url=self.proxy_url, timeout=30, headers=self._headers()
        ) as c:
            r = c.post("/key/generate", json=payload)
            r.raise_for_status()
            key = r.json()["key"]
        self._alive_keys.add(key)
        logger.info(
            "minted proxy key %s...%s (budget $%.2f)", key[:8], key[-4:], budget
        )
        return key

    def get_api_key_usage(self, api_key: str) -> dict:
        with httpx.Client(
            base_url=self.proxy_url, timeout=30, headers=self._headers()
        ) as c:
            r = c.get("/key/info", params={"key": api_key})
            r.raise_for_status()
            info = r.json()
        details = info.get("key_info") or [{}]
        d = details[0] if isinstance(details, list) else details
        return {
            "spend": d.get("spend", 0.0),
            "remaining": d.get("remaining_budget", None),
            "requests": d.get("num_requests", None) or d.get("requests", 0),
        }

    def delete_api_key(self, api_key: str) -> None:
        with httpx.Client(
            base_url=self.proxy_url, timeout=30, headers=self._headers()
        ) as c:
            r = c.post("/key/delete", json={"keys": [api_key]})
            r.raise_for_status()
        self._alive_keys.discard(api_key)

    def revoke_all(self) -> None:
        for key in list(self._alive_keys):
            try:
                self.delete_api_key(key)
            except Exception as e:  # noqa: BLE001
                logger.warning("failed to revoke key: %s", e)


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main() -> None:
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    ap = argparse.ArgumentParser(description="manage the ProtocolBench LLM proxy")
    ap.add_argument("action", choices=["start", "stop", "status"])
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--workdir", type=Path, default=None)
    args = ap.parse_args()
    mgr = LLMProxyManager(port=args.port, workdir=args.workdir)
    if args.action == "start":
        mgr.start()
        print(f"proxy: {mgr.url} master_key={mgr.master_key}")
    elif args.action == "stop":
        mgr.stop()
    else:
        print(f"running={mgr.is_running()} url={mgr.url}")


if __name__ == "__main__":
    main()
