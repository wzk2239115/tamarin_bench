#!/usr/bin/env bash
# Multi-tenant orchestration for tamarin_bench (pattern from ExploitGym's run_as.sh).
#
#   bash run_as.sh <name>           start/resume a named eval slot
#   INTERACTIVE=1 bash run_as.sh <name>   drop into the agent container instead
#   bash run_as.sh --stop <name>    layered teardown
#
# Per-slot resources: proxy port 4000+slot, out dir out/<name>/, lock file.
# Env: AGENT, TASKS_FILE, TIMEOUT, MAX_WORKERS, BUDGET, GLM_MODEL,
#      GLM_PROVIDER, GLM_API_KEY, MODEL_ALIAS, DIRECT=1 (bypass proxy).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${REPO_ROOT}"

STOP_GRACE="${STOP_GRACE:-90}"

# ── argument parsing ────────────────────────────────────────────────────────
ACTION="run"
NAME=""
if [ "${1:-}" = "--stop" ]; then
    ACTION="stop"; NAME="${2:?usage: run_as.sh --stop <name>}"
elif [ "${1:-}" = "--status" ]; then
    ACTION="status"; NAME="${2:?usage: run_as.sh --status <name>}"
else
    NAME="${1:?usage: run_as.sh <name> | --stop <name> | --status <name>}"
fi

LOCK_DIR="${REPO_ROOT}/logs/${NAME}"
OUT_DIR="${REPO_ROOT}/out/${NAME}/run_agent"
PROXY_PORT="${PROXY_PORT:-$((4000 + $(echo "$NAME" | cksum | cut -d' ' -f1) % 100))}"
RUNNER_PID_FILE="${LOCK_DIR}/runner.pid"
PROXY_PID_FILE="${LOCK_DIR}/proxy.pid"
mkdir -p "${LOCK_DIR}" "${OUT_DIR}"

# ── stop: layered teardown (runner → containers → proxy) ────────────────────
stop_slot() {
    echo ">> stopping slot '${NAME}'"
    # 1. runner: SIGINT (graceful) → SIGTERM → SIGKILL
    if [ -f "${RUNNER_PID_FILE}" ] && kill -0 "$(cat "${RUNNER_PID_FILE}")" 2>/dev/null; then
        PID="$(cat "${RUNNER_PID_FILE}")"
        echo ">> SIGINT runner (pid ${PID}), grace ${STOP_GRACE}s"
        kill -INT "${PID}" 2>/dev/null || true
        for _ in $(seq 1 "${STOP_GRACE}"); do
            kill -0 "${PID}" 2>/dev/null || break
            sleep 1
        done
        if kill -0 "${PID}" 2>/dev/null; then
            echo ">> SIGTERM runner"
            kill -TERM "${PID}" 2>/dev/null || true; sleep 10
        fi
        kill -0 "${PID}" 2>/dev/null && { echo ">> SIGKILL runner"; kill -KILL "${PID}" 2>/dev/null || true; }
    fi
    # 2. leftover eval containers (label-scoped, never by port)
    docker ps -q --filter "label=tamaringym.owner=${NAME}" | while read -r cid; do
        echo ">> removing leftover container ${cid:0:12}"
        docker rm -f "${cid}" >/dev/null 2>&1 || true
    done
    # 3. our litellm proxy subprocess (pid file), if DIRECT=0
    if [ -f "${PROXY_PID_FILE}" ] && kill -0 "$(cat "${PROXY_PID_FILE}")" 2>/dev/null; then
        echo ">> stopping proxy (pid $(cat "${PROXY_PID_FILE}"))"
        kill -TERM "$(cat "${PROXY_PID_FILE}")" 2>/dev/null || true
    fi
    rm -f "${LOCK_DIR}/run.lock" "${RUNNER_PID_FILE}" "${PROXY_PID_FILE}"
    echo ">> slot '${NAME}' stopped (firewall proxies are shared and left running)"
}

status_slot() {
    echo "slot '${NAME}':"
    [ -f "${LOCK_DIR}/run.lock" ] && echo "  lock: $(cat "${LOCK_DIR}/run.lock")" || echo "  lock: none"
    [ -f "${RUNNER_PID_FILE}" ] && kill -0 "$(cat "${RUNNER_PID_FILE}")" 2>/dev/null \
        && echo "  runner: running (pid $(cat "${RUNNER_PID_FILE}"))" || echo "  runner: not running"
    echo "  results: $(find "${OUT_DIR}" -name result.json 2>/dev/null | wc -l) tasks"
    echo "  containers: $(docker ps -q --filter "label=tamaringym.owner=${NAME}" | wc -l)"
}

