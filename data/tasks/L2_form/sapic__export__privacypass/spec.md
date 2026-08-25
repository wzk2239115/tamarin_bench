# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: true honnestauthri, false exec.

---

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
