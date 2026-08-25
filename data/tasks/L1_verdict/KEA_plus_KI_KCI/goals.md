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
| 1 | `keaplus_initiator_key` | all-traces | keaplus initiator key |
| 2 | `keaplus_responder_key` | all-traces | keaplus responder key |

## Protocol description (natural language)

---

### Description of the KEA+ Protocol

**Protocol Name:** KEA+  
**Modeler:** Cas Cremers  
**Date:** January/April 2012  
**Source:** "Security Analysis of KEA Authenticated Key Exchange Protocol" by Lauter, Mityagin, 2006  
**Security Properties:** Key Independence (KI), Key Compromise Impersonation (KCI)  
**Status:** Working  

**Overview:**
KEA+ is an authenticated key exchange protocol that facilitates secure communication between two parties, typically referred to as the initiator (I) and the responder (R). The protocol uses ephemeral keys along with long-term keys to establish a shared session key, ensuring the confidentiality of the exchanged information.

**Protocol Rules:**

1. **Key Generation (generate_ltk):**
   - The initiator generates a long-term key (Ltk) and the corresponding public key (Pk) using a generator g raised to the private key (lkA). This is done upon registration of the key.

2. **Initiator Phase (Init_1):**
   - The initiator derives an ephemeral public key (epkI) based on a fresh ephemeral key (ekI) and sends the initial message carrying this ephemeral key along with its long-term key (Ltk).

3. **Responder Phase (Init_2):**
   - The responder, upon receiving the initiator's message, computes their own public key (pkR) and derives a session key (key) using a hash function. The responder then responds with their public key and the computed session key.

4. **Response from Initiator (Resp_1):**
   - The initiator receives a message from the responder, which includes the responder's ephemeral key (epkR). The initiator computes the session key based on the received data, completing the key exchange.

5. **Reveal Rules:**
   - The protocol includes reveal rules to allow for the extraction of session keys, ephemeral keys, and long-term keys under specific conditions, which are crucial for analyzing the security properties of the protocol.

**Security Properties:**
- The protocol aims to ensure that:
  - The session key is not compromised even if the long-term key of one party is revealed.
  - The protocol provides security against key compromise impersonation (KCI) attacks.
  - The adversary cannot deduce the session key of a clean test session without violating the security properties laid out.

**Security Lemmas:**
- Two key lemmas confirm that if each agent registers at most one public key, then an attack is not possible. The lemmas outline conditions where an attacker could potentially reveal session keys or ephemeral keys, establishing the protocol's resistance to various forms of attack.

---
