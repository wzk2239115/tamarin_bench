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
| 1 | `authentic` | all-traces | authentic |
| 2 | `authentic_reachable` | exists-trace | authentic reachable |

## Protocol description (natural language)

---

### TESLA Protocol, Scheme 1 Description

**Protocol Name**: TESLA Protocol, Scheme 1  
**Modeler**: Simon Meier  
**Date**: May 2012  
**Status**: Working

#### Overview
The TESLA protocol is designed for broadcast authentication, allowing a sender (S) to authenticate a sequence of messages to one or more receivers (R). The protocol utilizes a delayed authentication mechanism based on shared secret keys and digital signatures to ensure that messages are authenticated in a secure and efficient manner.

#### Messages
The protocol involves a series of messages exchanged between the sender and the receiver, structured as follows:

1. **Initialization**:
   - **Msg 0a**: The receiver (R) sends a nonce `nR` to the sender (S).
   - **Msg 0b**: The sender responds with a commitment to the first key, signing the commitment with its long-term key (`ltkS`).
     - Format: `S -> R: {f(k1), nR}SK(S)`

2. **Authenticated Broadcast**:
   - **Msg 1**: The sender broadcasts the first data message along with its MAC (Message Authentication Code).
     - Format: `S -> R: D1, MAC(k1, D1)` where `D1 = m1, f(k2)`
   - **Msg 2**: The sender sends the second data message along with its MAC and the previous key.
     - Format: `S -> R: D2, MAC(k2, D2)` where `D2 = m2, f(k3), k1`
   
3. **Subsequent Messages** (for `n > 1`):
   - **Msg n**: The sender continues to broadcast messages, each containing the data, a MAC, and the relevant keys.
     - Format: `S -> R: Dn, MAC(kn, Dn)` where `Dn = mn, f(kn+1), kn-1`

#### Security Property
The protocol's security relies on the assumption that the sender's long-term key remains secret until the sender has completed its setup phase. The primary security property verified is:
- **Authenticity**: If a receiver claims to have received a message `m` from the sender, then:
  - Either the sender actually sent that data (with a guarantee of authenticity).
  - Or the sender's long-term key was compromised before the receiver's setup was complete.
  - Or an expiration condition was violated, indicating a potential replay attack.

#### Assumptions
- The protocol assumes the presence of an active adversary who may attempt to compromise messages or keys.
- Timing aspects are not modeled, meaning that while the protocol's cryptographic correctness is verified, timing assumptions must be validated externally.

#### References
1. Perrig, Adrian, et al. "The TESLA Broadcast Authentication Protocol." In RSA Cryptobytes, Summer 2002.
2. Philippa J. Hopcroft, Gavin Lowe. "Analysing a stream authentication protocol using model checking." Int. J. Inf. Sec. 3(1): 2-13 (2004).
3. David A. Basin, et al. "Formal Reasoning about Physical Properties of Security Protocols." ACM Trans. Inf. Syst. Secur. 14(2): 16 (2011).

---
