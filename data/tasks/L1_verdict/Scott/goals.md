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
| 1 | `key_agreement_reachable` | exists-trace | key agreement reachable |
| 2 | `key_secrecy` | all-traces | key secrecy |

## Protocol description (natural language)

The protocol described in the provided `spthy` file is the Scott identity-based key exchange protocol. Below is a detailed description content that outlines the key components, rules, and security properties of the protocol. This description can be used to generate a corresponding `spthy` file for Tamarin.

---

## Protocol Description: Scott Identity-Based Key Exchange

### Overview
The Scott protocol is an identity-based key exchange protocol designed to facilitate secure communication between two parties, A and B, without requiring them to share a common key beforehand. This protocol relies on a Key Generation Center (KGC) that issues long-term keys based on unique identities (IDs) of the users.

### Components

1. **Key Generation Center (KGC)**:
   - The KGC operates by generating a master secret key (MSK) and can issue long-term keys (LTK) for users identified by their unique IDs. 
   - The KGC setup is responsible for initializing the system with a master secret key.

2. **Key Exchange Process**:
   - The protocol consists of two main phases: Initialization and Response.
   - During the Initialization phase, party A computes a session key component using its secret and sends a message to party B.
   - In the Response phase, party B computes its part of the session key and replies to party A.

### Protocol Rules

1. **KGC Setup**:
   - The KGC sets up the system by generating a master secret key (MSK).
   - `KGC_Setup`: Takes a fresh master secret key and outputs it as `MSK`.

2. **Key Generation**:
   - Users request their long-term keys from the KGC.
   - `KGC_request`: Given the master secret, outputs the long-term key for a user based on their identity.

3. **Session Key Generation**:
   - In the `Init` phase, party A computes its long-term key (LTK) and sends a value `X` to party B.
   - In the `Resp` phase, party B generates its long-term key and computes a value `Y`, which it sends back to party A.

4. **Key Agreement**:
   - Both parties derive a session key using a key derivation function (KDF) that combines their respective computed values and identities.

### Reveals
The protocol includes specific rules to handle the revelation of keys:
- Long-term keys can be revealed through `LtkRev`.
- The master secret key can be revealed through `MskRev`.
- Session keys can be revealed through `SesskRev`.

### Security Properties

1. **Key Agreement Reachability**:
   - The protocol ensures that if two parties successfully complete the key exchange, they will have agreed on a common session key.

2. **Key Secrecy**:
   - The protocol is designed to maintain the secrecy of the session keys. It ensures that even if a session key is known to an adversary, specific conditions must be met to compromise the security of the key.

### Restrictions
- The protocol includes a restriction that prevents the use of neutral elements (like the identity element in cryptographic operations) during key generation and exchange, ensuring that all computations yield meaningful results.

### Conclusion
The Scott identity-based key exchange protocol provides a robust framework for secure communication between parties without prior shared secrets. Its reliance on the KGC for key generation and the structured exchange of messages ensures that both parties can securely derive a shared session key while maintaining the confidentiality of their long-term keys.

--- 

This description can be used to guide the development and understanding of the protocol's implementation in Tamarin, ensuring that the essential components, rules, and properties are well-documented and easily translatable into corresponding `spthy` syntax.
