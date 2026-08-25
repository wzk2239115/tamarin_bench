# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: reach, reach nested, secretp, injps, injsp, secrets.

---

* Protocol: SSH, with a single agent forwarding

   Proverif : everything in a 2 seconds.

   Tamarin : everything in 5 minutes.

   <!> We add a conditional test not in the program inside the remote P execution, that allows to close the sources of Tamarin. It should not change the security of the protocol, as if the check fails here, it would fail on the server side.
      This check is not required for Proverif to prove the protocol.
