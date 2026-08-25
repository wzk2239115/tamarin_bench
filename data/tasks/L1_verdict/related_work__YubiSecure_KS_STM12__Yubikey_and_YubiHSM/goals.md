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
| 1 | `adv_can_guess_counter` | all-traces | adv can guess counter |
| 2 | `otp_decode_does_not_help_adv_use_induction` | all-traces | otp decode does not help adv use induction |
| 3 | `neither_k_nor_k2_are_ever_leaked_inv` | all-traces | neither k nor k2 are ever leaked inv |
| 4 | `one_count_foreach_login` | all-traces | one count foreach login |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
