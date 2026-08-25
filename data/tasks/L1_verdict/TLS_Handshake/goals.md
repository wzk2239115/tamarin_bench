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
| 1 | `session_key_secrecy` | all-traces | session key secrecy |
| 2 | `injective_agree` | all-traces | injective agree |
| 3 | `session_key_setup_possible` | exists-trace | session key setup possible |

## Protocol description (natural language)

---

## TLS Handshake Protocol Description

### Overview
The TLS Handshake protocol is a cryptographic protocol that enables secure communication between a client and a server. The handshake process establishes the session keys used for encryption and ensures mutual authentication. This description outlines the critical components, message exchanges, and security properties modeled in Tamarin.

### Components
1. **Participants**: 
   - Client (C)
   - Server (S)

2. **Key Material**:
   - Long-term keys: `ltkA` (long-term key for A), `ltkC` (long-term key for Client), `ltkS` (long-term key for Server).
   - Public keys: `pk(A)` for each participant.
   - Session parameters: Nonces `nc` and `ns`, session identifiers `sid`, and pre-master secret `pms`.

### Protocol Steps
1. **Client Hello**: 
   - The client initiates the handshake by sending its identity, a nonce, a session identifier, and a public certificate to the server.
   - Message format: `C -> S: <C, nc, sid, pc>`

2. **Server Hello**: 
   - The server responds with its identity, a nonce, a session identifier, and its public certificate.
   - Message format: `C <- S: <ns, sid, ps>`

3. **Client Key Exchange and Finished**:
   - The client sends its pre-master secret encrypted with the server's public key, a signed message containing the nonce and session information, and a session message encrypted with the derived client key.
   - Message format: 
     ```plaintext
     C -> S:
     { '31', pms }pk(S),
     sign{ '32', h('32', ns, S, pms) }pk(C),
     { '33', sid, PRF(pms, nc, ns), nc, pc, C, ns, ps, S }
     h('clientKey', nc, ns, PRF(pms, nc, ns))
     ```

4. **Server Finished**:
   - The server sends a message containing session information encrypted with the derived server key.
   - Message format: 
     ```plaintext
     C <- S:
     { '4', sid, PRF(pms, nc, ns), nc, pc, C, ns, ps, S }
     h('serverKey', nc, ns, PRF(pms, nc, ns))
     ```

### Security Properties
1. **Session Key Secrecy**: Ensures that the session keys established between the client and server are not compromised by an adversary who has not revealed long-term keys.
   
2. **Injective Agreement**: Guarantees that if a participant commits to a session with specific parameters, another participant must also be running a session with the same parameters, or an adversary must have revealed a long-term key.

3. **Session Key Setup**: Demonstrates that it is possible to establish session keys between honest participants without revealing long-term keys.

### Conclusion
The TLS Handshake protocol is modeled in Tamarin to verify its security properties and correctness. The model captures both the message flows and the requisite encryption mechanisms, ensuring that the protocol provides strong security guarantees against potential adversaries. 

---
