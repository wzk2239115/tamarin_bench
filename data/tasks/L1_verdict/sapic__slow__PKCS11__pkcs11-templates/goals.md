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
| 1 | `dec_limits` | all-traces | dec limits |
| 2 | `bad_keys` | all-traces | bad keys |
| 3 | `no_key_is_wrap_and_dec__or_unwrap_and_dec_ind` | all-traces | no key is wrap and dec or unwrap and dec ind |
| 4 | `no_key_is_enc_and_unwrap` | all-traces | no key is enc and unwrap |
| 5 | `cannot_obtain_key_ind` | all-traces | cannot obtain key ind |
| 6 | `cannot_obtain_key` | all-traces | cannot obtain key |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
