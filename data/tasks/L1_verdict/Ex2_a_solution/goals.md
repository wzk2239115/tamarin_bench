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
| 1 | `ClientWellfounded` | all-traces | clientwellfounded |
| 2 | `Secrecy` | all-traces | secrecy |

## Protocol description (natural language)

Certainly! Below is the description content for the protocol represented in the provided Tamarin `spthy` file. This description can serve as a foundation for generating the corresponding `spthy` file.

---

### Description of the Authentication Protocol

#### Overview
The protocol is designed for secure communication between a client and a server using asymmetric and symmetric encryption. It involves the initialization of keys, the exchange of nonces, and the establishment of a secure session for message transmission.

#### Key Functions
- **h/1**: A hash function used to derive the session key from nonces.
  
#### Built-in Functions
- **symmetric-encryption**: Represents symmetric encryption operations.
- **asymmetric-encryption**: Represents asymmetric encryption operations.

#### Initialization
1. **Server Key Initialization**:
   - The server generates its secret key `skS` and derives its public key `pk(SK)`.
   - The public key `pk(~skS)` is sent to the client.

2. **Client Key Initialization**:
   - The client generates its secret key `skA` and derives its public key `pk(A)`.
   - The public key `pk(~skA)` is sent to the server.

#### Communication Phases

1. **Client Sends Initialization Message**:
   - The client generates a nonce `nonce1` and a unique identifier `cid`.
   - The client sends an encrypted message containing `nonce1` to the server using the server's public key.

2. **Server Receives Initialization Message**:
   - The server receives the encrypted message containing `nonce1` and decrypts it.
   - The server generates another nonce `nonce2` and derives a session key using the hash function `h` with `nonce1` and `nonce2`.
   - The server sends back an encrypted message containing both `nonce1` and `nonce2` to the client.

3. **Client Receives Nonce and Starts Session**:
   - The client receives the encrypted message, decrypts it, and derives the session key using `h`.
   - The client transitions to a session state with the established session key.

4. **Client Sends Payload**:
   - The client, while in the session state, can send encrypted messages (payload) to the server using the session key.

5. **Server Receives Payload**:
   - The server receives the encrypted message and processes it while maintaining the session state.

6. **Client Ends Session**:
   - When the client is done, it sends an end message to the server, indicating the termination of the session.

#### Restrictions
- **One Server Key**: Ensures that there is only one server key generated during the initialization phase.
- **One Client Key**: Ensures that there is only one client key generated during the initialization phase.

#### Lemmas
- **Client Well-foundedness**: Guarantees that if the client sends a payload, there exists a corresponding session start event.
- **Secrecy**: Ensures that once the client ends the session, the session key is not revealed or known to any external observer.

---

This description outlines the structure, flow, and security properties of the protocol, and you can use it to generate a corresponding Tamarin `spthy` file for analysis and verification.
