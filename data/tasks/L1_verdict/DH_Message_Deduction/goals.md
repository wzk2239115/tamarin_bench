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
| 1 | `key_deducible` | exists-trace | key deducible |

## Protocol description (natural language)

---

### Protocol Description: P_Msg

**Protocol Name:** P_Msg  
**Modeler:** Benedikt Schmidt  
**Date:** October 2012  
**Source:** "Ph.D. Thesis: Formal Analysis of Key Exchange Protocols and Physical Protocols"  
**Status:** Working  

**Overview:**
The P_Msg protocol is a demonstration protocol utilized in the thesis of Benedikt Schmidt to illustrate various concepts in the formal analysis of cryptographic protocols. It specifically showcases the Diffie-Hellman key exchange mechanism, which allows two parties to establish a shared secret over an insecure channel.

**Purpose:**
The primary aim of this protocol is to facilitate secure communication between two parties by allowing them to generate a common secret key without directly sharing it. This common key can then be used for encrypting subsequent communications.

**Key Components:**
1. **Builtins:** The protocol uses the Diffie-Hellman built-in operations to perform key generation based on the mathematical principles of modular exponentiation.
  
2. **Rules:**
   - **Start Rule:** This rule initializes the protocol by generating two fresh values, `x` and `y`, which represent the private keys of the two parties. The server sends a message containing `g^x` (where `g` is a generator) and the inverse of `y`. This message serves as the first step in the key exchange process.
   - **Fin Rule:** This rule signifies the completion of the protocol when a party receives the message `g^x`. It indicates that the necessary values have been exchanged, and the protocol execution can terminate.

**Key Deducibility Lemma:**
The protocol includes a lemma, `key_deducible`, which asserts that if the Start and Fin rules are executed in a trace, then there exists an execution path such that:
- The Start rule is executed at time `i`.
- The Fin rule is executed at time `j`.
- The execution of Start and Fin is unique to their respective timestamps.

This lemma is essential for proving the security properties of the protocol, particularly that the key can be derived by the legitimate parties involved.

---

### Corresponding spthy File Generation

You can use the provided description to create a new `spthy` file for Tamarin by ensuring that the elements such as rules, built-ins, and lemmas are accurately captured in the format shown in the initial `spthy` file. This includes defining the protocol structure, rules of operation, and any security properties you wish to analyze within Tamarin.
