# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: executability, secrecy, noninjectiveagreement b, noninjectiveagreement a, injectiveagreement b, injectiveagreement a.

---

Example for the Tamarin Prover
  ==============================

  Authors:       Stephanie Delaune
  Date:           March 2020
  Time:           ??

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/yahalomLowe.html)

  Lowe's modified version of Yahalom

  A, B, S :    principal
  Na, Nb :    number fresh
  Kas, Kbs, Kab :    key

  A knows :    A, B, S, Kas
  B knows :    B, S, Kbs
  S knows :    S, A, B, Kas, Kbs
 original version
  1.    A  ->  B  :    A, Na
  2.    B  ->  S  :    B, {A, Na, Nb}Kbs
  3.    S  ->  A  :    {B, Kab, Na, Nb}Kas, {A, Kab}Kbs
  4.    A  ->  B  :    {A, Kab}Kbs, {Nb}Kab

  1.    A  ->  B  :    A, Na
  2.    B  ->  S  :    {A, Na, Nb}Kbs
  3.    S  ->  A  :    {B, Kab, Na, Nb}Kas
  4.    S  ->  B  :    {A, Kab}Kbs
  5.    A  ->  B  :    {A, B, S, Nb}Kab

  The fresh symmetric shared key Kab is created by the server S
  and sent encrypted, in message 3 both to A (directly) and to B (indirectly).

  The protocol must guaranty the secrecy of Kab: in every session,
  the value of Kab must be known only by the participants playing the roles of A, B and S.

  A must be also properly authentified to B.

  This version of the Yahalom protocol is presented in its original paper to illustrate a verification technique by model checking.

  We model a variant with tags.
