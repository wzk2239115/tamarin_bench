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
| 1 | `executable` | exists-trace | executable |
| 2 | `secrecyA` | all-traces | secrecya |
| 3 | `secrecyB` | all-traces | secrecyb |
| 4 | `alivesness_B` | all-traces | alivesness b |
| 5 | `non_inj_agreement_B` | all-traces | non inj agreement b |
| 6 | `non_inj_agreement_A` | all-traces | non inj agreement a |
| 7 | `FinishedA_unique` | all-traces | finisheda unique |

## Protocol description (natural language)

---

### Protocol Description: Ex1_solution

#### 1. **Overview**
This protocol involves two parties, Alice and Bob, who aim to securely exchange messages using a combination of symmetric and asymmetric cryptography. The protocol employs public key infrastructure to establish initial keys and ensures message confidentiality, integrity, and authentication through signatures.

#### 2. **Equational Theory**
The protocol uses built-in theories for symmetric encryption, asymmetric encryption, and signing. These cryptographic primitives allow the parties to encrypt messages and verify signatures, ensuring that only intended recipients can read the messages and that the messages come from authenticated sources.

#### 3. **Public Key Setup**
- **Rule `PubKey`**: Each party, when initialized, generates a public-private key pair. Alice's secret key (`~ska`) and public key (`pk(~ska)`) are established and made available for use in the protocol.
- **Rule `Compromise`**: If Alice's secret key is compromised, it can be outputted, indicating a breach of security.

#### 4. **Protocol Rules**
- **Rule `AliceSends`**: 
  - Upon starting the communication with Bob, Alice generates a fresh message (`~ma`) and a fresh session key (`~kAB`). 
  - She encrypts the session key using Bob's public key and sends an encrypted message that includes `~ma` and a signature of `~ma` verified by Bob's identity. This ensures that Bob can verify the integrity and authenticity of the message.
  
- **Rule `BobReceived`**: 
  - When Bob receives the message, he decrypts it using his secret key. He verifies the signature against Alice's public key to ensure that the message is authentic. If the verification succeeds, he outputs a response containing his message (`~mb`) encrypted with the established session key (`~kAB`).

- **Rule `AliceReceives`**: 
  - Upon receiving Bob's response, Alice performs checks to ensure that the messages are fresh and that the original message `~ma` does not match Bob's message `~mb` (to prevent replay attacks). If all conditions are satisfied, the protocol concludes successfully.

#### 5. **Restrictions**
- **Equality Restriction**: Ensures that if two terms are equal, they are treated as identical.
- **Nequality Restriction**: Ensures that if two terms are not equal, they are treated as distinct.

#### 6. **Properties**
The protocol includes various properties that are to be verified:
- **Executability**: Ensures that there exists a trace in which both parties finish their processes.
- **Secrecy of Messages**: Ensures that messages intended for a party remain confidential unless that party is compromised.
- **Aliveness**: Guarantees that if Bob finishes his process, Alice or a compromised party is also actively engaged with him.
- **Non-Injective Agreement**: Ensures that if one party finishes, there exists a trace of the other party running the protocol or being compromised.
- **Uniqueness of Finished States**: Ensures that if two parties reach a finished state with the same messages, they do so in a unique manner (i.e., at the same time).

---
