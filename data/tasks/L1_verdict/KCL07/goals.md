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
| 1 | `recentalive_tag` | all-traces | recentalive tag |
| 2 | `executable` | exists-trace | executable |

## Protocol description (natural language)

---

### Protocol Description: KCL07

#### Roles:
1. **Reader (R)**: An entity that initiates communication with the RFID tag. It possesses shared knowledge `k` and the ID of the tag.
2. **RFID Tag (T)**: An entity that responds to the Reader's challenge. It shares the same knowledge `k` and ID with the Reader.

#### Shared Knowledge:
- **k**: A secret key shared between the Reader and the RFID Tag.
- **ID**: The unique identifier for the RFID Tag.

#### Interaction Steps:
1. **Setup Phase**:
   - The Reader and the RFID Tag are initialized with fresh values for `k` and `ID`.
   - Both entities are set up as valid roles in the system.

2. **Challenge from Reader**:
   - The Reader generates a fresh random nonce `r1` and sends it to the RFID Tag.
   - This nonce is used to ensure that each session is unique.

3. **Response from RFID Tag**:
   - Upon receiving the nonce `r1`, the RFID Tag generates its own fresh random nonce `r2`.
   - It responds to the Reader with two pieces of data:
     - The XOR of the ID and `r2`: `ID XOR r2`
     - The XOR of the hash of the nonce `r1` with the shared key `k` and the nonce `r2`: `h(r1, k) XOR r2`

4. **Recent Aliveness Check**:
   - The Reader checks the validity of the response from the RFID Tag.
   - The Reader considers the RFID Tag to be "recently alive" if it can find `ID` and `k` such that:
     - `ID XOR r2 XOR h(r1, k) XOR r2 = ID XOR h(r1, k)`
   - This check ensures that the Tag is alive and responding correctly, based on the most recent interaction.

#### Security Properties:
- **Recent Aliveness**: The protocol ensures that the Reader can confirm that the Tag is alive based on the response it receives.
- **Untraceability**: Although the protocol supports recent aliveness, it does not guarantee untraceability, meaning that an adversary could potentially trace the interactions based on the received nonces and responses.

#### Restrictions:
- **Equality Restriction**: Ensures that if two terms are considered equal at a certain point in time, they must be equal in all instances.
- **Unique Restriction**: Guarantees that any particular instance of an event (like `OnlyOnce`) can occur only once.

#### Proofs:
- **Recent Aliveness Lemma**: Demonstrates that if the Tag is alive, there must have been a valid challenge-response interaction.
- **Executable Lemma**: Shows that there exists a trace of execution where the Tag can be confirmed to be alive based on its response.

---
