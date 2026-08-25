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
| 1 | `executable` | exists-trace | executable |

## Protocol description (natural language)

---

### KEA+ Protocol Description

**Protocol Name**: KEA+  
**Modelers**: Jannik Dreier, Ralf Sasse  
**Date**: April 2015  
**Source**: Lauter, Mityagin, 2006  
**Property**: Key indistinguishable from randomness  
**Status**: (To be determined)

#### Overview
KEA+ is a key exchange protocol that allows two parties to establish a shared secret key over an insecure channel. The protocol is based on the Diffie-Hellman key exchange mechanism and incorporates additional security measures to ensure that the keys generated are indistinguishable from random values.

#### Key Components
1. **Functions**:
   - `h/1`: A cryptographic hash function used to generate keys from given inputs.
   - `g/0`: A generator for the Diffie-Hellman group used in the protocol.

2. **Long-term Keypair Generation**:
   - Each participant generates a long-term public/private key pair. The public key is derived from the private key using the generator.

3. **Initiator**:
   - **Step 1**: The initiator generates a session key using their ephemeral secret and sends it along with their identity and the public key of the responder to the responder.
   - **Step 2**: The initiator computes a derived key based on the public key received from the responder and their long-term key.

4. **Responder**:
   - **Step 1**: The responder receives the initiator's message, extracts the necessary information, and computes their own session key.
   - **Step 2**: The responder sends their ephemeral public key along with their computed session key back to the initiator.

#### Protocol Rules
- **Long-term Key Generation**: Each participant generates a long-term key pair and outputs their public key.
- **Initiation Phase**: The initiator sends a message to the responder containing their information and the computed session key.
- **Response Phase**: The responder processes the initiator's message, computes their session key, and sends a response back to the initiator.
  
#### Restrictions and Properties
- **One Key per Name**: A restriction is placed to ensure that each participant has a unique long-term key.
- **Key Initialization and Response**: The protocol ensures that both parties successfully derive and agree on the session key.

#### Security Lemmas
- The protocol guarantees that there exists a trace in which both the key initialization by the initiator and the key response by the responder can be observed, ensuring that the keys are established.

### Additional Notes
- The protocol is designed to prevent key compromise and ensure that the generated keys are secure.
- The key exchange is modeled within the eCK (extended Canetti-Krawczyk) framework to evaluate its security properties.

---
