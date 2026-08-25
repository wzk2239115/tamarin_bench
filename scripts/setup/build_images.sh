#!/usr/bin/env bash
# Build the agent and verifier images (pinned tamarin 1.12.0 from docker/bin/).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TAG="${TAMARIN_IMAGE_TAG:-1.12.0}"

for img in agent verifier; do
    docker build -f "${REPO_ROOT}/docker/${img}.Dockerfile" \
        -t "tamaringym/${img}:${TAG}" \
        "${REPO_ROOT}/docker"
done

echo "Built tamaringym/agent:${TAG} and tamaringym/verifier:${TAG}"
