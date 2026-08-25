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

## Protocol description (natural language)

Example for the Tamarin Prover
  ==============================

  Authors:        Stéphanie Delaune (CODAGE EN COURS)
  Date:           March 2020
  Time:            ??

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/yahalomBAN.html)

  BAN simplified version of Yahalom

  A, B, S :    principal
  Na, Nb :    number fresh
  Kas, Kbs, Kab :    key

  A knows :    A, B, S, Kas
  B knows :    B, S, Kbs
  S knows :    S, A, B, Kas, Kbs

  1.    A  ->  B  :    A, Na
  2.    B  ->  S  :    B, Nb, {A, Na}Kbs
  3.    S  ->  A  :    Nb, {B, Kab, Na}Kas, {A, Kab, Nb}Kbs
  4.    A  ->  B  :    {A, Kab, Nb}Kbs, {Nb}Kab

  The fresh symmetric shared key Kab is created by the server S
  and sent encrypted, in message 3 both to A (directly) and to B (indirectly).

  Compared to the original version of the Yahalom protocol,
  the nonce Nb is added to the second cipher of message 3,
  to prevent a malicious A to reuse an old value of Kab.

  Also, Nb is sent in cleartext in message 2, which makes possible the attacks below.

  The protocol must guaranty the secrecy of Kab: in every session,
  the value of Kab must be known only by the participants playing the roles of A, B and S.

  We consider here the tagged version of this protocol.
