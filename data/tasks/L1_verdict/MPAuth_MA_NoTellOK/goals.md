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
| 1 | `functional` | exists-trace | functional |

## Protocol description (natural language)

---

## Protocol Description: MP-Auth_MA

### Introduction
- **Protocol Name**: MP-Auth_MA
- **Modeler**: Lara Schmid
- **Date**: March 2020
- **Source**: "Advancing the Formal Foundations for Voting Protocols", Lara Schmid, PhD Thesis, ETH Zürich.

### Overview
The MP-Auth_MA protocol is designed to facilitate secure communication among multiple agents (humans and devices) while ensuring that sensitive information is not disclosed. The protocol incorporates mechanisms for fresh key generation, secure message sending, and reception, along with rules that define agent roles and interactions.

### Key Components
1. **Built-in Functions**:
   - **Signing**: For creating digital signatures.
   - **Asymmetric Encryption**: For secure key exchange and message confidentiality.
   - **Hashing**: For integrity checking.
   - **Symmetric Encryption**: For secure message transmission.

2. **Functions**:
   - `f/1`: A function used for processing protocol messages.
   - `m/1`: A function used to assign types to messages.

### Agents and Roles
- **Agents**: Include humans and devices.
- **Roles**:
  - Each agent can assume different roles such as Human, Device (D), Server (S), etc.
  - There are restrictions that prevent multiple roles from being executed by the same agent.

### Communication Mechanism
- The protocol utilizes both insecure and secure channels for communication:
  - **Insecure Channels**: For non-sensitive data transfer.
  - **Secure Channels**: For sensitive data transfer, ensuring confidentiality and integrity.

### Rules
- **Human Agent Rules**: Define how humans send and receive messages, manage keys, and interact with devices.
- **Device Agent Rules**: Specify how devices process messages and communicate with humans.
- **Channel Rules**: Outline how messages are sent and received over secure and insecure channels.

### Setup
- The protocol includes a setup phase where passwords, keys, and initial states are established for all agents involved.

### Axioms and Assumptions
- Assumptions include:
  - No secure channels exist between humans.
  - Each human starts in an initial setup state.
  - Distinct roles cannot be executed by the same agent.
  - Two humans cannot share a single device.

### Results
- When running the protocol under specific conditions, no traces were found indicating a functional flaw in the protocol, suggesting that the protocol maintains its integrity as designed.

### Lemmas
The protocol includes a lemma that states that if two humans set up their initial states, they must be distinct, ensuring that the protocol does not allow for ambiguity in agent identity.

---

### Corresponding `spthy` File Generation
To generate the corresponding `spthy` file, the above information should be transformed into Tamarin's syntax and structured according to its requirements. The existing file already provides a strong foundation, so the main task would be ensuring that the descriptions provided match the rules and axioms in the Tamarin model, ensuring consistency throughout.
