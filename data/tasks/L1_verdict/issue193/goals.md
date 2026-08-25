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
| 1 | `debug` | exists-trace | debug |

## Protocol description (natural language)

---

### Protocol Description: Revealing Signatures

**Overview:**
The Revealing Signatures protocol allows a signer to create a digital signature for a message while also providing a mechanism for revealing the signature in a secure manner. The protocol employs cryptographic functions including hashing and a revealing-signing function.

**Functions:**
- `h/7`: A hash function that takes seven inputs, typically used for hashing messages or signatures.

**Built-in Functions:**
- `hashing`: A built-in operation used for hash computation.
- `revealing-signing`: A built-in operation allowing the generation of a signature that can be revealed later.

**Rules:**

1. **Rule ONE: Signature Creation**
   - In this rule, the signer generates a public key (`pk`) from a secret key (`~sk`) and creates a revealing signature (`tSig`) using a random nonce (`~random`).
   - The inputs to this rule are:
     - A fresh secret key (`~sk`).
     - A random nonce (`~random`).
   - Upon execution, the rule outputs:
     - The revealing signature (`tSig`).
     - The key (`Key(~sk)`), which represents the holder's secret key used for signing.
   - This rule illustrates the signing process, where the secret key is transformed into a public key and a signature.

2. **Rule TWO: Signature Verification**
   - This rule is responsible for the verification of the signature. It checks whether a given signature (`sig`) is valid for a message (`m`) using the public key (`pk`).
   - The inputs to this rule include:
     - An incoming signature (`In(sig)`).
     - The signer's secret key (`Key(~sk)`).
   - The verification process involves checking if the signature correctly verifies against the message and the public key using the `revealVerify` function.
   - If the verification is successful (i.e., the equality holds true), no output is produced, indicating that the signature is valid.

**Lemmas:**

- **Lemma Debug: Existence of Trace**
  - This lemma asserts that there exists a trace where an action occurs at some index `i`. It is a way to specify that a certain event can be observed in the protocol's execution.

**Restrictions:**

- **Restriction Equality:**
  - This restriction states that if two values are declared equal at a certain time `i`, then they must indeed be equal in the protocol's execution. This is a crucial aspect of maintaining consistency in the protocol's logic.

---

### Summary:
The Revealing Signatures protocol combines the generation of a revealing signature with a verification mechanism, ensuring that signatures can be verified against messages while keeping the signing process secure and the secret key confidential. The use of built-in functions and the defined rules ensure that the protocol operates correctly within the Tamarin framework.
