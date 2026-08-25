# Protocol modeling task

Model the protocol described below in Tamarin and analyze it. Deliverables
follow the task README (`final.spthy`, `verdict.json`, `attack_report.md`
if any security goal fails). The security goals you formulate should cover,
at minimum: exists session, exists two sessions, i disagreement implies sr or siei compromise and psk compromise, r disagreement implies si or srer compromise and psk compromise, uks resistance, session uniqueness.

---

* Protocol:    Wireguard protocol
 * Modeler:     Kevin Milner & Jason Donenfeld
 * Date:        2017
 * Source:      Original
 * Status:      Basically complete? Use the 'i' heuristic to autoprove.
 *
 * TODO:
 * - Implement identity hiding using observational equivalence, instead of the weaker surrogate-based property.
 * - Prove indistinguishability using observational equivalence.
 * - Model ECDH(private, NULL) = NULL
