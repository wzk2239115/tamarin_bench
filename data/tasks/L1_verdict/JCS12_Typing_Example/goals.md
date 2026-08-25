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
| 1 | `typing_assertion` | all-traces | typing assertion |
| 2 | `Client_session_key_secrecy_raw` | all-traces | client session key secrecy raw |
| 3 | `Client_session_key_secrecy` | all-traces | client session key secrecy |
| 4 | `Client_auth` | all-traces | client auth |

## Protocol description (natural language)

---

### Protocol Description: Typing Assertion Example

#### Overview
This protocol is an instance of a cryptographic communication system that demonstrates the use of typing assertions as described in the paper "Efficient Construction of Machine-Checked Symbolic Protocol Security Proofs" by Simon Meier, Christian Cremers, and David Basin, presented at JCS'12. The protocol employs asymmetric encryption and hashing to facilitate secure communication between clients and a server.

#### Components
1. **Participants**:
   - **Client (C)**: Initiates requests to the server.
   - **Server (S)**: Responds to client requests and establishes session keys.

2. **Variables**:
   - `~ltk`: Long-term key of a participant.
   - `pk`: Public key corresponding to the long-term key.
   - `k`: Session key established between the client and server.

3. **Actions**:
   - `Out(m)`: Outputs message `m`.
   - `In(m)`: Inputs message `m`.
   - `LtkReveal(A)`: Adversary reveals the long-term key of participant `A`.
   - `Eq(x, y)`: Checks equality between `x` and `y`.

#### Protocol Steps
1. **Key Registration and Retrieval**:
   - A participant can register their long-term key and public key using the `Register_pk` rule.
   - Public keys can be retrieved using the `Get_pk` rule.
   - Long-term keys can be revealed using the `Reveal_ltk` rule.

2. **Client Communication**:
   - The client initiates a session using `Client_1`, sending an encrypted request to the server.
   - The client expects a response from the server.

3. **Server Response**:
   - The server processes the client's request in `Serv_1`, ensuring it matches expected tags to prevent message misinterpretation.
   - Upon successful validation, the server sends back a session key to the client.

#### Security Assertions
1. **Typing Assertion**:
   - Ensures that any message received by the server is either known to the adversary or originates from a legitimate source.

2. **Session Key Secrecy**:
   - Guarantees that if the adversary learns a session key established between a client and server, it must have revealed the long-term key of at least one of the parties involved before learning that key.

3. **Client Authentication**:
   - Verifies that all session key setups are either answered by the server or the adversary must have revealed a long-term key before the session key's establishment.

#### Implications
The protocol provides a structured approach to ensuring secure communication through the use of cryptographic methods and typing assertions, allowing for the verification of security properties through formal methods in the Tamarin tool.

---
