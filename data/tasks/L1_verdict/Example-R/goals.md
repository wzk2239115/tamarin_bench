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
| 1 | `Client_session_key_secrecy` | all-traces | client session key secrecy |
| 2 | `Client_auth` | all-traces | client auth |
| 3 | `Client_auth_injective` | all-traces | client auth injective |
| 4 | `Client_session_key_honest_setup` | exists-trace | client session key honest setup |

## Protocol description (natural language)

---

### Protocol Description

**Title:** Secure Client-Server Communication Protocol

**Authors:** Simon Meier, Benedikt Schmidt, Jannik Dreier, Ralf Sasse

**Date:** June 2016

**Overview:**
This protocol outlines a secure communication framework between clients and servers utilizing long-term keys for encryption and authentication. The main goal is to ensure confidentiality and integrity of messages exchanged, while also ensuring that session keys established during communication sessions remain secret.

**Key Components:**
1. **Long-term Keys (Ltk):** Each participant (client and server) maintains a long-term key used for generating public/private key pairs. These keys are crucial for the initial key exchange and verification processes.

2. **Public Keys (Pk):** The protocol allows clients and servers to register their public keys, enabling the secure exchange of session keys through asymmetric encryption.

3. **Session Keys (k):** Temporary keys generated for a specific session, which are used to encrypt messages between the client and the server. These keys are established after the client retrieves the server's public key and encrypts the session key for secure transmission.

4. **Requests and Responses:** The protocol involves the client sending encrypted requests to the server, which responds with either an answer or a hash of the decrypted request.

**Protocol Flow:**
1. **Registration of Public Keys:** 
   - A participant can register their long-term key and derive their public key, which is made available for other participants.

2. **Public Key Retrieval:**
   - The client retrieves the public key of the server, which is necessary for encrypting the session key.

3. **Session Key Establishment:**
   - The client generates a session key and sends it to the server encrypted with the server's public key.
   - Upon receiving the encrypted session key, the server decrypts it and confirms the session setup.

4. **Handling Requests:**
   - The server listens for incoming requests. Once a request is received, it decrypts the request using its long-term key and responds with either the answer or a hash of the request.

**Security Properties:**
- **Client Session Key Secrecy:** The protocol guarantees that a session key cannot be known by an adversary unless they have performed a long-term key reveal on the server. This ensures the confidentiality of the session keys.
  
- **Client Authentication:** For every session key established, there exists a corresponding server response to the client's request, ensuring that the client is communicating with the intended server and that no other client can impersonate them.

- **Injective Authentication:** The protocol ensures that for each session key established by a client, there is a unique corresponding request, preventing session key reuse and ensuring that no two clients can generate the same session key for the same server request without revealing their long-term keys.

- **Honest Setup of Session Keys:** The protocol ensures that session keys can only be established when the long-term key of the server has not been revealed, thus maintaining the integrity of the key setup.

**Conclusion:**
The protocol effectively establishes a secure communication model between clients and servers, utilizing public key cryptography to ensure confidentiality and integrity of exchanges. The lemmas defined in this protocol serve to prove essential security properties, ensuring that the established sessions are secure against potential adversarial actions.

---
