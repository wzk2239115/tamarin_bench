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
| 5 | `injectiveagreement_S` | all-traces | injectiveagreement s |
| 6 | `agreement_S` | all-traces | agreement s |

## Protocol description (natural language)

Example for the Tamarin Prover
  ==============================

  Authors:       Jannik Dreier
  Date:             April 2020
  Time:                ?

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/wideMouthedFrog.html)

  Wide Mouthed Frog

  A, S :    principal
  Kas, Kbs, Kab :    symkey
  Ta, Ts :    timestamp

  1.    A  ->  S  :    A, {Ta, B, Kab}Kas
  2.    S  ->  B  :    {Ts, A, Kab}Kbs

  "It is assumed that the encryption is done in such a way that we know the whole message was sent at once.
  If two separate encrypted sections are included in one message,
  we treat them as though they arrived in separate messages.
  A message cannot be understood by a principal who does not know the key
  (or, in the case of public-key cryptography, by a principal who does not know the inverse of the key);
  the key cannot be deduced from the encrypted message.
  Each encrypted message contains sufficient redundancy to allow a principal who decrypts it to verify that he has used the right key.
  In addition, messages contain sufficient information for a principal to detect (and ignore) his own messages."

  "A sends a session key to S, including a timestamp Ta.
  S checks that the first message is timely,
  and if it is, it forwards the message to B, together with its own timestamp Ts.
  B then checks that the timestamp from S is later than any other it has received from S."

  A sends a session key to S, including a timestamp Ta.
  S checks that the first message is timely,
  and if it is, it forwards the message to B, together with its own timestamp Ts.
  B then checks that the timestamp from S is later than any other it has received from S

  The protocol must guaranty the secrecy of the new shared key Kab: in every session,
  the value of Kab must be known only by the participants playing the roles of A and B and S.

  The protocol must guaranty the authenticity of Kab: in every session,
  on reception of message 2, B must be ensured that the key Kab in the message
  has been created by S in the same session on behalf of A.

  By replaying the second message within an appropriate time window,
  the intruder I can make the server S update the timestamp of an non-fresh key Kab.
  This way, he can extend the life time of a (possibly compromised) key Kab as wanted,
  whereas A and B think that it has expired and has been destroyed.
   i.1.   	 A 	  -> 	S 	:   	A, {Ta, B, Kab}Kas
   i.2.   	 S 	  -> 	B 	:   	{Ts, A, Kab}Kbs
   ii.1.   	I(B) -> 	S 	:   	B, {Ts, A, Kab}Kbs
   ii.2.   	S 	  -> 	A 	:   	{T's, B, Kab}Kas
   iii.1.   I(A) -> 	S 	:   	A, {T's, B, Kab}Kas
   iii.2.   S 	  -> 	B 	:   	{T''s, A, Kab}Kbs
   ....

  In this attack, B thinks that A has established two sessions with him,
  when A thinks he has established only one session.
   i.1.   	A 	-> 	S 	:   	A, {Ta, B, Kab}Kas
   i.2.   	S 	-> 	B 	:   	{Ts, A, Kab}Kbs
   ii.2.   S 	-> 	B 	:   	{Ts, A, Kab}Kbs

  We model a variant with tags.
