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
| 8 | `secretSskD` | all-traces | secretsskd |
| 9 | `ballotsFromVoters` | all-traces | ballotsfromvoters |
| 10 | `Tall_As_Rec_D_1` | all-traces | tall as rec d 1 |
| 11 | `Tall_As_Rec_D_2` | all-traces | tall as rec d 2 |
| 12 | `Tall_As_Rec_D_3` | all-traces | tall as rec d 3 |
| 13 | `Tall_As_Rec_D_4` | all-traces | tall as rec d 4 |
| 14 | `Tall_As_Rec_D_5` | all-traces | tall as rec d 5 |
| 15 | `Tall_As_Rec_D_6` | all-traces | tall as rec d 6 |
| 16 | `Tall_As_Rec_D_7` | all-traces | tall as rec d 7 |
| 17 | `Tall_As_Rec_D_8` | all-traces | tall as rec d 8 |
| 18 | `EligVerif_1` | all-traces | eligverif 1 |
| 19 | `EligVerif_2` | all-traces | eligverif 2 |
| 20 | `EligVerif_3` | all-traces | eligverif 3 |
| 21 | `EligVerif_4` | all-traces | eligverif 4 |
| 22 | `EligVerif_5` | all-traces | eligverif 5 |
| 23 | `EligVerif_6` | all-traces | eligverif 6 |
| 24 | `EligVerif_7` | all-traces | eligverif 7 |
| 25 | `EligVerif_8` | all-traces | eligverif 8 |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
