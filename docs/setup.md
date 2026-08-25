# Setup

## Prerequisites

- Linux host with Docker (28.x tested), ≥4 CPU / 8 GB free per concurrent task
- Python 3.12+ ([uv](https://docs.astral.sh/uv/))
- ~2 GB disk for images + task data

## Install

```bash
cd tamarin_bench
uv sync --extra proxy        # core deps + litellm proxy support
uv run prisma generate --schema "$(uv run python -c \
  "import litellm, pathlib; print(pathlib.Path(litellm.__file__).parent/'proxy'/'schema.prisma')")"
```

The prisma step is only needed for the LLM proxy's virtual-key budgets
(skip it when running with `DIRECT=1` or the mock agents).

## Build the images

```bash
bash scripts/setup/build_images.sh
```

Builds `tamaringym/agent:1.12.0` (debian:trixie + pinned tamarin-prover
1.12.0 + maude 3.4 + graphviz + toolbelt) and `tamaringym/verifier:1.12.0`
(minimal, scoring only). The Tamarin release archives are vendored under
`docker/bin/` — no network needed at build time beyond the base image and
packages.

Notes:

- arm64 hosts: the bottle binary's loader is patched to the system
  interpreter inside the Dockerfile.
- tamarin's output encoding requires `LANG=C.UTF-8` (set in both images and
  by the runner); with a C locale the ∀/∃ characters crash its output buffer.

## Build the agent runtime

```bash
bash scripts/setup/setup_runtime.sh
```

Downloads a static node build + the claude-code CLI into
`data/runtime/node/` (mounted read-only into agent containers at `/data`).
CLI updates never require an image rebuild.

## Task data

```bash
python scripts/convert_cfb.py          # CrypFormBench -> data/tasks/ (75 tasks)
python scripts/validate_tasks.py       # ground-truth re-validation in docker
```

`convert_cfb.py` reads the CrypFormBench checkout (default
`~/projects/CrypFormBench`). `validate_tasks.py` re-runs the pinned Tamarin
on every reference solution inside the verifier image and rewrites
`solution/ground_truth.json` (`validated: true`), including per-lemma
verdicts and attack-trace event sequences. **Re-run it whenever the pinned
Tamarin version changes** — verdicts are tool-version-sensitive.

Current v0 corpus: 75 tasks (L1×55, L2×10, L3×10), 46 SAFE / 29 UNSAFE,
all reference solutions terminate well under a minute.

## Pre-run check

```bash
python scripts/setup/pre_run.py        # add --check-only for a dry check
```

Verifies docker/tasks/images/runtime, then prints export lines for the
per-deployment secrets (token salt / flag seed) and optionally starts the
LLM proxy (+ postgres for virtual keys) and the two firewall proxies
(API-only *run* proxy + allow-all *install* proxy).
