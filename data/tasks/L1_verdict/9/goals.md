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
| 1 | `secrecy` | all-traces | secrecy |

## Protocol description (natural language)

### Description of the Protocol

#### Purpose
The protocol is designed for secure communication among three parties: Alice (A), Bob (B), and a trusted server (S). It allows Alice and Bob to exchange messages securely using both symmetric and asymmetric encryption techniques.

#### Components
1. **Keys**:
   - Each participant has a pair of asymmetric keys: a public key (pk) and a private key (sk).
   - A symmetric key (symK) is established for direct communication between Alice and Bob after initial setup.

2. **Functions**:
   - `pk/1`: Represents the public key of an entity.
   - `sk/1`: Represents the secret (private) key of an entity.
   - `aenc/2`: Represents asymmetric encryption of a message with a public key.
   - `adec/2`: Represents asymmetric decryption of a message with a private key.

3. **Built-in Functions**:
   - The protocol utilizes symmetric encryption for the confidentiality of messages.

#### Sequence of Actions
1. **Key Setup**:
   - Asymmetric keys are generated for Alice, Bob, and the server.
   - Public keys are published so that all parties can access them.

2. **Initial Knowledge**:
   - Each party initializes their state with their own keys and the keys of the other parties.

3. **Message Exchange**:
   - **Alice to Server (msg1_A)**: Alice sends an encrypted message containing her identity and public key to the server.
   - **Server to Alice (msg1_S)**: The server receives Alice's message and updates its state.
   - **Server to Bob (msg2_S)**: The server forwards a message to Bob that includes Alice's identity and a newly generated symmetric key.
   - **Bob to Server (msg2_B)**: Bob generates a symmetric key and sends it to the server in an encrypted form.
   - **Server to Bob (msg3_S)**: The server sends back the encrypted symmetric key to Bob.
   - **Bob to Alice (msg4_B)**: Bob sends a message back to Alice that is encrypted with Alice’s public key, which includes a secret message.

4. **Security Properties**:
   - The protocol ensures secrecy, meaning that if a secret is established, it cannot be revealed by any party without the appropriate keys.

#### Conclusion
The described protocol establishes a secure communication channel between Alice and Bob with the help of a trusted server, utilizing both asymmetric and symmetric encryption methods. The various states and message exchanges ensure that the participants can securely share information without exposing their private keys or the contents of their communications.

### Corresponding Tamarin spthy File Structure
Based on the above description, the spthy file structure provided initially is appropriate and correctly defines the roles, rules, and actions that implement the described protocol.