case "${ACTION}" in
    stop) stop_slot; exit 0 ;;
    status) status_slot; exit 0 ;;
esac

# ── mutual exclusion ────────────────────────────────────────────────────────
if [ -f "${LOCK_DIR}/run.lock" ] && [ -n "$(cat "${LOCK_DIR}/run.lock" 2>/dev/null)" ]; then
    LOCKED_BY="$(cat "${LOCK_DIR}/run.lock")"
    if [ "${FORCE_RUN:-0}" = "1" ]; then
        echo ">> FORCE_RUN=1: overriding lock held by '${LOCKED_BY}'"
    else
        echo "ERROR: slot '${NAME}' is locked by '${LOCKED_BY}'. Use FORCE_RUN=1 to take over or another name." >&2
        exit 1
    fi
fi
echo "$$ $(date -Is) ${USER:-unknown}" > "${LOCK_DIR}/run.lock"
trap 'rm -f "${LOCK_DIR}/run.lock"' EXIT

# ── configuration ───────────────────────────────────────────────────────────
AGENT="${AGENT:-claude_code}"
TASKS_FILE="${TASKS_FILE:-data/task_ids/v0.txt}"
TIMEOUT="${TIMEOUT:-3600}"
MAX_WORKERS="${MAX_WORKERS:-1}"
BUDGET="${BUDGET:-20}"
GLM_MODEL="${GLM_MODEL:-claude-sonnet-4-6}"
REASONING_EFFORT="${REASONING_EFFORT:-}"
INTERACTIVE="${INTERACTIVE:-0}"
DIRECT="${DIRECT:-0}"
export TAMARINGYM_OWNER="${NAME}"

# ── proxy ───────────────────────────────────────────────────────────────────
API_ARGS=()
if [ "${DIRECT}" = "1" ]; then
    echo ">> DIRECT=1: bypassing proxy, using ANTHROPIC_API_KEY from env"
    API_ARGS+=(--api-key "${ANTHROPIC_API_KEY:?ANTHROPIC_API_KEY required in DIRECT mode}")
    API_ARGS+=(--api-base-url "${ANTHROPIC_BASE_URL:-}")
else
    export TAMARINGYM_PROXY_DIR="${LOCK_DIR}/proxy"
    echo ">> starting LLM proxy on port ${PROXY_PORT} (GLM_PROVIDER=${GLM_PROVIDER:-none})"
    python -m tamaringym.llm_proxy start --port "${PROXY_PORT}" \
        --workdir "${LOCK_DIR}/proxy" >/dev/null 2>&1 &
    PROXY_PID=$!
    echo "${PROXY_PID}" > "${PROXY_PID_FILE}"
    for _ in $(seq 1 60); do
        curl -sf "http://127.0.0.1:${PROXY_PORT}/health/liveliness" >/dev/null 2>&1 && break
        sleep 1
    done
    API_ARGS+=(--api-base-url "http://127.0.0.1:${PROXY_PORT}")
    API_ARGS+=(--api-key "master-key-placeholder")  # runner mints per-task keys
fi

COMMON_ARGS=(
    --tasks-file "${TASKS_FILE}"
    --out-dir "${OUT_DIR}"
    --agent "${AGENT}"
    --claude-model "${GLM_MODEL}"
    --timeout "${TIMEOUT}"
    --max-workers "${MAX_WORKERS}"
    "${API_ARGS[@]}"
)
[ -n "${REASONING_EFFORT}" ] && COMMON_ARGS+=(--reasoning-effort "${REASONING_EFFORT}")

# ── run ─────────────────────────────────────────────────────────────────────
if [ "${INTERACTIVE}" = "1" ]; then
    echo ">> interactive mode: bash shell inside a task container"
    python scripts/interactive.py --task "$(head -1 "${TASKS_FILE}")" --name "${NAME}"
    exit 0
fi

echo ">> runner: ${AGENT} model=${GLM_MODEL} tasks=${TASKS_FILE} workers=${MAX_WORKERS} timeout=${TIMEOUT}s"
python examples/run_agent.py "${COMMON_ARGS[@]}" &
RUNNER_PID=$!
echo "${RUNNER_PID}" > "${RUNNER_PID_FILE}"
wait "${RUNNER_PID}"
RC=$?
rm -f "${RUNNER_PID_FILE}"
echo ">> runner finished with exit code ${RC}"
exit "${RC}"
