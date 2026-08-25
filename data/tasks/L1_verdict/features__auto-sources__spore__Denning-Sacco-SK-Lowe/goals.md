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
| 2 | `secrecy` | all-traces | secrecy |
| 3 | `noninjectiveagreement_B` | all-traces | noninjectiveagreement b |
| 4 | `noninjectiveagreement_A` | all-traces | noninjectiveagreement a |
| 5 | `injectiveagreement_B` | all-traces | injectiveagreement b |
| 6 | `injectiveagreement_A` | all-traces | injectiveagreement a |

## Protocol description (natural language)

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
