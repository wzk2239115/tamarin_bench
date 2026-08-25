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
| 1 | `functional` | exists-trace | functional |
| 2 | `indivVerif` | all-traces | indivverif |
| 3 | `Universal_VerProofV_v1` | all-traces | universal verproofv v1 |
| 4 | `Universal_VerProofV_v2` | all-traces | universal verproofv v2 |
| 5 | `Universal_VerProofV_v3` | all-traces | universal verproofv v3 |
| 6 | `Universal_VerProofV_v4` | all-traces | universal verproofv v4 |
| 7 | `Universal_VerProofV_v5` | all-traces | universal verproofv v5 |
| 8 | `Universal_VerProofV_v6` | all-traces | universal verproofv v6 |
| 9 | `Universal_VerProofV_v7` | all-traces | universal verproofv v7 |
| 10 | `Universal_VerProofV_v8` | all-traces | universal verproofv v8 |
| 11 | `Universal_VerProofY_v1` | all-traces | universal verproofy v1 |
| 12 | `Universal_VerProofY_v2` | all-traces | universal verproofy v2 |
| 13 | `Universal_VerProofY_v3` | all-traces | universal verproofy v3 |
| 14 | `Universal_VerProofY_v4` | all-traces | universal verproofy v4 |
| 15 | `Universal_VerProofY_v5` | all-traces | universal verproofy v5 |
| 16 | `Universal_VerProofY_v6` | all-traces | universal verproofy v6 |
| 17 | `Universal_VerProofY_v7` | all-traces | universal verproofy v7 |
| 18 | `Universal_VerProofY_v8` | all-traces | universal verproofy v8 |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
