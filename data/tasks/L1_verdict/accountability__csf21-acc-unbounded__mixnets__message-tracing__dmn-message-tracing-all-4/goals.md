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
| 1 | `finished` | exists-trace | finished |
| 2 | `valid` | exists-trace | valid |
| 3 | `blame` | exists-trace | blame |
| 4 | `missing` | all-traces | missing |

## Protocol description (natural language)

* Protocol: DMN + message tracing
 * Modeler:  Kevin Morio and Robert Künnemann
 * Date:     Sep 2020
 * Source:   "SoK: Techniques for Verifiable Mix Nets", Thomas Haines and Johannes Müller, CSF20
 * Status:   working
 * Notes:    Run with: tamarin-prover +RTS -N4 -RTS --stop-on-trace=seqdfs --prove --heuristic=o \
 *                     --oraclename=oracle-dmn-message-tracing dmn-message-tracing-all-4.spthy
 *
 * In this version, the audit continues after detecting the first unexpected message on the bulletin board.
