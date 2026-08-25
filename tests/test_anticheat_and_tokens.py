"""Tests for anti-cheat structural checks and token utilities."""

import pytest

from tamaringym.evaluation.anticheat import (
    check_given_rules_unchanged,
    check_lemma_coverage,
    check_lemma_fact_references,
    check_no_trivial_lemmas,
)
from tamaringym.task.spthy import parse_theory
from tamaringym.task.token import (
    generate_token,
    generate_verdict_key,
    verify_token,
)

GIVEN = """theory t begin
rule Init:
  [ Fr(~k) ]
--[ Started(~k) ]->
  [ Out(~k) ]
restriction honest:
  "All A #i #j. Reg(A)@i & Reg(A)@j ==> #i = #j"
lemma secrecy:
  all-traces
  "All k #i. Started(k) @ i ==> not (Ex #j. K(k) @ j)"
end
"""


def _final_with(**changes):
    """Build a final theory from GIVEN with targeted modifications."""
    text = GIVEN
    if changes.get("drop_rule"):
        text = text.replace(
            "rule Init:\n  [ Fr(~k) ]\n--[ Started(~k) ]->\n  [ Out(~k) ]\n", ""
        )
    if changes.get("weaken_rule"):
        text = text.replace("[ Out(~k) ]", "[ Out(~k) ]  /* added */").replace(
            "Out(~k)", "Out(~k) "
        )
    if changes.get("drop_restriction"):
        text = text.replace(
            'restriction honest:\n  "All A #i #j. Reg(A)@i & Reg(A)@j ==> #i = #j"\n',
            "",
        )
    if changes.get("trivial_lemma"):
        text = text.replace(
            '"All k #i. Started(k) @ i ==> not (Ex #j. K(k) @ j)"',
            '"All k #i. Started(k) @ i ==> Started(k) @ i"',
        )
    if changes.get("no_fact_lemma"):
        text = text.replace(
            '"All k #i. Started(k) @ i ==> not (Ex #j. K(k) @ j)"',
            '"All x. x = x"',
        )
    return text


class TestGivenRulesUnchanged:
    def test_identical_theory_passes(self):
        given = parse_theory(GIVEN)
        final = parse_theory(GIVEN)
        r = check_given_rules_unchanged(given, final)
        assert r.score == 1.0

    def test_whitespace_only_changes_pass(self):
        given = parse_theory(GIVEN)
        final = parse_theory(GIVEN.replace("[ Fr(~k) ]", "[  Fr(~k)  ]"))
        r = check_given_rules_unchanged(given, final)
        assert r.score == 1.0

    def test_removed_rule_fails(self):
        given = parse_theory(GIVEN)
        final = parse_theory(_final_with(drop_rule=True))
        r = check_given_rules_unchanged(given, final)
        assert r.score < 1.0
        assert any(p["issue"] == "removed" for p in r.details["problems"])

    def test_modified_rule_fails(self):
        given = parse_theory(GIVEN)
        final = parse_theory(GIVEN.replace("[ Fr(~k) ]", "[ Fr(~k), In(zzz) ]"))
        r = check_given_rules_unchanged(given, final)
        assert r.score < 1.0

    def test_dropped_restriction_fails(self):
        given = parse_theory(GIVEN)
        final = parse_theory(_final_with(drop_restriction=True))
        r = check_given_rules_unchanged(given, final)
        assert r.score < 1.0


class TestLemmaChecks:
    def test_coverage_ok(self):
        given = parse_theory(GIVEN)
        final = parse_theory(GIVEN)
        assert check_lemma_coverage(given.lemmas, final).score == 1.0
        assert check_lemma_fact_references(given.lemmas, final).score == 1.0

    def test_missing_lemma_fails_coverage(self):
        given = parse_theory(GIVEN)
        final = parse_theory(GIVEN.replace("lemma secrecy:", "lemma other:"))
        r = check_lemma_coverage(given.lemmas, final)
        assert r.score == 0.0

    def test_factless_lemma_fails_references(self):
        given = parse_theory(GIVEN)
        final = parse_theory(_final_with(no_fact_lemma=True))
        r = check_lemma_fact_references(given.lemmas, final)
        assert r.score == 0.0
        assert r.details["violations"][0]["missing_facts"] == ["Started"]

    def test_trivial_lemma_detected(self):
        final = parse_theory(_final_with(trivial_lemma=True))
        r = check_no_trivial_lemmas(final)
        assert r.score == 0.0
        assert "secrecy" in r.details["trivial"]

    def test_extra_facts_allowed(self):
        given = parse_theory(GIVEN)
        final = parse_theory(
            GIVEN.replace(
                '"All k #i. Started(k) @ i ==> not (Ex #j. K(k) @ j)"',
                '"All k #i. Started(k) @ i & Extra(k) @ i ==> not (Ex #j. K(k) @ j)"',
            )
        )
        assert check_lemma_fact_references(given.lemmas, final).score == 1.0


class TestTokens:
    def test_token_roundtrip(self):
        agent_id, token = generate_token("L1:NSPK3", salt="s3cret")
        assert verify_token(agent_id, token, salt="s3cret") == "L1:NSPK3"

    def test_wrong_salt_rejected(self):
        agent_id, token = generate_token("L1:NSPK3", salt="s3cret")
        assert verify_token(agent_id, token, salt="other") is None

    def test_wrong_agent_rejected(self):
        _, token = generate_token("L1:NSPK3", salt="s3cret", agent_id="a1")
        assert verify_token("a2", token, salt="s3cret") is None

    def test_verdict_key_deterministic_and_seed_sensitive(self):
        a = generate_verdict_key("L1:NSPK3", seed="seed1")
        b = generate_verdict_key("L1:NSPK3", seed="seed1")
        c = generate_verdict_key("L1:NSPK3", seed="seed2")
        assert a == b
        assert a != c
        assert a.startswith("tvk-")

    def test_empty_secrets_rejected(self):
        with pytest.raises(ValueError):
            generate_token("L1:x", salt="")
        with pytest.raises(ValueError):
            generate_verdict_key("L1:x", seed="")


class TestMetadata:
    def test_registry_loads(self):
        from tamaringym.task.metadata import load_task_registry

        registry = load_task_registry()
        total = sum(len(v) for v in registry.values())
        if total == 0:
            pytest.skip("tasks not generated yet")
        assert total >= 70  # 55 L1 + 10 L2 + 10 L3

    def test_task_dir_for(self):
        from tamaringym.task.metadata import task_dir_for

        p = task_dir_for("L1:NSPK3")
        assert p.name == "NSPK3"
        assert p.parent.name == "L1_verdict"
        with pytest.raises(ValueError):
            task_dir_for("malformed-no-colon")
