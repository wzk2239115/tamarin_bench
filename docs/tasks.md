# Task design

Three levels, all derived from the CrypFormBench spthy corpus (58 distinct
protocol theories; 5 with no provable goals were excluded, leaving 55).

## L1_verdict — property formulation & verdict (55 tasks)

**Given**: the complete theory with all security lemmas stripped
(`theory.spthy`) + `goals.md` (lemma names, quantifiers, NL description).

**Do**: formulate each goal as a Tamarin lemma (name and quantifier are
binding; helper/source lemmas allowed), drive `--prove` to termination,
deliver `final.spthy` + `verdict.json` (+ `attack_report.md` when UNSAFE).

**Why**: tests the core agentic skill — knowing *what* to verify and
driving an interactive prover — without free-form modeling noise. The agent
does not know whether the protocol is safe; 46 of the 55 are SAFE, 9 hide
attacks.

## L2_form — modeling from a natural-language spec (10 tasks)

**Given**: `spec.md` only (CrypFormBench's NL protocol descriptions).

**Do**: build the full theory from scratch, verify, discover the attack.

**Selection**: the 10 attack-bearing protocols of the corpus (NSPK3,
CCITT-X509-R, dh_alternative, ...) — every ground truth is UNSAFE, so the
level measures attack discovery through honest modeling.

## L3_repair — theory repair & attack discovery (10 tasks)

**Given**: `broken.spthy` (CrypFormBench's `errorcode` variants: syntax /
wellformedness / modeling errors) + `error_hint.txt`.

**Do**: repair the theory, verify, and determine the verdict.

**Selection**: NSPK3 and RYY_PFS use the *falsely-passing* variants
(the broken model masks a real attack — the agent must both repair and
discover); the rest are error variants with mixed verdicts.

## Ground truth

`solution/ground_truth.json` per task, produced by
`scripts/validate_tasks.py` (real Tamarin 1.12.0 runs in the verifier
image): overall verdict, per-lemma verdicts + proof steps, and per falsified
lemma the **protocol-rule event sequences** of every attack trace
(`--output-json`). Ground truth never enters the agent workspace.

Special cases handled:

- diff-term theories (`probEnc`, `issue193`, ...) run with `--diff`; their
  goal is the default observational-equivalence check.
- Theories whose lemmas live inside (nested!) block comments or `#ifdef`
  regions have no provable goals — excluded at conversion time.
- `falsified - no trace found` (negated exists-trace) counts as falsified.

## Anti-cheat

The objective checks are the primary defense (structure + clean-container
re-run). The prompt-level ground rules forbid altering given rules and
weakening goals; `check_given_rules_unchanged` (normalized SHA-256 per
block), `check_lemma_coverage`, `check_lemma_fact_references` and
`check_no_trivial_lemmas` enforce them mechanically. Network egress is
allowlisted to LLM endpoints only (no fetching published proofs), and
WebSearch/WebFetch are disabled in the CLI.

## Difficulty axes (future)

- Information provided: with/without `goals.md` lemma names, with/without
  the NL spec (L1 → L2 continuum).
- Tooling: allow/disallow `--auto-sources`, oracles.
- Budget: per-task timeout (Tamarin non-termination is a real constraint).
