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
| 1 | `invariant_sources` | all-traces | invariant sources |
| 2 | `commit_unique` | all-traces | commit unique |
| 3 | `token_compromise_source` | all-traces | token compromise source |
| 4 | `force_nonce_ordering` | all-traces | force nonce ordering |
| 5 | `exists_session` | exists-trace | exists session |
| 6 | `exists_second_session` | exists-trace | exists second session |
| 7 | `exists_detect_no_I_compromise` | exists-trace | exists detect no i compromise |
| 8 | `detect_sound` | all-traces | detect sound |
| 9 | `correct_dolevyao` | all-traces | correct dolevyao |
| 10 | `matching_detects_prior_misuse` | all-traces | matching detects prior misuse |
| 11 | `sent_commit_implies_generated` | all-traces | sent commit implies generated |
| 12 | `sessions_injective` | all-traces | sessions injective |
| 13 | `matching_detects_later_misuse` | all-traces | matching detects later misuse |

## Protocol description (natural language)

Protocol:    Token commitment protocol applied to ISO-IEC-9798-3-3
   Modeler:     Kevin Milner
   Date:        July 2016
   Source:      Original
