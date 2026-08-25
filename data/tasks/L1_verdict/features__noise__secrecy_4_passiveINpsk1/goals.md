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
| 1 | `Secrecy_INpsk1_4_for_Initiator_unless_active_or_reveal_psk_AnyTime_end` | all-traces | secrecy inpsk1 4 for initiator unless active or reveal psk anytime end |
| 2 | `Secrecy_INpsk1_4_for_Initiator_unless_active_or_reveal_re_AnyTime_or_reveal_psk_AnyTime_end` | all-traces | secrecy inpsk1 4 for initiator unless active or reveal re anytime or reveal psk anytime end |
| 3 | `Secrecy_INpsk1_4_for_Initiator_unless_active_or_reveal_s_AnyTime_or_reveal_psk_AnyTime_end` | all-traces | secrecy inpsk1 4 for initiator unless active or reveal s anytime or reveal psk anytime end |
| 4 | `Secrecy_INpsk1_4_for_Initiator_unless_active_or_reveal_s_AnyTime_or_reveal_re_AnyTime_end` | all-traces | secrecy inpsk1 4 for initiator unless active or reveal s anytime or reveal re anytime end |
| 5 | `Secrecy_INpsk1_4_for_Initiator_unless_active_or_reveal_s_AnyTime_or_reveal_re_AnyTime_or_reveal_psk_AnyTime_end` | all-traces | secrecy inpsk1 4 for initiator unless active or reveal s anytime or reveal re anytime or reveal psk anytime end |
| 6 | `Secrecy_INpsk1_4_for_Initiator_unless_active_or_reveal_e_AnyTime_or_reveal_re_AnyTime_end` | all-traces | secrecy inpsk1 4 for initiator unless active or reveal e anytime or reveal re anytime end |
| 7 | `Secrecy_INpsk1_4_for_Initiator_unless_active_or_reveal_e_AnyTime_or_reveal_s_AnyTime_or_reveal_re_AnyTime_end` | all-traces | secrecy inpsk1 4 for initiator unless active or reveal e anytime or reveal s anytime or reveal re anytime end |
| 8 | `Secrecy_INpsk1_4_for_Responder_unless_active_or_reveal_psk_AnyTime_end` | all-traces | secrecy inpsk1 4 for responder unless active or reveal psk anytime end |
| 9 | `Secrecy_INpsk1_4_for_Responder_unless_active_or_reveal_rs_AnyTime_or_reveal_psk_AnyTime_end` | all-traces | secrecy inpsk1 4 for responder unless active or reveal rs anytime or reveal psk anytime end |
| 10 | `Secrecy_INpsk1_4_for_Responder_unless_active_or_reveal_re_AnyTime_or_reveal_psk_AnyTime_end` | all-traces | secrecy inpsk1 4 for responder unless active or reveal re anytime or reveal psk anytime end |
| 11 | `Secrecy_INpsk1_4_for_Responder_unless_active_or_reveal_re_AnyTime_or_reveal_rs_AnyTime_or_reveal_psk_AnyTime_end` | all-traces | secrecy inpsk1 4 for responder unless active or reveal re anytime or reveal rs anytime or reveal psk anytime end |
| 12 | `Secrecy_INpsk1_4_for_Responder_unless_active_or_reveal_e_AnyTime_or_reveal_rs_AnyTime_end` | all-traces | secrecy inpsk1 4 for responder unless active or reveal e anytime or reveal rs anytime end |
| 13 | `Secrecy_INpsk1_4_for_Responder_unless_active_or_reveal_e_AnyTime_or_reveal_re_AnyTime_end` | all-traces | secrecy inpsk1 4 for responder unless active or reveal e anytime or reveal re anytime end |
| 14 | `Secrecy_INpsk1_4_for_Responder_unless_active_or_reveal_e_AnyTime_or_reveal_re_AnyTime_or_reveal_rs_AnyTime_end` | all-traces | secrecy inpsk1 4 for responder unless active or reveal e anytime or reveal re anytime or reveal rs anytime end |
| 15 | `executabilityPassiveAdv` | exists-trace | executabilitypassiveadv |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
