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
| 1 | `Observational_equivalence` | diff | observational equivalence of the two diff-term sides |

## Protocol description (natural language)

### Description of the Protocol: Probabilistic Encryption

#### Overview
The Probabilistic Encryption protocol is designed to provide a secure method for encrypting messages using a public key encryption scheme. This protocol allows for the encryption of messages in such a way that even if the same message is encrypted multiple times, the resulting ciphertexts will be different due to the inclusion of randomness. The security of this protocol is based on the notion of observational equivalence, which ensures that an observer cannot distinguish between encryptions of different messages.

#### Components
1. **Functions**:
   - `penc(m, pk(k), r)`: This function represents the probabilistic encryption of a message `m` using a public key `pk(k)` and a random nonce `r`.
   - `pdec(c, k)`: This function represents the decryption of a ciphertext `c` using a private key `k`. The decryption should yield the original message.
   - `pk(k)`: This function generates the public key associated with the private key `k`.

2. **Equations**:
   - The core equation of the protocol is `pdec(penc(m, pk(k), r), k) = m`, which states that decrypting the encryption of a message `m` with the corresponding private key `k` will yield the original message `m`. This ensures the correctness of the encryption and decryption process.

#### Protocol Rules
1. **Key Generation Rule (`gen`)**:
   - This rule models the generation of a new key pair. When a fresh key `~k` is created (represented by `Fr(~k)`), the rule produces a public key `pk(~k)` and announces it to the network. This step is crucial for setting up the protocol and allowing participants to use the generated public key for encryption.

2. **Encryption Rule (`enc`)**:
   - This rule defines the process of encrypting a message. When a participant has a valid key `k` (denoted by `!Key(k)`), two fresh random values `~r1` and `~r2` are created (indicated by `Fr(~r1)` and `Fr(~r2)`). The participant then takes an input message `x` and produces an output that is the encrypted form of `x` using the public key `pk(k)` and the random value `~r2`. The output is represented as `diff(~r1, penc(x, pk(k), ~r2))`, where `diff` is used to represent the relationship between the random value and the ciphertext.

#### Security and Performance
The protocol is designed to ensure that the encryption is non-deterministic, meaning that the same message encrypted multiple times will yield different ciphertexts. This non-determinism is achieved through the use of fresh random values during the encryption process. The security of the protocol has been formally verified, proving that it maintains observational equivalence, which implies that it is secure against chosen plaintext attacks.

This description provides a comprehensive overview of the Probabilistic Encryption protocol, detailing its components, rules, and security properties. From this description, a corresponding spthy file can be constructed to model and analyze the protocol using the Tamarin tool.

### Generated spthy File
```plaintext
theory probEnc 
begin

/*
 * Protocol:     Probabilistic encryption
 * Modeler:      Jannik Dreier and Ralf Sasse
 * Described in: Automated Symbolic Proofs of Observational Equivalence [CCS'15]
 * Date:         April 2015
 *
 * Status:       working
// Observational equivalence is proven automatically in less than 0.4 seconds.
 */

functions: penc/3, pdec/2, pk/1

equations: pdec(penc(m, pk(k), r), k) = m

rule gen:
  [ Fr(~k) ]
--[ ]->
  [ !Key(~k), Out(pk(~k)) ]

rule enc:
  [ !Key(k), Fr(~r1), Fr(~r2), In(x) ]
--[ ]->
  [ Out(diff(~r1, penc(x, pk(k), ~r2))) ]

end
```
