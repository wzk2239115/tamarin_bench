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
| 2 | `entity_authentication` | all-traces | entity authentication |
| 3 | `device_authentication` | all-traces | device authentication |

## Protocol description (natural language)

---

### Google 2-step Authentication Protocol Description

#### Introduction
The Google 2-step authentication protocol enhances security by requiring two forms of verification: a password and a one-time code. This protocol was modeled by Lara Schmid in March 2020 as part of her PhD thesis at ETH Zürich, titled "Advancing the Formal Foundations for Voting Protocols."

#### Protocol Overview
1. **Participants**:
   - **Human User (H)**: The individual attempting to authenticate.
   - **Device (D)**: The device that the user is authenticating from.
   - **Service (S)**: The service requiring authentication.

2. **Process**:
   - The user first sets up their account by providing a password, which is securely distributed to the system.
   - During authentication, the user inputs their password and receives a one-time code sent to their device.
   - The user sends the password and the received code to the service for verification.
   - The service validates the code and password to authenticate the user.

#### Security Considerations
- **Human Agents**: The protocol accounts for both infallible (trained) and fallible (untrained) human agents, incorporating rules that define their actions in secure and insecure channel communications.
- **Channel Security**: The protocol distinguishes between secure and insecure channels, ensuring that sensitive information is transmitted securely when required, while acknowledging that human communication can occur over insecure channels.

#### Results
- The verification of the protocol under different assumptions shows that it meets its security objectives:
  - **Functional Correctness**: Verified with 7 steps for infallible humans, 7 steps for fallible humans.
  - **Entity Authentication**: Verified for all traces within 5 steps for untrained humans, and 7 steps for trained humans.
  - **Device Authentication**: Same as entity authentication.

#### Assumptions
- Each human agent initiates in a unique state.
- No secure channels exist between humans, ensuring that they communicate via insecure channels.
- Distinct roles are not shared between agents, and no two humans share a device.

#### Lemmas
- **Functional Lemma**: Establishes that the setup for each human is unique.
- **Entity Authentication Lemma**: Ensures that a successful authentication process can only occur after the correct sequence of steps.
- **Device Authentication Lemma**: Validates that the device used for authentication is uniquely tied to the human agent.

---
