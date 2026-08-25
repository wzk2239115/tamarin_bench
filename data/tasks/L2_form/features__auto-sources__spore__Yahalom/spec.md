# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: executability, secrecy, noninjectiveagreement b, noninjectiveagreement a, injectiveagreement b, injectiveagreement a.

---

Example for the Tamarin Prover
  ==============================

  Authors:        Stéphanie Delaune
  Date:           March 2020
  Time:            ??

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/yahalom.html)

  Yahalom

  A, B, S :    principal
  Na, Nb :    number fresh
  Kas, Kbs, Kab :    key

  A knows :    A, B, S, Kas
  B knows :    B, S, Kbs
  S knows :    S, A, B, Kas, Kbs

  1.    A  ->  B  :    A, Na
  2.    B  ->  S  :    B, {A, Na, Nb}Kbs
  3.    S  ->  A  :    {B, Kab, Na, Nb}Kas, {A, Kab}Kbs
  4.    A  ->  B  :    {A, Kab}Kbs, {Nb}Kab

  The fresh symmetric shared key Kab is created by the server S
  and sent encrypted, in message 3 both to A (directly) and to B (indirectly).

  The protocol must guaranty the secrecy of Kab: in every session,
  the value of Kab must be known only by the participants playing the roles of A, B and S.

  A must be also properly authentified to B.

  We consider here the tagged version of this protocol.
