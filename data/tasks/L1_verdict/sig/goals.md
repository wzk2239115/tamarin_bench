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
| 2 | `signature_sent_by_agent` | all-traces | signature sent by agent |

## Protocol description (natural language)

---

### Description of the Protocol

**Overview:**

This protocol is designed to facilitate secure communication between agents using digital signatures. The primary goal is to ensure that messages sent between agents can be verified for authenticity, ensuring that they were indeed sent by the claimed sender.

**Entities:**

- **Agents ($A$)**: The participants in the protocol who wish to communicate securely.
- **Long-term Key (ltk)**: A secret key associated with an agent, used for signing messages.
- **Public Key (pk)**: The public counterpart of the long-term key, which is shared with other agents to verify signatures.

**Protocol Steps:**

1. **Key Generation:**
   - The protocol begins with a Public Key Infrastructure (PKI) mechanism where each agent generates a long-term key (`ltk`) and derives its public key (`pk`). This public key is then made available for other agents to use for verifying signatures later.
   - The rule `LtkGen` captures this key generation process, where a fresh long-term key is created, and both the long-term and public keys are registered in the system.

2. **Sending Signatures:**
   - When an agent wants to send a message, it generates a nonce (`n`) and signs it using its long-term key (`ltkA`). This signature is included with the message to ensure its authenticity.
   - The `Send_Signature` rule describes this operation, where the agent sends the message `<n, sign{n}ltkA>` to the recipient.

3. **Receiving Signatures:**
   - Upon receiving a message, the recipient agent checks the signature against the nonce and the sender's public key. If the verification is successful, the agent can be assured that the message came from the claimed sender and has not been altered.
   - The `Recv_Signature` rule encapsulates this process, where the recipient verifies the signature using the received message and the public key.

**Security Properties:**

The protocol is designed to uphold the following security properties:

- **Signature Verification**: The restriction `equal` ensures that the verification process for signatures is sound, stating that if two values are considered equal in the process, they must indeed be equal in the underlying semantics.
  
- **Executable Lemma**: The `executable` lemma guarantees that there exists a trace where an agent sends a message and later receives it, indicating that the protocol can be effectively executed.

- **Signature Transmission Property**: The `signature_sent_by_agent` lemma states that if an agent successfully receives a message, there must have been a prior instance where that agent sent a corresponding message. This property ensures that the flow of messages is coherent and traceable.

---
