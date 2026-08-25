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
| 1 | `key_secret` | all-traces | key secret |
| 2 | `key_secretA` | all-traces | key secreta |
| 3 | `key_secretB` | all-traces | key secretb |

## Protocol description (natural language)

---

## Description of the Signed Diffie-Hellman Protocol

### Overview
The Signed Diffie-Hellman protocol allows two parties, traditionally named Alice (A) and Bob (B), to securely establish a shared secret key over an insecure channel. The protocol utilizes asymmetric key pairs for each participant, where each has a public key and a corresponding private key.

### Key Components
1. **Functions**:
   - `pk/1`: Represents the public key of a participant.
   - `sk/1`: Represents the private key of a participant.
   - `aenc/2`: Represents asymmetric encryption of a message with a public key.
   - `adec/2`: Represents asymmetric decryption of a message with a private key.
   - `g/0`: A generator used in the Diffie-Hellman key exchange.

2. **Built-ins**:
   - `diffie-hellman`: Built-in support for the Diffie-Hellman key agreement.

### Equations
The protocol defines two equations for the encryption and decryption processes, ensuring that the decryption of an encrypted message returns the original message when the correct key is used.

- \( \text{adec}(\text{aenc}(x.1, \text{sk}(x.2)), \text{pk}(x.2)) = x.1 \)
- \( \text{adec}(\text{aenc}(x.1, \text{pk}(x.2)), \text{sk}(x.2)) = x.1 \)

### Protocol Steps
1. **Asymmetric Key Setup**:
   - Each participant generates a pair of keys (public and private). The public keys are published.

2. **Publish Public Keys**:
   - Participants publish their public keys to the network.

3. **Initialization of Knowledge**:
   - Both participants initialize their state with their own and the other participant's public and private keys.

4. **Role A (Alice)**:
   - **Step 1 (dh_1_A)**: Alice sends an encrypted message containing the string "One", her identity, Bob's identity, and a random value \( x \) to Bob.
   - **Step 2 (dh_2_A)**: Upon receiving Bob's response (an encrypted message containing "Two" and a value \( \alpha \)), Alice computes her secret key by combining \( \alpha \) and her random value \( x \).

5. **Role B (Bob)**:
   - **Step 1 (dh_1_B)**: Bob, upon initialization, waits for Alice's message.
   - **Step 2 (dh_2_B)**: Bob sends a response to Alice with an encrypted message containing "Two" and a random value \( y \). He computes his secret key by combining \( \alpha \) and his random value \( y \).

### Security Properties
The protocol includes lemmas that assert the secrecy of the generated keys:
- **Key Secrecy**: Ensures that no message can reveal the secret keys held by either party.
- **Key Secrecy for Alice**: Ensures that Alice's derived secret key is kept secret.
- **Key Secrecy for Bob**: Ensures that Bob's derived secret key is kept secret.

---
