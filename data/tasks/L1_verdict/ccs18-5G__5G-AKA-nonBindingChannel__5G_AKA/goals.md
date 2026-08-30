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
| 13 | `weakagreement_ue_seaf_noRev` | all-traces | weakagreement ue seaf norev |
| 14 | `weakagreement_ue_seaf_keyConf_noRev` | all-traces | weakagreement ue seaf keyconf norev |
| 15 | `weakagreement_ue_hss_noAsyKeyRev_noSupiRev_noSqnRev_noChanRev` | all-traces | weakagreement ue hss noasykeyrev nosupirev nosqnrev nochanrev |
| 16 | `cleanAttack_injectiveagreement_ue_hss_supi_noRev` | all-traces | cleanattack injectiveagreement ue hss supi norev |
| 17 | `noninjectiveagreement_ue_hss_supi_noKeyRev` | all-traces | noninjectiveagreement ue hss supi nokeyrev |
| 18 | `noninjectiveagreement_ue_hss_kseaf_noRev` | all-traces | noninjectiveagreement ue hss kseaf norev |
| 19 | `noninjectiveagreement_ue_hss_snname_noRev` | all-traces | noninjectiveagreement ue hss snname norev |
| 20 | `weakagreement_ue_hss_keyConf_noAsyKeyRev_noSupiRev_noSqnRev_noChanRev` | all-traces | weakagreement ue hss keyconf noasykeyrev nosupirev nosqnrev nochanrev |
| 21 | `injectiveagreement_ue_hss_kseaf_keyConf_noKeyRev` | all-traces | injectiveagreement ue hss kseaf keyconf nokeyrev |
| 22 | `noninjectiveagreement_ue_hss_snname_keyConf_noKeyRev` | all-traces | noninjectiveagreement ue hss snname keyconf nokeyrev |
| 23 | `cleanAttack_injectiveagreement_ue_hss_keyConf_supi_noRev` | all-traces | cleanattack injectiveagreement ue hss keyconf supi norev |
| 24 | `noninjectiveagreement_ue_hss_keyConf_supi_noKeyRev` | all-traces | noninjectiveagreement ue hss keyconf supi nokeyrev |
| 25 | `noninjectiveagreement_seaf_ue_kseaf_noRev` | all-traces | noninjectiveagreement seaf ue kseaf norev |
| 26 | `cleanAttack_injectiveagreement_seaf_ue_supi_noRev` | all-traces | cleanattack injectiveagreement seaf ue supi norev |
| 27 | `noninjectiveagreement_seaf_ue_supi_noKeyRev_noChanRev` | all-traces | noninjectiveagreement seaf ue supi nokeyrev nochanrev |
| 28 | `weakagreement_seaf_ue_noKeyRev_noAsyKeyRev_noSupiRev_noSqnRev` | all-traces | weakagreement seaf ue nokeyrev noasykeyrev nosupirev nosqnrev |
| 29 | `weakagreement_seaf_ue_noAsyKeyRev_noSupiRev_noSqnRev_noChanRev` | all-traces | weakagreement seaf ue noasykeyrev nosupirev nosqnrev nochanrev |
| 30 | `weakagreement_seaf_ue_noKeyRev_noChanRev` | all-traces | weakagreement seaf ue nokeyrev nochanrev |
| 31 | `noninjectiveagreement_seaf_ue_kseaf_keyConf_noRev` | all-traces | noninjectiveagreement seaf ue kseaf keyconf norev |
| 32 | `noninjectiveagreement_seaf_ue_keyConf_supi_noKeyRev_noChanRev` | all-traces | noninjectiveagreement seaf ue keyconf supi nokeyrev nochanrev |
| 33 | `weakagreement_seaf_ue_KeyConf_noKeyRev_noAsyKeyRev_noSupiRev_noSqnRev` | all-traces | weakagreement seaf ue keyconf nokeyrev noasykeyrev nosupirev nosqnrev |
| 34 | `weakagreement_seaf_ue_KeyConf_noKeyRev_noChanRev` | all-traces | weakagreement seaf ue keyconf nokeyrev nochanrev |
| 35 | `weakagreement_seaf_ue_KeyConf_noAsyKeyRev_noSupiRev_noSqnRev_noChanRev` | all-traces | weakagreement seaf ue keyconf noasykeyrev nosupirev nosqnrev nochanrev |
| 36 | `weakagreement_seaf_hss_noAsyKeyRev_noSupiRev_noSqnRev_noKeyRev` | all-traces | weakagreement seaf hss noasykeyrev nosupirev nosqnrev nokeyrev |
| 37 | `noninjectiveagreement_seaf_hss_kseaf_noChanRev` | all-traces | noninjectiveagreement seaf hss kseaf nochanrev |
| 38 | `injectiveagreement_seaf_hss_kseaf_noChanRev_noSqnRev_noSupiRev_noAsyKeyRev` | all-traces | injectiveagreement seaf hss kseaf nochanrev nosqnrev nosupirev noasykeyrev |
| 39 | `injectiveagreement_seaf_hss_kseaf_noKeyRev_noChanRev` | all-traces | injectiveagreement seaf hss kseaf nokeyrev nochanrev |
| 40 | `noninjectiveagreement_seaf_hss_supi_noChanRev` | all-traces | noninjectiveagreement seaf hss supi nochanrev |
| 41 | `weakagreement_seaf_hss_keyConf_noAsyKeyRev_noSupiRev_noSqnRev_noKeyRev` | all-traces | weakagreement seaf hss keyconf noasykeyrev nosupirev nosqnrev nokeyrev |
| 42 | `noninjectiveagreement_seaf_hss_kseaf_keyConf_noChanRev` | all-traces | noninjectiveagreement seaf hss kseaf keyconf nochanrev |
| 43 | `injectiveagreement_seaf_hss_kseaf_keyConf_noChanRev_noSqnRev_noSupiRev_noAsyKeyRev` | all-traces | injectiveagreement seaf hss kseaf keyconf nochanrev nosqnrev nosupirev noasykeyrev |
| 44 | `injectiveagreement_seaf_hss_kseaf_keyConf_noKeyRev_noChanRev` | all-traces | injectiveagreement seaf hss kseaf keyconf nokeyrev nochanrev |
| 45 | `noninjectiveagreement_seaf_hss_keyConf_supi_noChanRev` | all-traces | noninjectiveagreement seaf hss keyconf supi nochanrev |
| 46 | `injectiveagreement_hss_ue_kseaf_noKeyRev` | all-traces | injectiveagreement hss ue kseaf nokeyrev |
| 47 | `weakagreement_hss_ue_noAsyKeyRev_noSupiRev_noSqnRev_noChanRev` | all-traces | weakagreement hss ue noasykeyrev nosupirev nosqnrev nochanrev |
| 48 | `noninjectiveagreement_hss_ue_supi_noKeyRev` | all-traces | noninjectiveagreement hss ue supi nokeyrev |
| 49 | `noninjectiveagreement_hss_ue_snname_noKeyRev` | all-traces | noninjectiveagreement hss ue snname nokeyrev |
| 50 | `injectiveagreement_hss_seaf_kseaf_noChanRev` | all-traces | injectiveagreement hss seaf kseaf nochanrev |
| 51 | `weakagreement_hss_seaf_noAsyKeyRev_noSupiRev_noSqnRev_noKeyRev` | all-traces | weakagreement hss seaf noasykeyrev nosupirev nosqnrev nokeyrev |
| 52 | `noninjectiveagreement_hss_seaf_supi_noRev` | all-traces | noninjectiveagreement hss seaf supi norev |
| 53 | `cleanAttack_secrecy_ue_supi_noRev` | all-traces | cleanattack secrecy ue supi norev |
| 54 | `secrecy_ue_supi_noChanRevAtAll_noSupiRev_noAsyKeyRev` | all-traces | secrecy ue supi nochanrevatall nosupirev noasykeyrev |
| 55 | `secrecy_ue_supi_noChanRevAtAll_noSupiRev_noKeyRev_noSqnRev` | all-traces | secrecy ue supi nochanrevatall nosupirev nokeyrev nosqnrev |
| 56 | `cleanAttack_secrecy_ue_supi_keyConf_noRev` | all-traces | cleanattack secrecy ue supi keyconf norev |
| 57 | `secrecy_ue_kseaf_noKeyRev_noChanRev` | all-traces | secrecy ue kseaf nokeyrev nochanrev |
| 58 | `secrecy_ue_kseaf_noChanRev_noSupiRev_noSqnRev_noAsyKeyRev` | all-traces | secrecy ue kseaf nochanrev nosupirev nosqnrev noasykeyrev |
| 59 | `secrecy_ue_kseaf_noKeyRev_noSupiRev_noSqnRev_noAsyKeyRev` | all-traces | secrecy ue kseaf nokeyrev nosupirev nosqnrev noasykeyrev |
| 60 | `secrecy_ue_k_noKeyRev` | all-traces | secrecy ue k nokeyrev |
| 61 | `secrecy_hss_kseaf_noKeyRev_noSupiRev_noSqnRev_noAsyKeyRev` | all-traces | secrecy hss kseaf nokeyrev nosupirev nosqnrev noasykeyrev |
| 62 | `secrecy_hss_kseaf_noChanRev_noSupiRev_noSqnRev_noAsyKeyRev` | all-traces | secrecy hss kseaf nochanrev nosupirev nosqnrev noasykeyrev |
| 63 | `secrecy_hss_kseaf_noChanRev_noKeyRev` | all-traces | secrecy hss kseaf nochanrev nokeyrev |
| 64 | `cleanAttack_secrecy_hss_supi_noRev` | all-traces | cleanattack secrecy hss supi norev |
| 65 | `secrecy_hss_supi_noChanRevAtAll_noSupiRev_noAsyKeyRev` | all-traces | secrecy hss supi nochanrevatall nosupirev noasykeyrev |
| 66 | `secrecy_hss_supi_noChanRevAtAll_noSupiRev_noKeyRev_noSqnRev` | all-traces | secrecy hss supi nochanrevatall nosupirev nokeyrev nosqnrev |
| 67 | `secrecy_hss_k_noKeyRev` | all-traces | secrecy hss k nokeyrev |
| 68 | `secrecy_seaf_kseaf_noChanRev_noKeyRev` | all-traces | secrecy seaf kseaf nochanrev nokeyrev |
| 69 | `secrecy_seaf_kseaf_noChanRev_noSupiRev_noSqnRev_noAsyKeyRev` | all-traces | secrecy seaf kseaf nochanrev nosupirev nosqnrev noasykeyrev |
| 70 | `secrecy_seaf_kseaf_noKeyRev_noSupiRev_noSqnRev_noAsyKeyRev` | all-traces | secrecy seaf kseaf nokeyrev nosupirev nosqnrev noasykeyrev |
| 71 | `cleanAttack_secrecy_seaf_supi_noRev` | all-traces | cleanattack secrecy seaf supi norev |
| 72 | `secrecy_seaf_supi_noChanRevAtAll_noSupiRev_noAsyKeyRev` | all-traces | secrecy seaf supi nochanrevatall nosupirev noasykeyrev |
| 73 | `secrecy_seaf_supi_noChanRevAtAll_noSupiRev_noKeyRev_noSqnRev` | all-traces | secrecy seaf supi nochanrevatall nosupirev nokeyrev nosqnrev |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
