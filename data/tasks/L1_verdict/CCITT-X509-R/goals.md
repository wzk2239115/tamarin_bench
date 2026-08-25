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
| 1 | `Secrecy` | all-traces | secrecy |
| 2 | `injectiveagreement_B` | all-traces | injectiveagreement b |
| 3 | `agreement_B` | all-traces | agreement b |
| 4 | `Session_key_honest_setup` | exists-trace | session key honest setup |

## Protocol description (natural language)

---

### CCITT X.509 Protocol Description

**Authors:** Jannik Dreier  
**Date:** April 2020  
**Link:** [Tamarin Prover Example](https://github.com/tamarin-prover/tamarin-prover/blob/bb1a083f6092f5827c8bea6980caf5927578b9df/examples/features/auto-sources/spore/CCITT_X509_1.spthy#L12)

#### Overview
The CCITT X.509 protocol is designed for secure communication between two principals, A and B. It utilizes asymmetric encryption and signing to ensure the confidentiality and authenticity of the transmitted data. The following elements play critical roles in the protocol:

- **Principals:** A, B
- **Nonces:** Na, Nb (used to prevent replay attacks)
- **Timestamps:** Ta, Tb (to ensure freshness of messages)
- **User Data:** Ya, Yb (the actual data sent)
- **Additional User Data:** Xa, Xb
- **Keys:** PK, SK (public and secret key pairs for each principal)

#### Protocol Steps
1. **Message Sending:** A sends a message to B containing the following components:
   - Its identity A
   - Timestamp Ta
   - Nonce Na
   - The identity of the recipient B
   - User data Xa
   - Encrypted user data Ya using the public key of B, denoted as {Ya}PK(B)
   - A signature over the entire message for authenticity, which includes a hash of the message and is generated using the secret key SK(A)

   The formal representation of this step is:
   ```
   A -> B : A, Ta, Na, B, Xa, {Ya}PK(B), {h(Ta, Na, B, Xa, {Ya}PK(B))}SK(A)
   ```

   Here, h is a one-way hash function.

#### Security Properties
The protocol aims to achieve the following security goals:
- **Confidentiality of Ya:** An attacker should not be able to obtain the sensitive user data Ya if both A and B adhere to the protocol.
- **Authenticity of Data:** B must be assured that the data Xa and Ya indeed originated from A.

#### Failure Scenarios
The protocol also addresses scenarios where authenticity might fail:
- If an intruder I intercepts the message from A to B, it could potentially send a forged message to B, which is represented as:
  ```
  A -> I(B) : A, {Ta, Na, B, Xa, {Ya}PK(B)}SK(A)
  I -> B : I, {Ta, Na, B, Xa, {Ya}PK(B)}SK(I)
  ```

### Key Components of the Tamarin Model
The Tamarin model captures the protocol's logic with the following key components:
- **Rules for Registering Public Keys and Retrieving Them:** This ensures that public keys can be registered and later retrieved for verification.
- **Rules for Sending and Receiving Messages:** These encapsulate the communication between A and B, including the steps for message creation, sending, and reception.
- **Lemmas for Security Properties:** The model includes lemmas to verify the secrecy of the transmitted data, the authenticity of the messages, and the possibility of honest execution.

---

### Tamarin File Structure
With this description, the Tamarin `.spthy` file can be structured to define the necessary rules, lemmas, and functions as already outlined in the provided example. The model would include rules for sending and receiving messages, as well as checks for security properties to ensure the protocol adheres to its design goals.
