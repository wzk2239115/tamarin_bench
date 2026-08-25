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
  (http://www.lsv.fr/Software/spore/ccittx509_3.html)

  CCITT X.509 (3)

  A, B :    principal
  Na, Nb :    nonce
  Ta, Tb :    timestamp
  Ya, Yb :    userdata
  Xa, Xb :    userdata
  PK, SK :    principal -> key (keypair)

  Spore simplification
  1.    A  ->  B  :    A, {Ta, Na, B, Xa, {Ya}PK(B)}SK(A)
  2.    B  ->  A  :    B, {Tb, Nb, A, Na, Xb, {Yb}PK(A)}SK(B)
  3.    A  ->  B  :    A, {Nb}SK(A)
  Spore reminder of actual specification
  1.    A  ->  B  :    A, Ta, Na, B, Xa, {Ya}PK(B), {h(Ta, Na, B, Xa, {Ya}PK(B))}SK(A)
  2.    B  ->  A  :    B, Tb, Nb, A, Na, Xb, {Yb}PK(A), {h(B, Tb, Nb, A, Na, Xb, {Yb}PK(A))}SK(B)
  3.    A  ->  B  :    A, {Nb}SK(A)

  h is a one-way function.

  The protocol must ensure the confidentiality of Ya and Yb:
    if A and B follow the protocol, then an attacker should not be able to obtain Ya or Yb.

  The protocol must ensure the recipient B of the message 1 that the data Xa and Ya originate from A.

  The protocol must ensure the recipient A of the message 2 that the data Xb and Yb originate from B.

  This parallel session attack presented in [BAN89] works if B does not check the timestamp Ta in the first message.
  i.1.      A  ->  I(B)  :    A, {Ta, Na, B, Xa, {Ya}PK(B)}SK(A)
  i.1.      I(A)  ->  B  :    A, {Ta, Na, B, Xa, {Ya}PK(B)}SK(A)
  i.2.      B  ->  I(A)  :    B, {Tb, Nb, A, Na, Xb, {Yb}PK(A)}SK(B)
  ii.1.    A  ->  I  :      A, {Ta', Na', C, Xa', {Ya'}PK(I)}SK(A)
  ii.2.    I  ->  A  :      I, {Ti, Nb, A, N'a,Xi, {Yi}PK(A)}SK(I)
  ii.3.    A  ->  I  :      A, {Nb}SK(A)
  ii.3.    I(A)  ->  B  :    A, {Nb}SK(A)

  Another attack can be found in :
    Colin l'Anson and Chris Mitchell.
    Security defects in the ccitt recomendation x.509 - the directory authentication framework.
    Computer Communication Review, 20(2):30--34, april 1990.
      http://www.chrismitchell.net/sdicrx.pdf
      (authentication failure by replay considering no checking of timestamps)
      (is similar to the previous attack)
