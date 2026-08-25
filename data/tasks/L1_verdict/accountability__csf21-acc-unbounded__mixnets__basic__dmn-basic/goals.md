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
| 1 | `sanity_submit` | exists-trace | sanity submit |
| 2 | `sanity_mix` | exists-trace | sanity mix |
| 3 | `sanity_receive` | exists-trace | sanity receive |
| 4 | `correctness` | all-traces | correctness |
| 5 | `duplicates` | all-traces | duplicates |

## Protocol description (natural language)

* Protocol: Basic DMN
 * Modeler:  Kevin Morio and Robert Künnemann
 * Date:     Sep 2020
 * Source:   "SoK: Techniques for Verifiable Mix Nets", Thomas Haines and Johannes Müller, CSF20
 * Status:   working
 * Notes:    Run with: tamarin-prover +RTS -N4 -RTS --prove --heuristic=o --oraclename=oracle-dmn-basic dmn-basic.spthy
