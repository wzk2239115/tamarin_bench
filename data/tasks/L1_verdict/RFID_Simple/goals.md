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
| 2 | `Device_ToBob` | all-traces | device tobob |
| 3 | `Device_Init_Use_Set` | all-traces | device init use set |
| 4 | `reachability_left` | exists-trace | reachability left |

## Protocol description (natural language)

---

**Protocol Description: Extended RFID Protocol**

**Overview:**
The protocol is an extended version of a simple RFID system, inspired by the running example from the StatVerif paper by Simon Meier, dated May 2012. It incorporates asymmetric encryption to manage the communication between an RFID device and an external entity, referred to as "Bob". The design aims to secure the interaction and ensure that sensitive data is transmitted only when appropriate conditions are met.

**Key Components:**
1. **Asymmetric Encryption:** The protocol utilizes asymmetric encryption to ensure secure communication. Each RFID device generates a public/private key pair, where the public key is made available to the adversary for encryption purposes.

2. **Device Initialization:** Each RFID device is identified by its private key, which is essential for the device's operations. The device generates a unique key during initialization.

3. **Communication Flow:**
   - The device (Alice) can send encrypted messages to Bob containing sensitive information, but only after it has been authorized to do so.
   - The device allows access to specific information based on the conditions defined in the protocol, ensuring that only the intended data is revealed.

**Rules:**
1. **Key Generation (`GenKey`):** 
   - A new key is generated for the device, which is then made public, allowing the adversary to know the public key while keeping the private key secret.

2. **Alice Sending Data (`Alice`):**
   - When Alice (the device) is ready to use the key, it generates a pair of unique identifiers (`~x` and `~y`) and sends them encrypted using its public key.

3. **Device Communication to Bob (`DeviceToBob`):**
   - The device communicates with Bob by transitioning its state to `Device_Select`, indicating readiness to process requests.

4. **Selection Rules (`Select_Left`, `Select_Right`):**
   - The device can select which piece of information to disclose (left or right) based on internal logic.

5. **Decryption Rules (`Decrypt_Left`, `Decrypt_Right`):**
   - Based on the selection made, the device can decrypt and send the appropriate information (`x` or `y`) to Bob, provided Bob has the necessary access rights.

**Lemmas:**
1. **Types Lemma:** Ensures that for any message `m` accessed, there exists either a knowledge or exclusivity condition that holds true.
  
2. **Device to Bob Lemma:** Establishes that once the device is in use, it cannot be handed over to Bob without following the proper sequence of events.

3. **Device Initialization and Use Lemma:** Guarantees that a device cannot be reused after it has been initialized and used, maintaining the integrity of the device's state.

4. **Reachability Lemmas:** 
   - The protocol includes reachability properties that show the potential for exclusive access to resources under certain conditions.

5. **Secrecy Lemma:** Asserts that under the protocol, no two pieces of exclusive information can be simultaneously known.

**Security Considerations:**
The protocol ensures that sensitive information is only accessible under specific conditions, thereby mitigating risks associated with unauthorized access. The use of asymmetric encryption adds a layer of security by separating the key used for encryption from the key used for decryption.

---
