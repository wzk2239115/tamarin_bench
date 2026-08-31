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
| 1 | `Smart_adversary_simpleTx` | all-traces | smart adversary simpletx |
| 2 | `Smart_adversary_CommitCoin` | all-traces | smart adversary commitcoin |
| 3 | `originalCoin` | all-traces | originalcoin |
| 4 | `commitLedgerTick` | all-traces | commitledgertick |
| 5 | `commitOpenTick` | all-traces | commitopentick |
| 6 | `commitToutTick` | all-traces | committouttick |
| 7 | `uniqueTick` | all-traces | uniquetick |
| 8 | `CommitTout_blockchain1_executable` | exists-trace | committout blockchain1 executable |
| 9 | `CommitTout_blockchain2_executable` | exists-trace | committout blockchain2 executable |
| 10 | `CommitOpen_blockchain1_executable` | exists-trace | commitopen blockchain1 executable |
| 11 | `CommitOpen_blockchain2_executable` | exists-trace | commitopen blockchain2 executable |
| 12 | `Alice11` | exists-trace | alice11 |
| 13 | `Alice_3` | exists-trace | alice 3 |
| 14 | `Bob_receive` | exists-trace | bob receive |
| 15 | `Security_1_Alice` | all-traces | security 1 alice |
| 16 | `Security_2_Alice` | all-traces | security 2 alice |
| 17 | `Security_3_Bob` | all-traces | security 3 bob |
| 18 | `Security_4_Bob` | all-traces | security 4 bob |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
