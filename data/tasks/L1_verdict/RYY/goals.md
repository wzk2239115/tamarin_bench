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
| 1 | `key_agreement_reachable` | exists-trace | key agreement reachable |
| 2 | `key_secrecy_WPFS` | all-traces | key secrecy wpfs |

## Protocol description (natural language)

---

**Protocol Description: RYY**

**Protocol Name:** RYY  
**Modeler:** Benedikt Schmidt  
**Date:** July 2012  
**Source:** Boyd overview identity-based key exchange protocols  

**Overview:**
The RYY protocol is an identity-based key exchange protocol that enables two parties, typically referred to as Alice (A) and Bob (B), to establish a shared session key over an insecure channel. The protocol relies on a Key Generation Center (KGC) that issues long-term keys to the users based on their identities.

**Key Components:**

1. **Key Generation Center (KGC):**
   - The KGC is responsible for generating a master secret key (MSK) and for issuing long-term keys (LTKs) to users.
   - The master secret key is used to derive long-term keys for users based on their identity.

2. **Key Generation Rules:**
   - `KGC_Setup`: The KGC generates a master secret key (msk).
   - `KGC_request`: Users request their long-term keys (LTKs) from the KGC, which are computed as a function of the user's identity and the master secret key.

3. **Reveals:**
   - The protocol includes several rules governing the revelation of keys:
     - `Reveal_ltk`: Allows revealing a user's long-term key.
     - `Reveal_master_key`: Allows revealing the master secret key.
     - `Reveal_session_key`: Allows revealing the session key established during the protocol execution.

4. **Protocol Execution:**
   - The protocol involves two main phases: initialization and response.
   - **Initialization Phase (Init):**
     - Alice initiates the protocol by generating an ephemeral key and sending a value derived from it.
     - Upon receiving the value, Bob responds with his own ephemeral key and computes a session key based on both ephemeral keys and their respective long-term keys.
   - **Response Phase (Resp):**
     - Bob sends his ephemeral key back to Alice, allowing both parties to compute the shared session key.

5. **Key Agreement:**
   - The protocol guarantees that both parties end up with the same session key if the interaction is successful, which is expressed in the `key_agreement_reachable` lemma.

6. **Key Secrecy:**
   - The protocol is designed to ensure that if an attacker learns the session key of a test session, then the test session must have been compromised in one of several ways, as specified in the `key_secrecy_WPFS` lemma. This includes conditions such as:
     - The session key being revealed.
     - The long-term key of either party being revealed before the session is complete.
     - The master key being revealed.

**Security Goals:**
- The main security goals of the RYY protocol are to ensure mutual key agreement and the secrecy of the session keys against adversarial attacks. The protocol should withstand attempts by an adversary to compromise the session keys, long-term keys, or the master key.

---
