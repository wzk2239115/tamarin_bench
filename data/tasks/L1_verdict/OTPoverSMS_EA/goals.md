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

**Theory: OTP over SMS**

**Introduction:**
- **Protocol:** OTP over SMS
- **Modeler:** Lara Schmid
- **Date:** March 2020
- **Source:** "Advancing the Formal Foundations for Voting Protocols", Lara Schmid, PhD Thesis, ETH Zürich.

**Summary:**
The OTP over SMS protocol is designed for secure communication using one-time passwords (OTPs) sent via SMS. The protocol involves a human agent (H) and two devices, a server (S) and a device (D), that work together to authenticate the human and ensure the integrity of the messages being exchanged.

**Roles:**
- **Human Agent (H):** The user interacting with the protocol.
- **Device (D):** The device used by the human agent to receive OTPs.
- **Server (S):** The server that sends the OTPs to the device of the human agent.

**Setup:**
The protocol begins with the setup phase where the human agent initializes their identity and establishes keys with the devices involved in the communication. The human agent, server, and device perform various roles, ensuring secure key exchanges and the integrity of the transmitted messages.

**Communication Rules:**
- **Sending OTPs:** The server generates a one-time password and sends it securely to the device of the human agent.
- **Receiving OTPs:** The human agent receives the OTP and sends it back to the server to complete the authentication process.
- **Secure Channels:** Communications between the server and device are secure, while human communication may occur over insecure channels.

**Security Properties:**
- **Entity Authentication:** The protocol ensures that the human agent is authenticated through the successful exchange of OTPs.
- **Device Authentication:** The protocol verifies that the device being used is indeed the correct device associated with the human agent.

**Results:**
The protocol's security properties are verified through several lemmas:
- **Functionality Lemma:** Verifies that the setup phase is unique for each agent.
- **Entity Authentication Lemma:** Ensures that the human agent can successfully authenticate themselves to the server.
- **Device Authentication Lemma:** Confirms that the server can accurately authenticate the device being used by the human agent.

**Human Agent Behavior:**
- The human agent's behavior is modeled under different assumptions (infallible vs. fallible), affecting how they can send and receive messages, and how the protocol handles insecure communication.

**Assumptions:**
- No secure channels exist between human agents.
- Distinct roles are not executed by the same agent.
- No two human agents share a single device.

---
