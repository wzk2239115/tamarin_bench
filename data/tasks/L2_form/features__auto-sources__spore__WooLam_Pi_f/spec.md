# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: executability, secrecy, injectiveagreement b, agreement b.

---

Example for the Tamarin Prover
  ==============================

  Authors:       Jannik Dreier
  Date:             April 2020
  Time:                 ?

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/wooLamPif.html)

  Woo and Lam Pi f

  A, B, S :   	principal
  shared :   	(principal, principal):key
  Nb :   	nonce

  1.   	A 	-> 	B 	:   	A
  2.   	B 	-> 	A 	:   	Nb
  3.   	A 	-> 	B 	:   	{A,B,Nb}shared(A, S)
  4.  	B 	-> 	S 	:   	{A, B, Nb, {A, B, Nb}shared(A, S)}shared(B, S)
  5.   	S 	-> 	B 	:   	{A, B, Nb}shared(B, S)

  shared(A, S) is a long term symmetric key shared by A and S.
  Initially, A only knowns shared(A, S) and the name of B,
  B only knowns shared(B, S)
  and S knowns all shared keys,
  i.e. S given any principal's name X, S knowns shared(X, S),
  or in other terms, S knows the ``function'' shared.

  Woo and Lam give the following definition of correctness for this protocol:

  whenever the principal B finishes the execution of the protocol,
  the initiator of the protocol execution is in fact the principal A claimed in message 1.

  We model a variant with tags, and consider only one server.
