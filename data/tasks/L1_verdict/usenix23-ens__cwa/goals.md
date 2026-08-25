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
| 1 | `secret_guid` | all-traces | secret guid |
| 2 | `secret_regToken` | all-traces | secret regtoken |
| 3 | `secret_tan` | all-traces | secret tan |
| 4 | `secret_key` | all-traces | secret key |
| 5 | `upload_auth` | all-traces | upload auth |
| 6 | `soundness` | all-traces | soundness |

## Protocol description (natural language)

* Protocol:   German Corona-Warn App (CWA)
 * Modeler:    Robert Künnemann, Kevin Morio, and Dennis Jackson
 * Date:       April 2021
 * Status:     working
 *
 * Sources:    https://github.com/DP-3T/documents
 *             https://github.com/corona-warn-app/cwa-documentation/blob/e4203a628a4b5c225c7d2b9fa386b0d88ee0373c/solution_architecture.md
 *             https://blog.google/documents/69/Exposure_Notification_-_Cryptography_Specification_v1.2.1.pdf
 *
 * Invocation: tamarin-prover --prove cwa.spthy
