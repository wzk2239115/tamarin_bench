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

### Description of the Diffie-Hellman Protocol

The Diffie-Hellman protocol is a method for two parties to securely establish a shared secret over an insecure channel. The protocol uses asymmetric key cryptography to exchange public keys and then derives a symmetric key using those keys.

#### Functions:
1. **pk/1**: Represents a public key associated with an entity.
2. **sk/1**: Represents a private key associated with an entity.
3. **aenc/2**: Represents asymmetric encryption, taking a message and a public key as inputs.
4. **adec/2**: Represents asymmetric decryption, taking an encrypted message and a private key as inputs.

#### Built-in Functions:
- **diffie-hellman**: A built-in function that facilitates the Diffie-Hellman key exchange process.
- **symmetric-encryption**: A built-in function used for encrypting messages with a symmetric key.

#### Equations:
1. `adec(aenc(x.1, sk(x.2)), pk(x.2)) = x.1`: This equation states that decrypting a message encrypted with a private key using the corresponding public key returns the original message.
2. `adec(aenc(x.1, pk(x.2)), sk(x.2)) = x.1`: This equation states that decrypting a message encrypted with a public key using the corresponding private key returns the original message.

#### Rules:
1. **Asymmetric Key Setup**: Each participant generates a pair of keys (public and private) using a fresh random value.
2. **Publish Public Keys**: A participant sends their public key to the other party.
3. **Symmetric Key Setup**: A fresh symmetric key is generated for communication between the two parties.

#### Initial Knowledge:
Both parties have knowledge of their own and each other's public and private keys.

#### Role A:
- **Step 1 (dh_1_A)**: Participant A generates a random number `x` and sends `g^x` to participant B.
- **Step 2 (dh_2_A)**: Participant A receives `alpha` from participant B.
- **Step 3 (dh_3_A)**: Participant A generates a fresh random number `n` and sends the symmetric encryption of `(alpha^x)` using the symmetric key.

#### Role B:
- **Step 1 (dh_1_B)**: Participant B receives `alpha` from participant A.
- **Step 2 (dh_2_B)**: Participant B generates a random number `y` and sends `g^y` to participant A.
- **Step 3 (dh_3_B)**: Participant B decrypts the message received from A and establishes the symmetric key using `(alpha^y)`.

#### Security Lemmas:
1. **key_secret**: Asserts that no message can be the shared secret of both parties.
2. **key_secretA**: Asserts that no message can be the secret key known to A.
3. **key_secretB**: Asserts that no message can be the secret key known to B.

---
