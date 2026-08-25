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
| 1 | `JKL2008_2_initiator_key` | all-traces | jkl2008 2 initiator key |
| 2 | `JKL2008_2_responder_key` | all-traces | jkl2008 2 responder key |

## Protocol description (natural language)

---

### Protocol Description: JKL-TS2-2008

#### Overview
The JKL-TS2-2008 protocol is an authenticated key exchange protocol designed for two parties, as introduced by Jeong, Katz, and Lee in their 2008 paper titled "One-Round Protocols for Two-Party Authenticated Key Exchange." The protocol aims to facilitate secure communication between two parties, ensuring that both can derive a shared session key while maintaining privacy and integrity.

#### Key Features
- **One-Round Communication**: The protocol achieves authenticated key exchange in a single round of communication.
- **Long-Term Keys**: Each party possesses a long-term key, which is used to establish trust and derive session keys.
- **Ephemeral Keys**: The use of ephemeral keys enhances security by ensuring that session keys are not compromised even if long-term keys are revealed in the future.

#### Participants
- **Initiator (I)**: The party that begins the protocol.
- **Responder (R)**: The party that responds to the initiator’s request.

#### Protocol Steps
1. **Key Generation**: The initiator generates a long-term key (`lk`) and a corresponding public key (`Pk`) based on a generator `g`.
2. **Initiator Sends Message**: The initiator sends a message that includes a session identifier and the initiator's public information.
3. **Responder Receives and Responds**: The responder receives the message, generates their own ephemeral key, and sends back a response that includes their public information and a commitment to a shared session key.
4. **Session Key Generation**: Both parties compute the shared session key based on the exchanged messages and their respective long-term and ephemeral keys.

#### Security Properties
- **Key Agreement**: The protocol guarantees that both parties can compute the same session key without revealing it to any adversaries.
- **Resistance to Key Reveal Attacks**: The protocol is designed to prevent an attacker from obtaining session keys or long-term keys, even if they can intercept messages.
- **Weak Perfect Forward Secrecy (wPFS)**: The protocol achieves weak perfect forward secrecy, ensuring that the compromise of long-term keys does not compromise past session keys.

#### Attacks and Safety Lemmas
1. **Key Reveal for Initiator**: The protocol ensures that if an attacker can deduce the session key from the initiator's session, certain conditions must hold, such as the absence of key reveals.
2. **Key Reveal for Responder**: Similar conditions apply for the responder's session, ensuring that any session key reveal must follow strict rules to maintain security.

---

### Corresponding `spthy` File

You can generate the corresponding `spthy` file based on the description provided above. Ensure that the structure follows the existing `spthy` file format, maintaining the outlined protocol rules, security properties, and necessary lemmas to validate the protocol's security.
