# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: executability, secrecy, noninjectiveagreement b, injectiveagreement b.

---

Example for the Tamarin Prover
  ==============================

  Authors:        Stéphanie Delaune
  Date:           March 2020
  Time:             ??

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/denningSacco.html)

  Denning-Sacco shared key

  A, B, S :    principal
  Kas, Kbs, Kab :    key
  T :    timestamp

  1.    A  ->  S  :    A, B
  2.    S  ->  A  :    {B, Kab, T, {Kab, A, T}Kbs}Kas
  3.    A  ->  B  :    {Kab,A, T}Kbs

  The nonces of Needham Schroeder Symmetric Key (for mutual authentication of A and B) have been replaced by a timestamp T.

  The shared symmetric key established by the protocol is Kab.

  The protocol must guaranty the secrecy of Kab: in every session, the value of Kab must be known only 
  by the participants playing the roles of A, B and S in that session.

  A must be properly authentified to B

  This protocol is subject to a mutiplicity attack.
  i.1.    A  ->  S  :    A, B
  i.2.    S  ->  A  :    {B, Kab, T, {Kab, A, T}Kbs}Kas
  i.3.    A  ->  B  :    {Kab,A, T}Kbs
  ii.3.   I(A)  ->  B  :    {Kab,A, T}Kbs
  In session ii, B thinks that A wants to establish a new shared key and accepts it.

  We consider here the tagged version of this protocol.
