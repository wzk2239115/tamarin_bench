# Verification goals

You are given the protocol theory in `theory.spthy`. The theory is complete
**except for its security lemmas**, which have been removed. Your job is to:

1. Formulate a security lemma for **each** goal listed below, using the given
   lemma names (Tamarin will match them when grading).
2. Run the Tamarin prover and drive the analysis to completion: every lemma
   must terminate with `verified` or `falsified - found trace`.
3. Produce the deliverables described in the task README
   (`final.spthy`, `verdict.json`, `attack_report.md` if unsafe).

Notes:

- Lemma statements are yours to write; the quantifier column is binding.
- Helper/source lemmas beyond the listed goals are allowed (and often
  needed to make the prover terminate).
- Some theories use `diff()` terms (observational equivalence):
  analyzing them requires `tamarin-prover --diff`.

## Goals to formalize

| # | Lemma name | Quantifier | Property |
|---|------------|------------|----------|
| 1 | `executability` | exists-trace | executability |
| 2 | `Secrecy` | all-traces | secrecy |
| 3 | `injectiveagreement_B` | all-traces | injectiveagreement b |
| 4 | `agreement_B` | all-traces | agreement b |

## Protocol description (natural language)

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
