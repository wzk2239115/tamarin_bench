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
| 2 | `functional2` | exists-trace | functional2 |
| 3 | `functional3` | exists-trace | functional3 |
| 4 | `indivVerif_ps` | all-traces | indivverif ps |
| 5 | `indivVerif_sel` | all-traces | indivverif sel |
| 6 | `univVerif_sel` | all-traces | univverif sel |

## Protocol description (natural language)

To generate the description content of the Alethea's voting protocol as specified in the provided Tamarin spthy file, we can break down the key components of the protocol and its verification results. Below is a structured description that encapsulates the essential elements of the protocol, its functionality, and the lemmas that validate its security properties.

---

### Protocol Description: Alethea's Selection Phase

#### Overview
- **Protocol Name**: Alethea's Selection Phase
- **Modeler**: Lara Schmid
- **Date**: March 2020
- **Source**: "Advancing the Formal Foundations for Voting Protocols", PhD Thesis, ETH Zürich.

#### Purpose
The Alethea's Selection Phase protocol is designed to ensure the secure selection of voters in a voting process while maintaining individual and universal verifiability. The protocol employs cryptographic techniques to guarantee the integrity of the voting process and the confidentiality of voter identities.

#### Key Components
1. **Cryptographic Functions**: 
   - The protocol utilizes various cryptographic operations including signing, asymmetric encryption, hashing, and symmetric encryption.
   - A multiset is also used to manage the collections of votes and cryptographic keys.

2. **Channel Rules**: 
   - The protocol defines rules for secure communication between participants, including sending and receiving messages.

3. **Protocol Execution**:
   - The protocol consists of multiple rules that govern the actions of the server (S), devices (D), auditors (A), and the environment (E).
   - The setup phase initializes the long-term keys for the server and devices, and establishes communication protocols.
   - Voter pseudonyms are published, and the selection of votes is verified in a secure manner.

#### Results
The protocol has undergone rigorous verification, yielding the following results:

- **Functional Lemmas**:
  1. **functional**: Verified without oracle (ensures that if voters are selected, their pseudonyms can be verified).
  2. **functional2**: Verified without oracle (ensures that a different pseudonym can be selected).
  3. **functional3**: Verified without oracle (ensures that even in different scenarios, pseudonyms can be verified).

- **Individual Verifiability**:
  1. **indivVerif_ps**: Verified without oracle (ensures that voters can confirm their pseudonyms are in the list).
  2. **indivVerif_sel**: Verified without oracle (ensures that selected voters can verify their selection).

- **Universal Verifiability**:
  1. **univVerif_sel**: Verified without oracle (ensures that all selections made are verifiable regardless of the environment's choice).

#### Restrictions
- **One Setup**: The protocol enforces the restriction that only one setup can occur, ensuring the integrity of the initial conditions.

#### Conclusion
The Alethea's Selection Phase protocol provides a robust framework for secure and verifiable voting processes. Its formal verification through Tamarin demonstrates its reliability in maintaining the confidentiality and integrity of voter identities while enabling verifiability for all participants involved.

---

This description captures the essence of the provided spthy file, summarizing the protocol, its components, results, and restrictions. You can now use this structured content to create a corresponding spthy file for Tamarin if required.
