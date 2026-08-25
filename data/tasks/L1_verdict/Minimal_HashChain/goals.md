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
| 1 | `Loop_Start` | all-traces | loop start |
| 2 | `Loop_Success_ord` | all-traces | loop success ord |
| 3 | `Loop_charn` | all-traces | loop charn |
| 4 | `Helper_Loop_and_success` | all-traces | helper loop and success |
| 5 | `Loop_and_success` | all-traces | loop and success |
| 6 | `Helper_Success_charn` | all-traces | helper success charn |
| 7 | `Success_charn` | all-traces | success charn |

## Protocol description (natural language)

---

### Protocol Description: Minimal HashChain

#### Overview
The Minimal HashChain protocol is inspired by the TESLA 2 protocol and is designed to illustrate the key challenges in proving the security of a hash chain with re-authentication. The protocol involves generating a sequence of keys through hash functions, which are used for message authentication, ensuring that each key is derived from its predecessor.

#### Goals
The primary goal of this protocol is to establish a mechanism for verifying that a given key is indeed a part of the hash chain, thus ensuring the authenticity of messages sent over a potentially insecure channel.

#### Components
1. **Functions**:
   - `f/1`: This function represents the hash function used for generating subsequent keys in the chain.

2. **Chain Setup Phase**:
   - **Key Generation**:
     - **Gen_Start**: The protocol begins by generating an initial key from a given seed and outputs it.
     - **Gen_Step**: Each time a new key is generated, it is linked to the previous key in the hash chain, ensuring that each key is derived from the last using the hash function `f`.
     - **Gen_Stop**: The sender can decide to stop generating new keys at any point, marking the final key in the chain.

3. **Key Checking**:
   - **Check0**: The process of verifying a key starts with the original key that needs to be checked.
   - **Check**: The verification process involves iterating through the hash chain, checking each key against the original key.
   - **Success**: If the verification process successfully reaches the final key, it concludes that the original key is valid.

#### Lemmas
The protocol includes several lemmas that restrict the search space and establish important relationships between various states within the protocol:
- **Loop_Start**: Ensures that if a loop is initiated with a key, there is a corresponding start statement.
- **Loop_Success_ord**: Establishes an order between looping and successful verification.
- **Loop_charn**: Connects an arbitrary loop step with its starting point.
- **Helper_Loop_and_success**: Links different keys within the loop to ensure the chain's integrity.
- **Loop_and_success**: Relates loops to successful verification conditions.
- **Success_charn**: Confirms that a successful verification is linked to an existing key in the chain.

#### Limitations
The current implementation of the protocol is noted to be incomplete, specifically in its reasoning about multisets and repeated exponentiation. Further development is required to address these issues.

#### Future Work
To enhance the protocol, a better framework for expressing smaller relations in an axiomatic manner is needed. Current attempts have shown that the interactions are too strong and require refinement.

---
