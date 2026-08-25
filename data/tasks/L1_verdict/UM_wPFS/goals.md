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
| 1 | `wPFS_initiator_key` | all-traces | wpfs initiator key |
| 2 | `wPFS_responder_key` | all-traces | wpfs responder key |

## Protocol description (natural language)

The Unified Model (UM) Key-Exchange Protocol is a cryptographic protocol designed to facilitate secure key exchange between two parties, referred to as the initiator ($I$) and the responder ($R$). The protocol incorporates elements of the Diffie-Hellman key exchange method and aims to provide weak Perfect Forward Secrecy (wPFS), which ensures that even if long-term keys are compromised in the future, past session keys remain secure.

### Overview of the Protocol

1. **Key Generation**: 
   - The protocol begins with the generation of a long-term key (Ltk) for each participant, which is a prerequisite for subsequent operations.
   - The initiator generates a key $lk$ and publishes its public key as `Pk($A, 'g'^~lk)`, where `g` is a generator.

2. **Initiation Phase**:
   - The initiator ($I$) starts the protocol by creating an ephemeral key (`~ekI`) and sends a message to the responder ($R$), including its ephemeral public key (`'g'^~ekI`) and the session identifier (`SidI_1`).
   - The initiator also includes a hash of the ephemeral key and the responder's public key, which is used for session key derivation.

3. **Response Phase**:
   - Upon receiving the message from the initiator, the responder ($R$) generates its own ephemeral key (`~ekR`) and responds with its ephemeral public key (`'g'^~ekR`), along with a hash that combines both parties' ephemeral keys and the initiator's public key.
   - The responder also creates a session key based on this hash.

4. **Session Key Derivation**:
   - Both parties derive a session key (`Sessk`) using the shared ephemeral keys and the public keys.
   - The session key is uniquely tied to the session and is used for encrypting further communication between the parties.

### Security Properties

- **Weak Perfect Forward Secrecy (wPFS)**: The protocol ensures that if long-term keys are compromised after a session has ended, previous session keys cannot be retroactively decrypted. This is achieved by preventing the revelation of ephemeral keys and ensuring that session keys are only derived from ephemeral keys.

- **Key Agreement Reachability**: The protocol models the ability to establish a session key and ensures that the session key must be reached without revealing any long-term keys before the session concludes.

- **Reveal Mechanisms**: The protocol includes rules for revealing long-term keys, ephemeral keys, and session keys, providing a way to test the security of the key agreement process.

### Rules

1. **Key Generation (`generate_ltk`)**: 
   - Generates a long-term key for a participant and publishes its corresponding public key.

2. **Initiator Rules (`Init_1`, `Init_2`)**:
   - `Init_1`: Initiates the session with an ephemeral key and sends the first message.
   - `Init_2`: Processes the responder's message and derives the session key.

3. **Responder Rules (`Resp_1`)**:
   - `Resp_1`: Acknowledges the initiator's message, generates its ephemeral key, and sends a response containing its public key and derived session key.

4. **Reveal Rules**: 
   - `Sessk_reveal`, `Ephk_reveal`, `Ltk_reveal`: Allow for the revelation of session keys, ephemeral keys, and long-term keys, respectively, under controlled conditions.

### Conclusion

The Unified Model Key-Exchange Protocol aims to provide a secure and efficient method for two parties to establish a shared session key while maintaining the confidentiality of past sessions through weak Perfect Forward Secrecy. The protocol is modeled in a way that allows for formal verification using the Tamarin tool, ensuring that the defined security properties hold against potential attacks. 

This description provides a comprehensive explanation of the protocol, which can be translated into an appropriate spthy file for use with the Tamarin tool.
