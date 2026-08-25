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
| 4 | `missing_excl_0_1` | all-traces | missing excl 0 1 |
| 5 | `missing_excl_0_2` | all-traces | missing excl 0 2 |
| 6 | `missing_excl_0_3` | all-traces | missing excl 0 3 |
| 7 | `missing_excl_1_2` | all-traces | missing excl 1 2 |
| 8 | `missing_excl_1_3` | all-traces | missing excl 1 3 |
| 9 | `missing_excl_2_3` | all-traces | missing excl 2 3 |
| 10 | `missing_exh` | all-traces | missing exh |
| 11 | `missing_suf_0` | exists-trace | missing suf 0 |
| 12 | `missing_suf_1` | exists-trace | missing suf 1 |
| 13 | `missing_ver_empty_3` | all-traces | missing ver empty 3 |
| 14 | `missing_ver_nonempty_0` | all-traces | missing ver nonempty 0 |
| 15 | `missing_ver_nonempty_1` | all-traces | missing ver nonempty 1 |
| 16 | `missing_ver_nonempty_2` | all-traces | missing ver nonempty 2 |
| 17 | `missing_min_0_0` | all-traces | missing min 0 0 |
| 18 | `missing_min_1_0` | all-traces | missing min 1 0 |
| 19 | `missing_uniq_sing_0` | all-traces | missing uniq sing 0 |
| 20 | `missing_uniq_sing_1` | all-traces | missing uniq sing 1 |

## Protocol description (natural language)

* Protocol: DMN + message tracing (fixed identities)
 * Modeler:  Kevin Morio and Robert Künnemann
 * Date:     Sep 2020
 * Source:   "SoK: Techniques for Verifiable Mix Nets", Thomas Haines and Johannes Müller, CSF20
 * Status:   working (deprecated)
 * Notes:    Run with: tamarin-prover +RTS -N4 -RTS --stop-on-trace=seqdfs --prove --heuristic=o \
 *                     --oraclename=oracle-dmn-message-tracing dmn-message-tracing-all-2-fixed.spthy
 *
 * In this version, the audit continues after detecting the first unexpected message on the bulletin board.
