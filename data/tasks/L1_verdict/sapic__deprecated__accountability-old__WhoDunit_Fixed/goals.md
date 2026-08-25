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
| 1 | `acc_coarse_excl_0_1` | all-traces | acc coarse excl 0 1 |
| 2 | `acc_coarse_exh` | all-traces | acc coarse exh |
| 3 | `acc_coarse_suf_0_0` | exists-trace | acc coarse suf 0 0 |
| 4 | `acc_coarse_ver_empty_1` | all-traces | acc coarse ver empty 1 |
| 5 | `acc_coarse_ver_nonempty_0` | all-traces | acc coarse ver nonempty 0 |
| 6 | `acc_coarse_min_0_0_0` | all-traces | acc coarse min 0 0 0 |
| 7 | `acc_coarse_uniq_0` | all-traces | acc coarse uniq 0 |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
