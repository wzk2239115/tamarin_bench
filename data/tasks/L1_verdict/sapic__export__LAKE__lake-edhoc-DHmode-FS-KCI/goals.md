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
| 1 | `executableR1` | exists-trace | executabler1 |
| 2 | `executableR2` | exists-trace | executabler2 |
| 3 | `executableI` | exists-trace | executablei |
| 4 | `secretR` | all-traces | secretr |
| 5 | `secretI` | all-traces | secreti |
| 6 | `honnestauthRI` | all-traces | honnestauthri |
| 7 | `honnestauthIR` | all-traces | honnestauthir |

## Protocol description (natural language)

* Protocol:   LAKE
   https://datatracker.ietf.org/doc/html/draft-ietf-lake-edhoc-02

   A lightweight DD based key exchange.

   It comes with two possible modes, either a signature is used for
   authentication, or a long term dh key.
   This file proposes the two modes, with I1 or I2.

   We also  provide a model of dynamic compromission.

   Proverif : 16 seconds

   Tamarin : 2 minutes with 10 cores
