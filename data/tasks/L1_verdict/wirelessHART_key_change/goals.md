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
| 1 | `key_received_UC` | exists-trace | key received uc |
| 2 | `key_authentication_UC` | all-traces | key authentication uc |
| 3 | `key_secrecy_UC` | all-traces | key secrecy uc |
| 4 | `key_received_BC` | exists-trace | key received bc |
| 5 | `key_authentication_BC` | all-traces | key authentication bc |
| 6 | `key_secrecy_BC` | all-traces | key secrecy bc |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
