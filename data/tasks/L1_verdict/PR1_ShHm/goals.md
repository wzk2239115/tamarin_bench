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
| 2 | `AuthP` | all-traces | authp |

## Protocol description (natural language)

---

### Protocol Description: Protocol PR_1

**Overview:**
Protocol PR_1 is designed as a simple voting mechanism to demonstrate a possibility result in the context of dispute resolution in voting scenarios. It establishes the interactions between a voter (H), a server (S), and a partially trusted party (P) while ensuring the integrity and authenticity of the votes cast.

**Key Participants:**
- **Voter (H)**: The individual casting the vote.
- **Server (S)**: The entity responsible for tallying the votes.
- **Partially Trusted Party (P)**: A mediator that forwards messages between the voter and the server.

**Assumptions:**
- The protocol uses a public key infrastructure (PKI) to manage keys.
- Messages are sent over both reliable and unreliable channels.
- The adversary may attempt to create fake evidence but is limited by the protocol’s restrictions.

**Mechanics:**
1. **Setup Phase:**
   - A long-term key pair (private and public) is generated for the voter (H).
   - The system is initialized with the voter and the server, establishing their roles.

2. **Voting Process:**
   - The voter sends their ballot to the partially trusted party (P).
   - P forwards the ballot to the server (S) while ensuring the message's integrity is maintained.

3. **Server Processing:**
   - The server receives the ballot from P and verifies its format.
   - Upon verification, the server generates and sends back ballot status (`bs`) and vote status (`vs`) messages.

4. **Ballot Recording and Tallying:**
   - The ballot is recorded and tallied by the server.
   - The results are published, ensuring that the voting process is transparent and accountable.

**Channels:**
- **Reliable Insecure Channel (IR)**: Ensures that messages are sent and received unchanged.
- **Undeniable Insecure Channel (IU)**: Similar to IR but ensures that the sender cannot deny having sent the message.

**Restrictions:**
- The protocol is designed to have a single setup phase, preventing multiple initializations.

**Lemmas:**
- **Functional Lemma**: Establishes that there exists a trace of the protocol that leads to a recorded ballot and a tallied vote.
- **AuthP Lemma**: Ensures that if the server is honest, no faulty behavior occurs regarding the ballots being processed.

**Conclusion:**
Protocol PR_1 is a foundational framework for understanding how to securely conduct a voting process with the potential for dispute resolution. By utilizing cryptographic signatures and a structured communication protocol, it aims to maintain the integrity of each vote cast while allowing for verification and transparency.

---
