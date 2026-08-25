# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: secrecy, injectiveagreement a, injectiveagreement b, noninjectiveagreement a, noninjectiveagreement b, session key honest setup.

---

Example for the Tamarin Prover
  ==============================

  Authors:       Jannik Dreier
  Date:             March 2020
  Time:                ?

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/andrewBAN2.html)

  Ban Concrete Andrew Secure RPC Protocol

  A, B :    principal
  Kab, K'ab :    symkey
  Na, Nb, N'b :    nonce
  succ :    nonce -> nonce

  1.    A  ->  B  :    A, Na
  2.    B  ->  A  :    {Na, K'ab}Kab  SendNsk(xna, ~nsk, xsk, $A, $B)
  3.    A  ->  B  :    {Na}K'ab       ReturnNsk(~na, xnsk, ~sk, $A, $B)
  4.    B  ->  A  :    Nb             SendNb(~nb, xna, ~nsk, ~sk, $A,$B)  ReceiveNb(xnb)

  The protocol must guaranty the secrecy of the new shared key K'ab:
    in every session, the value of K'ab must be known only by the participants playing the roles of A and B.

  The protocol must guaranty the authenticity of K'ab:
    in every session, on reception of message 4,
    A must be ensured that the key K'ab in the message has been created by A in the same session.

  with 2 parallel runs where the intruder I impersonates B.
  i.1.      A  ->  I(B)  :    A, Na
  ii.1.    I(B)  ->  A  :    B, Na
  ii.2.    A  ->  I(B)  :    {Na, K'ab}Kab
  i.2.      I(B)  ->  A  :    {Na, K'ab}Kab
  i.3.      A  ->  I(B)  :    {Na}K'ab
  ii.3.    I(B)  ->  A  :    {Na}K'ab
  i.4.      I(B)  ->  A  :    Ni
  ii.4.    A  ->  I(B)  :    Nb
