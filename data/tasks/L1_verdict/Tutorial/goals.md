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
| 1 | `Client_session_key_secrecy` | all-traces | client session key secrecy |
| 2 | `Client_auth` | all-traces | client auth |
| 3 | `Client_auth_injective` | all-traces | client auth injective |
| 4 | `Client_session_key_honest_setup` | exists-trace | client session key honest setup |

## Protocol description (natural language)

Tutorial for the Tamarin prover for security protocol analysis
==============================================================

Authors: 	Simon Meier, Benedikt Schmidt
Date: 	        September 2012

Introduction
------------

This user guide assumes that you have a copy of the submitted draft of Meier's
PhD thesis, which is  available from
http://www.infsec.ethz.ch/research/software/tamarin.

The input files for the Tamarin prover have the extension .spthy, which is
short for 'security protocol theory'. A security protocol theory specifies

  1. the signature and equational theory to use for the message algebra,
  2. the set of multiset rewriting rules modeling the protocol and
     the adversary capabilities, and
  3. the guarded trace properties whose satisfiability or validity we wish to
     check for this set of multiset rewriting rules.

We explain each of these parts where they occur in the following security
protocol theory. Before we start, let us add a few notes on the syntax.
As you probably noticed, comments are C-style. All identifiers are
case-sensitive. The parser is layout-insensitive, i.e., your are free to use
whitespace as it suits you. We provide a complete specification of the input
syntax in the REFERENCE MANUAL (available at doc/MANUAL.md).

Modeling a security protocol
----------------------------

Every security protocol theory starts with a header of the following form.
