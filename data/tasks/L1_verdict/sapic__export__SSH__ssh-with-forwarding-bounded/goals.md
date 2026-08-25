# Verification goals

You are given the protocol theory in `theory.spthy`. The theory is complete
**except for its security lemmas**, which have been removed. Your job is to:

1. Formulate a security lemma for **each** goal listed below, using the given
   lemma names (Tamarin will match them when grading).
2. Run the Tamarin prover and drive the analysis to completion: every lemma
   must terminate with `verified` or `falsified - found trace`.
3. Produce the deliverables described in the task README
   (`final.spthy`, `verdict.json`, `attack_report.md` if unsafe).

Notes:

- Lemma statements are yours to write; the quantifier column is binding.
- Helper/source lemmas beyond the listed goals are allowed (and often
  needed to make the prover terminate).
- Some theories use `diff()` terms (observational equivalence):
  analyzing them requires `tamarin-prover --diff`.

## Goals to formalize

| # | Lemma name | Quantifier | Property |
|---|------------|------------|----------|
| 1 | `secretShares` | all-traces | secretshares |
| 2 | `injPS` | all-traces | injps |
| 3 | `injSP` | all-traces | injsp |
| 4 | `secretS` | all-traces | secrets |

## Protocol description (natural language)

* Protocol: SSH, with generic agent forwarding, but the agent refuses to sign over some depth.

   Proverif : everything in a few minutes, depending on the depth of nesting.
     Depth 1 - 7 secs
     Depth 2 - 20 secs
     Depth 3 - 1 minute
     Depth 4 - 2 minutes 24
     Depth 5 - 6 minutes 10
   Tamarin : Not working, over  a thousand partial deconstruction.
