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
| 1 | `init_server` | all-traces | init server |
| 2 | `init_server_secrecy` | all-traces | init server secrecy |
| 3 | `init_yubikey` | all-traces | init yubikey |
| 4 | `slightly_weaker_invariant` | all-traces | slightly weaker invariant |
| 5 | `one_count_foreach_login` | all-traces | one count foreach login |
| 6 | `no_replay` | all-traces | no replay |
| 7 | `injective_correspondance` | all-traces | injective correspondance |
| 8 | `Login_invalidates_smaller_counters` | all-traces | login invalidates smaller counters |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
