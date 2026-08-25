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
| 2 | `onlyonce2` | all-traces | onlyonce2 |
| 3 | `onlyonce3` | all-traces | onlyonce3 |
| 4 | `onlyonce4` | all-traces | onlyonce4 |
| 5 | `onlyonce5` | all-traces | onlyonce5 |
| 6 | `onlyonce6` | all-traces | onlyonce6 |
| 7 | `onlyonce7` | all-traces | onlyonce7 |
| 8 | `onlyonce8` | all-traces | onlyonce8 |
| 9 | `onlyonce9` | all-traces | onlyonce9 |
| 10 | `onlyonce10` | all-traces | onlyonce10 |
| 11 | `functional` | exists-trace | functional |
| 12 | `indivVerif_v` | all-traces | indivverif v |
| 13 | `indivVerif_b` | all-traces | indivverif b |
| 14 | `DRvoterC` | all-traces | drvoterc |
| 15 | `DRvoterT` | all-traces | drvotert |
| 16 | `Uniqueness` | all-traces | uniqueness |
| 17 | `secretSskD` | all-traces | secretsskd |
| 18 | `ballotsFromVoters` | all-traces | ballotsfromvoters |
| 19 | `Tall_As_Rec_D` | all-traces | tall as rec d |
| 20 | `EligVerif_DR` | all-traces | eligverif dr |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
