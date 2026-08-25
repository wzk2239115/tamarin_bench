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
| 1 | `acc_ca_excl_0_1` | all-traces | acc ca excl 0 1 |
| 2 | `acc_ca_exh` | all-traces | acc ca exh |
| 3 | `acc_ca_suf_0_0` | exists-trace | acc ca suf 0 0 |
| 4 | `acc_ca_ver_empty_1` | all-traces | acc ca ver empty 1 |
| 5 | `acc_ca_ver_nonempty_0` | all-traces | acc ca ver nonempty 0 |
| 6 | `acc_ca_min_0_0_0` | all-traces | acc ca min 0 0 0 |
| 7 | `acc_ca_uniq_0` | all-traces | acc ca uniq 0 |
| 8 | `acc_la_excl_0_1` | all-traces | acc la excl 0 1 |
| 9 | `acc_la_exh` | all-traces | acc la exh |
| 10 | `acc_la_suf_0_0` | exists-trace | acc la suf 0 0 |
| 11 | `acc_la_ver_empty_1` | all-traces | acc la ver empty 1 |
| 12 | `acc_la_ver_nonempty_0` | all-traces | acc la ver nonempty 0 |
| 13 | `acc_la_min_0_0_0` | all-traces | acc la min 0 0 0 |
| 14 | `acc_la_uniq_0` | all-traces | acc la uniq 0 |
| 15 | `acc_excl_0_1` | all-traces | acc excl 0 1 |
| 16 | `acc_excl_0_2` | all-traces | acc excl 0 2 |
| 17 | `acc_excl_0_3` | all-traces | acc excl 0 3 |
| 18 | `acc_excl_1_2` | all-traces | acc excl 1 2 |
| 19 | `acc_excl_1_3` | all-traces | acc excl 1 3 |
| 20 | `acc_excl_2_3` | all-traces | acc excl 2 3 |
| 21 | `acc_exh` | all-traces | acc exh |
| 22 | `acc_suf_0` | exists-trace | acc suf 0 |
| 23 | `acc_suf_1` | exists-trace | acc suf 1 |
| 24 | `acc_ver_empty_3` | all-traces | acc ver empty 3 |
| 25 | `acc_ver_nonempty_0` | all-traces | acc ver nonempty 0 |
| 26 | `acc_ver_nonempty_1` | all-traces | acc ver nonempty 1 |
| 27 | `acc_ver_nonempty_2` | all-traces | acc ver nonempty 2 |
| 28 | `acc_min_0_0` | all-traces | acc min 0 0 |
| 29 | `acc_min_1_0` | all-traces | acc min 1 0 |
| 30 | `acc_uniq_sing_0` | all-traces | acc uniq sing 0 |
| 31 | `acc_uniq_sing_1` | all-traces | acc uniq sing 1 |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
