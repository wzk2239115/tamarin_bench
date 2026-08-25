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
| 1 | `upload_auth` | all-traces | upload auth |
| 2 | `soundness` | all-traces | soundness |

## Protocol description (natural language)

* Protocol:    DP3T (Decentralized Privacy-Preserving Proximity Tracing) design 3
 * Modeler:     Robert Künnemann, Kevin Morio and Dennis Jackson
 * Date:        April 2021
 * Status:      working
 *
 * Source:      https://github.com/DP-3T/documents
 *
 * Invocation:  tamarin-prover --prove dp3t.spthy
