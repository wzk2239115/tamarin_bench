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
| 1 | `exists_session` | exists-trace | exists session |
| 2 | `exists_two_sessions` | exists-trace | exists two sessions |
| 3 | `I_disagreement_implies_Sr_or_SiEi_compromise_and_PSK_compromise` | all-traces | i disagreement implies sr or siei compromise and psk compromise |
| 4 | `R_disagreement_implies_Si_or_SrEr_compromise_and_PSK_compromise` | all-traces | r disagreement implies si or srer compromise and psk compromise |
| 5 | `UKS_resistance` | all-traces | uks resistance |
| 6 | `session_uniqueness` | all-traces | session uniqueness |
| 7 | `key_secrecy` | all-traces | key secrecy |
| 8 | `identity_hiding` | all-traces | identity hiding |

## Protocol description (natural language)

* Protocol:    Wireguard protocol
 * Modeler:     Kevin Milner & Jason Donenfeld
 * Date:        2017
 * Source:      Original
 * Status:      Basically complete? Use the 'i' heuristic to autoprove.
 *
 * TODO:
 * - Implement identity hiding using observational equivalence, instead of the weaker surrogate-based property.
 * - Prove indistinguishability using observational equivalence.
 * - Model ECDH(private, NULL) = NULL
