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
| 2 | `key_secrecy_PFS` | all-traces | key secrecy pfs |

## Protocol description (natural language)

Certainly! Below is the description content generated for the RYY protocol based on the provided spthy file:

---

## Protocol Description: RYY

### Overview
The RYY protocol is an identity-based key exchange protocol designed to allow two parties to securely establish a shared secret key over an insecure channel. This protocol utilizes a key generation center (KGC) to facilitate the generation of long-term keys and session keys.

### Components
1. **Key Generation Center (KGC)**: 
   - The KGC is responsible for generating and distributing the master secret key (MSK) and for providing long-term keys (LTK) to users upon request.
   
2. **Users**: 
   - Two parties, referred to as Alice (A) and Bob (B), engage in the key exchange process using ephemeral keys generated for each session.

### Key Functions
- **kdf/1**: A key derivation function that generates a session key based on inputs including the identities of both parties and their ephemeral keys.
- **hp/1**: A hash function used to derive values from identities.

### Protocol Steps
1. **KGC Setup**: 
   - The KGC initializes by generating a master secret key (MSK).

2. **Key Request**: 
   - Users request their long-term keys from the KGC using their identities.

3. **Session Initialization (Init)**: 
   - Alice generates an ephemeral key and sends a message containing her ephemeral key (X) to Bob, along with a public value derived from her ephemeral key.
   - Bob receives X and generates his own ephemeral key (Y). He then computes a session key using the received value and sends back his public value (Y) to Alice.

4. **Session Key Agreement**: 
   - Both parties compute the shared session key independently using their respective long-term keys, ephemeral keys, and the public values exchanged.

### Security Properties
1. **Key Agreement**: 
   - The protocol guarantees that both parties can derive the same session key while ensuring that the session keys are unique for each session.
   
2. **Key Secrecy and Perfect Forward Secrecy (PFS)**: 
   - The protocol ensures that even if an adversary gains knowledge of a session key, it cannot compromise the keys generated in future sessions. This is achieved through the use of ephemeral keys, which are not reused.

### Reveal Rules
- The protocol includes rules for revealing long-term keys, master keys, and session keys, allowing specified adversarial actions to be modeled and analyzed.

### Lemmas
- **Key Agreement Reachable**: This lemma states that there exists a trace in which both parties can accept a session key that is derived from the exchanged ephemeral keys and long-term keys.
  
- **Key Secrecy and PFS**: This lemma outlines conditions under which the session key remains secure, even when adversarial actions are taken, such as revealing long-term keys or session keys.

### Conclusion
The RYY protocol exemplifies a secure identity-based key exchange mechanism, ensuring that both parties can establish a session key without the need for prior shared secrets, while also maintaining security against potential adversaries.

---

This description captures the essence and structure of the RYY protocol, providing the necessary details to create a corresponding spthy file for Tamarin.
