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
  (http://www.lsv.fr/Software/spore/andrewBAN.html)

  Modified version of Andrew Secure RPC correcting a freshness flaw. Exchanged of a fresh shared key, Symmetric key cryptography.

  Protocol specification (in common syntax)
  A, B :  	principal
  Kab, K'ab :  	symkey
  Na, Nb, N'b :  	nonce
  succ :  	nonce -> nonce

  1.  	A	->	B	:  	A, {Na}Kab
  2.  	B	->	A	:  	{succNa, Nb}Kab
  3.  	A	->	B	:  	{succNb}Kab
  4.  	B	->	A	:  	{K'ab, N'b, Na}Kab

  The nonce Na has been added to the message 4 of Andrew Secure RPC to prevent the flow presented in Andrew Secure RPC.

  We model a variant with tags.
