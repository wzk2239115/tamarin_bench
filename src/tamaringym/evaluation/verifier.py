"""Parsers for Tamarin prover output and attack-trace JSON.

Used both by ``scripts/validate_tasks.py`` (ground-truth generation) and by
the evaluator (scoring agent runs). Parsing is anchored on Tamarin 1.12.0's
``--prove`` console output and ``--output-json`` trace format; the formats
are stable across patch versions but should be re-verified when the pinned
version changes.
"""

from __future__ import annotations

import json
import re

__all__ = [
    "parse_prove_output",
    "parse_attack_traces",
    "trace_rule_multiset",
]

# ── --prove console output ───────────────────────────────────────────────────

_SUMMARY_LEMMA_RE = re.compile(
    r"^\s+(?:(?P<side>LHS|RHS)\s*:\s+)?(?P<name>\S+)\s+\((?P<quant>all-traces|exists-trace|trace)\):\s+"
    r"(?P<verdict>verified|falsified - found trace|falsified - no trace found|incomplete|processing error)"
    r"(?:\s+\((?P<steps>\d+) steps?\))?",
    re.M,
)

_DIFF_LEMMA_RE = re.compile(
    r"^\s+DiffLemma:\s+(?P<name>\S+)\s*:\s+"
    r"(?P<verdict>verified|falsified|incomplete|processing error)"
    r"(?:\s+\((?P<steps>\d+) steps?\))?",
    re.M,
)

_WF_FAIL_RE = re.compile(
    r"WARNING: (?:the following )?wellformedness checks? (?:check )?failed", re.I
)
_WF_FAIL_RE2 = re.compile(r"wellformedness check failed", re.I)
_WF_OK_RE = re.compile(r"All wellformedness checks were successful", re.I)

_PROC_TIME_RE = re.compile(r"processing time:\s*([0-9.]+)s", re.I)
_VERSION_RE = re.compile(r"tamarin-prover\s+([0-9][0-9.]*)", re.I)

VERDICT_VERIFIED = "verified"
VERDICT_FALSIFIED = "falsified"
VERDICT_INCOMPLETE = "incomplete"
VERDICT_ERROR = "processing error"

_VERDICT_MAP = {
    "verified": VERDICT_VERIFIED,
    "falsified - found trace": VERDICT_FALSIFIED,
    "falsified - no trace found": VERDICT_FALSIFIED,
    "falsified": VERDICT_FALSIFIED,
    "incomplete": VERDICT_INCOMPLETE,
    "processing error": VERDICT_ERROR,
}


def parse_prove_output(stdout: str, *, exit_code: int | str | None = None) -> dict:
    """Parse ``tamarin-prover <file> --prove`` console output.

    Returns::

        {
            "lemmas": [(name, quantifier, verdict, steps), ...],
            "wellformedness_ok": bool | None,   # None = no signal found
            "processing_time": float | None,
            "tamarin_version": str | None,
            "timeout": bool,                    # exit code 124 (timeout(1))
            "parse_error": bool,                # hard errors before any summary
            "errors": [str, ...],               # raw error lines
        }
    """
    try:
        code = int(exit_code) if exit_code is not None else None
    except (TypeError, ValueError):
        code = None

    lemmas = [
        (
            m.group("name"),
            m.group("quant"),
            _VERDICT_MAP[m.group("verdict")],
            int(m.group("steps")) if m.group("steps") else None,
        )
        for m in _SUMMARY_LEMMA_RE.finditer(stdout)
    ]
    # diff-mode summaries: `DiffLemma:  <name> : verdict (steps)`; LHS/RHS
    # lines of the same lemma are duplicates — keep the first per name
    seen = {name for name, _, _, _ in lemmas}
    for m in _DIFF_LEMMA_RE.finditer(stdout):
        name = m.group("name")
        if name in seen:
            continue
        seen.add(name)
        lemmas.append(
            (
                name,
                "diff",
                _VERDICT_MAP[m.group("verdict")],
                int(m.group("steps")) if m.group("steps") else None,
            )
        )
    # LHS/RHS report the same lemma name twice — dedupe, keeping the first
    deduped: list[tuple[str, str, str, int | None]] = []
    for entry in lemmas:
        if entry[0] not in {e[0] for e in deduped}:
            deduped.append(entry)
    lemmas = deduped

    if _WF_FAIL_RE.search(stdout) or _WF_FAIL_RE2.search(stdout):
        wf_ok = False
    elif _WF_OK_RE.search(stdout):
        wf_ok = True
    else:
        wf_ok = None

    t = _PROC_TIME_RE.search(stdout)
    v = _VERSION_RE.search(stdout)

    error_lines = [
        line.strip()
        for line in stdout.splitlines()
        if line.strip().startswith(("Error:", "error:", "tamarin-prover: Error"))
    ]

    return {
        "lemmas": lemmas,
        "wellformedness_ok": wf_ok,
        "processing_time": float(t.group(1)) if t else None,
        "tamarin_version": v.group(1) if v else None,
        "timeout": code == 124,
        "parse_error": not lemmas and code not in (0, None),
        "errors": error_lines[:10],
    }


# ── --output-json attack traces ──────────────────────────────────────────────


def _protocol_rules_of_graph(graph: dict) -> list[str]:
    """Protocol-rule event names of one trace graph, in node order."""
    rules = []
    for node in graph.get("jgNodes", []):
        if node.get("jgnType") == "isProtocolRule":
            label = node.get("jgnLabel", "")
            if label:
                rules.append(label)
    return rules


def _lemma_of_label(label: str, known_lemma_names: list[str]) -> str:
    """Attribute a trace graph to a lemma via its label.

    Labels look like ``trace_<Theory>_SL2-AS0-...-NB_<lemma_name>-<rules>``.
    When ``NB_<name>`` cannot be matched, fall back to the longest known
    lemma name that occurs in the label.
    """
    if not known_lemma_names:
        return ""
    m = re.search(r"-NB_(?P<rest>.*)$", label)
    if m:
        rest = m.group("rest")
        for name in sorted(known_lemma_names, key=len, reverse=True):
            if rest.startswith(name + "-") or rest == name:
                return name
    for name in sorted(known_lemma_names, key=len, reverse=True):
        if name in label:
            return name
    return ""


def parse_attack_traces(
    traces_json: str, known_lemma_names: list[str]
) -> dict[str, list[list[str]]]:
    """Parse ``--output-json`` output into per-lemma trace event sequences.

    Returns ``{lemma_name: [ [rule, ...], ... ]}`` — one list of protocol-rule
    events per found trace. Malformed/empty input yields ``{}``.
    """
    if not traces_json.strip():
        return {}
    try:
        data = json.loads(traces_json)
    except json.JSONDecodeError:
        return {}

    out: dict[str, list[list[str]]] = {}
    for graph in data.get("graphs", []):
        lemma = _lemma_of_label(graph.get("jgLabel", ""), known_lemma_names)
        if not lemma:
            continue  # cannot attribute (e.g. witness trace of an unknown lemma)
        rules = _protocol_rules_of_graph(graph)
        if not rules:
            continue
        out.setdefault(lemma, []).append(rules)
    return out


def trace_rule_multiset(traces: list[list[str]]) -> dict[str, int]:
    """Aggregate event multisets across all traces of one lemma."""
    counts: dict[str, int] = {}
    for seq in traces:
        for r in seq:
            counts[r] = counts.get(r, 0) + 1
    return counts
