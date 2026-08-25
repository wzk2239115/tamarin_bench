---

### Protocol Description: ExerciseADH

#### Overview
This protocol implements a key exchange and message sending mechanism between two parties, Alice (A) and Bob (B), utilizing Diffie-Hellman (DH) key exchange and symmetric encryption. The protocol is designed with several security properties in mind, including confidentiality of messages and the establishment of a shared secret key between the two parties. The protocol also incorporates an adversary (adv) who may attempt to intercept or manipulate messages exchanged between Alice and Bob.

#### Assumptions
1. **Unique Keys and Names**: Each entity has a unique identity and corresponding keys, ensuring that the adversary cannot register arbitrary keys or names.
2. **Unique Key-ID Binding**: Each key is uniquely bound to its identity, preventing the adversary from registering false bindings.
3. **Distinct Name Spaces**: The identity names and keys are maintained in separate name spaces, which simplifies verification and reduces potential conflicts.

#### Protocol Steps

1. **Key Generation (Rule Ltk)**:
   - Alice creates a fresh secret key (sk) and a corresponding public key (pk) associated with her identity (id).
   - These keys are stored securely, and the public key is made available to the adversary.

2. **Alice Initiates Key Exchange (Rule A_Init)**:
   - Alice constructs a key exchange message (m1) that contains her identity, Bob's identity, and her public key.
   - She sends this message (m1) to Bob via the adversary and maintains her state for the next invocation.

3. **Bob Receives Key Exchange Message (Rule B_Init)**:
   - Upon receiving m1, Bob retrieves his own secret key and public key and verifies Alice's public key using the established PKI (Public Key Infrastructure).
   - Bob generates a shared secret using his private key and Alice's public key and constructs a response message (m2) containing an acknowledgment and his public key.
   - This message is then sent back to Alice.

4. **Alice Sends Messages (Rule A_SendMsg)**:
   - Alice receives Bob's acknowledgment message (m2) and uses the shared secret to construct a secure message (m3) to send to Bob.
   - The message is encrypted with the shared key, ensuring confidentiality.

#### Security Properties

- **Secrecy of Keys**: The protocol ensures that the established keys (A's initiator key and B's responder key) are not known to the adversary at any point in time.
- **Message Confidentiality**: Messages sent between Alice and Bob are encrypted, making them confidential against potential adversarial interception.
- **Agreement on Keys**: The protocol guarantees that both parties end up with the same shared secret key, ensuring that they can communicate securely.
- **PKI Correctness**: The protocol verifies that all public keys and secret keys are uniquely registered, ensuring the integrity of the key exchange process.

#### Lemmas and Properties

- **Executability**: The protocol allows for traces that demonstrate the successful execution of key exchanges and message sending.
- **Secrecy Lemmas**: Formal statements ensure that no information about the keys or messages is revealed to the adversary.
- **Agreement Lemmas**: Guarantees that if one party has established a key, the other party has also established the same key, ensuring consistency in communication.
- **Uniqueness of Keys**: The protocol asserts that keys established between parties remain the same across multiple runs, ensuring stable communication.

#### Concluding Note
This protocol serves as an educational exercise in implementing secure communication mechanisms using the Tamarin tool, providing valuable insights into cryptographic principles and the importance of rigorous security analysis.

---