# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: finished, valid, blame, missing.

---

* Protocol: DMN + message tracing
 * Modeler:  Kevin Morio and Robert Künnemann
 * Date:     Sep 2020
 * Source:   "SoK: Techniques for Verifiable Mix Nets", Thomas Haines and Johannes Müller, CSF20
 * Status:   working
 * Notes:    Run with: tamarin-prover +RTS -N4 -RTS --stop-on-trace=seqdfs --prove --heuristic=o \
 *                     --oraclename=oracle-dmn-message-tracing dmn-message-tracing-all-2.spthy
 *
 * In this version, the audit continues after detecting the first unexpected message on the bulletin board.
