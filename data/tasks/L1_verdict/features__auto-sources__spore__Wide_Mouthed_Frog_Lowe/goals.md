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
| 7 | `injectiveagreement_A` | all-traces | injectiveagreement a |
| 8 | `agreement_A` | all-traces | agreement a |

## Protocol description (natural language)

Example for the Tamarin Prover
  ==============================

  Authors:       Jannik Dreier
  Date:             April 2020
  Time:                 ?

  Description from SPORE:
  (http://www.lsv.fr/Software/spore/wideMouthedFrogLowe.html)

  Lowe modified Wide Mouthed Frog

  A, S :   	principal
  Kas, Kbs, Kab :   	symkey
  Nb :   	nonce
  Ta, Ts :   	timestamp
  suc :   	nonce -> nonce

  1.   	A 	-> 	S 	:   	A, {Ta, B, Kab}Kas
  2.   	S 	-> 	B 	:   	{Ts, A, Kab}Kbs
  3.   	B 	-> 	A 	:   	{Nb}Kab
  4.   	A 	-> 	B 	:   	{succ(Nb)}Kab

  Two messages have been appened to Wide Mouthed Frog for mutual authentification of A and B (nonce handshake).

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

  We model a variant with tags.
