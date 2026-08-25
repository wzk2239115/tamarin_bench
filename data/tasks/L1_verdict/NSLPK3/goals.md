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
- Some theories use `diff()` terms (observational equivalence): analyzing
  them requires `tamarin-prover --diff`; the default observational
  equivalence check covers theories with no explicit lemmas.

## Goals to formalize

| # | Lemma name | Quantifier | Property |
|---|------------|------------|----------|
| 1 | `types` | all-traces | types |
| 2 | `nonce_secrecy` | all-traces | nonce secrecy |
| 3 | `injective_agree` | all-traces | injective agree |
| 4 | `session_key_setup_possible` | exists-trace | session key setup possible |

## Protocol description (natural language)

---

### Protocol Description: Needham-Schroeder-Lowe Public Key Protocol (Three-Messages)

**Protocol Name:** Needham-Schroeder-Lowe Public Key Protocol (NSLPK3)

**Modeler:** Simon Meier

**Date:** June 2012

**Source:** Modeled after the description by Paulson in Isabelle/HOL/Auth/NS_Public.thy.

**Status:** Working

#### Overview
The Needham-Schroeder-Lowe Public Key Protocol is a cryptographic protocol designed to facilitate secure communication between two parties by using public key encryption. The protocol is characterized by the following three main message exchanges, which ensure that both parties are authenticated and a shared secret (session key) is established.

#### Participants
- **Initiator (I):** The party that initiates the protocol.
- **Responder (R):** The party that responds to the initiator's request.

#### Key Components
- **Long-term Keys (Ltk):** Each participant possesses a long-term private key (ltk) and a corresponding public key (pk). 
- **Nonces (ni, nr):** Randomly generated values used to ensure freshness and prevent replay attacks.

#### Protocol Steps
1. **Message 1: Initiator to Responder**
   - The initiator (I) sends a message to the responder (R) containing:
     - A nonce (ni)
     - The initiator's identity (I)
   - This message is encrypted with the responder's public key (pk(R)).

2. **Message 2: Responder to Initiator**
   - Upon receiving the first message, the responder (R) decrypts it and retrieves the nonce (ni) and initiator's identity (I). 
   - The responder then generates a new nonce (nr) and sends back a message to the initiator containing:
     - The newly generated nonce (nr)
     - The original nonce (ni)
     - The responder's identity (R)
   - This message is encrypted with the initiator's public key (pk(I)).

3. **Message 3: Initiator to Responder**
   - After receiving the second message, the initiator decrypts it to get both nonces (ni and nr). 
   - The initiator then sends a confirmation message back to the responder, which contains:
     - The responder's nonce (nr)
   - This message is encrypted with the responder's public key (pk(R)).

#### Security Goals
- **Nonce Secrecy:** Ensures that the nonces exchanged during the protocol remain secret from any adversary.
- **Injective Agreement:** Guarantees that if an agent commits to a session with certain parameters, they are uniquely associated with that session, preventing replay and impersonation attacks.
- **Session Key Setup:** Ensures that it is possible for honest participants to establish a shared secret without the adversary having knowledge of it.

#### Additional Notes
- The protocol utilizes a public key infrastructure (PKI) for key management.
- The model captures both the protocol execution and the potential actions of an adversary, including key reveals and message interception.
- The protocol guarantees that even if an adversary reveals a long-term key, they cannot gain information about the session keys established by honest agents.

---
