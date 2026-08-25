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
| 11 | `missing_excl_0_8` | all-traces | missing excl 0 8 |
| 12 | `missing_excl_0_9` | all-traces | missing excl 0 9 |
| 13 | `missing_excl_0_10` | all-traces | missing excl 0 10 |
| 14 | `missing_excl_0_11` | all-traces | missing excl 0 11 |
| 15 | `missing_excl_0_12` | all-traces | missing excl 0 12 |
| 16 | `missing_excl_0_13` | all-traces | missing excl 0 13 |
| 17 | `missing_excl_0_14` | all-traces | missing excl 0 14 |
| 18 | `missing_excl_0_15` | all-traces | missing excl 0 15 |
| 19 | `missing_excl_1_2` | all-traces | missing excl 1 2 |
| 20 | `missing_excl_1_3` | all-traces | missing excl 1 3 |
| 21 | `missing_excl_1_4` | all-traces | missing excl 1 4 |
| 22 | `missing_excl_1_5` | all-traces | missing excl 1 5 |
| 23 | `missing_excl_1_6` | all-traces | missing excl 1 6 |
| 24 | `missing_excl_1_7` | all-traces | missing excl 1 7 |
| 25 | `missing_excl_1_8` | all-traces | missing excl 1 8 |
| 26 | `missing_excl_1_9` | all-traces | missing excl 1 9 |
| 27 | `missing_excl_1_10` | all-traces | missing excl 1 10 |
| 28 | `missing_excl_1_11` | all-traces | missing excl 1 11 |
| 29 | `missing_excl_1_12` | all-traces | missing excl 1 12 |
| 30 | `missing_excl_1_13` | all-traces | missing excl 1 13 |
| 31 | `missing_excl_1_14` | all-traces | missing excl 1 14 |
| 32 | `missing_excl_1_15` | all-traces | missing excl 1 15 |
| 33 | `missing_excl_2_3` | all-traces | missing excl 2 3 |
| 34 | `missing_excl_2_4` | all-traces | missing excl 2 4 |
| 35 | `missing_excl_2_5` | all-traces | missing excl 2 5 |
| 36 | `missing_excl_2_6` | all-traces | missing excl 2 6 |
| 37 | `missing_excl_2_7` | all-traces | missing excl 2 7 |
| 38 | `missing_excl_2_8` | all-traces | missing excl 2 8 |
| 39 | `missing_excl_2_9` | all-traces | missing excl 2 9 |
| 40 | `missing_excl_2_10` | all-traces | missing excl 2 10 |
| 41 | `missing_excl_2_11` | all-traces | missing excl 2 11 |
| 42 | `missing_excl_2_12` | all-traces | missing excl 2 12 |
| 43 | `missing_excl_2_13` | all-traces | missing excl 2 13 |
| 44 | `missing_excl_2_14` | all-traces | missing excl 2 14 |
| 45 | `missing_excl_2_15` | all-traces | missing excl 2 15 |
| 46 | `missing_excl_3_4` | all-traces | missing excl 3 4 |
| 47 | `missing_excl_3_5` | all-traces | missing excl 3 5 |
| 48 | `missing_excl_3_6` | all-traces | missing excl 3 6 |
| 49 | `missing_excl_3_7` | all-traces | missing excl 3 7 |
| 50 | `missing_excl_3_8` | all-traces | missing excl 3 8 |
| 51 | `missing_excl_3_9` | all-traces | missing excl 3 9 |
| 52 | `missing_excl_3_10` | all-traces | missing excl 3 10 |
| 53 | `missing_excl_3_11` | all-traces | missing excl 3 11 |
| 54 | `missing_excl_3_12` | all-traces | missing excl 3 12 |
| 55 | `missing_excl_3_13` | all-traces | missing excl 3 13 |
| 56 | `missing_excl_3_14` | all-traces | missing excl 3 14 |
| 57 | `missing_excl_3_15` | all-traces | missing excl 3 15 |
| 58 | `missing_excl_4_5` | all-traces | missing excl 4 5 |
| 59 | `missing_excl_4_6` | all-traces | missing excl 4 6 |
| 60 | `missing_excl_4_7` | all-traces | missing excl 4 7 |
| 61 | `missing_excl_4_8` | all-traces | missing excl 4 8 |
| 62 | `missing_excl_4_9` | all-traces | missing excl 4 9 |
| 63 | `missing_excl_4_10` | all-traces | missing excl 4 10 |
| 64 | `missing_excl_4_11` | all-traces | missing excl 4 11 |
| 65 | `missing_excl_4_12` | all-traces | missing excl 4 12 |
| 66 | `missing_excl_4_13` | all-traces | missing excl 4 13 |
| 67 | `missing_excl_4_14` | all-traces | missing excl 4 14 |
| 68 | `missing_excl_4_15` | all-traces | missing excl 4 15 |
| 69 | `missing_excl_5_6` | all-traces | missing excl 5 6 |
| 70 | `missing_excl_5_7` | all-traces | missing excl 5 7 |
| 71 | `missing_excl_5_8` | all-traces | missing excl 5 8 |
| 72 | `missing_excl_5_9` | all-traces | missing excl 5 9 |
| 73 | `missing_excl_5_10` | all-traces | missing excl 5 10 |
| 74 | `missing_excl_5_11` | all-traces | missing excl 5 11 |
| 75 | `missing_excl_5_12` | all-traces | missing excl 5 12 |
| 76 | `missing_excl_5_13` | all-traces | missing excl 5 13 |
| 77 | `missing_excl_5_14` | all-traces | missing excl 5 14 |
| 78 | `missing_excl_5_15` | all-traces | missing excl 5 15 |
| 79 | `missing_excl_6_7` | all-traces | missing excl 6 7 |
| 80 | `missing_excl_6_8` | all-traces | missing excl 6 8 |
| 81 | `missing_excl_6_9` | all-traces | missing excl 6 9 |
| 82 | `missing_excl_6_10` | all-traces | missing excl 6 10 |
| 83 | `missing_excl_6_11` | all-traces | missing excl 6 11 |
| 84 | `missing_excl_6_12` | all-traces | missing excl 6 12 |
| 85 | `missing_excl_6_13` | all-traces | missing excl 6 13 |
| 86 | `missing_excl_6_14` | all-traces | missing excl 6 14 |
| 87 | `missing_excl_6_15` | all-traces | missing excl 6 15 |
| 88 | `missing_excl_7_8` | all-traces | missing excl 7 8 |
| 89 | `missing_excl_7_9` | all-traces | missing excl 7 9 |
| 90 | `missing_excl_7_10` | all-traces | missing excl 7 10 |
| 91 | `missing_excl_7_11` | all-traces | missing excl 7 11 |
| 92 | `missing_excl_7_12` | all-traces | missing excl 7 12 |
| 93 | `missing_excl_7_13` | all-traces | missing excl 7 13 |
| 94 | `missing_excl_7_14` | all-traces | missing excl 7 14 |
| 95 | `missing_excl_7_15` | all-traces | missing excl 7 15 |
| 96 | `missing_excl_8_9` | all-traces | missing excl 8 9 |
| 97 | `missing_excl_8_10` | all-traces | missing excl 8 10 |
| 98 | `missing_excl_8_11` | all-traces | missing excl 8 11 |
| 99 | `missing_excl_8_12` | all-traces | missing excl 8 12 |
| 100 | `missing_excl_8_13` | all-traces | missing excl 8 13 |
| 101 | `missing_excl_8_14` | all-traces | missing excl 8 14 |
| 102 | `missing_excl_8_15` | all-traces | missing excl 8 15 |
| 103 | `missing_excl_9_10` | all-traces | missing excl 9 10 |
| 104 | `missing_excl_9_11` | all-traces | missing excl 9 11 |
| 105 | `missing_excl_9_12` | all-traces | missing excl 9 12 |
| 106 | `missing_excl_9_13` | all-traces | missing excl 9 13 |
| 107 | `missing_excl_9_14` | all-traces | missing excl 9 14 |
| 108 | `missing_excl_9_15` | all-traces | missing excl 9 15 |
| 109 | `missing_excl_10_11` | all-traces | missing excl 10 11 |
| 110 | `missing_excl_10_12` | all-traces | missing excl 10 12 |
| 111 | `missing_excl_10_13` | all-traces | missing excl 10 13 |
| 112 | `missing_excl_10_14` | all-traces | missing excl 10 14 |
| 113 | `missing_excl_10_15` | all-traces | missing excl 10 15 |
| 114 | `missing_excl_11_12` | all-traces | missing excl 11 12 |
| 115 | `missing_excl_11_13` | all-traces | missing excl 11 13 |
| 116 | `missing_excl_11_14` | all-traces | missing excl 11 14 |
| 117 | `missing_excl_11_15` | all-traces | missing excl 11 15 |
| 118 | `missing_excl_12_13` | all-traces | missing excl 12 13 |
| 119 | `missing_excl_12_14` | all-traces | missing excl 12 14 |
| 120 | `missing_excl_12_15` | all-traces | missing excl 12 15 |
| 121 | `missing_excl_13_14` | all-traces | missing excl 13 14 |
| 122 | `missing_excl_13_15` | all-traces | missing excl 13 15 |
| 123 | `missing_excl_14_15` | all-traces | missing excl 14 15 |
| 124 | `missing_exh` | all-traces | missing exh |
| 125 | `missing_suf_0` | exists-trace | missing suf 0 |
| 126 | `missing_suf_1` | exists-trace | missing suf 1 |
| 127 | `missing_suf_2` | exists-trace | missing suf 2 |
| 128 | `missing_suf_3` | exists-trace | missing suf 3 |
| 129 | `missing_ver_empty_15` | all-traces | missing ver empty 15 |
| 130 | `missing_ver_nonempty_0` | all-traces | missing ver nonempty 0 |
| 131 | `missing_ver_nonempty_1` | all-traces | missing ver nonempty 1 |
| 132 | `missing_ver_nonempty_2` | all-traces | missing ver nonempty 2 |
| 133 | `missing_ver_nonempty_3` | all-traces | missing ver nonempty 3 |
| 134 | `missing_ver_nonempty_4` | all-traces | missing ver nonempty 4 |
| 135 | `missing_ver_nonempty_5` | all-traces | missing ver nonempty 5 |
| 136 | `missing_ver_nonempty_6` | all-traces | missing ver nonempty 6 |
| 137 | `missing_ver_nonempty_7` | all-traces | missing ver nonempty 7 |
| 138 | `missing_ver_nonempty_8` | all-traces | missing ver nonempty 8 |
| 139 | `missing_ver_nonempty_9` | all-traces | missing ver nonempty 9 |
| 140 | `missing_ver_nonempty_10` | all-traces | missing ver nonempty 10 |
| 141 | `missing_ver_nonempty_11` | all-traces | missing ver nonempty 11 |
| 142 | `missing_ver_nonempty_12` | all-traces | missing ver nonempty 12 |
| 143 | `missing_ver_nonempty_13` | all-traces | missing ver nonempty 13 |
| 144 | `missing_ver_nonempty_14` | all-traces | missing ver nonempty 14 |
| 145 | `missing_min_0_0` | all-traces | missing min 0 0 |
| 146 | `missing_min_1_0` | all-traces | missing min 1 0 |
| 147 | `missing_min_2_0` | all-traces | missing min 2 0 |
| 148 | `missing_min_3_0` | all-traces | missing min 3 0 |
| 149 | `missing_uniq_sing_0` | all-traces | missing uniq sing 0 |
| 150 | `missing_uniq_sing_1` | all-traces | missing uniq sing 1 |
| 151 | `missing_uniq_sing_2` | all-traces | missing uniq sing 2 |
| 152 | `missing_uniq_sing_3` | all-traces | missing uniq sing 3 |

## Protocol description (natural language)

* Protocol: DMN + message tracing (fixed identities)
 * Modeler:  Kevin Morio and Robert Künnemann
 * Date:     Sep 2020
 * Source:   "SoK: Techniques for Verifiable Mix Nets", Thomas Haines and Johannes Müller, CSF20
 * Status:   working (deprecated)
 * Notes:    Run with: tamarin-prover +RTS -N4 -RTS --stop-on-trace=seqdfs --prove --heuristic=o \
 *                     --oraclename=oracle-dmn-message-tracing dmn-message-tracing-all-4-fixed.spthy
 *
 * In this version, the audit continues after detecting the first unexpected message on the bulletin board.
