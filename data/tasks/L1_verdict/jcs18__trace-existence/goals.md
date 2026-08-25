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
| 1 | `countervalue_uniqueness` | all-traces | countervalue uniqueness |
| 2 | `CSQ_Uniqueness` | all-traces | csq uniqueness |
| 3 | `exists_trace` | exists-trace | exists trace |
| 4 | `sessions_unique` | all-traces | sessions unique |
| 5 | `update_key_sourced` | all-traces | update key sourced |
| 6 | `update_key_agreement` | all-traces | update key agreement |
| 7 | `update_key_secrecy` | all-traces | update key secrecy |
| 8 | `session_key_secrecy` | all-traces | session key secrecy |
| 9 | `sessionkeys_sourced` | all-traces | sessionkeys sourced |
| 10 | `skiup_agreement` | all-traces | skiup agreement |
| 11 | `asdu_agreement_implies_mode_agreement` | all-traces | asdu agreement implies mode agreement |
| 12 | `asdu_aliveness` | all-traces | asdu aliveness |
| 13 | `asdu_injective_agreement` | all-traces | asdu injective agreement |

## Protocol description (natural language)

This file contains the manual proof for the exists-trace lemma.
 This is not included in the main dnp3.m4/dnp3.spthy file as the proof
 is rather long and unwieldy to include, and isn't found quickly by
 Tamarin's autoproving functionality.
