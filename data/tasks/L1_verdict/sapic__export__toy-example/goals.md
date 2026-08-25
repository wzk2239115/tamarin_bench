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
| 1 | `Auth` | all-traces | auth |

## Protocol description (natural language)

toy example from the paper

Reachability query verified with
 $ tamarin-prover toy-example.spthy --prove
 $ tamarin-prover toy-example.spthy -m=proverif > te-reach.pv; proverif te-reach.pv

Unlinkability query "cannot be proved" with
 $ tamarin-prover toy-example.spthy -m=proverifequiv > te-un.pv; proverif te-un.pv

Unlinkability disproved with:
 $ tamarin-prover toy-example.spthy -m=deepsec > te-un.ds; deepsec te-un.ds
