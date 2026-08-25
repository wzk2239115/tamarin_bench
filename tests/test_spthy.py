"""Tests for the .spthy structural parser against real corpus theories."""

from pathlib import Path

import pytest

from tamaringym.task.spthy import (
    SpthyParseError,
    lemma_referenced_facts,
    normalize_block,
    parse_theory,
    strip_lemmas,
)

TASKS_DIR = Path(__file__).parents[2] / "data" / "tasks"

SIMPLE = """theory test begin

rule Init:
  [ Fr(~k) ]
--[ Started(~k) ]->
  [ Out(~k) ]

rule Resp:
  [ In(x) ]
--[ Accepted(x) ]->
  [ Done(x) ]

lemma secrecy:
  all-traces
  "All k #i. Started(k) @ i ==> not (Ex #j. K(k) @ j)"

lemma executable:
  exists-trace
  "Ex x #i. Accepted(x) @ i"

end
"""

NESTED_COMMENT = """theory nested begin
rule R:
  [ In(x) ] --> [ Out(x) ]
/*
/* double-nested comment disables the lemma below */
lemma disabled:
  "All #i. Something() @ i ==> False"
*/
lemma alive:
  "All #i. True() @ i ==> True() @ i"
end
"""

IFDEF = """theory pp begin
rule R:
  [ In(x) ] --> [ Out(x) ]
#ifdef secure
lemma secret:
  "All k #i. Secret(k) @ i ==> not (Ex #j. K(k) @ j)"
#endif
lemma always:
  "All #i. Tick() @ i ==> Tick() @ i"
end
"""

DIFF_THEORY = """theory diffy begin
rule enc:
  [ In(x), Fr(~r) ]
--[ ]->
  [ Out(diff(~r, senc(x, ~r))) ]
DiffLemma equivalence:
  "Ex #i. ..."
end
"""


class TestBasicParsing:
    def test_rules_and_lemmas(self):
        t = parse_theory(SIMPLE)
        assert [r.name for r in t.rules] == ["Init", "Resp"]
        assert [l.name for l in t.lemmas] == ["secrecy", "executable"]
        assert t.lemmas[0].quantifier == "all-traces"
        assert t.lemmas[1].quantifier == "exists-trace"

    def test_lemma_formula_extraction(self):
        t = parse_theory(SIMPLE)
        assert "Started(k)" in t.lemmas[0].formula
        assert "Accepted(x)" in t.lemmas[1].formula

    def test_missing_header_raises(self):
        with pytest.raises(SpthyParseError):
            parse_theory("rule R: [In(x)] --> [Out(x)]\nend")

    def test_missing_begin_raises(self):
        with pytest.raises(SpthyParseError):
            parse_theory("theory t\nrule R: [In(x)] --> [Out(x)]\nend")

    def test_theory_begin_same_line(self):
        t = parse_theory("theory foo begin\nrule R:\n [In(x)] --> [Out(x)]\nend\n")
        assert t.name == "foo"
        assert len(t.rules) == 1


class TestCommentsAndPreprocessor:
    def test_nested_comments_disable_lemmas(self):
        t = parse_theory(NESTED_COMMENT)
        assert [l.name for l in t.lemmas] == ["alive"]

    def test_ifdef_regions_inactive_by_default(self):
        t = parse_theory(IFDEF)
        assert [l.name for l in t.lemmas] == ["always"]

    def test_line_comments_ignored(self):
        text = SIMPLE.replace("rule Resp:", "// rule Resp:").replace(
            "  [ In(x) ]\n--[ Accepted(x) ]->\n  [ Done(x) ]\n\n", ""
        )
        t = parse_theory(text)
        assert [r.name for r in t.rules] == ["Init"]

    def test_difflemma_quantifier(self):
        t = parse_theory(DIFF_THEORY)
        assert len(t.lemmas) == 1
        assert t.lemmas[0].quantifier == "diff"


class TestStripLemmas:
    def test_strip_removes_all_lemmas(self):
        stripped = strip_lemmas(SIMPLE)
        t = parse_theory(stripped)
        assert t.lemmas == []
        assert [r.name for r in t.rules] == ["Init", "Resp"]

    def test_strip_keep_names(self):
        stripped = strip_lemmas(SIMPLE, keep_names={"secrecy"})
        t = parse_theory(stripped)
        assert [l.name for l in t.lemmas] == ["secrecy"]

    def test_strip_preserves_commented_lemmas(self):
        stripped = strip_lemmas(NESTED_COMMENT)
        # the commented-out lemma was never active; its text survives
        assert "disabled" in stripped
        # the active lemma is removed
        t = parse_theory(stripped)
        assert t.lemmas == []

    def test_strip_iffdef(self):
        stripped = strip_lemmas(IFDEF)
        # pp-inactive region is untouched (never was an active lemma)
        assert "#ifdef secure" in stripped
        assert "lemma secret" in stripped
        # the active lemma is removed
        t = parse_theory(stripped)
        assert t.lemmas == []


class TestFactReferences:
    def test_protocol_facts_extracted(self):
        t = parse_theory(SIMPLE)
        assert lemma_referenced_facts(t.lemmas[0]) == {"Started"}
        # Accepted is protocol-level too (not in the standard set)
        assert lemma_referenced_facts(t.lemmas[1]) == {"Accepted"}

    def test_standard_facts_skipped(self):
        text = 'theory t begin\nrule R:\n [In(x)] --> [Out(x)]\nlemma l:\n "All k #i #j. Secret(k)@i & K(k)@j ==> False"\nend\n'
        t = parse_theory(text)
        assert lemma_referenced_facts(t.lemmas[0]) == {"Secret"}


class TestNormalizeBlock:
    def test_whitespace_and_comments_insensitive(self):
        a = "rule R:\n  /* hi */ [ In(x) ] --> [ Out(x) ] // trailing\n"
        b = "rule R: [In(x)] --> [Out(x)]"
        assert normalize_block(a) == normalize_block(b)

    def test_different_bodies_differ(self):
        assert normalize_block("rule R: [In(x)] --> [Out(x)]") != normalize_block(
            "rule R: [In(x)] --> [Out(y)]"
        )


class TestCorpus:
    """Every converted task's solution must parse; stripped L1 theories must
    still parse with zero lemmas and identical rules."""

    @pytest.fixture(scope="class")
    def l1_tasks(self):
        d = TASKS_DIR / "L1_verdict"
        return sorted(d.iterdir()) if d.is_dir() else []

    def test_all_l1_solutions_parse(self, l1_tasks):
        for tdir in l1_tasks:
            sol = tdir / "solution" / "solution.spthy"
            if not sol.is_file():
                continue
            theory = parse_theory(sol.read_text())
            assert theory.rules, f"{tdir.name}: no rules parsed"

    def test_l1_theory_has_no_lemmas(self, l1_tasks):
        for tdir in l1_tasks:
            given = tdir / "theory.spthy"
            if not given.is_file():
                continue
            theory = parse_theory(given.read_text())
            assert theory.lemmas == [], f"{tdir.name}: given theory still has lemmas"

    def test_l1_rules_match_solution(self, l1_tasks):
        for tdir in l1_tasks:
            given = tdir / "theory.spthy"
            sol = tdir / "solution" / "solution.spthy"
            if not (given.is_file() and sol.is_file()):
                continue
            g = parse_theory(given.read_text())
            s = parse_theory(sol.read_text())
            assert [r.name for r in g.rules] == [r.name for r in s.rules], tdir.name
            assert [r.body for r in g.rules] == [r.body for r in s.rules], tdir.name
