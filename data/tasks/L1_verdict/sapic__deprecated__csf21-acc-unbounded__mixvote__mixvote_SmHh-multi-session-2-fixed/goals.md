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
| 1 | `onlyonce1` | all-traces | onlyonce1 |
| 2 | `onlyonce2` | all-traces | onlyonce2 |
| 3 | `onlyonce3` | all-traces | onlyonce3 |
| 4 | `onlyonce4` | all-traces | onlyonce4 |
| 5 | `onlyonce5` | all-traces | onlyonce5 |
| 6 | `onlyonce6` | all-traces | onlyonce6 |
| 7 | `onlyonce7` | all-traces | onlyonce7 |
| 8 | `onlyonce8` | all-traces | onlyonce8 |
| 9 | `onlyonce9` | all-traces | onlyonce9 |
| 10 | `onlyonce10` | all-traces | onlyonce10 |
| 11 | `functional` | exists-trace | functional |
| 12 | `indivVerif` | all-traces | indivverif |
| 13 | `VoterC` | all-traces | voterc |
| 14 | `TimelyP` | all-traces | timelyp |
| 15 | `Uniqueness` | all-traces | uniqueness |
| 16 | `secretSskD` | all-traces | secretsskd |
| 17 | `ballotsFromVoters` | all-traces | ballotsfromvoters |
| 18 | `TalliedAsRecorded` | all-traces | talliedasrecorded |
| 19 | `EligVerif` | all-traces | eligverif |
| 20 | `acc_VoterC_excl_0_1` | all-traces | acc voterc excl 0 1 |
| 21 | `acc_VoterC_excl_0_2` | all-traces | acc voterc excl 0 2 |
| 22 | `acc_VoterC_excl_0_3` | all-traces | acc voterc excl 0 3 |
| 23 | `acc_VoterC_excl_1_2` | all-traces | acc voterc excl 1 2 |
| 24 | `acc_VoterC_excl_1_3` | all-traces | acc voterc excl 1 3 |
| 25 | `acc_VoterC_excl_2_3` | all-traces | acc voterc excl 2 3 |
| 26 | `acc_VoterC_exh` | all-traces | acc voterc exh |
| 27 | `acc_VoterC_suf_0` | exists-trace | acc voterc suf 0 |
| 28 | `acc_VoterC_suf_1` | exists-trace | acc voterc suf 1 |
| 29 | `acc_VoterC_ver_empty_3` | all-traces | acc voterc ver empty 3 |
| 30 | `acc_VoterC_ver_nonempty_0` | all-traces | acc voterc ver nonempty 0 |
| 31 | `acc_VoterC_ver_nonempty_1` | all-traces | acc voterc ver nonempty 1 |
| 32 | `acc_VoterC_ver_nonempty_2` | all-traces | acc voterc ver nonempty 2 |
| 33 | `acc_VoterC_min_0_0` | all-traces | acc voterc min 0 0 |
| 34 | `acc_VoterC_min_1_0` | all-traces | acc voterc min 1 0 |
| 35 | `acc_VoterC_uniq_sing_0` | all-traces | acc voterc uniq sing 0 |
| 36 | `acc_VoterC_uniq_sing_1` | all-traces | acc voterc uniq sing 1 |
| 37 | `acc_TimelyP_excl_0_1` | all-traces | acc timelyp excl 0 1 |
| 38 | `acc_TimelyP_excl_0_2` | all-traces | acc timelyp excl 0 2 |
| 39 | `acc_TimelyP_excl_0_3` | all-traces | acc timelyp excl 0 3 |
| 40 | `acc_TimelyP_excl_1_2` | all-traces | acc timelyp excl 1 2 |
| 41 | `acc_TimelyP_excl_1_3` | all-traces | acc timelyp excl 1 3 |
| 42 | `acc_TimelyP_excl_2_3` | all-traces | acc timelyp excl 2 3 |
| 43 | `acc_TimelyP_exh` | all-traces | acc timelyp exh |
| 44 | `acc_TimelyP_suf_0` | exists-trace | acc timelyp suf 0 |
| 45 | `acc_TimelyP_suf_1` | exists-trace | acc timelyp suf 1 |
| 46 | `acc_TimelyP_ver_empty_3` | all-traces | acc timelyp ver empty 3 |
| 47 | `acc_TimelyP_ver_nonempty_0` | all-traces | acc timelyp ver nonempty 0 |
| 48 | `acc_TimelyP_ver_nonempty_1` | all-traces | acc timelyp ver nonempty 1 |
| 49 | `acc_TimelyP_ver_nonempty_2` | all-traces | acc timelyp ver nonempty 2 |
| 50 | `acc_TimelyP_min_0_0` | all-traces | acc timelyp min 0 0 |
| 51 | `acc_TimelyP_min_1_0` | all-traces | acc timelyp min 1 0 |
| 52 | `acc_TimelyP_uniq_sing_0` | all-traces | acc timelyp uniq sing 0 |
| 53 | `acc_TimelyP_uniq_sing_1` | all-traces | acc timelyp uniq sing 1 |

## Protocol description (natural language)

* Protocol: MixVote (accountability)
 * Modeler   (original): Lara Schmid
 * Modeler   (accountability): Kevin Morio and Robert Künnemann
 * Date:     Sep 2020
 * Source:	 "Dispute Resolution in Voting", David Basin, Sasa Radomirovic, and Lara Schmid, CSF20
 * Status:   working (deprecated)
