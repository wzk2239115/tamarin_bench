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
| 1 | `HonestServerTrace` | exists-trace | honestservertrace |
| 2 | `HonestTrace` | exists-trace | honesttrace |
| 3 | `KeySecrecy` | all-traces | keysecrecy |
| 4 | `ServerLiveness` | all-traces | serverliveness |
| 5 | `ClientLiveness` | all-traces | clientliveness |
| 6 | `InjectiveAgreement` | all-traces | injectiveagreement |

## Protocol description (natural language)

### Protocol Description

**Name**: MLS04 (Multi-Level Security Protocol 04)

**Overview**: The MLS04 protocol is designed for secure communication between a client (C) and a server (S). It utilizes asymmetric encryption, hashing, and digital signatures to establish a secure session key that remains confidential unless the long-term keys of either party are compromised.

#### Key Components:

1. **Built-in Functions**:
   - **Hashing**: Used for generating message authentication codes (MACs).
   - **Signing**: Provides authenticity and integrity of the messages exchanged.
   - **Asymmetric Encryption**: Enables secure key exchanges and ensures confidentiality.

2. **Functions**:
   - **mac/2**: A function to compute message authentication codes.

3. **Public Key Infrastructure (PKI)**:
   - **RegisterPK Rule**: Allows an entity to register its long-term key (LTK) and public key (PK) and outputs the public key for communication.
   - **RevealLTK Rule**: Enables the revelation of a long-term key when requested, ensuring confidentiality.

#### Client Logic:

1. **Client Initialization**:
   - The client generates a public key (`gx`) and signs it along with its identity and public key. This signed message (`uik`) is sent to the server.

2. **Client Finish**:
   - The client receives a welcome message from the server containing a session key and other information. It verifies the received add request and checks the integrity of the data using MAC. If all checks pass, the client completes the session.

#### Server Logic:

1. **Server Initialization**:
   - The server receives the client's initialization message, verifies the signature, and prepares a welcome message which includes a session key (`k`) and additional information. The server also computes a MAC for the add request before sending it back to the client.

#### Security Properties:

1. **Restrictions**:
   - **Equality**: Ensures that if two values are equal at any point, they are indeed the same.
   - **Inequality**: Ensures that if two values are deemed not equal, they are genuinely different.

2. **Liveness and Secrecy Lemmas**:
   - **HonestServerTrace**: Asserts that if the server successfully completes its operation, it does so without revealing any long-term keys.
   - **HonestTrace**: Guarantees that both the client and server can successfully complete their operations without revealing any long-term keys.
   - **KeySecrecy**: Ensures that the established session key remains secret unless one of the long-term keys is compromised.
   - **ServerLiveness**: States that if a client successfully completes the session, the server must have responded correctly, or a long-term key has been revealed.
   - **ClientLiveness**: Ensures that if the server has established a session key, it must be based on a valid client initialization.
   - **InjectiveAgreement**: Guarantees that each session key is uniquely tied to a specific client-server interaction.

### Conclusion

The MLS04 protocol provides a robust framework for secure communication between clients and servers, addressing key establishment, message integrity, and confidentiality through a combination of cryptographic techniques. The protocol's design ensures that session keys are kept secret and that the parties involved maintain a secure interaction, even in the presence of potential attackers.
