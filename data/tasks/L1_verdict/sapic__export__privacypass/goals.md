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
| 1 | `true_honnestauthRI` | all-traces | true honnestauthri |
| 2 | `false_exec` | all-traces | false exec |

## Protocol description (natural language)

* Protocol:    Privacy Pass
   https://tools.ietf.org/html/draft-davidson-pp-protocol-01

   We verify both reachability and equivalence properties.

   Proverif: everything in a second
    tamarin-prover privacypass.spthy -m=proverif > pp-reach.pv; proverif pp-reach.pv
    tamarin-prover privacypass.spthy -m=proverifequiv > pp-ind.pv; proverif pp-ind.pv

   Tamarin : everything in a few seconds
    tamarin-prover privacypass.spthy --prove

We rely on a an abstract VOPRF, has described in
https://tools.ietf.org/html/draft-irtf-cfrg-voprf-03#section-4.2.2
To follow the notations of privacy pass, we rename k as sk and Y has pkV(sk),

VOPRF
Setup phase
V --------- P
            new sk ;
 <-- pkV(sk) ------

Evalution phase
V(x,aux,pkS) ----------- P(sk,pkV(sk))
(r,M) = VBlind(x)
   ------------ M  --------->
                       ZD = VEvaluate(sk,pkV(sk),M)
  <-------- ZD -------------
N = VUnblind(r,pkS,M,ZD)
ret VFinalize(x,pkS,N,aux)

ZD = VEvaluate(sk,pkV(sk),M)
VFinalize(x, pkV(sk) , VUnblind(r,pkV(sk),M,ZD), aux)
      == H_2(H_2(DST, x .. F(sk,x)), aux)

DST := Domain Separation Label (tag), F PRF, and H_2 hash function
