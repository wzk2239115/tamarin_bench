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
| 1 | `count_unique` | all-traces | count unique |
| 2 | `nonces_unique` | all-traces | nonces unique |
| 3 | `force_nonce_ordering` | all-traces | force nonce ordering |
| 4 | `exists_session` | exists-trace | exists session |
| 5 | `exists_second_session` | exists-trace | exists second session |
| 6 | `exists_detect_no_C_compromise` | exists-trace | exists detect no c compromise |
| 7 | `exists_detect_no_I_compromise` | exists-trace | exists detect no i compromise |
| 8 | `injectivity` | all-traces | injectivity |
| 9 | `detect_sound` | all-traces | detect sound |
| 10 | `correct_dolevyao` | all-traces | correct dolevyao |
| 11 | `unmatching_implies_detect_with_W_uncompromised` | all-traces | unmatching implies detect with w uncompromised |

## Protocol description (natural language)

* Protocol:    Modified Keyless SSL protocol for Client Detection
 * Modeler: 	Kevin Milner
 * Source:	    Original
