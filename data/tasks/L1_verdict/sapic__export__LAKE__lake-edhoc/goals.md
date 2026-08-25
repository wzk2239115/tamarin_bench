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
| 1 | `secretR` | all-traces | secretr |
| 2 | `secretI` | all-traces | secreti |
| 3 | `executableR` | exists-trace | executabler |
| 4 | `executableI` | exists-trace | executablei |
| 5 | `executableIhonnest` | exists-trace | executableihonnest |
| 6 | `executableRhonnest` | exists-trace | executablerhonnest |
| 7 | `false_dishonnestnoauthRI` | all-traces | false dishonnestnoauthri |
| 8 | `false_dishonnestnoauthIR` | all-traces | false dishonnestnoauthir |
| 9 | `honnestauthRI` | all-traces | honnestauthri |
| 10 | `honnestauthIR` | all-traces | honnestauthir |

## Protocol description (natural language)

* Protocol:    LAKE
   https://datatracker.ietf.org/doc/html/draft-ietf-lake-edhoc-02

   A lightweight DH based key exchange.

   It comes with two possible modes, either a signature is used for
   authentication, or a long term dh key. This file present the signature only
   version.

   Proverif : everything in a few seconds.

   Tamarin : everything in 1 minutes on colosseus.
