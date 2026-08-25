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
| 1 | `executability` | exists-trace | executability |
| 2 | `injectiveagreement_ue_gnb_k_gnb` | all-traces | injectiveagreement ue gnb k gnb |
| 3 | `injectiveagreement_gnb_ue_k_gnb` | all-traces | injectiveagreement gnb ue k gnb |
| 4 | `secret_k_asme` | all-traces | secret k asme |
| 5 | `secret_k_amf` | all-traces | secret k amf |
| 6 | `secret_k_enb` | all-traces | secret k enb |
| 7 | `secret_k_gnb_star` | all-traces | secret k gnb star |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
