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
| 7 | `missing_excl_0_4` | all-traces | missing excl 0 4 |
| 8 | `missing_excl_0_5` | all-traces | missing excl 0 5 |
| 9 | `missing_excl_0_6` | all-traces | missing excl 0 6 |
| 10 | `missing_excl_0_7` | all-traces | missing excl 0 7 |
| 11 | `missing_excl_1_2` | all-traces | missing excl 1 2 |
| 12 | `missing_excl_1_3` | all-traces | missing excl 1 3 |
| 13 | `missing_excl_1_4` | all-traces | missing excl 1 4 |
| 14 | `missing_excl_1_5` | all-traces | missing excl 1 5 |
| 15 | `missing_excl_1_6` | all-traces | missing excl 1 6 |
| 16 | `missing_excl_1_7` | all-traces | missing excl 1 7 |
| 17 | `missing_excl_2_3` | all-traces | missing excl 2 3 |
| 18 | `missing_excl_2_4` | all-traces | missing excl 2 4 |
| 19 | `missing_excl_2_5` | all-traces | missing excl 2 5 |
| 20 | `missing_excl_2_6` | all-traces | missing excl 2 6 |
| 21 | `missing_excl_2_7` | all-traces | missing excl 2 7 |
| 22 | `missing_excl_3_4` | all-traces | missing excl 3 4 |
| 23 | `missing_excl_3_5` | all-traces | missing excl 3 5 |
| 24 | `missing_excl_3_6` | all-traces | missing excl 3 6 |
| 25 | `missing_excl_3_7` | all-traces | missing excl 3 7 |
| 26 | `missing_excl_4_5` | all-traces | missing excl 4 5 |
| 27 | `missing_excl_4_6` | all-traces | missing excl 4 6 |
| 28 | `missing_excl_4_7` | all-traces | missing excl 4 7 |
| 29 | `missing_excl_5_6` | all-traces | missing excl 5 6 |
| 30 | `missing_excl_5_7` | all-traces | missing excl 5 7 |
| 31 | `missing_excl_6_7` | all-traces | missing excl 6 7 |
| 32 | `missing_exh` | all-traces | missing exh |
| 33 | `missing_suf_0` | exists-trace | missing suf 0 |
| 34 | `missing_suf_1` | exists-trace | missing suf 1 |
| 35 | `missing_suf_2` | exists-trace | missing suf 2 |
| 36 | `missing_ver_empty_7` | all-traces | missing ver empty 7 |
| 37 | `missing_ver_nonempty_0` | all-traces | missing ver nonempty 0 |
| 38 | `missing_ver_nonempty_1` | all-traces | missing ver nonempty 1 |
| 39 | `missing_ver_nonempty_2` | all-traces | missing ver nonempty 2 |
| 40 | `missing_ver_nonempty_3` | all-traces | missing ver nonempty 3 |
| 41 | `missing_ver_nonempty_4` | all-traces | missing ver nonempty 4 |
| 42 | `missing_ver_nonempty_5` | all-traces | missing ver nonempty 5 |
| 43 | `missing_ver_nonempty_6` | all-traces | missing ver nonempty 6 |
| 44 | `missing_min_0_0` | all-traces | missing min 0 0 |
| 45 | `missing_min_1_0` | all-traces | missing min 1 0 |
| 46 | `missing_min_2_0` | all-traces | missing min 2 0 |
| 47 | `missing_uniq_sing_0` | all-traces | missing uniq sing 0 |
| 48 | `missing_uniq_sing_1` | all-traces | missing uniq sing 1 |
| 49 | `missing_uniq_sing_2` | all-traces | missing uniq sing 2 |

## Protocol description (natural language)

* Protocol: DMN + message tracing (fixed identities)
 * Modeler:  Kevin Morio and Robert Künnemann
 * Date:     Sep 2020
 * Source:   "SoK: Techniques for Verifiable Mix Nets", Thomas Haines and Johannes Müller, CSF20
 * Status:   working (deprecated)
 * Notes:    Run with: tamarin-prover +RTS -N4 -RTS --stop-on-trace=seqdfs --prove --heuristic=o \
 *                     --oraclename=oracle-dmn-message-tracing dmn-message-tracing-all-3-fixed.spthy
 *
 * In this version, the audit continues after detecting the first unexpected message on the bulletin board.
