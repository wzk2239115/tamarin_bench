# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: auth.

---

toy example from the paper

Reachability query verified with
 $ tamarin-prover toy-example.spthy --prove
 $ tamarin-prover toy-example.spthy -m=proverif > te-reach.pv; proverif te-reach.pv

Unlinkability query "cannot be proved" with
 $ tamarin-prover toy-example.spthy -m=proverifequiv > te-un.pv; proverif te-un.pv

Unlinkability disproved with:
 $ tamarin-prover toy-example.spthy -m=deepsec > te-un.ds; deepsec te-un.ds
