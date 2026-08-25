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
| 15 | `indivVerif` | all-traces | indivverif |
| 16 | `indivVerif` | all-traces | indivverif |
| 17 | `VoterC` | all-traces | voterc |
| 18 | `VoterC` | all-traces | voterc |
| 19 | `TimelyP` | all-traces | timelyp |
| 20 | `TimelyP` | all-traces | timelyp |
| 21 | `AuthP` | all-traces | authp |
| 22 | `AuthP` | all-traces | authp |
| 23 | `Uniqueness` | all-traces | uniqueness |
| 24 | `Uniqueness` | all-traces | uniqueness |
| 25 | `Observational_equivalence[heuristic={Observational_equivalence}]` | diff | observational equivalence[heuristic={observational equivalence}] |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
