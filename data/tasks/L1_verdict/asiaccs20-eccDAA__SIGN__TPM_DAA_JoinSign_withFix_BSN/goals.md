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
| 1 | `auto_bind_restriction` | all-traces | auto bind restriction |
| 2 | `auto_restriction_one_host_per_tpm` | all-traces | auto restriction one host per tpm |
| 3 | `auto_restriction_one_tpm_per_host` | all-traces | auto restriction one tpm per host |
| 4 | `auto_restricition_pke_comes_from_tpm` | all-traces | auto restricition pke comes from tpm |
| 5 | `auto_restriction_single_issuer` | all-traces | auto restriction single issuer |
| 6 | `auto_verify_multiple_pkes` | exists-trace | auto verify multiple pkes |
| 7 | `oracle_correctness_two_sigs_same_credentials_same_bsn` | exists-trace | oracle correctness two sigs same credentials same bsn |
| 8 | `oracle_correctness_two_sigs_same_credentials_different_bsn` | exists-trace | oracle correctness two sigs same credentials different bsn |
| 9 | `oracle_correctness_two_sigs_different_credentials_same_bsn` | exists-trace | oracle correctness two sigs different credentials same bsn |
| 10 | `oracle_correctness_two_sigs_different_credentials_different_bsn` | exists-trace | oracle correctness two sigs different credentials different bsn |
| 11 | `oracle_correctness_two_valid_linked_sigs` | exists-trace | oracle correctness two valid linked sigs |
| 12 | `oracle_correctness_two_valid_unlinked_sigs` | exists-trace | oracle correctness two valid unlinked sigs |
| 13 | `oracle_correctness_join_only` | exists-trace | oracle correctness join only |
| 14 | `oracle_correctness_no_verify` | exists-trace | oracle correctness no verify |
| 15 | `oracle_correctness_with_verify` | exists-trace | oracle correctness with verify |
| 16 | `oracle_auth_aliveness_host_very_weak` | all-traces | oracle auth aliveness host very weak |
| 17 | `oracle_auth_aliveness_host` | all-traces | oracle auth aliveness host |
| 18 | `oracle_auth_aliveness_issuer` | all-traces | oracle auth aliveness issuer |
| 19 | `oracle_auth_weak_agreement_host` | all-traces | oracle auth weak agreement host |
| 20 | `oracle_auth_non_injective_agreement_host_issuer` | all-traces | oracle auth non injective agreement host issuer |
| 21 | `oracle_auth_injective_agreement_host_issuer` | all-traces | oracle auth injective agreement host issuer |
| 22 | `oracle_auth_secrecy_cre` | all-traces | oracle auth secrecy cre |
| 23 | `auto_SP2_UserControlledLinkability` | all-traces | auto sp2 usercontrolledlinkability |
| 24 | `oracle_SP3_Unforgeability` | all-traces | oracle sp3 unforgeability |
| 25 | `oracle_SP4_NonFrameability` | all-traces | oracle sp4 nonframeability |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
