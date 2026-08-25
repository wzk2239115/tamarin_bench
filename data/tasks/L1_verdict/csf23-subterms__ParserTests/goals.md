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
| 1 | `SnatChain` | all-traces | snatchain |
| 2 | `SnegRecurse` | all-traces | snegrecurse |
| 3 | `SnegACRecurse` | all-traces | snegacrecurse |
| 4 | `Sneg` | all-traces | sneg |
| 5 | `Sinvalid` | all-traces | sinvalid |
| 6 | `Schain` | all-traces | schain |
| 7 | `SRecurse` | all-traces | srecurse |
| 8 | `SACRecurse` | all-traces | sacrecurse |
| 9 | `testEqual` | all-traces | testequal |
| 10 | `arityOneDeduction` | all-traces | arityonededuction |
| 11 | `antiCharlie` | all-traces | anticharlie |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
