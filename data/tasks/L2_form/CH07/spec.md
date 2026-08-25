---

**Protocol Description: RFID Protocol for Authentication**

This model represents an RFID protocol designed to facilitate secure communication between a Reader (R) and a Tag (T). The primary focus of the protocol is to ensure authentication properties, specifically recent aliveness and agreement, as outlined in the paper "Attacks on RFID protocols" by Ton van Deursen and Sasa Radomirovic (v1.1, Aug 6, 2009).

**Components**:
- **Entities**: 
  - Reader (R)
  - Tag (T)

- **Shared Knowledge**: 
  - A secret key \( k \)
  - An identifier \( ID \)

**Initial Setup**:
- Both the Reader (R) and the Tag (T) possess the shared knowledge of the key \( k \) and the identifier \( ID \).
- The protocol begins with the Reader generating a fresh random number \( r1 \) and sending it to the Tag.

**Protocol Steps**:
1. **Reader Initialization**: 
   - The Reader generates a random challenge \( r1 \) and sends it to the Tag.
   
2. **Tag Response**:
   - Upon receiving \( r1 \), the Tag generates its own fresh random number \( r2 \).
   - The Tag computes a hash based on the challenge values and the shared secret, and sends back \( r2 \) along with a hashed value that combines the identifier and the challenges.

3. **Reader Verification**:
   - The Reader verifies the response from the Tag by checking the received values against expected computations.
   - If verification is successful, the Reader sends a confirmation response back to the Tag.

4. **Tag Confirmation**:
   - The Tag, upon receiving the confirmation from the Reader, acknowledges the communication, thus completing the authentication process.

**Security Properties**:
- **Recent Aliveness**: Ensures that both entities can prove they are alive and engaged in the session.
- **Agreement**: Ensures that both parties agree on the established session parameters and that no other entity can impersonate them.

**Rules**:
- The model encapsulates several rules regarding the initialization, communication, and verification processes. These rules dictate how the entities interact, handle fresh random numbers, and verify the integrity of the exchanged messages.

**Lemmas**:
- The model includes lemmas to automatically find potential attacks, ensure the correctness of execution, and prove properties like non-injective agreement between the Reader and the Tag.

---