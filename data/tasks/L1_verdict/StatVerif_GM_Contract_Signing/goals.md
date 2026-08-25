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
| 1 | `aborted_and_resolved_exclusive` | all-traces | aborted and resolved exclusive |
| 2 | `aborted_contract_reachable` | exists-trace | aborted contract reachable |
| 3 | `resolved1_contract_reachable` | exists-trace | resolved1 contract reachable |
| 4 | `resolved2_contract_reachable` | exists-trace | resolved2 contract reachable |

## Protocol description (natural language)

## Description of the Contract Signing Protocol

### Overview
The Contract Signing Protocol is a two-party protocol designed to allow two parties, denoted as 'x' and 'y', to securely sign a contract while ensuring that neither party can manipulate the outcome of the process. The protocol is inspired by the work of Garay, Jakobsson, and MacKenzie on abuse-free optimistic contract signing. The protocol involves a Trusted Third Party (TTP) that plays a central role in validating actions and ensuring that both parties adhere to the protocol's rules.

### Participants
- **Party x**: The first participant who initiates the contract signing.
- **Party y**: The second participant who responds to the contract signing request.
- **Trusted Third Party (TTP)**: A trusted entity that facilitates the signing process and resolves disputes.

### Protocol Steps
1. **Setup of the Trusted Third Party**: The TTP generates a signing key and makes its public key known to both parties. This is done once at the beginning of the protocol.

2. **Contract Initiation**: 
   - Party x proposes a contract 'ct' and sends it to the TTP along with its public key 'pk1' and the public key 'pk2' of Party y.
   - The TTP holds the contract and waits for actions from either Party x or Party y.

3. **Abort Request**: 
   - Either party can request to abort the contract. If Party x sends an abort request to the TTP, it checks the validity of the request based on the contract and the associated signatures.
   - If valid, the TTP issues an abort certificate, effectively terminating the contract.

4. **Resolve Requests**: 
   - If either party wants to resolve the contract, they send a resolve request to the TTP along with their respective signatures of the contract.
   - The TTP verifies the signatures and, if valid, issues a resolve certificate that confirms the contract has been signed by both parties.

5. **Witnessing Events**: 
   - The TTP can generate certificates for both aborted and resolved contracts. This ensures there is an official record of the contract's status that can be referred to later.

### Security Properties
- **Non-repudiation**: Once the contract is signed by both parties, neither party can deny having signed it.
- **Integrity**: The contents of the contract and the associated signatures are protected from modification.
- **Confidentiality**: The private keys used for signing are not disclosed, ensuring that only authorized parties can sign contracts.

### Important Functions
- **pk/1**: Function to retrieve the public key of a participant.
- **sign/2**: Function to sign a message using a private key.
- **pcs/3**: Function for creating a private contract signature.
- **check_getmsg/2**: Verifies the signature and retrieves the original message.
- **checkpcs/5**: Checks the validity of the private contract signature.
- **convertpcs/2**: Converts a private contract signature into a standard signature.

### Goals and Restrictions
The protocol aims to ensure that there cannot be a situation where an adversary can obtain both an abort certificate and a resolve certificate for the same contract. The uniqueness of responses from the TTP and the validity of signature checks are crucial to maintaining this property. Additionally, it is assumed that the TTP will only respond to a request once and that no equality checks will fail.

### Conclusion
The Contract Signing Protocol provides a robust framework for secure contract signing between two parties, with the involvement of a trusted third party to prevent disputes and ensure fairness. The underlying theory and rules detailed in this protocol aim to uphold essential security properties in the contract signing process. 

This description can be directly used to generate the corresponding `.spthy` file for the Tamarin tool, which will validate the protocol's security properties and functionality.
