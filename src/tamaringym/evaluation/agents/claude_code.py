"""Claude Code CLI agent (pattern from ExploitGym).

The CLI is a static node build mounted read-only into the agent container
at ``/data/node/bin/claude-code.sh`` (see ``scripts/setup/setup_runtime.sh``).
Invocation:

    cat /tmp/prompt.txt | timeout <t> /data/node/bin/claude-code.sh \
        --verbose --output-format=stream-json \
        --permission-mode=bypassPermissions \
        --disallowed-tools WebSearch,WebFetch \
        2>&1 | tee /logs/claude_code.log

Environment pins the model, disables non-essential traffic, and forces all
model aliases to the configured model when a custom base URL is used.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from tamaringym.evaluation.agents.base import Agent
from tamaringym.evaluation.types import AgentFnArguments
from tamaringym.utils import get_docker_client

logger = logging.getLogger(__name__)

DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-6"
CLAUDE_CODE_BIN_PATH = "/data/node/bin/claude-code.sh"

VALID_EFFORT_LEVELS = {"low", "medium", "high", "xhigh", "max", "auto"}


def run_claude_code_with_container(args: AgentFnArguments) -> None:
    claude_model = args.extra_kwargs.get("claude_model", DEFAULT_CLAUDE_MODEL)
    reasoning_effort = args.extra_kwargs.get("reasoning_effort")
    claude_code_bin = args.extra_kwargs.get("claude_code_bin", CLAUDE_CODE_BIN_PATH)
    if reasoning_effort is not None and reasoning_effort not in VALID_EFFORT_LEVELS:
        raise ValueError(
            f"Invalid reasoning_effort {reasoning_effort!r}; "
            f"expected one of {sorted(VALID_EFFORT_LEVELS)}"
        )

    if not args.api_key and not args.credential_path:
        raise ValueError("Either api_key or credential_path must be provided")
    if not args.container_id:
        raise ValueError("container_id is required")

    logger.info(
        "Starting Claude Code agent: model=%s, effort=%s, timeout=%ds",
        claude_model,
        reasoning_effort or "<cli default>",
        args.agent_timeout_seconds,
    )

    client = get_docker_client()
    container = client.containers.get(args.container_id)
    container.exec_run(["mkdir", "-p", "/logs"])

    # symlink credential file if provided (docker-cp'd by the caller)
    if args.credential_path:
        resolved = Path(args.credential_path).expanduser().resolve()
        if not resolved.exists():
            raise FileNotFoundError(f"Credential file not found: {resolved}")
        cred_link = f"/logs/{resolved.name}"
        container.exec_run(["ln", "-sf", f"/logs/cred_{resolved.name}", cred_link])

    prompt = args.task_description
    prompt_path = "/tmp/prompt.txt"
    container.exec_run(
        [
            "bash",
            "-c",
            f"cat > {prompt_path} << 'PROMPT_EOF'\n{prompt}\nPROMPT_EOF",
        ]
    )

    extra_args = ""
    if args.disable_web_search:
        extra_args += "--disallowed-tools WebSearch,WebFetch"
    claude_command = (
        f"cat {prompt_path} | timeout {args.agent_timeout_seconds} "
        f"{claude_code_bin} "
        "--verbose --output-format=stream-json "
        "--permission-mode=bypassPermissions "
        f"{extra_args} "
        f"2>&1 | tee /logs/claude_code.log"
    )
    env = {
        "ANTHROPIC_BASE_URL": args.api_base_url or os.environ.get("ANTHROPIC_BASE_URL"),
        "ANTHROPIC_API_KEY": args.api_key,
        "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
        "ANTHROPIC_MODEL": claude_model,
        "IS_SANDBOX": "1",
        "CLAUDE_CONFIG_DIR": "/logs",
        "API_TIMEOUT_MS": "3000000",
        "CLAUDE_CODE_MAX_RETRIES": "10",
        "CLAUDE_CODE_EFFORT_LEVEL": reasoning_effort,
    }
    # Bearer-token auth (Z.AI / 360 native Anthropic endpoints): claude code
    # sends Authorization: Bearer for ANTHROPIC_AUTH_TOKEN instead of the
    # x-api-key header it uses for ANTHROPIC_API_KEY.
    auth_token = args.extra_kwargs.get("auth_token") or os.environ.get(
        "ANTHROPIC_AUTH_TOKEN"
    )
    if auth_token:
        env["ANTHROPIC_AUTH_TOKEN"] = auth_token
        env.pop("ANTHROPIC_API_KEY", None)
    if args.firewall_env:
        env.update(args.firewall_env)
    env = {k: v for k, v in env.items() if v is not None}
    if "ANTHROPIC_BASE_URL" in env and "ANTHROPIC_MODEL" in env:
        env["ANTHROPIC_DEFAULT_SONNET_MODEL"] = env["ANTHROPIC_MODEL"]
        env["ANTHROPIC_DEFAULT_OPUS_MODEL"] = env["ANTHROPIC_MODEL"]
        env["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = env["ANTHROPIC_MODEL"]
        env["CLAUDE_CODE_SUBAGENT_MODEL"] = env["ANTHROPIC_MODEL"]

    resp = client.api.exec_create(
        args.container_id,
        ["bash", "-c", claude_command],
        stdout=True,
        stderr=True,
        environment=env,
        workdir="/workspace",
    )
    exec_output = client.api.exec_start(resp["Id"], stream=True, socket=False)

    rendered_log_dir = args.out_dir / "logs"
    rendered_log_dir.mkdir(parents=True, exist_ok=True)
    rendered_log_path = rendered_log_dir / "claude_code.log"
    with rendered_log_path.open("w", encoding="utf-8") as out:
        for chunk in exec_output:
            if chunk:
                out.write(chunk.decode(errors="replace"))
                out.flush()

    exit_code = client.api.exec_inspect(resp["Id"])["ExitCode"]
    logger.info("Claude Code exit code: %d", exit_code)


class ClaudeCodeAgent(Agent):
    def run(self, args: AgentFnArguments) -> None:
        run_claude_code_with_container(args)
