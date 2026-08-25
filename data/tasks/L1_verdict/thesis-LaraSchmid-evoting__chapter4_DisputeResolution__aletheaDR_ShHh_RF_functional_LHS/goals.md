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
| 1 | `onlyonce1` | all-traces | onlyonce1 |
| 2 | `onlyonce1` | all-traces | onlyonce1 |
| 3 | `onlyonce2` | all-traces | onlyonce2 |
| 4 | `onlyonce2` | all-traces | onlyonce2 |
| 5 | `onlyonce3` | all-traces | onlyonce3 |
| 6 | `onlyonce3` | all-traces | onlyonce3 |
| 7 | `onlyonce4` | all-traces | onlyonce4 |
| 8 | `onlyonce4` | all-traces | onlyonce4 |
| 9 | `onlyonce5` | all-traces | onlyonce5 |
| 10 | `onlyonce5` | all-traces | onlyonce5 |
| 11 | `onlyonce6` | all-traces | onlyonce6 |
| 12 | `onlyonce6` | all-traces | onlyonce6 |
| 13 | `functional` | exists-trace | functional |
| 14 | `functional` | exists-trace | functional |
| 15 | `indivVerif_v` | all-traces | indivverif v |
| 16 | `indivVerif_v` | all-traces | indivverif v |
| 17 | `indivVerif_b` | all-traces | indivverif b |
| 18 | `indivVerif_b` | all-traces | indivverif b |
| 19 | `DRvoterC` | all-traces | drvoterc |
| 20 | `DRvoterC` | all-traces | drvoterc |
| 21 | `DRvoterT` | all-traces | drvotert |
| 22 | `DRvoterT` | all-traces | drvotert |
| 23 | `DRauth` | all-traces | drauth |
| 24 | `DRauth` | all-traces | drauth |
| 25 | `Uniqueness` | all-traces | uniqueness |
| 26 | `Uniqueness` | all-traces | uniqueness |
| 27 | `Observational_equivalence` | diff | observational equivalence |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
