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
| 1 | `types` | all-traces | types |
| 2 | `Unbind_PCR_charn` | all-traces | unbind pcr charn |
| 3 | `exclusive_secrets` | all-traces | exclusive secrets |
| 4 | `left_reachable` | exists-trace | left reachable |
| 5 | `right_reachable` | exists-trace | right reachable |

## Protocol description (natural language)

---

## Protocol Description: TPM Exclusive Secrets

### Overview
This protocol demonstrates the use of Trusted Platform Modules (TPMs) to ensure exclusive access to secrets. The primary goal is to verify that an adversary cannot simultaneously access two secrets encrypted by Alice using distinct keys certified by the TPM.

### Context and Background
The protocol is an adaptation of the running example presented by Delaune et al. in their paper on the formal analysis of protocols based on TPM state registers. The analysis is relevant in understanding how secrets can be securely managed and accessed in a system that utilizes TPM functionality.

### Components
- **TPM Initialization**: The TPM is initialized with a unique Authentication Identity Key (AIK), designated to maintain the integrity of the secrets handled within the system.
- **PCR (Platform Configuration Register)**: The protocol uses a single PCR, which starts with an initial value. This register can be extended with new values as actions occur within the protocol.
- **Key Creation and Certification**: Keys are generated and certified by the TPM's AIK, binding them to the current state of the PCR. This binding ensures that only when the PCR matches the expected state can the associated secrets be decrypted.

### Protocol Rules
1. **PCR Initialization**: A unique AIK is established, and the PCR value is set.
2. **PCR Extension**: The PCR can be extended with new values as secrets are introduced.
3. **Key Creation**: New keys are generated and stored in a key table, bound to the current state of the PCR.
4. **Key Certification**: The TPM certifies these keys using the AIK, producing signatures that can be verified by Alice.
5. **Unbinding Secrets**: Secrets can only be decrypted using the keys if the current PCR state matches the expected state.

### Security Properties
- The protocol aims to prevent the simultaneous retrieval of both secrets by any adversary. This is enforced by ensuring that each secret is only accessible through its uniquely bound key.
- A set of lemmas are included to verify the security properties, including:
  - **Exclusive Secrets**: It asserts that no adversary can retrieve both secrets simultaneously.
  - **Reachability**: Individual access to each secret is guaranteed, ensuring that secrets can be accessed independently.

### Axioms and Restrictions
The protocol includes several restrictions to ensure unique initial states and successful inequality checks, which are crucial for maintaining security throughout the execution of the protocol.

### Conclusion
The TPM Exclusive Secrets protocol effectively demonstrates how TPMs can be utilized to manage secrets securely, ensuring that they remain inaccessible to unauthorized entities while allowing legitimate access under the right conditions.

---
