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
| 1 | `Smart_adversary` | all-traces | smart adversary |
| 2 | `ledger` | exists-trace | ledger |
| 3 | `Coin2Hcoin` | exists-trace | coin2hcoin |
| 4 | `Hcoin2coinBC1` | exists-trace | hcoin2coinbc1 |
| 5 | `Hcoin2coinBC2` | exists-trace | hcoin2coinbc2 |
| 6 | `Alice` | exists-trace | alice |
| 7 | `Alice11` | exists-trace | alice11 |
| 8 | `Alice_3` | exists-trace | alice 3 |
| 9 | `Bob_3_receive` | exists-trace | bob 3 receive |
| 10 | `Bob_2_execu` | exists-trace | bob 2 execu |
| 11 | `Bob_2` | exists-trace | bob 2 |
| 12 | `Bob_1` | exists-trace | bob 1 |
| 13 | `BC2lamma` | exists-trace | bc2lamma |
| 14 | `Alice_no_early_redeem` | all-traces | alice no early redeem |
| 15 | `Test_malicious` | exists-trace | test malicious |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
