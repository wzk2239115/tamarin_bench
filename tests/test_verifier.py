"""Tests for Tamarin output parsing (verifier.py)."""

from tamaringym.evaluation.verifier import (
    parse_attack_traces,
    parse_prove_output,
    trace_rule_multiset,
)

PLAIN_OUTPUT = """
maude tool: 'maude'
 checking version: tamarin-prover 1.12.0, (C) ...

/* All wellformedness checks were successful. */

==============================================================================
summary of summaries:

analyzed: solution.spthy

  processing time: 2.11s

  types (all-traces): verified (32 steps)
  nonce_secrecy (all-traces): falsified - found trace (16 steps)
  injective_agree (all-traces): falsified - no trace found (14 steps)
  session_key_setup_possible (exists-trace): verified (5 steps)

==============================================================================
"""

WF_FAIL_OUTPUT = """
WARNING: the following wellformedness checks failed!

Message Derivation Checks
=========================

  Rule Init_Knowledge:
  Failed to derive Variable(s): k_A

  processing time: 1.10s

  WARNING: 1 wellformedness check failed!
           The analysis results might be wrong!

  secrecy (all-traces): verified (8 steps)
"""

DIFF_OUTPUT = """
  processing time: 0.17s

  LHS :  debug (exists-trace): verified (4 steps)
  RHS :  debug (exists-trace): verified (4 steps)
  DiffLemma:  Observational_equivalence : verified (75 steps)
"""

TRACES_JSON = {
    "graphs": [
        {
            "jgLabel": "trace_NSPK3_SL2-AS0-CL0-A1-C1-NB_nonce_secrecy-R_2_case_1",
            "jgNodes": [
                {
                    "jgnId": "#i",
                    "jgnType": "isProtocolRule",
                    "jgnLabel": "Secrecy_claim",
                },
                {"jgnId": "#j", "jgnType": "isIntruderRule", "jgnLabel": "Send"},
                {"jgnId": "#vr", "jgnType": "isProtocolRule", "jgnLabel": "R_2"},
                {"jgnId": "#vr.1", "jgnType": "isProtocolRule", "jgnLabel": "R_1"},
            ],
            "jgEdges": [],
        },
        {
            "jgLabel": "trace_NSPK3_SL2-AS0-CL0-A1-C1-NB_injective_agree-R_2",
            "jgNodes": [
                {"jgnId": "#vr", "jgnType": "isProtocolRule", "jgnLabel": "R_2"},
            ],
            "jgEdges": [],
        },
    ]
}


class TestParseProveOutput:
    def test_lemmas_and_verdicts(self):
        r = parse_prove_output(PLAIN_OUTPUT)
        names = [(n, v) for n, _, v, _ in r["lemmas"]]
        assert ("types", "verified") in names
        assert ("nonce_secrecy", "falsified") in names
        assert ("injective_agree", "falsified") in names
        assert ("session_key_setup_possible", "verified") in names
        assert r["wellformedness_ok"] is True
        assert r["processing_time"] == 2.11
        assert r["tamarin_version"] == "1.12.0"
        assert r["timeout"] is False

    def test_no_trace_falsified_is_falsified(self):
        r = parse_prove_output(PLAIN_OUTPUT)
        verdicts = {n: v for n, _, v, _ in r["lemmas"]}
        assert verdicts["injective_agree"] == "falsified"

    def test_wellformedness_failure(self):
        r = parse_prove_output(WF_FAIL_OUTPUT)
        assert r["wellformedness_ok"] is False
        assert r["lemmas"][0][0] == "secrecy"

    def test_diff_output(self):
        r = parse_prove_output(DIFF_OUTPUT)
        quants = {n: q for n, q, _, _ in r["lemmas"]}
        assert quants["Observational_equivalence"] == "diff"
        verdicts = {n: v for n, _, v, _ in r["lemmas"]}
        assert verdicts["Observational_equivalence"] == "verified"
        assert verdicts["debug"] == "verified"

    def test_timeout_by_exit_code(self):
        r = parse_prove_output("partial output", exit_code=124)
        assert r["timeout"] is True

    def test_empty_output(self):
        r = parse_prove_output("")
        assert r["lemmas"] == []
        assert r["wellformedness_ok"] is None


class TestParseAttackTraces:
    def test_lemma_attribution(self):
        import json

        traces = parse_attack_traces(
            json.dumps(TRACES_JSON), ["nonce_secrecy", "injective_agree", "types"]
        )
        assert set(traces) == {"nonce_secrecy", "injective_agree"}
        # only protocol rules are events
        assert traces["nonce_secrecy"][0] == ["Secrecy_claim", "R_2", "R_1"]

    def test_multiset(self):
        import json

        traces = parse_attack_traces(
            json.dumps(TRACES_JSON), ["nonce_secrecy", "injective_agree"]
        )
        ms = trace_rule_multiset(traces["nonce_secrecy"])
        assert ms == {"Secrecy_claim": 1, "R_2": 1, "R_1": 1}

    def test_malformed_input(self):
        assert parse_attack_traces("", ["x"]) == {}
        assert parse_attack_traces("not json", ["x"]) == {}

    def test_unknown_lemma_label(self):
        import json

        traces = parse_attack_traces(json.dumps(TRACES_JSON), ["other"])
        assert traces == {}
