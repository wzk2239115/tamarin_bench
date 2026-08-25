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
| 1 | `secrecy` | all-traces | secrecy |
| 2 | `injectiveagreement_A` | all-traces | injectiveagreement a |
| 3 | `injectiveagreement_B` | all-traces | injectiveagreement b |
| 4 | `noninjectiveagreement_A` | all-traces | noninjectiveagreement a |
| 5 | `noninjectiveagreement_B` | all-traces | noninjectiveagreement b |
| 6 | `Session_key_honest_setup` | exists-trace | session key honest setup |

## Protocol description (natural language)

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
