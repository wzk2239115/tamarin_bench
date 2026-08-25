# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: executability, secrecy, injectiveagreement b, agreement b, injectiveagreement a, agreement a.

---

Example for the Tamarin Prover
  ==============================

  Authors:       Jannik Dreier
  Date:             April 2020
  Time:                ?

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/spliceas3.html)

  Clark and Jacob modified Hwang and Chen modified SPLICE/AS

  S, C, AS :   	principal
  N1, N2, N3 :   	nonce
  T :   	timestamp
  L :   	lifetime
  pk, sk :   	principal -> key (keypair)

  1.   	C 	-> 	AS 	:   	C, S, N1
  2.   	AS 	-> 	C 	:   	AS, {AS, C, N1, S, pk(S)}sk(AS)
  3.   	C 	-> 	S 	 :   	C, S, {T, L, {C, N2}pk(S)}sk(C)
  4.   	S 	-> 	AS 	:   	S, C, N3
  5.   	AS 	-> 	S 	:   	AS, {AS, S, N3, C, pk(C)}sk(AS)
  6.   	S 	-> 	C 	 :   	S, C, {inc(N2)}pk(C)

  This protocol is an optimised version of the following modification of Hwang and Chen modified SPLICE/AS:
  1.   	C 	-> 	AS 	:   	C, S, N1
  2.   	AS 	-> 	C 	:   	AS, {AS, C, N1, S, pk(S)}sk(AS)
  3.   	C 	-> 	S 	 :   	C, S, {C, T, L, {C, N2}pk(S)}sk(C)
  4.   	S 	-> 	AS 	:   	S, C, N3
  5.   	AS 	-> 	S 	:   	AS, {AS, S, N3, C, pk(C)}sk(AS)
  6.   	S 	-> 	C 	 :   	S, C, {S, inc(N2)}pk(C)
  The messages 3 and 6 are optimised by suppressing some redundancies:
  the redundant C is not included in the signed part of message 3 and S in not included in the cipher of message 6

  Note that the name of the owner of the public key is included in certificate
  to overcomes the flaws of SPLICE/AS presented in [HC95]
  (i.e. a certificate for the public key pk(S) is here {AS, C, N1, S, pk(S)}sk(AS)
  rather than {AS, C, N1, pk(S)}sk(AS) in SPLICE/AS).

  key is the type of public/private keys.
  The functions pk and sk associate to a principal's name its public key, resp. private key.

  We assume that initially, the client C and the server S only know their own public and private key,
  and that the authority AS known the function pk, i.e. he knows everyone's public key.

  {AS, C, N1, pk(S)}sk(AS) (in message 2) and {AS, S, N3, pk(C)}sk(AS) (in message 5)
  are certificates signed and distributed by the authority AS, for the respective public keys pk(S) and pk(C).

  After a successfull run of the protocol,
  the value of N2 can be used by C and S as a symmetric key for secure communications.

  The protocol must guaranty the secrecy of N2: in every session,
  the value of N2 must be known only by the participants playing the roles of C, S.

  The protocol must also ensure C that S has received N2 and S that the N2 he has received in message 3 originated from C.

  Lowe demonstrate a multiplicity attack on this protocol,
  where I impersonates C in a new session ii, by replaying message 3 of session i. I does however not learn N2.
  i.1.   	C 	-> 	AS 	:   	C, S, N1
  i.2.   	AS 	-> 	C 	:   	AS, {AS, C, N1, S, pk(S)}sk(AS)
  i.3.   	C 	-> 	S 	:   	C, S, {T, L, {C, N2}pk(S)}sk(C)
  i.4.   	S 	-> 	AS 	:   	S, C, N3
  i.5.   	AS 	-> 	S 	:   	AS, {AS, S, N3, C, pk(C)}sk(AS)
  i.6.   	S 	-> 	C 	:   	S, C, {inc(N2)}pk(C)
  ii.3.   	I(C) 	-> 	S 	:   	C, S, {T, L, {C, N2}pk(S)}sk(C)
  ii.4.   	S 	-> 	AS 	:   	S, C, N'3
  ii.5.   	AS 	-> 	S 	:   	AS, {AS, S, N'3, C, pk(C)}sk(AS)
  ii.6.   	S 	-> 	I(C) 	:   	S, C, {inc(N2)}pk(C)
  Lowe suggests to add a nonce challenge to prevent this attack.

  We model a variant with tags, and assume a single authority AS.
