#!/usr/bin/env bash
# Build the portable agent runtime: static node + claude-code CLI (+ codex).
# Mounted read-only into agent containers at /data (ExploitGym-style: CLI
# updates never require image rebuilds).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RUNTIME_DIR="${REPO_ROOT}/data/runtime"
NODE_VERSION="${NODE_VERSION:-v22.14.0}"
NODE_DIR="${RUNTIME_DIR}/node"
BIN_DIR="${NODE_DIR}/bin"

mkdir -p "${RUNTIME_DIR}"

if [ -x "${BIN_DIR}/node" ] && [ -x "${BIN_DIR}/claude-code.sh" ]; then
    echo "runtime already present at ${NODE_DIR}; set FORCE=1 to rebuild"
    [ "${FORCE:-0}" = "1" ] || exit 0
fi

WORK="$(mktemp -d)"
trap 'rm -rf "${WORK}"' EXIT

echo ">> downloading node ${NODE_VERSION} (static)..."
ARCH="$(uname -m)"
case "${ARCH}" in
    x86_64)  NODE_ARCH=x64 ;;
    aarch64) NODE_ARCH=arm64 ;;
    *) echo "unsupported arch ${ARCH}" >&2; exit 1 ;;
esac
curl -fsSL --retry 3 -o "${WORK}/node.tar.xz" \
    "https://nodejs.org/dist/${NODE_VERSION}/node-${NODE_VERSION}-linux-${NODE_ARCH}.tar.xz"
mkdir -p "${NODE_DIR}"
tar -xJf "${WORK}/node.tar.xz" -C "${NODE_DIR}" --strip-components=1

echo ">> installing claude-code CLI..."
export PATH="${BIN_DIR}:${PATH}"
npm install -g @anthropic-ai/claude-code --prefix "${NODE_DIR}"

cat > "${BIN_DIR}/claude-code.sh" <<'EOF'
#!/usr/bin/env bash
# Wrapper: claude-code >= 2.1 ships a native binary (bin/claude.exe on
# Linux despite the name); older versions needed node + cli.js.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG="${DIR}/../lib/node_modules/@anthropic-ai/claude-code"
if [ -x "${PKG}/bin/claude.exe" ]; then
    exec "${PKG}/bin/claude.exe" "$@"
else
    exec "${DIR}/node" "${PKG}/cli.js" "$@"
fi
EOF
chmod +x "${BIN_DIR}/claude-code.sh"

echo ">> verifying..."
"${BIN_DIR}/node" --version
"${BIN_DIR}/claude-code.sh" --version || true

echo "runtime ready: ${NODE_DIR}"
