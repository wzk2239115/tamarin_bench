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
| 1 | `dummy` | all-traces | dummy |
| 2 | `rand_autn_src` | all-traces | rand autn src |
| 3 | `sqn_ue_invariance` | all-traces | sqn ue invariance |
| 4 | `sqn_hss_invariance` | all-traces | sqn hss invariance |
| 5 | `sqn_ue_src` | all-traces | sqn ue src |
| 6 | `sqn_hss_src` | all-traces | sqn hss src |
| 7 | `sqn_ue_nodecrease` | all-traces | sqn ue nodecrease |
| 8 | `sqn_ue_unique` | all-traces | sqn ue unique |
| 9 | `executability_honest` | exists-trace | executability honest |
| 10 | `executability_keyConf_honest` | exists-trace | executability keyconf honest |
| 11 | `executability_desync` | exists-trace | executability desync |
| 12 | `executability_resync` | exists-trace | executability resync |
| 13 | `injectiveagreement_ue_hss_kseaf_noKeyRev` | all-traces | injectiveagreement ue hss kseaf nokeyrev |
| 14 | `noninjectiveagreement_ue_hss_snname_noKeyRev` | all-traces | noninjectiveagreement ue hss snname nokeyrev |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
