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
  (http://www.lsv.fr/Software/spore/nssk_amended.html)

  Amended Needham Schroeder Symmetric Key

  A, B, S :    principal
  Na, Nb :    number
  Kas, Kbs, Kab :    key
  dec :    number -> number

  1.    A  ->  B  :    A
  2.    B  ->  A  :    {A, Nb}Kbs
  3.    A  ->  S  :    A, B, Na, {A, Nb}Kbs
  4.    S  ->  A  :    {Na, B, Kab, {Kab, Nb, A}Kbs}Kas
  5.    A  ->  B  :    {Kab, Nb, A}Kbs
  6.    B  ->  A  :    {Nb}Kab
  7.    A  ->  B  :    {dec(Nb)}Kab

  The extra exchange of the nonce Nb prevents the Denning Sacco freshness attack described in Needham Schroeder Symmetric Key.

  This protocol establishes the fresh shared symmetric key Kab.

  Messages 1-3 perform the distribution of the fresh shared symmetric key Kab
  and messages 4-5 are for mutual authentification of A and B.

  The operator dec is decrementation.

  The protocol must guaranty the secrecy of Kab: in every session,
  the value of Kab must be known only by the participants playing the roles of A, B and S in that session.

  If the participant playing B accepts the last message 5,
  then Kab has been sent in message 3. by A (whose identity is included in the cipher of message 3).

  We use tags and only one server.
