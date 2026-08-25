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
| 1 | `type_assertion` | all-traces | type assertion |
| 2 | `Responder_secrecy` | all-traces | responder secrecy |
| 3 | `Public_part_public` | exists-trace | public part public |

## Protocol description (natural language)

---

**Protocol Description: Interaction between Sources and Destructors**

**Protocol Name:** Demonstration of the interaction between sources and destructors  
**Modeler:** Simon Meier  
**Date:** July 2012  
**Status:** Working / Misses theory extension (see issue #104)  

**Overview:**  
This protocol serves as a demonstration of the interaction between sources and destructors in a cryptographic context. It is a variant of the 'Minimal_Typing_Example' and employs explicit destructors rather than relying on pattern matching. The verification of this protocol is not straightforward due to the restrictive nature of the current implementation of guarded trace properties, which complicates the formalization of the required type invariant.

**Key Features:**
- The protocol utilizes symmetric encryption and hashing as built-in primitives.
- The protocol includes rules for setting up keys, revealing keys, and the interactions between an initiator and a responder.
- Explicit destructors are used to allow more permissive rule firing, even in cases where failure terms may be involved.

**Protocol Rules:**
1. **Setup Key:** The protocol begins with a setup rule that introduces a fresh key `k`, marking it as a valid key within the system.
2. **Reveal Key:** There is a rule that allows for the revelation of the key `k`, which can be compromised by an adversary.
3. **Initiator Rule:** The initiator constructs a message using symmetric encryption, which includes a secret and a public value. This message can be sent out into the environment.
4. **Responder Rule:** The responder receives the message, decodes it using the associated key, and checks the validity of the public component, ensuring that it is not a failure term. If the checks are successful, the responder outputs the public value.

**Restrictions and Assertions:**
- A restriction (`No_failure_terms`) is suggested to filter out traces that contain disallowed failure terms, which simplifies verification.
- A lemma (`type_assertion`) is included to assert the types of messages received by the responder, ensuring that they either originate from the adversary or from an initiator.
- Additional lemmas (`Responder_secrecy` and `Public_part_public`) are provided to verify the secrecy of the responder's messages and the accessibility of the public part of messages to the adversary.

**Conclusion:**
This protocol presents a rich interaction model between sources and destructors, highlighting the complexities involved in formal verification within cryptographic systems. The use of explicit destructors allows for a broader range of trace behaviors, while the defined lemmas and restrictions aim to ensure the security properties of the protocol.

---
