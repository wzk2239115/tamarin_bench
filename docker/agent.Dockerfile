# ProtocolBench agent image: Tamarin + Verifpal multi-tool environment.
# Two symbolic protocol verifiers for tool-agnostic protocol analysis.
# Pinned: tamarin-prover 1.12.0, Verifpal 1.3.6
# (ProVerif to be added in a future build stage)
FROM debian:trixie

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

# maude 3.4, graphviz, analysis toolbelt
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
        maude libgmp10 graphviz patchelf xz-utils ca-certificates curl \
        python3 python3-pip ripgrep grep sed gawk jq file less vim nano \
        netcat-openbsd tmux git unzip \
    && rm -rf /var/lib/apt/lists/*

# ── Tamarin Prover 1.12.0 (vendored binaries) ────────────────────────────────
COPY bin/ /tmp/tamarin-dist/
RUN arch="$(dpkg --print-architecture)" && \
    if [ "$arch" = "arm64" ]; then \
        tar xzf /tmp/tamarin-dist/tamarin-prover-1.12.0-arm64.tar.gz -C /opt/ && \
        mv /opt/tamarin-prover/1.12.0/bin/tamarin-prover /usr/local/bin/tamarin-prover && \
        patchelf --set-interpreter /lib/ld-linux-aarch64.so.1 /usr/local/bin/tamarin-prover; \
    elif [ "$arch" = "amd64" ]; then \
        tar xzf /tmp/tamarin-dist/tamarin-prover-1.12.0-amd64.tar.gz -C /tmp/ && \
        mv /tmp/tamarin-prover /usr/local/bin/tamarin-prover; \
    else \
        echo "unsupported architecture: $arch" >&2; exit 1; \
    fi && \
    rm -rf /tmp/tamarin-dist /opt/tamarin-prover && \
    chmod +x /usr/local/bin/tamarin-prover

# ── Verifpal 1.3.6 (static binary, from release zip) ─────────────────────────
COPY bin/verifpal-arm64 /usr/local/bin/verifpal
RUN chmod +x /usr/local/bin/verifpal

# ── Verifpal example models (reference for agent) ───────────────────────────
COPY bin/verifpal-examples/ /opt/verifpal-examples/

# ── Protocol reference docs ──────────────────────────────────────────────────
RUN mkdir -p /opt/protocol-docs

# Sanity checks
RUN tamarin-prover --version 2>&1 | grep -q "1.12.0" && \
    verifpal --version 2>&1 | grep -q "1.3" && \
    maude --version | head -1

WORKDIR /workspace
CMD ["tail", "-f", "/dev/null"]
