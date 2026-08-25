# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: secrecy, injectiveagreement b, agreement b, injectiveagreement a, agreement a, session key honest setup.

---

Example for the Tamarin Prover
  ==============================

  Authors:       Jannik Dreier
  Date:             April 2020
  Time:                 ?

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/ccittx509_3BAN.html)

  BAN modified version of CCITT X.509 (3)

  A, B :    principal
  Na, Nb :    nonce
  Ya, Yb :    userdata
  Xa, Xb :    userdata
  PK, SK :    principal -> key (keypair)

  Spore specification
  1.    A  ->  B  :    A, {Na, B, Xa, {Ya}PK(B)}SK(A)
  2.    B  ->  A  :    B, {Nb, A, Na, Xb, {Yb}PK(A)}SK(B)
  3.    A  ->  B  :    A, {B, Nb}SK(A)
  Reconstruction to fit the original specification
  1.    A  ->  B  :    A, Na, B, Xa, {Ya}PK(B), {h(Na, B, Xa, {Ya}PK(B))}SK(A)
  2.    B  ->  A  :    B, Nb, A, Na, Xb, {Yb}PK(A), {h(B, Nb, A, Na, Xb, {Yb}PK(A))}SK(B)
  3.    A  ->  B  :    A, {B, Nb}SK(A)

  h is a one-way function.

  The protocol must ensure the confidentiality of Ya and Yb:
    if A and B follow the protocol, then an attacker should not be able to obtain Ya or Yb.

  The protocol must ensure the recipient B of the message 1 that the data Xa and Ya originate from A.

  The protocol must ensure the recipient A of the message 2 that the data Xb and Yb originate from B.
