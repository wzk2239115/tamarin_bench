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
| 1 | `functional_correctness` | exists-trace | functional correctness |
| 2 | `functional_correctness_dishonest_send` | exists-trace | functional correctness dishonest send |
| 3 | `functional_correctness_group_verification` | exists-trace | functional correctness group verification |
| 4 | `aliveness` | all-traces | aliveness |
| 5 | `weak_agreement_any_reveal` | all-traces | weak agreement any reveal |
| 6 | `weak_agreement` | all-traces | weak agreement |
| 7 | `ni_agreement_any_reveal` | all-traces | ni agreement any reveal |
| 8 | `ni_agreement` | all-traces | ni agreement |
| 9 | `i_agreement` | all-traces | i agreement |
| 10 | `secrecy_cre` | all-traces | secrecy cre |
| 11 | `can_be_deanonymised` | exists-trace | can be deanonymised |
| 12 | `user_controlled_linkability` | all-traces | user controlled linkability |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
