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
| 1 | `one_C0_per_tid` | all-traces | one c0 per tid |
| 2 | `one_C1_per_tid` | all-traces | one c1 per tid |
| 3 | `one_C1_retry_per_tid` | all-traces | one c1 retry per tid |
| 4 | `one_S1_per_tid` | all-traces | one s1 per tid |
| 5 | `one_S1_PSK_per_tid` | all-traces | one s1 psk per tid |
| 6 | `one_S1_PSK_DHE_per_tid` | all-traces | one s1 psk dhe per tid |
| 7 | `one_C1_PSK_per_tid` | all-traces | one c1 psk per tid |
| 8 | `one_C1_PSK_DHE_per_tid` | all-traces | one c1 psk dhe per tid |
| 9 | `one_S2a_per_tid` | all-traces | one s2a per tid |
| 10 | `one_S2b_per_tid` | all-traces | one s2b per tid |
| 11 | `one_S2c_per_tid` | all-traces | one s2c per tid |
| 12 | `one_S2c_req_per_tid` | all-traces | one s2c req per tid |
| 13 | `one_S2d_per_tid` | all-traces | one s2d per tid |
| 14 | `one_S2d_PSK_per_tid` | all-traces | one s2d psk per tid |
| 15 | `one_C2a_per_tid` | all-traces | one c2a per tid |
| 16 | `one_C2b_per_tid` | all-traces | one c2b per tid |
| 17 | `one_C2c_per_tid` | all-traces | one c2c per tid |
| 18 | `one_C2c_req_per_tid` | all-traces | one c2c req per tid |
| 19 | `one_C2d_per_tid` | all-traces | one c2d per tid |
| 20 | `one_C2d_PSK_per_tid` | all-traces | one c2d psk per tid |
| 21 | `one_C3_per_tid` | all-traces | one c3 per tid |
| 22 | `one_C3_cert_per_tid` | all-traces | one c3 cert per tid |
| 23 | `one_S3_per_tid` | all-traces | one s3 per tid |
| 24 | `one_S3_cert_per_tid` | all-traces | one s3 cert per tid |
| 25 | `S1_vs_S1_PSK_DHE` | all-traces | s1 vs s1 psk dhe |
| 26 | `S1_PSK_vs_S1_PSK_DHE` | all-traces | s1 psk vs s1 psk dhe |
| 27 | `S1_PSK_vs_S1` | all-traces | s1 psk vs s1 |
| 28 | `C1_vs_C1_PSK_DHE` | all-traces | c1 vs c1 psk dhe |
| 29 | `C1_PSK_vs_C1_PSK_DHE` | all-traces | c1 psk vs c1 psk dhe |
| 30 | `C1_PSK_vs_C1` | all-traces | c1 psk vs c1 |
| 31 | `S3_vs_S3_cert` | all-traces | s3 vs s3 cert |
| 32 | `C3_vs_C3_cert` | all-traces | c3 vs c3 cert |
| 33 | `S2d_vs_S2d_PSK` | all-traces | s2d vs s2d psk |
| 34 | `C2d_vs_C2d_PSK` | all-traces | c2d vs c2d psk |
| 35 | `cert_req_origin` | all-traces | cert req origin |
| 36 | `nst_source` | all-traces | nst source |
| 37 | `ku_extract` | all-traces | ku extract |
| 38 | `ku_expand` | all-traces | ku expand |
| 39 | `ku_ltk` | all-traces | ku ltk |
| 40 | `hsms_derive` | all-traces | hsms derive |
| 41 | `posths_rms` | all-traces | posths rms |
| 42 | `matching_transcripts_posths` | all-traces | matching transcripts posths |
| 43 | `matching_rms_posths` | all-traces | matching rms posths |
| 44 | `rms_derives_hs` | all-traces | rms derives hs |
| 45 | `sig_origin` | all-traces | sig origin |
| 46 | `post_master_secret` | all-traces | post master secret |
| 47 | `invariant_post_hs` | all-traces | invariant post hs |
| 48 | `handshake_secret` | all-traces | handshake secret |
| 49 | `secret_session_keys` | all-traces | secret session keys |
| 50 | `pfs_handshake_secret` | all-traces | pfs handshake secret |
| 51 | `secret_session_keys_pfs` | all-traces | secret session keys pfs |
| 52 | `unique_session_keys` | all-traces | unique session keys |
| 53 | `consistent_nonces` | all-traces | consistent nonces |
| 54 | `auth_psk` | all-traces | auth psk |
| 55 | `entity_authentication` | all-traces | entity authentication |
| 56 | `transcript_agreement` | all-traces | transcript agreement |
| 57 | `mutual_entity_authentication` | all-traces | mutual entity authentication |
| 58 | `mutual_transcript_agreement` | all-traces | mutual transcript agreement |
| 59 | `injective_mutual_entity_authentication` | all-traces | injective mutual entity authentication |
| 60 | `tid_invariant` | all-traces | tid invariant |
| 61 | `one_start_per_tid` | all-traces | one start per tid |
| 62 | `ku_fresh_psk` | all-traces | ku fresh psk |
| 63 | `session_key_agreement` | all-traces | session key agreement |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
