# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: executabler1, executabler2, executablei, secretr, secreti, honnestauthri.

---

* Protocol:   LAKE
   https://datatracker.ietf.org/doc/html/draft-ietf-lake-edhoc-02

   A lightweight DD based key exchange.

   It comes with two possible modes, either a signature is used for
   authentication, or a long term dh key.
   This file proposes the two modes, with I1 or I2.

   We also  provide a model of dynamic compromission.

   Proverif : 16 seconds

   Tamarin : 2 minutes with 10 cores
