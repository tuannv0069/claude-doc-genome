"""Turning a rule or guide into comparable text units.

A unit is a paragraph, a list item or a table row. Called by the entry point to
build the units, by `duplicates.py` through them, and by `ledger.py` for `normalize`.
"""
from __future__ import annotations

import re
import unicodedata

STOP = set(
    "the a an of to in for and or is are be it its this that with on by as not no "
    # The second group is Vietnamese: a project may document in a language other than English,
    # and a stopword that never occurs simply never fires.
    "khong la cua va cho mot duoc thi neu".split())
SEPARATOR = re.compile(r"^\s*\|[\s:|-]+\|\s*$")


def normalize(s: str) -> list[str]:
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"`[^`]*`", " ", s)
    s = re.sub(r"[^\w\s]", " ", s)
    return [w for w in s.split() if len(w) > 2 and w not in STOP]


def _is_table_header(raw: str, next_raw: str = "") -> bool:
    """A header row = a pipe row with a SEPARATOR row directly beneath it.

    Deliberately not a keyword list: a real rule row whose first cell reads `file` / `id` /
    `step` would be dropped silently. Structure is exact where a keyword list is a guess.
    """
    if not raw.lstrip().startswith("|"):
        return False
    return bool(SEPARATOR.match(next_raw))


def rule_lines(text: str) -> list[tuple[int, str, set[str]]]:
    """Read paragraphs, list items and table rows as comparable text units.

    A wrapped paragraph is one unit with the same content as its single-line
    form. Headings, metadata, examples and fenced code are not duplicate rules.
    """
    out, pending = [], []
    start = 0
    fenced = example = metadata = False
    lines = text.splitlines()

    def flush():
        nonlocal pending
        if pending:
            unit = " ".join(pending)
            tokens = set(normalize(unit))
            if tokens:
                out.append((start, unit, tokens))
            pending = []

    for i, raw in enumerate(lines, 1):
        value = raw.strip()
        if i == 1 and value == "---":
            metadata = True
            continue
        if metadata:
            if value == "---": metadata = False
            continue
        if value.startswith(("<example>", "<example ")):
            flush(); example = True; continue
        if value.startswith("</example>"):
            example = False; continue
        if example: continue
        if re.match(r"^(?:`{3,}|~{3,})", value):
            flush(); fenced = not fenced; continue
        if fenced: continue
        if not value or value.startswith(("#", "<", "scope:", "core:", "note:")):
            flush(); continue
        following = lines[i] if i < len(lines) else ""
        if SEPARATOR.match(raw) or _is_table_header(raw, following):
            flush(); continue
        if value.startswith("|"):
            flush(); start = i; pending = [value]; flush(); continue
        if re.match(r"^(?:[-*]|\d+[.)])\s+", value):
            flush(); start = i
            pending = [re.sub(r"^(?:[-*]|\d+[.)])\s+", "", value)]
        else:
            if not pending: start = i
            pending.append(value)
    flush()
    return out
