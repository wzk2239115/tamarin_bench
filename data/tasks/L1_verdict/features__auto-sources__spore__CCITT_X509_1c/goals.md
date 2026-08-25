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
| 4 | `Session_key_honest_setup` | exists-trace | session key honest setup |

## Protocol description (natural language)

Example for the Tamarin Prover
  ==============================

  Authors:       Jannik Dreier
  Date:             April 2020
  Time:                      ?

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/ccittx509_1c.html)

  CCITT X.509 (1c)

  A, B :    principal
  Na, Nb :    nonce
  Ta, Tb :    timestamp
  Ya, Yb :    userdata
  Xa, Xb :    userdata
  PK, SK :    principal -> key (keypair)
  h :    userdata -> userdata (one-way)

  Spore specification
  1.    A  ->  B  :    A, {Ta, Na, B, Xa, {Ya, {h(Ya)}SK(A)}PK(B)}SK(A)
  Reconstruction to fit the original specification
  1.    A  ->  B  :    A, Ta, Na, B, Xa, {Ya, {h(Ya)}SK(A)}PK(B), {h(Ta, Na, B, Xa, {Ya, {h(Ya)}SK(A)}PK(B))}SK(A)

  h is a one-way function.

  The timestamp Ta and nonce Na are not used here.
  Xa and Ya are the data transmitted,
  the privacy of Ya is ensured by its encryption with the public key of B and
  the authenticity of Xa and Ya is ensured by the encryption with the private key of A.

  The protocol must ensure the confidentiality of Ya:
    if A and B follow the protocol,
    then an attacker should not be able to obtain Ya.

  The protocol must ensure the recipient B of the message that the data Xa and Ya originate from A.
