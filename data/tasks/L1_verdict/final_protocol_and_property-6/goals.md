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
| 1 | `message_authentication` | all-traces | message authentication |

## Protocol description (natural language)

### Protocol Description

#### Title: Protocol3

#### Overview
This protocol facilitates secure communication between two parties, Alice (A) and Bob (B), using a combination of asymmetric and symmetric encryption techniques. The protocol incorporates a public key infrastructure (PKI) to manage public keys and ensure the authenticity and confidentiality of messages exchanged.

#### Components
1. **Built-in Cryptographic Functions**:
    - **Asymmetric Encryption**: Used for exchanging public keys and securely encrypting messages with the recipient's public key.
    - **Symmetric Encryption**: Used for encrypting messages with a shared secret key.

2. **Key Registration and Retrieval**:
    - **Register_pk**: This rule allows a user (e.g., Alice or Bob) to register their long-term key (ltk) in the system. The corresponding public key (pk) is generated and made available.
    - **Get_pk**: This rule enables a user to retrieve the public key of another user, which can be used for secure communication.

#### Protocol Steps
1. **Alice Sends an Encrypted Message**:
    - **Rule A_1**: Alice generates a fresh symmetric key and sends an encrypted message containing her identity and the plaintext message, encrypted with the symmetric key. The message is sent to Bob, and Alice transitions to `A_State_1`, storing her state information.

2. **Bob Receives and Acknowledges**:
    - **Rule B_1**: Upon receiving the encrypted message from Alice, Bob decrypts it using his long-term key (ltkB) to obtain the message. He responds with a nonce (`n`) to confirm receipt, updating his state to `B_State_1`.

3. **Alice Sends Encrypted Nonce**:
    - **Rule A_2**: After receiving the nonce from Bob, Alice sends an encrypted message containing the nonce and the symmetric key, encrypted with Bob's public key (pkB).

4. **Bob Authenticates the Nonce**:
    - **Rule B_2**: Bob receives the encrypted message containing the nonce and the symmetric key, verifies the authenticity of the nonce, and transitions to a state where he has successfully authenticated the message.

#### Security Property
- **Message Authentication**: The protocol includes a lemma that asserts the authenticity of messages exchanged between parties. It ensures that if a message is authenticated, there exists a point in time where that message was sent by the corresponding party.

### Conclusion
Protocol3 is designed to establish a secure communication channel between Alice and Bob by leveraging both asymmetric and symmetric encryption techniques along with a public key infrastructure. The protocol ensures that messages remain confidential and authentic, preventing unauthorized access and providing assurances of identity verification.

### Corresponding spthy Generation
The above descriptions can be directly translated into the `spthy` file format required by Tamarin, as demonstrated in the provided code snippet. The key steps, rules, and properties are already structured in the appropriate syntax for execution within the Tamarin Prover.
