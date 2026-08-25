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
| 23 | `acc_VoterC_excl_0_4` | all-traces | acc voterc excl 0 4 |
| 24 | `acc_VoterC_excl_0_5` | all-traces | acc voterc excl 0 5 |
| 25 | `acc_VoterC_excl_0_6` | all-traces | acc voterc excl 0 6 |
| 26 | `acc_VoterC_excl_0_7` | all-traces | acc voterc excl 0 7 |
| 27 | `acc_VoterC_excl_1_2` | all-traces | acc voterc excl 1 2 |
| 28 | `acc_VoterC_excl_1_3` | all-traces | acc voterc excl 1 3 |
| 29 | `acc_VoterC_excl_1_4` | all-traces | acc voterc excl 1 4 |
| 30 | `acc_VoterC_excl_1_5` | all-traces | acc voterc excl 1 5 |
| 31 | `acc_VoterC_excl_1_6` | all-traces | acc voterc excl 1 6 |
| 32 | `acc_VoterC_excl_1_7` | all-traces | acc voterc excl 1 7 |
| 33 | `acc_VoterC_excl_2_3` | all-traces | acc voterc excl 2 3 |
| 34 | `acc_VoterC_excl_2_4` | all-traces | acc voterc excl 2 4 |
| 35 | `acc_VoterC_excl_2_5` | all-traces | acc voterc excl 2 5 |
| 36 | `acc_VoterC_excl_2_6` | all-traces | acc voterc excl 2 6 |
| 37 | `acc_VoterC_excl_2_7` | all-traces | acc voterc excl 2 7 |
| 38 | `acc_VoterC_excl_3_4` | all-traces | acc voterc excl 3 4 |
| 39 | `acc_VoterC_excl_3_5` | all-traces | acc voterc excl 3 5 |
| 40 | `acc_VoterC_excl_3_6` | all-traces | acc voterc excl 3 6 |
| 41 | `acc_VoterC_excl_3_7` | all-traces | acc voterc excl 3 7 |
| 42 | `acc_VoterC_excl_4_5` | all-traces | acc voterc excl 4 5 |
| 43 | `acc_VoterC_excl_4_6` | all-traces | acc voterc excl 4 6 |
| 44 | `acc_VoterC_excl_4_7` | all-traces | acc voterc excl 4 7 |
| 45 | `acc_VoterC_excl_5_6` | all-traces | acc voterc excl 5 6 |
| 46 | `acc_VoterC_excl_5_7` | all-traces | acc voterc excl 5 7 |
| 47 | `acc_VoterC_excl_6_7` | all-traces | acc voterc excl 6 7 |
| 48 | `acc_VoterC_exh` | all-traces | acc voterc exh |
| 49 | `acc_VoterC_suf_0` | exists-trace | acc voterc suf 0 |
| 50 | `acc_VoterC_suf_1` | exists-trace | acc voterc suf 1 |
| 51 | `acc_VoterC_suf_2` | exists-trace | acc voterc suf 2 |
| 52 | `acc_VoterC_ver_empty_7` | all-traces | acc voterc ver empty 7 |
| 53 | `acc_VoterC_ver_nonempty_0` | all-traces | acc voterc ver nonempty 0 |
| 54 | `acc_VoterC_ver_nonempty_1` | all-traces | acc voterc ver nonempty 1 |
| 55 | `acc_VoterC_ver_nonempty_2` | all-traces | acc voterc ver nonempty 2 |
| 56 | `acc_VoterC_ver_nonempty_3` | all-traces | acc voterc ver nonempty 3 |
| 57 | `acc_VoterC_ver_nonempty_4` | all-traces | acc voterc ver nonempty 4 |
| 58 | `acc_VoterC_ver_nonempty_5` | all-traces | acc voterc ver nonempty 5 |
| 59 | `acc_VoterC_ver_nonempty_6` | all-traces | acc voterc ver nonempty 6 |
| 60 | `acc_VoterC_min_0_0` | all-traces | acc voterc min 0 0 |
| 61 | `acc_VoterC_min_1_0` | all-traces | acc voterc min 1 0 |
| 62 | `acc_VoterC_min_2_0` | all-traces | acc voterc min 2 0 |
| 63 | `acc_VoterC_uniq_sing_0` | all-traces | acc voterc uniq sing 0 |
| 64 | `acc_VoterC_uniq_sing_1` | all-traces | acc voterc uniq sing 1 |
| 65 | `acc_VoterC_uniq_sing_2` | all-traces | acc voterc uniq sing 2 |
| 66 | `acc_TimelyP_excl_0_1` | all-traces | acc timelyp excl 0 1 |
| 67 | `acc_TimelyP_excl_0_2` | all-traces | acc timelyp excl 0 2 |
| 68 | `acc_TimelyP_excl_0_3` | all-traces | acc timelyp excl 0 3 |
| 69 | `acc_TimelyP_excl_0_4` | all-traces | acc timelyp excl 0 4 |
| 70 | `acc_TimelyP_excl_0_5` | all-traces | acc timelyp excl 0 5 |
| 71 | `acc_TimelyP_excl_0_6` | all-traces | acc timelyp excl 0 6 |
| 72 | `acc_TimelyP_excl_0_7` | all-traces | acc timelyp excl 0 7 |
| 73 | `acc_TimelyP_excl_1_2` | all-traces | acc timelyp excl 1 2 |
| 74 | `acc_TimelyP_excl_1_3` | all-traces | acc timelyp excl 1 3 |
| 75 | `acc_TimelyP_excl_1_4` | all-traces | acc timelyp excl 1 4 |
| 76 | `acc_TimelyP_excl_1_5` | all-traces | acc timelyp excl 1 5 |
| 77 | `acc_TimelyP_excl_1_6` | all-traces | acc timelyp excl 1 6 |
| 78 | `acc_TimelyP_excl_1_7` | all-traces | acc timelyp excl 1 7 |
| 79 | `acc_TimelyP_excl_2_3` | all-traces | acc timelyp excl 2 3 |
| 80 | `acc_TimelyP_excl_2_4` | all-traces | acc timelyp excl 2 4 |
| 81 | `acc_TimelyP_excl_2_5` | all-traces | acc timelyp excl 2 5 |
| 82 | `acc_TimelyP_excl_2_6` | all-traces | acc timelyp excl 2 6 |
| 83 | `acc_TimelyP_excl_2_7` | all-traces | acc timelyp excl 2 7 |
| 84 | `acc_TimelyP_excl_3_4` | all-traces | acc timelyp excl 3 4 |
| 85 | `acc_TimelyP_excl_3_5` | all-traces | acc timelyp excl 3 5 |
| 86 | `acc_TimelyP_excl_3_6` | all-traces | acc timelyp excl 3 6 |
| 87 | `acc_TimelyP_excl_3_7` | all-traces | acc timelyp excl 3 7 |
| 88 | `acc_TimelyP_excl_4_5` | all-traces | acc timelyp excl 4 5 |
| 89 | `acc_TimelyP_excl_4_6` | all-traces | acc timelyp excl 4 6 |
| 90 | `acc_TimelyP_excl_4_7` | all-traces | acc timelyp excl 4 7 |
| 91 | `acc_TimelyP_excl_5_6` | all-traces | acc timelyp excl 5 6 |
| 92 | `acc_TimelyP_excl_5_7` | all-traces | acc timelyp excl 5 7 |
| 93 | `acc_TimelyP_excl_6_7` | all-traces | acc timelyp excl 6 7 |
| 94 | `acc_TimelyP_exh` | all-traces | acc timelyp exh |
| 95 | `acc_TimelyP_suf_0` | exists-trace | acc timelyp suf 0 |
| 96 | `acc_TimelyP_suf_1` | exists-trace | acc timelyp suf 1 |
| 97 | `acc_TimelyP_suf_2` | exists-trace | acc timelyp suf 2 |
| 98 | `acc_TimelyP_ver_empty_7` | all-traces | acc timelyp ver empty 7 |
| 99 | `acc_TimelyP_ver_nonempty_0` | all-traces | acc timelyp ver nonempty 0 |
| 100 | `acc_TimelyP_ver_nonempty_1` | all-traces | acc timelyp ver nonempty 1 |
| 101 | `acc_TimelyP_ver_nonempty_2` | all-traces | acc timelyp ver nonempty 2 |
| 102 | `acc_TimelyP_ver_nonempty_3` | all-traces | acc timelyp ver nonempty 3 |
| 103 | `acc_TimelyP_ver_nonempty_4` | all-traces | acc timelyp ver nonempty 4 |
| 104 | `acc_TimelyP_ver_nonempty_5` | all-traces | acc timelyp ver nonempty 5 |
| 105 | `acc_TimelyP_ver_nonempty_6` | all-traces | acc timelyp ver nonempty 6 |
| 106 | `acc_TimelyP_min_0_0` | all-traces | acc timelyp min 0 0 |
| 107 | `acc_TimelyP_min_1_0` | all-traces | acc timelyp min 1 0 |
| 108 | `acc_TimelyP_min_2_0` | all-traces | acc timelyp min 2 0 |
| 109 | `acc_TimelyP_uniq_sing_0` | all-traces | acc timelyp uniq sing 0 |
| 110 | `acc_TimelyP_uniq_sing_1` | all-traces | acc timelyp uniq sing 1 |
| 111 | `acc_TimelyP_uniq_sing_2` | all-traces | acc timelyp uniq sing 2 |

## Protocol description (natural language)

* Protocol: MixVote (accountability)
 * Modeler   (original): Lara Schmid
 * Modeler   (accountability): Kevin Morio and Robert Künnemann
 * Date:     Sep 2020
 * Source:	 "Dispute Resolution in Voting", David Basin, Sasa Radomirovic, and Lara Schmid, CSF20
 * Status:   working (deprecated)
