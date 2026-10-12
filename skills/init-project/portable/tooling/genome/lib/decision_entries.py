"""Finding and reading the entries of the decision journal.

Used by the journal gate (`verify_decision_log.py`) and by the archive command
(`archive_decisions.py`), which must agree on where an entry may live and how
its frontmatter is read. The layout is defined in `guide/general/decision-journal.md` §4.
"""
from __future__ import annotations

import re
from pathlib import Path

SHARD = re.compile(r"^\d{4}-\d{2}$")
ARCHIVE_YEAR = re.compile(r"^\d{4}$")


def parse_entry(path: Path):
    """Return (frontmatter, body lines, problems raised by reading the file itself)."""
    problems: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [], [f"{path}: no opening `---` frontmatter on line 1"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, [], [f"{path}: frontmatter is never closed by `---`"]
    fm: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if ":" not in raw:
            problems.append(f"{path}: frontmatter line is not `key: value`: {raw!r}")
            continue
        key, _, value = raw.partition(":")
        fm[key.strip()] = value.strip()
    body = [ln for ln in lines[end + 1:] if ln.strip()]
    return fm, body, problems


def collect(decisions: Path):
    """Every valid entry lives in `YYYY-MM/` or `archive/YYYY/`, nowhere else."""
    problems: list[str] = []
    entries: list[Path] = []
    if not decisions.exists():
        return entries, [f"{decisions}: the decision-journal directory does not exist"]
    for item in sorted(decisions.iterdir()):
        if item.is_file():
            if item.name != "index.md":
                problems.append(f"{item}: file sits outside a shard — an entry belongs in `YYYY-MM/`")
            continue
        if item.name == "archive":
            for year in sorted(item.iterdir()):
                if not year.is_dir() or not ARCHIVE_YEAR.match(year.name):
                    problems.append(f"{year}: only `YYYY` directories are allowed under `archive/`")
                    continue
                entries += sorted(p for p in year.iterdir() if p.is_file())
            continue
        if not SHARD.match(item.name):
            problems.append(f"{item}: directory is not a `YYYY-MM` shard")
            continue
        entries += sorted(p for p in item.iterdir() if p.is_file())
    return entries, problems
