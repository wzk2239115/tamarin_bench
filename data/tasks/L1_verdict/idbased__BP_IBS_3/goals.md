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
| 1 | `secrecy_session_key` | all-traces | secrecy session key |
| 2 | `session_escrow` | exists-trace | session escrow |
| 3 | `Weak_Forward_Secrecy_key` | all-traces | weak forward secrecy key |
| 4 | `Strong_Forward_Secrecy_key` | all-traces | strong forward secrecy key |
| 5 | `alivenessInitiatorNoAuthReveal` | all-traces | alivenessinitiatornoauthreveal |
| 6 | `alivenessInitiatorNoSignReveal` | all-traces | alivenessinitiatornosignreveal |
| 7 | `weakagreementInitiatorNoSignReveal` | all-traces | weakagreementinitiatornosignreveal |
| 8 | `noninjectiveagreemenInitiatorNoSignReveal` | all-traces | noninjectiveagreemeninitiatornosignreveal |
| 9 | `injectiveagreementInitiatorNoSignReveal` | all-traces | injectiveagreementinitiatornosignreveal |
| 10 | `alivenessResponderNoAuthReveal` | all-traces | alivenessrespondernoauthreveal |
| 11 | `alivenessResponderNoSignReveal` | all-traces | alivenessrespondernosignreveal |
| 12 | `weakagreementResponderNoSignReveal` | all-traces | weakagreementrespondernosignreveal |
| 13 | `noninjectiveagreemenResponderNoSignReveal` | all-traces | noninjectiveagreemenrespondernosignreveal |
| 14 | `injectiveagreementResponderNoSignReveal` | all-traces | injectiveagreementrespondernosignreveal |
| 15 | `executability_lemma` | exists-trace | executability lemma |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
