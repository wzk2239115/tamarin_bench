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
| 1 | `sanity_check` | all-traces | sanity check |
| 2 | `cannot_Verify_A_Bad_EAT_or_Compromised_Attester` | all-traces | cannot verify a bad eat or compromised attester |
| 3 | `attester_private_key_compromised` | all-traces | attester private key compromised |
| 4 | `verifier_private_key_compromised` | all-traces | verifier private key compromised |
| 5 | `nonce_freshness_across_sessions` | all-traces | nonce freshness across sessions |
| 6 | `attester_does_not_agree_on_nonce_origin` | exists-trace | attester does not agree on nonce origin |
| 7 | `adversary_learns_the_EAT_information` | all-traces | adversary learns the eat information |

## Protocol description (natural language)

---

## Protocol Description: ThirdEATImplementation

### Overview
This protocol is designed to manage the attestation of a device (referred to as the "attester") using a mechanism called EAT (Evidence of Attestation). The protocol emphasizes the relationship between the attester and the verifier (or relying party), assuming they trust each other and may even be the same entity.

### Entities
1. **Attester**: The device whose state is being verified. It can be in one of three states:
   - **Good State**: The device is operating normally.
   - **Bad State**: The device is compromised or has outdated firmware.
   - **Partially Compromised**: An adversary has tricked the attester into reporting good data when it is not.

2. **Verifier**: The entity that requests attestation from the attester and verifies the attestation evidence.

### Key Operations
- **Identity Creation**: Each entity (attester and verifier) generates a unique identity and corresponding keys.
  
- **Nonce Exchange**: The verifier sends a nonce (a unique number used once) to the attester, which is signed to ensure authenticity.

- **EAT Generation**: The attester generates an EAT based on its current state:
  - If in a good state, it sends valid attestation data.
  - If in a bad state or partially compromised, it may send misleading or bad data.

### State Transitions
1. **Attester State Changes**: The attester can transition between states based on its security condition:
   - From good to bad state if compromised.
   - From good to partially compromised state if an adversary tricks it.
   
2. **EAT Sending**: The attester sends its EAT to the verifier. The EAT includes a signed message containing the nonce and the attester's state.

3. **Verification**: The verifier checks the signature and the nonce:
   - If the EAT is valid and in the good state, the verification succeeds.
   - If the EAT is from a bad state or if the nonce does not match, verification fails.

### Restrictions and Lemmas
The protocol includes specific restrictions to ensure integrity:
- **Equality**: If two values are equal in different instances, they are the same.
- **Unique Identity**: Each entity can only have one identity.

Additionally, several lemmas are established to verify the security properties of the protocol:
- **Sanity Check**: Verifies that the protocol can reach a successful verification state despite potential compromises.
- **Non-Verification of Bad States**: Confirms that an attester in a bad state cannot be successfully verified.
- **Key Compromise**: Establishes that the long-term keys of the attester and verifier remain confidential throughout the protocol execution.

### Security Goals
The primary goal of this protocol is to ensure that:
- The attester can provide reliable attestation only when in a good state.
- The verifier can confidently reject attestations that are from compromised states.
- The long-term keys of both parties remain secret from adversaries.

---
