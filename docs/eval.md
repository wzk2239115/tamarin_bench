# Running evaluations

## Single task / debugging

```bash
# interactive bash inside a prepared task container (workspace at /workspace)
python scripts/interactive.py --task L1:NSPK3
```

Inside the container the agent CLI is at `/data/node/bin/claude-code.sh`
(run it with `--permission-mode=bypassPermissions
--disallowed-tools WebSearch,WebFetch`).

## Batch

```bash
# smoke (no LLM needed — reference-solution agent, must score 1.0)
python examples/run_agent.py --tasks-file data/task_ids/sample.txt \
    --out-dir out/mock --agent mock_perfect --max-workers 2

# real run (Claude Code against a native Anthropic endpoint)
export ANTHROPIC_AUTH_TOKEN=...          # or --api-key
python examples/run_agent.py --tasks-file data/task_ids/v0.txt \
    --out-dir out/run1 --agent claude_code --claude-model glm-5.3 \
    --api-base-url https://api.z.ai/api/anthropic \
    --timeout 3600 --max-workers 4
```

Runner features (mirrors ExploitGym):

- **Resume**: a task directory with an existing `result.json` is skipped;
  re-run the same command to continue after an interruption.
- Process pool with startup staggering, SIGINT/SIGTERM graceful shutdown.
- Per-task outputs: `result.json`, `config.json`, `outputs/` (final.spthy,
  verdict.json, attack_report.md, rerun_summary.json), `workspace/`
  snapshot (size-capped), `logs/claude_code.log` (stream-json).

## Multi-tenant slots

```bash
TASKS_FILE=data/task_ids/v0.txt MAX_WORKERS=6 TIMEOUT=3600 \
GLM_PROVIDER=anthropic GLM_MODEL=deepseek/deepseek-v4-pro \
bash run_as.sh myslot          # start/resume
bash run_as.sh --status myslot
bash run_as.sh --stop myslot   # layered teardown: runner -> containers -> proxy
```

`DIRECT=1 bash run_as.sh <name>` bypasses the proxy (uses
`ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL` from the environment).
`INTERACTIVE=1` drops you into the first task's container instead.

## Scoring

Each task produces a `result.json` with weighted checks:

| check | weight | meaning |
|---|---|---|
| outputs_present | .05 | final.spthy + verdict.json delivered |
| parses | .10 | Tamarin accepts the theory (clean re-run) |
| wellformed | .05 | matches the reference wellformedness state |
| given_rules_unchanged | .15 | given rules/restrictions intact (L2: rule-name coverage) |
| lemma_coverage | .10 | every goal stated, right name + quantifier |
| lemma_fact_references | .10 | lemmas reference the reference protocol facts |
| no_trivial_lemmas | .05 | no `P ==> P` style bodies |
| verdict_match | .25 | per-lemma verdicts equal ground truth |
| attack_trace_match | .10 | falsified-lemma traces match (multiset Jaccard) |
| attack_report_match | .05 | report cites the reference trace rules |

The verdict/trace checks **never trust the agent's claims**: the agent's
`final.spthy` is re-run with the pinned Tamarin in a fresh verifier
container and compared against `ground_truth.json` (which lives outside
the workspace). Attack-trace matching compares the protocol-rule event
multisets of the re-run traces vs the ground-truth traces.

Aggregate with:

```bash
python scripts/aggregate_results.py out/run1   # summary + per-check breakdown
```
