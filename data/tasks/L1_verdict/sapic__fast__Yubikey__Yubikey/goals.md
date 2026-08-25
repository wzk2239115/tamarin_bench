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
- An `oracle` proof-heuristic file is provided; keep it in the working directory when running tamarin (it guides proof search).
Some theories use `diff()` terms (observational equivalence):
  analyzing them requires `tamarin-prover --diff`.

## Goals to formalize

| # | Lemma name | Quantifier | Property |
|---|------------|------------|----------|
| 1 | `secrecy_enc` | all-traces | secrecy enc |
| 2 | `init_server` | all-traces | init server |
| 3 | `init_server_secrecy` | all-traces | init server secrecy |
| 4 | `Login_reachable` | exists-trace | login reachable |
| 5 | `Login_reachable_two` | exists-trace | login reachable two |
| 6 | `one_count_foreach_login` | all-traces | one count foreach login |
| 7 | `no_replay` | all-traces | no replay |
| 8 | `injective_correspondance` | all-traces | injective correspondance |
| 9 | `Login_invalidates_smaller_counters` | all-traces | login invalidates smaller counters |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
