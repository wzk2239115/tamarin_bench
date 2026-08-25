# TamarinGym agent image: Tamarin + toolchain for the CLI agent.
# Pinned: tamarin-prover 1.12.0 (vendored binaries in docker/bin/), maude 3.4 (debian:trixie).
FROM debian:trixie

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

# maude 3.4 (supported by tamarin 1.12.0), graphviz for trace rendering,
# plus a basic analysis toolbelt for the agent.
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
        maude libgmp10 graphviz patchelf xz-utils ca-certificates curl \
        python3 python3-pip ripgrep grep sed gawk jq file less vim nano \
        netcat-openbsd tmux git unzip \
    && rm -rf /var/lib/apt/lists/*

# Install pinned tamarin-prover from the vendored release archives.
# arm64: homebrew bottle (loader patched to the system interpreter)
# amd64: official linux64-ubuntu static-ish build (standard loader)
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

# Sanity check: tamarin + maude versions (fails the build on a broken toolchain).
RUN tamarin-prover --version 2>&1 | grep -q "1.12.0" && maude --version | head -1

WORKDIR /workspace
CMD ["tail", "-f", "/dev/null"]
