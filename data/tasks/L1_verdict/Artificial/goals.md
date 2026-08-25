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
| 1 | `Characterize_Fin` | exists-trace | characterize fin |
| 2 | `Fin_unique` | all-traces | fin unique |
| 3 | `Keys_must_be_revealed` | all-traces | keys must be revealed |

## Protocol description (natural language)

---

## Protocol Description: Example Protocol P_{Ex2}

### Overview

The Example Protocol P_{Ex2} is an artificial cryptographic protocol introduced in Simon Meier's PhD thesis and further discussed in the CSF'12 paper. The protocol demonstrates the use of symmetric encryption for secure communication between agents. The primary focus of this protocol is to illustrate the use of constraint solving and characterization in formal verification.

### Participants

The protocol involves two main participants:
- **Agent x**: The initiator of the protocol who generates a session key.
- **Agent S**: The responder who receives the session key and acknowledges the conclusion of the session.

### Key Operations

The protocol consists of two main steps and includes operations for key generation, message sending, and key revealing:

1. **Step 1**: Key Generation and Sending
   - Agent x creates a fresh session key `k` and sends a message encrypted with this key to another agent `S`. The message includes the session identifier `St(x, k)` and the symmetric encryption of the key `senc(x, k)`.
   - The key `k` is stored for future reference, allowing x to reveal it later if necessary.

2. **Step 2**: Finishing the Session
   - Agent S, upon receiving the message, sends a finishing signal `Fin(x, k)` back to agent x. This indicates that the session has concluded successfully and that S has accepted the communication.

3. **Reveal Key**: Key Revelation
   - At any point, an agent can reveal the session key `k` using the operation `Rev(k)`. This allows for the auditing and validation of the session key.

### Lemmas

The protocol includes several important lemmas that ensure the security and correctness of the protocol:

1. **Characterize_Fin**: 
   - This lemma states that there exists a trace where the finishing operation `Fin(S, k)` occurs. It is essential for characterizing the possible execution traces of the protocol.

2. **Fin_unique**:
   - This lemma ensures that for any session `S` and key `k`, the finishing operation `Fin(S, k)` can only occur at one specific point in time. It prevents multiple acknowledgments for the same session, thus ensuring consistency.

3. **Keys_must_be_revealed**:
   - The final lemma asserts that if a finishing signal `Fin(S, k)` has been received, then the session key `k` must have been revealed at some point before the finishing signal. This encapsulates the idea that keys used in the session are not hidden indefinitely and must be disclosed for transparency.

### Conclusion

The Example Protocol P_{Ex2} serves as a foundational illustration of cryptographic protocol analysis using the Tamarin prover. Its construction and the associated lemmas provide a clear framework for understanding session key management and the importance of traceability in secure communications. The lemmas help to assert properties that are crucial for ensuring the reliability and security of the protocol.

---
