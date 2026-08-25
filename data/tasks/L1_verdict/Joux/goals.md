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
| 1 | `session_key_establish` | exists-trace | session key establish |
| 2 | `Session_Key_Secrecy_PFS` | all-traces | session key secrecy pfs |

## Protocol description (natural language)

---

### Description of the Joux Protocol

#### Overview
The Joux Protocol is a cryptographic protocol designed for secure tripartite key exchange using digital signatures. It enables three parties to establish a shared session key in a single round of communication, leveraging bilinear pairings and public key infrastructure. This protocol is particularly useful in scenarios where efficient key establishment is crucial.

#### Participants
The protocol involves three parties:
- **A**: The first participant
- **B**: The second participant
- **C**: The third participant

Each participant has a long-term secret key (ltk) and a corresponding public key (pk) that is registered in a public key infrastructure.

#### Key Operations
1. **Key Registration**:
   - Each participant registers their public keys in the system using their long-term secret keys. This is done through the `Register_pk` rule, where a participant's long-term key is mapped to their public key, and the public key is sent out for others to obtain.

2. **Key Reveal**:
   - If a participant needs to reveal their long-term key, they can do so using the `Reveal_ltk` rule, which allows the participant to output their long-term key upon request.

3. **Protocol Execution**:
   - The protocol consists of two main steps:
     - **Step 1 (Proto1)**: Participant A computes a hash key (`hkA`) using a pairing operation and their own long-term key. A then sends a message containing this hash key and a signature of the message, which includes the identities of all three participants.
     - **Step 2 (Proto2)**: Participants B and C receive messages from each other, which include their respective signatures. Upon receiving these signed messages and the necessary public keys, all three participants compute a session key using their long-term keys and the received signatures.

#### Security Properties
The protocol aims to ensure:
- **Session Key Establishment**:
  - The lemma `session_key_establish` verifies that all three participants can establish a common session key without revealing their long-term keys during the protocol execution.

- **Perfect Forward Secrecy (PFS)**:
  - The lemma `Session_Key_Secrecy_PFS` asserts that even if a participant’s long-term key is revealed at some point in the future, it does not compromise the secrecy of the session keys established prior to that revelation.

#### Conclusion
The Joux Protocol demonstrates an efficient method for three-party key exchange while maintaining crucial security properties such as perfect forward secrecy. This makes it suitable for applications requiring secure communications among multiple parties.

---
