# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: secret guid, secret regtoken, secret tan, secret key, upload auth, soundness.

---

* Protocol:   German Corona-Warn App (CWA)
 * Modeler:    Robert Künnemann, Kevin Morio, and Dennis Jackson
 * Date:       April 2021
 * Status:     working
 *
 * Sources:    https://github.com/DP-3T/documents
 *             https://github.com/corona-warn-app/cwa-documentation/blob/e4203a628a4b5c225c7d2b9fa386b0d88ee0373c/solution_architecture.md
 *             https://blog.google/documents/69/Exposure_Notification_-_Cryptography_Specification_v1.2.1.pdf
 *
 * Invocation: tamarin-prover --prove cwa.spthy
