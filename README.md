# tamarin_bench (TamarinGym)

A benchmark for evaluating AI **agents** (Claude Code / Codex CLI harnesses in Docker
containers, long-horizon tasks) on **security protocol formal verification with
[Tamarin](https://tamarin-prover.github.io/)**: modeling protocols, formulating
security properties, driving the prover, and **discovering attacks**.

Tasks are derived from the [CrypFormBench](https://arxiv.org/abs/2606.25561)
spthy dataset (58+ verified protocol theories with ground-truth verdicts) and
re-packaged as long-horizon agentic tasks in the style of
[ExploitGym](https://arxiv.org/abs/2605.11086): pinned CLI agents, isolated
containers, egress firewalls, objective multi-stage scoring, and anti-cheat
verification in a clean verifier container.

## Task levels

| Level | Given | Goal | Count |
|---|---|---|---|
| `L1_verdict` | Full `.spthy` theory with all **lemmas removed** + NL description of the security goals + lemma names | Formulate the lemmas, drive Tamarin to termination, deliver a SAFE/UNSAFE verdict; extract the attack trace if UNSAFE | 55 |
| `L2_form` | Natural-language protocol specification **only** | Build the full model from scratch, verify, and find the attack (all ground truths are attack-bearing protocols) | 10 |
| `L3_repair` | A **broken** theory (syntax/wellformedness errors, or a subtly wrong model that masks a real attack) | Repair the theory, verify, and discover the underlying attack | 10 |

## Architecture

```
┌────────────┐   egress firewall (squid allowlist)   ┌──────────────┐
│  agent     │◄────────────────────────────────────► │  LLM proxy   │
│  container │                                       │ (LiteLLM,    │
│  (tamarin +│                                       │  budgets, no │
│   CLI)     │                                       │  web search) │
└────────────┘                                       └──────────────┘
       │ outputs (/workspace/final.spthy, verdict.json, attack_report.md)
       ▼
┌────────────────┐    tamarin --prove --output-json    ┌──────────────┐
│  evaluator     │───────────────────────────────────► │  verifier    │
│  (runner)      │◄──────────────────────────────────── │  container   │
└────────────────┘        per-lemma verdicts + traces   └──────────────┘
       │
       ▼ compare vs ground_truth.json + structural anti-cheat
   result.json (CheckResult list, resumable batch runs)
```

- **Scoring is objective and staged**: parse → wellformedness → structural
  anti-cheat (given rules must be unchanged, lemma coverage + fact-reference
  checks) → per-lemma verdict match vs ground truth → clean-container
  reproduction → attack report ↔ trace event match.
- **Anti-cheat**: verification never trusts anything inside the agent
  container; the final theory is re-run with a pinned Tamarin in a fresh
  verifier container. Network egress is allowlisted (no fetching published
  proofs); WebSearch/WebFetch are disabled at the CLI level.

## Quick start

```bash
uv sync --extra proxy                       # python 3.12+; core + litellm proxy
uv run prisma generate --schema "$(uv run python -c \
  "import litellm, pathlib; print(pathlib.Path(litellm.__file__).parent/'proxy'/'schema.prisma')")"
bash scripts/setup/build_images.sh          # agent + verifier images (pinned tamarin 1.12.0)
bash scripts/setup/setup_runtime.sh         # static node + claude-code CLI -> data/runtime/
python scripts/convert_cfb.py               # CrypFormBench JSON -> data/tasks/ (75 tasks)
python scripts/validate_tasks.py            # ground-truth re-validation in docker (slow)
python scripts/setup/pre_run.py             # readiness check (+ services, prints secrets)

# pipeline smoke test — no LLM needed, must score 1.0:
python examples/run_agent.py --tasks-file data/task_ids/sample.txt \
    --out-dir out/mock --agent mock_perfect

# real run (Claude Code via a native Anthropic endpoint):
export ANTHROPIC_AUTH_TOKEN=...
python examples/run_agent.py --tasks-file data/task_ids/v0.txt \
    --out-dir out/run1 --agent claude_code --claude-model glm-5.3 \
    --api-base-url https://api.z.ai/api/anthropic --timeout 3600 --max-workers 4

python scripts/aggregate_results.py out/run1 # summary + per-check breakdown
```

See `docs/` (setup.md, eval.md, tasks.md) for details. Layout follows
ExploitGym conventions (`run_as.sh` multi-tenant orchestration, per-task
`result.json` resume, `out/<user>/run_agent/...` outputs).

## Repository layout

```
data/tasks/           per-task dirs: theory/solution/task.json/ground_truth.json
data/task_ids/        canonical task lists (v0.txt, sample.txt)
data/runtime/         portable tools mounted into agent containers (node+CLIs)
docker/               agent.Dockerfile, verifier.Dockerfile, pinned binaries
examples/run_agent.py main batch runner
scripts/              conversion, validation, setup, analysis
src/tamaringym/       the python package (task/evaluation/server/firewall/llm_proxy)
tests/                pytest suite
```

## Licenses

Code: Apache-2.0. Task data derived from CrypFormBench retains its upstream
license/terms (see DATA_LICENSE.md).
