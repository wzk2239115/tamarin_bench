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
  (http://www.lsv.fr/Software/spore/andrew.html)

  Andrew Secure RPC Protocol

  A, B :  principal
  Kab, K'ab :  symkey
  Na, Nb, N'b :  nonce
  succ :  nonce -> nonce

  1.  A  ->  B  :  A, {Na}Kab
  2.  B  ->  A  :  {succNa, Nb}Kab
  3.  A  ->  B  :  {succNb}Kab
  4.  B  ->  A  :  {K'ab, N'b}Kab

  The protocol must guaranty the secrecy of the new shared key K'ab:
  in every session, the value of K'ab must be known only by the participants playing the roles of A and B.

  The protocol must guaranty the authenticity of K'ab:
  in every session, on reception of message 4,
  A must be ensured that the key K'ab in the message has been created by A in the same session.

  The message 4 contains nothing that A knows to be fresh.
  Hence, an intruder I can replay this message in another session of the protocol
  to convinced B to accept an old compromised key.
  i.1.   A  ->  B  :  A, {Na}Kab
  i.2.   B  ->  A  :  {succNa, Nb}Kab
  i.3.   A  ->  B  :  {succNb}Kab
  i.4.   B  ->  A  :  {K'ab, N'b}Kab
  ii.1.  A  ->  B  :  A, {Ma}Kab
  ii.2.  B  ->  A  :  {succMa, Mb}Kab
  ii.3.  A  ->  B  :  {succMb}Kab
  ii.4.  B  ->  I(A)  :  {K''ab, M'b}Kab
  ii.4.  I(B)  ->  A  :  {K'ab, N'b}Kab

  We model a variant with tags.
