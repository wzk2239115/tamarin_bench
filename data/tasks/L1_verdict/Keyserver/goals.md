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
| 1 | `Knows_Honest_Key_imp_Revoked` | all-traces | knows honest key imp revoked |

## Protocol description (natural language)

---

## Keyserver Protocol Description

### Overview
The Keyserver protocol is designed for secure key management and renewal in a client-server architecture. The protocol allows clients to register public keys with the server, request renewal of keys, and ensures that private keys are managed securely, preventing unauthorized access or leaks.

### Modeler and Date
- **Modeler:** Simon Meier
- **Date:** June 2012

### Problem Statement
The protocol addresses the security of public key registrations and renewals, ensuring that keys remain valid and protected against unauthorized access.

### Types
- **Agents:** {a, b, c, i, s} - Represents different entities in the protocol (clients, server, intruders).
- **User Set (U):** {a, b, c} - Clients that interact with the server.
- **Server Set (S):** {s} - The keyserver that manages keys.
- **Honest Set (H):** {a, b} - Honest agents who follow the protocol.
- **Dishonest Set (D):** {c, i} - Agents that may attempt to act maliciously.
- **Dynamic Users (DU):** {c} - Users that may not have a legitimate key.
- **Status (Sts):** {valid, revoked} - Indicates the state of keys.
- **Public Key (PK), New Public Key (NPK):** Values representing keys.
- **Messages (M1, M2):** Untyped messages used in the protocol.

### Sets
- **Ring (U):** Represents the set of users.
- **Database (db):** A database containing keys and their statuses for the server.

### Functions
- **Public Functions:** `sign/2`, `pair/2` - For signing messages and creating pairs of messages.
- **Private Function:** `inv/1` - Represents the inversion of a key.

### Facts
- **iknows/1:** Indicates knowledge of a certain piece of information.
- **attack/0:** Represents an attack scenario.

### Rules
1. **Knowledge Initialization:** Each agent knows itself.
2. **Signing Knowledge:** If an agent knows a signed message, it knows the message itself.
3. **Pairing Knowledge:** If an agent knows a pair of messages, it knows both messages.
4. **Key Registration:** Agents can register keys with the server.
5. **Key Renewal (Honest):** Honest clients can renew their keys through a request and the server acknowledges this.
6. **Key Renewal (Dishonest):** Dishonest clients can attempt to register any key, potentially leading to security issues.
7. **Server Key Setup:** The server can generate a key pair for signing.
8. **Client Key Leak:** If a client requests a renewal and the server confirms it, the client's private key may be leaked.
9. **Database Update:** The server updates its database with the new keys and marks old keys as revoked.

### Security Properties
- **Revocation Knowledge:** If an honest agent knows the inverse of a public key that is valid, it indicates a potential attack scenario.
- **Revocation Tracking:** The protocol ensures that any renewal request leads to the revocation of the old key, allowing for secure key management.

### Lemmas
1. **Knows_Honest_Key_imp_Revoked:** If an honest key is known, it must eventually be revoked.
2. **Honest_Revoked_Known_Reachable:** Existence of a trace indicating that honest keys are eventually revoked.

---

This description outlines the key features and operational aspects of the keyserver protocol. It serves as a guideline for implementing the corresponding spthy file to be executed in Tamarin for formal verification and analysis.
