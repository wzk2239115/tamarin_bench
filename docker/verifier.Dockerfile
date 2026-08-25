# TamarinGym verifier image: minimal Tamarin environment for scoring.
# Same pinned tamarin as the agent image so verdicts are comparable.
FROM debian:trixie

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
        maude libgmp10 graphviz patchelf ca-certificates python3-minimal \
    && rm -rf /var/lib/apt/lists/*

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

RUN tamarin-prover --version 2>&1 | grep -q "1.12.0"

WORKDIR /verify
CMD ["true"]
