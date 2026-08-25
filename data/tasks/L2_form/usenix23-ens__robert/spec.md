# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: geneph storeeph, upload auth, soundness.

---

* Protocol:   ROBERT (ROBust and privacy-presERving proximity Tracing) / TousAntiCovid
 * Modeler:    Robert Künnemann, Kevin Morio, and Dennis Jackson
 * Date:       April 2021
 * Status:     working
 *
 * Sources:    https://github.com/ROBERT-proximity-tracing/documents/blob/e220bfff3a36f0a94feb723533547bfe699df186/ROBERT-specification-EN-v1_1.pdf
 *             https://gitlab.inria.fr/stopcovid19
 *
 * Invocation: tamarin-prover --prove robert.spthy
