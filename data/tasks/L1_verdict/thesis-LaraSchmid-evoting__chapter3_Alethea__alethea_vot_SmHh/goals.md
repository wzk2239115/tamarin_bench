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
| 2 | `indivVerif_v` | all-traces | indivverif v |
| 3 | `indivVerif_b` | all-traces | indivverif b |
| 4 | `vsFromBB` | all-traces | vsfrombb |
| 5 | `bsFromBB` | all-traces | bsfrombb |
| 6 | `vsFromAdversary` | all-traces | vsfromadversary |
| 7 | `secretRandomness` | all-traces | secretrandomness |
| 8 | `Tall_As_Rec_1` | all-traces | tall as rec 1 |
| 9 | `Tall_As_Rec_2` | all-traces | tall as rec 2 |
| 10 | `Tall_As_Rec_3` | all-traces | tall as rec 3 |
| 11 | `Tall_As_Rec_4` | all-traces | tall as rec 4 |
| 12 | `Tall_As_Rec_5` | all-traces | tall as rec 5 |
| 13 | `Tall_As_Rec_6` | all-traces | tall as rec 6 |
| 14 | `Tall_As_Rec_7` | all-traces | tall as rec 7 |
| 15 | `Tall_As_Rec_8` | all-traces | tall as rec 8 |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
