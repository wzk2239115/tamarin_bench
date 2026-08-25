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
| 1 | `Secrecy` | all-traces | secrecy |
| 2 | `injectiveagreement_B` | all-traces | injectiveagreement b |
| 3 | `agreement_B` | all-traces | agreement b |
| 4 | `injectiveagreement_A` | all-traces | injectiveagreement a |
| 5 | `agreement_A` | all-traces | agreement a |
| 6 | `Session_key_honest_setup` | exists-trace | session key honest setup |

## Protocol description (natural language)

Example for the Tamarin Prover
  ==============================

  Authors:       Jannik Dreier
  Date:             April 2020
  Time:                 ?

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/ccittx509_3.html)

  CCITT X.509 (3)

  A, B :    principal
  Na, Nb :    nonce
  Ta, Tb :    timestamp
  Ya, Yb :    userdata
  Xa, Xb :    userdata
  PK, SK :    principal -> key (keypair)

  Spore simplification
  1.    A  ->  B  :    A, {Ta, Na, B, Xa, {Ya}PK(B)}SK(A)
  2.    B  ->  A  :    B, {Tb, Nb, A, Na, Xb, {Yb}PK(A)}SK(B)
  3.    A  ->  B  :    A, {Nb}SK(A)
  Spore reminder of actual specification
  1.    A  ->  B  :    A, Ta, Na, B, Xa, {Ya}PK(B), {h(Ta, Na, B, Xa, {Ya}PK(B))}SK(A)
  2.    B  ->  A  :    B, Tb, Nb, A, Na, Xb, {Yb}PK(A), {h(B, Tb, Nb, A, Na, Xb, {Yb}PK(A))}SK(B)
  3.    A  ->  B  :    A, {Nb}SK(A)

  h is a one-way function.

  The protocol must ensure the confidentiality of Ya and Yb:
    if A and B follow the protocol, then an attacker should not be able to obtain Ya or Yb.

  The protocol must ensure the recipient B of the message 1 that the data Xa and Ya originate from A.

  The protocol must ensure the recipient A of the message 2 that the data Xb and Yb originate from B.

  This parallel session attack presented in [BAN89] works if B does not check the timestamp Ta in the first message.
  i.1.      A  ->  I(B)  :    A, {Ta, Na, B, Xa, {Ya}PK(B)}SK(A)
  i.1.      I(A)  ->  B  :    A, {Ta, Na, B, Xa, {Ya}PK(B)}SK(A)
  i.2.      B  ->  I(A)  :    B, {Tb, Nb, A, Na, Xb, {Yb}PK(A)}SK(B)
  ii.1.    A  ->  I  :      A, {Ta', Na', C, Xa', {Ya'}PK(I)}SK(A)
  ii.2.    I  ->  A  :      I, {Ti, Nb, A, N'a,Xi, {Yi}PK(A)}SK(I)
  ii.3.    A  ->  I  :      A, {Nb}SK(A)
  ii.3.    I(A)  ->  B  :    A, {Nb}SK(A)

  Another attack can be found in :
    Colin l'Anson and Chris Mitchell.
    Security defects in the ccitt recomendation x.509 - the directory authentication framework.
    Computer Communication Review, 20(2):30--34, april 1990.
      http://www.chrismitchell.net/sdicrx.pdf
      (authentication failure by replay considering no checking of timestamps)
      (is similar to the previous attack)
