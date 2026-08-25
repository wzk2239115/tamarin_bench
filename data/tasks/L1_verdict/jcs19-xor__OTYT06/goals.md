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
- An `oracle` proof-heuristic file is provided; keep it in the working directory when running tamarin (it guides proof search).
Some theories use `diff()` terms (observational equivalence):
  analyzing them requires `tamarin-prover --diff`.

## Goals to formalize

| # | Lemma name | Quantifier | Property |
|---|------------|------------|----------|
| 1 | `helping_reader_start` | all-traces | helping reader start |
| 2 | `helping_tag_start` | all-traces | helping tag start |
| 3 | `helping_keys_reader_are_secret` | all-traces | helping keys reader are secret |
| 4 | `helping_keys_disjoint_challenge` | all-traces | helping keys disjoint challenge |
| 5 | `helping_keys_disjoint_XX` | all-traces | helping keys disjoint xx |
| 6 | `helping_keys_disjoint_XS` | all-traces | helping keys disjoint xs |
| 7 | `helping_keys_disjoint_DD` | all-traces | helping keys disjoint dd |
| 8 | `helping_keys_disjoint_OutX` | all-traces | helping keys disjoint outx |
| 9 | `alive_tag` | all-traces | alive tag |
| 10 | `recentalive_tag_bounded` | all-traces | recentalive tag bounded |
| 11 | `WA_tag` | all-traces | wa tag |
| 12 | `alive_reader` | all-traces | alive reader |
| 13 | `desynch_impossible` | all-traces | desynch impossible |
| 14 | `executable` | exists-trace | executable |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
