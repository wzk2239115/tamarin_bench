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
| 1 | `secrecyV` | all-traces | secrecyv |
| 2 | `weak_agreement` | all-traces | weak agreement |
| 3 | `recent_aliveness` | all-traces | recent aliveness |

## Protocol description (natural language)

### Protocol Description for SAKE

**Involved Parties:**
- **Verifier (V):** The party that initiates the protocol and verifies the identity of the device.
- **Device (D):** The party that responds to the verifier and establishes a shared secret key.

**Protocol Steps:**

1. **Initialization by Verifier:**
   - V generates a random secret \( a \).
   - Computes \( v0 = g^a \mod p \).
   - Computes \( v1 = h(v0) \) and \( v2 = h(v1) \).
   - Computes a checksum \( c = cksum(v2) \).
   - Sends \( v2 \) to D.

2. **Response from Device:**
   - D computes the checksum \( c = cksum(v2) \).
   - Generates a random value \( r \) and computes:
     - \( w0 = h(c | r) \)
     - \( w1 = h(w0) \)
     - \( w2 = h(w1) \)
   - Generates another random value \( b \) and computes \( k = g^b \mod p \).
   - Sends \( (w2, mac(c, w2)) \) to V.

3. **Verification by Verifier:**
   - V checks if the received MAC \( mac(c, w2) \) matches the computed MAC.
   - If valid, V sends \( v1 \) to D.

4. **Device Verification:**
   - D checks if \( v2 \) is equal to \( h(v1) \).
   - If valid, D sends \( (w1, k, mac(w2, k)) \) to V.

5. **Final Verification by Verifier:**
   - V checks if the received MAC \( mac(w2, k) \) matches the computed MAC.
   - Also checks if \( w2 \) is equal to \( h(w1) \).
   - If both checks pass, V sends \( v0 \) to D.

6. **Final Device Verification:**
   - D checks if \( v1 \) is equal to \( h(v0) \).
   - If valid, computes the shared secret \( sk_{VD} = v0^b = (g^a)^b \mod p \).
   - D sends \( w0 \) to V.

7. **Final Verification by Verifier:**
   - V checks if \( w1 \) is equal to \( h(w0) \).
   - If valid, it confirms the shared secret \( sk_{VD} = k^a = (g^b)^a \mod p \).

**Security Properties:**
- **Secrecy** of the shared key \( sk_{VD} \).
- **Authentication** of both parties.
- **Integrity** of the messages exchanged through the use of MACs.
- **Freshness** guaranteed by the use of random values and checksums.
