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
| 1 | `KI_Perfect_Forward_Secrecy_I` | all-traces | ki perfect forward secrecy i |
| 2 | `KI_Perfect_Forward_Secrecy_R` | all-traces | ki perfect forward secrecy r |

## Protocol description (natural language)

---

### Protocol Description: Station-To-Station Protocol (MAC Version)

**Overview:**
The Station-To-Station (STS) protocol is designed for secure authentication and key exchange between two parties (denoted as $I$ and $R$). This specific implementation includes a Message Authentication Code (MAC) variant that addresses vulnerabilities associated with Unknown Key-Share (UKS) attacks by incorporating proof-of-possession checks of the private key exponents.

**Key Features:**
- **Public Key Infrastructure:** The protocol uses public keys where the `!Pk` facts can be interpreted as certificates for the corresponding long-term keys.
- **Proof-of-Possession Check:** The protocol ensures that a party can only register a public key if it can demonstrate knowledge of the associated private key (exponent).
- **Session Keys:** The protocol establishes session keys derived from shared secrets, ensuring forward secrecy.

**Roles:**
- **Initiator ($I$):** The party that starts the protocol by sending an initial message containing its public key.
- **Responder ($R$):** The party that responds to the initiator's initial message and completes the handshake.

**Protocol Steps:**
1. **Key Registration:**
   - **Normal Registration:** A legitimate party can register its public key using its long-term key (`ltk`).
   - **Evil Registration:** A corrupted party can register a key if it can provide the long-term key of the entity it impersonates.

2. **Initiation Phase:**
   - The initiator generates its ephemeral public key (`epkI`) and sends an initialization message containing its identity, the responder’s identity, and the ephemeral key.

3. **Response Phase:**
   - The responder, upon receiving the initialization message, generates its ephemeral public key (`epkR`), signs relevant information, and sends it back to the initiator along with a MAC for integrity.

4. **Finalization Phase:**
   - The initiator verifies the responder's message, signs its own response, and sends it back, confirming the establishment of the session key based on the derived key material.

**Security Guarantees:**
- **Perfect Forward Secrecy:** The protocol guarantees that even if long-term keys are compromised in the future, past session keys remain secure and cannot be derived by an attacker who has gained access to those long-term keys.
- **Integrity and Authenticity:** The use of signatures and MACs ensures that messages are authenticated and have not been tampered with during transmission.

**Implementation Details:**
- The protocol leverages Diffie-Hellman key exchange and digital signatures to establish secure communication channels.
- The key derivation function (KDF) is used to generate session keys from shared secrets.

---
