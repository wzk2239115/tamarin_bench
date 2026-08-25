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

**Protocol Description: Pattern Matching and Destructors**

**Protocol Name:** Demonstration of Pattern Matching Using Destructor Functions  
**Modelers:** Simon Meier, Benedikt Schmidt  
**Date Created:** July 2012  
**Status:** Working (Note: The constant 'true' is not allowed)

**Overview:**  
This protocol serves as a demonstration on how pattern matching can be effectively described using explicit destructor functions in the Tamarin verification tool. It is a variant of the 'Minimal Typing Example' and showcases the ability to handle message structures without relying on traditional pattern matching.

**Key Components:**

1. **Built-in Functions:**
   - **symmetric-encryption:** A built-in function to implement symmetric encryption.
   - **hashing:** A built-in function for hashing messages.
   
2. **Custom Functions:**
   - **isPair/1:** A function that checks if a given input is a pair.
   - **true/0:** A function representing a true value.
   - **encSucc/2:** A function that checks if a symmetric encryption was successful.
   - **and/2:** A function that evaluates logical conjunction.

3. **Equations:**
   - `isPair(pair(x, y)) = true`: This equation asserts that a pair structure is valid.
   - `encSucc(senc(x,y), y) = true`: This defines the success condition for symmetric encryption.
   - `and(true, true) = true`: This states that the conjunction of two true values remains true.

**Protocol Rules:**

1. **Setup_Key:**  
   This rule allows for the creation of a shared key, `k`, which can be compromised later. The rule specifies that a fresh key can be generated and marked as a valid key.

2. **Reveal_Key:**  
   This rule handles the scenario where a valid key `k` is revealed to the adversary, allowing them to output this key.

3. **Initiator:**  
   The initiator constructs a message using symmetric encryption of a secret and a public value, then outputs this message while making the public key available.

4. **Responder:**  
   The responder receives an encrypted message and uses explicit destructors to decrypt it. It checks that the decryption was successful and validates its structure. If successful, it outputs the public part of the original message.

**Restrictions:**
- The protocol includes a restriction that asserts all expressions evaluated as true must equate to the constant true, ensuring consistency in truth evaluations.

**Lemmas:**

1. **Type Assertion:**  
   This lemma states that for any message received by the responder, it either originates from the adversary (who knows the secret key) or comes from a legitimate initiator.

2. **Responder Secrecy:**  
   This lemma ensures that the secret part of the message received by the responder remains confidential, provided that the key has not been compromised.

3. **Public Part Accessibility:**  
   This lemma states that the public part of a message is accessible to the adversary without requiring a key reveal, confirming that the adversary can ascertain public values independently.

---
