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
| 1 | `injectivity_check` | all-traces | injectivity check |

## Protocol description (natural language)

---

**Protocol Description: Injectivity Test**

**Overview:**
The Injectivity Test protocol is a simple yet illustrative example designed to demonstrate the injectivity constraint-reduction rule within the Tamarin verification framework. This protocol serves as a foundational model for understanding how injectivity can be preserved in the presence of operations that manipulate states.

**Purpose:**
The primary objective of the Injectivity Test is to ensure that once an object (or identifier) has been initiated, it cannot be simultaneously copied and removed in such a way that would violate its injectivity. This is critical in scenarios where the uniqueness of identifiers must be maintained throughout various operations.

**Components:**
1. **Rules:**
   - **Init Rule:** This rule initiates an identifier `~i`. When an identifier is fresh (not previously initiated), the action of initiating (`Initiated(~i)`) transforms the state to reflect that the identifier is now considered injected (`Inj(~i)`).
   - **Copy Rule:** The copy rule allows for the duplication of an already injected identifier. When an identifier `i` is marked as injected (`Inj(i)`), it can be copied, and the resulting state remains injected.
   - **Remove Rule:** This rule allows for the removal of an injected identifier. If an identifier `i` is injected, it can be removed, transitioning the state to an empty set, indicating that the identifier is no longer present.

2. **Lemma:**
   - The protocol includes a lemma named `injectivity_check`, which states that it is impossible to have a sequence of events where an identifier is initiated, removed, and copied in a way that contradicts injectivity. The lemma asserts that there cannot be an identifier `id` that exists in such a conflicting series of operations (`Initiated(id)`, `Removed(id)`, and `Copied(id)`) occurring in strict chronological order.

**Status:**
The Injectivity Test protocol is currently in a working state, having been validated for its intended constraints and operational rules.

**Modeler:**
This protocol was modeled by Nick Moore in May 2017, reflecting a straightforward application of Tamarin's capabilities to enforce injectivity constraints.

---
