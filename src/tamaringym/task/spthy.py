"""Parser for Tamarin ``.spthy`` theory files.

We only need structural information (sections, declarations, lemmas, rules,
facts), not full term semantics — enough to

* strip lemmas from a complete theory (L1 task generation),
* compare given-rule sections for structural anti-cheat,
* compute which facts each lemma references (trivially-true-lemma defense),
* enumerate protocol rule names (attack-trace event matching).

The parser is comment-aware (``/* ... */`` block comments — which the
Tamarin case studies use heavily to comment out hard lemmas — and ``//``
line comments): declarations inside comments do not exist. This matters
because several CrypFormBench "complete" theories carry their security
lemmas commented out; those theories have no provable goals and are
excluded from task generation.

``DiffLemma`` declarations (observational equivalence mode) are parsed as
lemmas with ``quantifier="diff"``.

All functions raise :class:`SpthyParseError` on clearly malformed input and
are covered by tests against the actual task corpus.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

__all__ = [
    "SpthyParseError",
    "Lemma",
    "Rule",
    "Theory",
    "parse_theory",
    "strip_lemmas",
    "lemma_referenced_facts",
    "normalize_block",
]


class SpthyParseError(ValueError):
    """Raised when an .spthy file cannot be parsed structurally."""


@dataclass
class Lemma:
    name: str
    body: str  # full declaration text, from `lemma` keyword to closing quote + attrs
    quantifier: str | None = None  # "all-traces" / "exists-trace" / "diff"
    attributes: list[str] = field(default_factory=list)
    formula: str = ""  # the quoted formula text
    start_line: int = -1  # 0-based line of the `lemma` keyword
    end_line: int = -1  # 0-based last line of the declaration block


@dataclass
class Rule:
    name: str
    body: str  # full declaration text
    kind: str = "rule"  # rule | restriction | axiom


@dataclass
class Theory:
    name: str
    text: str  # original full text
    lemmas: list[Lemma] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)  # plain rules only
    restrictions: list[Rule] = field(default_factory=list)
    axioms: list[Rule] = field(default_factory=list)

    @property
    def protocol_rule_names(self) -> list[str]:
        return [r.name for r in self.rules]


# ── lexical helpers ──────────────────────────────────────────────────────────

_HEADER_RE = re.compile(
    r"^\s*theory\s+([A-Za-z0-9_][A-Za-z0-9_'\-]*)", re.IGNORECASE | re.MULTILINE
)
_END_RE = re.compile(r"^\s*end\b", re.IGNORECASE | re.MULTILINE)

# Top-level declarations we care about. ``DiffLemma`` is case-sensitive in
# Tamarin; the others are matched case-insensitively.
_DECL_RE = re.compile(
    r"^(?P<indent>[ \t]*)(?P<kind>DiffLemma|lemma|restriction|axiom|rule)\b[ \t]*"
    r"(?P<rest>[^\n]*)$",
    re.IGNORECASE | re.MULTILINE,
)


def _comment_state(text: str) -> list[bool]:
    """Per-character flag: True when the char is inside a comment.

    Handles ``/* ... */`` — **nesting** (Tamarin follows the Haskell
    tradition here; corpus files use nested comments to disable lemmas) —
    and ``//`` line comments.
    """
    state = [False] * len(text)
    i = 0
    depth = 0
    n = len(text)
    while i < n:
        if depth > 0:
            state[i] = True
            if text.startswith("/*", i):
                depth += 1
                state[i + 1] = True
                i += 2
            elif text.startswith("*/", i):
                depth -= 1
                state[i + 1] = True
                i += 2
            else:
                i += 1
        else:
            if text.startswith("/*", i):
                state[i] = True
                state[i + 1] = True
                depth = 1
                i += 2
            elif text.startswith("//", i):
                j = text.find("\n", i)
                j = n if j == -1 else j
                for k in range(i, j):
                    state[k] = True
                i = j
            else:
                i += 1
    return state


def _line_starts(text: str) -> list[int]:
    starts = [0]
    for i, c in enumerate(text):
        if c == "\n":
            starts.append(i + 1)
    return starts


_PP_DIRECTIVE_RE = re.compile(
    r"^[ \t]*#[ \t]*(?P<cmd>ifdef|ifndef|else|endif|define)\b[ \t]*(?P<arg>\S*)",
    re.MULTILINE,
)


def _pp_state(text: str, defines: set[str] | None = None) -> list[bool]:
    """Per-character flag: True when inside a preprocessor-inactive region.

    Tamarin supports a C-style preprocessor (``--defines``). We never pass
    defines by default, so ``#ifdef X`` regions are inactive and
    ``#ifndef X`` regions are active. Handles nesting and ``#else``.
    """
    defines = defines or set()
    state = [False] * len(text)
    stack: list[bool] = []
    for m in _PP_DIRECTIVE_RE.finditer(text):
        cmd = m.group("cmd")
        arg = m.group("arg")
        line_end = text.find("\n", m.start())
        line_end = len(text) if line_end == -1 else line_end
        parent_active = all(stack)
        if cmd in ("ifdef", "ifndef"):
            cond = (arg in defines) if cmd == "ifdef" else (arg not in defines)
            stack.append(parent_active and cond)
        elif cmd == "else":
            if stack:
                prev = stack.pop()
                stack.append(parent_active and not prev)
        elif cmd == "endif":
            if stack:
                stack.pop()
        # mark the region following this directive as inactive when the
        # current branch is inactive
        if not all(stack):
            nxt = _PP_DIRECTIVE_RE.search(text, line_end)
            end = nxt.start() if nxt else len(text)
            for i in range(line_end, end):
                state[i] = True
    return state


def _offset_to_line(line_starts: list[int], offset: int) -> int:
    # binary search
    lo, hi = 0, len(line_starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if line_starts[mid] <= offset:
            lo = mid
        else:
            hi = mid - 1
    return lo


def _find_closing_quote(text: str, start: int, state: list[bool]) -> int:
    """Index of the closing double quote for a formula opened before *start*.

    Scans from *start*; skips escaped characters and commented regions.
    """
    i = start
    while i < len(text):
        if state[i]:
            # skip commented region
            j = i
            while j < len(text) and state[j]:
                j += 1
            i = j
            continue
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == '"':
            return i
        i += 1
    raise SpthyParseError("unterminated double-quoted formula")


def _parse_attributes(attr_text: str | None) -> list[str]:
    if not attr_text:
        return []
    inner = attr_text.strip("[]").strip()
    if not inner:
        return []
    return [p.strip() for p in inner.split(",") if p.strip()]


def _hidden_state(text: str, defines: set[str] | None = None) -> list[bool]:
    """Per-character flag: True when commented out OR pp-inactive."""
    comments = _comment_state(text)
    pp = _pp_state(text, defines)
    return [c or p for c, p in zip(comments, pp)]


def _uncommented_declarations(text: str, state: list[bool]):
    """Yield decl matches outside comments and inactive preprocessor regions."""
    for m in _DECL_RE.finditer(text):
        kind_start = m.start("kind")
        if state[kind_start]:
            continue
        yield m


def parse_theory(text: str, *, defines: set[str] | None = None) -> Theory:
    """Parse the structural elements of a .spthy theory.

    Tolerant by design: sections like ``functions:``, ``builtins:``,
    ``equations:`` are not modeled. Raises :class:`SpthyParseError` when the
    theory header is missing — a strong signal the file is not a theory.
    """
    hm = _HEADER_RE.search(text)
    if not hm:
        raise SpthyParseError("no 'theory <name>' header found")
    name = hm.group(1)
    after_header = text[hm.end() :]
    header_tail = after_header.split("\n", 1)[0]
    if not re.search(r"\bbegin\b", header_tail) and not re.search(
        r"^\s*begin\b", after_header, re.IGNORECASE | re.MULTILINE
    ):
        raise SpthyParseError("no 'begin' marker found")

    theory = Theory(name=name, text=text)
    state = _hidden_state(text, defines)
    line_starts = _line_starts(text)

    decls = list(_uncommented_declarations(text, state))
    # block boundaries: each decl runs until the next decl / `end` / EOF
    ends = []
    for m in _DECL_RE.finditer(text):
        if not state[m.start("kind")]:
            ends.append(m.start())
    for m in _END_RE.finditer(text):
        if not state[m.start()]:
            ends.append(m.start())
    ends.append(len(text))

    for m in decls:
        start = m.start()
        # find the first boundary strictly after this decl's start
        block_end = min(e for e in ends if e > start)
        body = text[start:block_end].rstrip()
        start_line = _offset_to_line(line_starts, start)
        end_line = (
            _offset_to_line(line_starts, start + len(body) - 1) if body else start_line
        )
        kind_raw = m.group("kind")
        kind = "difflemma" if kind_raw == "DiffLemma" else kind_raw.lower()
        rest = m.group("rest")

        if kind == "rule":
            name_m = re.match(
                r"^(?P<name>[A-Za-z_][A-Za-z0-9_'\-]*)\s*(\[[^\]]*\])?\s*:?\s*$", rest
            ) or re.match(r"^(?P<name>[A-Za-z_][A-Za-z0-9_'\-]*)", rest)
            theory.rules.append(
                Rule(
                    name=name_m.group("name") if name_m else "<anonymous>",
                    body=body,
                    kind="rule",
                )
            )
        elif kind in ("restriction", "axiom"):
            name_m = re.match(
                r"^(?P<name>[A-Za-z_][A-Za-z0-9_'\-]*)\s*(\[[^\]]*\])?\s*:\s*$", rest
            ) or re.match(r"^(?P<name>[A-Za-z_][A-Za-z0-9_'\-]*)", rest)
            target = theory.restrictions if kind == "restriction" else theory.axioms
            target.append(
                Rule(
                    name=name_m.group("name") if name_m else "<anonymous>",
                    body=body,
                    kind=kind,
                )
            )
        elif kind in ("lemma", "difflemma"):
            # first uncommented double quote in the block
            q_open = None
            for i in range(start, min(block_end, len(text))):
                if not state[i] and text[i] == '"' and text[i - 1] != "\\":
                    q_open = i
                    break
            if q_open is None:
                if kind == "difflemma":
                    # diffLemma bodies may carry an inline proof script
                    # (e.g. "diffLemma X: rule-equivalence ...") instead of a
                    # quoted formula — record it with an empty formula.
                    head_name = (
                        re.sub(
                            r"^\s*(?:DiffLemma|lemma)\b",
                            "",
                            rest,
                            count=1,
                            flags=re.IGNORECASE,
                        )
                        .strip()
                        .splitlines()[0]
                        .split(":")[0]
                        .strip()
                        or "<anonymous>"
                    )
                    theory.lemmas.append(
                        Lemma(
                            name=head_name,
                            body=body,
                            quantifier="diff",
                            formula="",
                            start_line=start_line,
                            end_line=end_line,
                        )
                    )
                    continue
                raise SpthyParseError(
                    f"lemma at line {start_line + 1} has no quoted formula"
                )
            q_close = _find_closing_quote(text, q_open + 1, state)
            formula = text[q_open + 1 : q_close]
            head_text = text[start:q_open]
            # strip the leading decl keyword; the lemma name follows it
            head_first_line = (
                re.sub(
                    r"^\s*(?:DiffLemma|lemma)\b",
                    "",
                    head_text,
                    count=1,
                    flags=re.IGNORECASE,
                )
                .strip()
                .splitlines()[0]
                if head_text.strip()
                else ""
            )
            attrs: list[str] = []
            hm2 = re.match(
                r"^(?P<name>[A-Za-z_][A-Za-z0-9_'\-]*)\s*(?P<attrs>\[[^\]]*\])?\s*:",
                head_first_line,
            )
            if hm2:
                lemma_name = hm2.group("name")
                attrs = _parse_attributes(hm2.group("attrs"))
            else:
                hm3 = re.match(r"^(?P<name>[A-Za-z_][A-Za-z0-9_'\-]*)", head_first_line)
                if not hm3:
                    raise SpthyParseError(
                        f"cannot parse lemma head at line {start_line + 1}: {head_text!r}"
                    )
                lemma_name = hm3.group("name")
            # attributes may also trail the closing quote
            tail = text[q_close + 1 : block_end]
            tail_attrs = re.search(r"\[([^\]]*)\]", tail)
            if tail_attrs:
                attrs.extend(_parse_attributes("[" + tail_attrs.group(1) + "]"))

            if kind == "difflemma":
                quantifier = "diff"
            elif re.search(r"\ball[- ]traces\b", head_text, re.IGNORECASE):
                quantifier = "all-traces"
            elif re.search(r"\bexists[- ]trace\b", head_text, re.IGNORECASE):
                quantifier = "exists-trace"
            elif re.match(r"^\s*(Ex|∃)", formula):
                quantifier = "exists-trace"
            else:
                quantifier = "all-traces"

            theory.lemmas.append(
                Lemma(
                    name=lemma_name,
                    body=body,
                    quantifier=quantifier,
                    attributes=attrs,
                    formula=formula,
                    start_line=start_line,
                    end_line=end_line,
                )
            )

    return theory


def strip_lemmas(text: str, *, keep_names: set[str] | None = None) -> str:
    """Return *text* with lemma declarations removed.

    If *keep_names* is given, lemmas whose names are in the set survive.
    Removal preserves all other content byte-for-byte except for the removed
    blocks and resulting consecutive blank lines (collapsed to one).
    """
    theory = parse_theory(text)
    keep = keep_names or set()
    lines = text.splitlines(keepends=True)
    drop_lines: set[int] = set()
    for lem in theory.lemmas:
        if lem.name not in keep:
            drop_lines.update(range(lem.start_line, lem.end_line + 1))

    if not drop_lines:
        return text

    out = [ln for k, ln in enumerate(lines) if k not in drop_lines]
    result = "".join(out)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result


_FACT_RE = re.compile(r"\b(?:!|~|\$)?(?P<name>[A-Z][A-Za-z0-9_]*)\s*\(")


def lemma_referenced_facts(lemma: Lemma, *, skip_standard: bool = True) -> set[str]:
    """Public fact names referenced by a lemma formula.

    Standard facts (``K``, ``In``, ``Out``, ``Fr``, ...) are dropped unless
    *skip_standard* is False — the anti-cheat check cares about
    *protocol-level* events (``Secret``, ``Commit``, state facts ...).
    """
    standard = {
        "K",
        "In",
        "Out",
        "Fr",
        "Setup",
        "Eq",
        "KU",
        "KD",
        "F",
        "VK",
        "PF",
        "Isend",
        "Irecv",
        "C",
        "PK",
        "SK",
        "Temp",
        "V",
        "G",
    }
    names = set(_FACT_RE.findall(lemma.formula))
    if skip_standard:
        names -= standard
    return names


def normalize_block(text: str) -> str:
    """Whitespace/comment-insensitive canonical form of a rule/lemma block.

    Used for the structural anti-cheat comparison: the agent's copy of a given
    rule must match the reference modulo whitespace and comments. All
    whitespace is removed (not collapsed) so ``[ In(x) ]`` == ``[In(x)]``.
    """
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"//[^\n]*", "", text)
    text = re.sub(r"\s+", "", text)
    return text.strip()
