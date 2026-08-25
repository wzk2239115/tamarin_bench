# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: secrecy, injectiveagreement b, agreement b, session key honest setup.

---

Example for the Tamarin Prover
  ==============================

  Authors:       Jannik Dreier
  Date:             April 2020
  Time:                      ?

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/ccittx509_1c.html)

  CCITT X.509 (1c)

  A, B :    principal
  Na, Nb :    nonce
  Ta, Tb :    timestamp
  Ya, Yb :    userdata
  Xa, Xb :    userdata
  PK, SK :    principal -> key (keypair)
  h :    userdata -> userdata (one-way)

  Spore specification
  1.    A  ->  B  :    A, {Ta, Na, B, Xa, {Ya, {h(Ya)}SK(A)}PK(B)}SK(A)
  Reconstruction to fit the original specification
  1.    A  ->  B  :    A, Ta, Na, B, Xa, {Ya, {h(Ya)}SK(A)}PK(B), {h(Ta, Na, B, Xa, {Ya, {h(Ya)}SK(A)}PK(B))}SK(A)

  h is a one-way function.

  The timestamp Ta and nonce Na are not used here.
  Xa and Ya are the data transmitted,
  the privacy of Ya is ensured by its encryption with the public key of B and
  the authenticity of Xa and Ya is ensured by the encryption with the private key of A.

  The protocol must ensure the confidentiality of Ya:
    if A and B follow the protocol,
    then an attacker should not be able to obtain Ya.

  The protocol must ensure the recipient B of the message that the data Xa and Ya originate from A.
