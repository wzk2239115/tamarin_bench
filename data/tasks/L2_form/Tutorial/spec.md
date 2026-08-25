# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: client session key secrecy, client auth, client auth injective, client session key honest setup.

---

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
