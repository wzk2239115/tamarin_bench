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
  4.    B  ->  A  :    {Nb}Kab
  5.    A  ->  B  :    {hash(Nb)}Kab

  This version add a nonce handshake (messages 4, 5) at the end of Denning-Sacco shared key 
  to prevent the attack from [Low97].

  The nonces of Needham Schroeder Symmetric Key (for mutual authentication of A and B) have been replaced by a timestamp T.

  The shared symmetric key established by the protocol is Kab.

  We consider here the tagged version of this protocol.
