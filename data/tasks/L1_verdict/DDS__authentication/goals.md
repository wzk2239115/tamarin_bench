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
| 1 | `key_exchange_without_compromise` | exists-trace | key exchange without compromise |
| 2 | `aliveness_AB` | all-traces | aliveness ab |
| 3 | `weak_agreement_AB` | all-traces | weak agreement ab |
| 4 | `noninjective_agreement_AB` | all-traces | noninjective agreement ab |
| 5 | `injective_agreement_AB` | all-traces | injective agreement ab |
| 6 | `aliveness_BA` | all-traces | aliveness ba |
| 7 | `weak_agreement_BA` | all-traces | weak agreement ba |
| 8 | `noninjective_agreement_BA` | all-traces | noninjective agreement ba |
| 9 | `injective_agreement_BA` | all-traces | injective agreement ba |
| 10 | `secrecy` | all-traces | secrecy |
| 11 | `pfs_of_shared_secret` | all-traces | pfs of shared secret |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
