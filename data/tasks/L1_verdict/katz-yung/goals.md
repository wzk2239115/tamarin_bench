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
| 1 | `HonestTrace` | exists-trace | honesttrace |
| 2 | `KeySecrecy` | all-traces | keysecrecy |
| 3 | `ServerLiveness` | all-traces | serverliveness |
| 4 | `ClientLiveness` | all-traces | clientliveness |
| 5 | `InjectiveAgreement` | all-traces | injectiveagreement |

## Protocol description (natural language)

---

### Protocol Description: Katz-Yung Key Exchange Protocol

**Overview:**
The Katz-Yung protocol is a secure key exchange protocol that allows a client (C) and a server (S) to establish a shared session key using public key cryptography and Diffie-Hellman key exchange. The protocol leverages long-term keys for authentication and ensures that the session key remains confidential, even in the presence of an adversary.

**Key Components:**
1. **Participants:**
   - Client (C)
   - Server (S)
   - Long-term keys (Ltk) for both the client and server.

2. **Public Key Infrastructure (PKI):**
   - Each participant has a long-term key (ltk) and a corresponding public key (pk).
   - The server's public key is used to verify signatures, and the client signs messages with its long-term key.

3. **Message Types:**
   - Nonces: Random values used to prevent replay attacks (e.g., `rC`, `rS`).
   - Diffie-Hellman values: `g^x` for the server and `g^y` for the client, where `g` is a generator of a cyclic group.

**Protocol Steps:**
1. **PKI Provisioning:**
   - The server registers its long-term key and public key, which can be revealed later for verification.

2. **Client Initialization:**
   - The client sends a request to the server along with its nonce.

3. **Server Response:**
   - The server responds with its Diffie-Hellman value, along with a signature that includes the Diffie-Hellman value and the nonces. This ensures that the response is authentic.

4. **Client Finishing:**
   - After receiving the server's message, the client computes the session key and responds back to the server with its own Diffie-Hellman value and a signature.

5. **Server Finishing:**
   - The server verifies the client's message and, upon successful verification, establishes the session key.

**Security Properties:**
- **Key Secrecy:** The shared session key cannot be derived by an attacker unless one of the long-term keys is compromised.
- **Client and Server Liveness:** If the client successfully establishes a session key, it must have received a response from the server, and vice versa.
- **Injective Agreement:** If multiple sessions are established, each session key is unique to the client-server pair.

**Restrictions:**
- Equality and inequality restrictions ensure that the protocol maintains integrity in its messages and states.

**Formal Lemmas:**
- **HonestTrace:** There exists a trace where both client and server complete their session without revealing long-term keys.
- **KeySecrecy:** If a session key is established, it is not known to the attacker unless long-term keys are revealed.
- **ServerLiveness and ClientLiveness:** Conditions under which the server and client must have received messages from each other to establish a session key.

---
