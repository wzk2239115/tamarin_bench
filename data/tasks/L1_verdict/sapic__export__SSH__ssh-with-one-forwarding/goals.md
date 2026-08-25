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
| 1 | `reach` | exists-trace | reach |
| 2 | `reach_nested` | exists-trace | reach nested |
| 3 | `secretP` | all-traces | secretp |
| 4 | `injPS` | all-traces | injps |
| 5 | `injSP` | all-traces | injsp |
| 6 | `secretS` | all-traces | secrets |

## Protocol description (natural language)

* Protocol: SSH, with a single agent forwarding

   Proverif : everything in a 2 seconds.

   Tamarin : everything in 5 minutes.

   <!> We add a conditional test not in the program inside the remote P execution, that allows to close the sources of Tamarin. It should not change the security of the protocol, as if the check fails here, it would fail on the server side.
      This check is not required for Proverif to prove the protocol.
