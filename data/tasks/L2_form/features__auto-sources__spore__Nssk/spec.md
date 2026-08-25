# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: executability, secrecy, injectiveagreement b, agreement b, injectiveagreement a, agreement a.

---

Example for the Tamarin Prover
  ==============================

  Authors:       Jannik Dreier
  Date:             March 2020
  Time:

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/nssk.html)

  Needham Schroeder Symmetric Key

  A, B, S :           principal
  Na, Nb :             nonce
  Kas, Kbs, Kab :     key
  dec :               nonce -> nonce

  1.    A  ->  S  :    A, B, Na
  2.    S  ->  A  :    {Na, B, Kab, {Kab, A}Kbs}Kas
  3.    A  ->  B  :    {Kab,A}Kbs
  4.    B  ->  A  :    {Nb}Kab
  5.    A  ->  B  :    {dec(Nb)}Kab

  This protocol establishes the fresh shared symmetric key Kab.

  Messages 1-3 perform the distribution of the fresh shared symmetric key Kab
  and messages 4-5 are for mutual authentification of A and B.

  The operator dec is decrementation.

  The protocol must guaranty the secrecy of Kab: in every session,
  the value of Kab must be known only by the participants playing the roles of A, B and S in that session.

  If the participant playing B accepts the last message 5,
  then Kab has been sent in message 3. by A (whose identity is included in the cipher of message 3).

  Authentication attack by Denning and Sacco.
  Assume that I has recorded the session i and that Kab is compromised.
  After the session ii, B is convinced that he shares the secret key Kab only with A.
  i.1.    A  ->  S    :      A, B, Na
  i.2.    S  ->  A    :      {Na, B, Kab, {Kab, A}Kbs }Kas
  i.3.    A  ->  I(B)  :      {Kab,A}Kbs
                 assume that Kab is compromised
  ii.3.    I(A)  ->  B  :    {Kab,A}Kbs
  ii.4.    B  ->  I(A)  :    {Nb}Kab
  ii.5.    I(A)  ->  B  :    {dec(Nb)}Kab

  We use tags and only one server.
