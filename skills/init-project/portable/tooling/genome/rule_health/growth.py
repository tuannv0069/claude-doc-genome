"""The growth signal: a file that has only ever gained lines.

Reads each file's version history. Called by the entry point.
"""
from __future__ import annotations

from pathlib import Path

from lib.git import run_git

LESSONS_DIR = ".agent-workspace/lessons"
GROWTH_MIN_COMMITS = 4
GROWTH_MIN_LINES = 100


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    return s[min(len(s) - 1, int(len(s) * q))]


def is_growth_eligible(path: Path, commits: int, lines: int) -> bool:
    if LESSONS_DIR in str(path).replace("\\", "/"):
        return False
    return commits >= GROWTH_MIN_COMMITS and lines >= GROWTH_MIN_LINES


def _git_numstat(root: Path, path: Path) -> tuple[int, int, int]:
    out = run_git(["log", "--follow", "--numstat", "--format=%H", "--", str(path)], root).stdout
    added = deleted = commits = 0
    for ln in out.splitlines():
        parts = ln.split("\t")
        if len(parts) == 3 and parts[0].isdigit():
            added += int(parts[0])
            deleted += int(parts[1])
        elif ln.strip() and "\t" not in ln:
            commits += 1
    return added, deleted, commits


def signal_growth(files: list[Path], root: Path) -> tuple[list[dict], dict]:
    rows = []
    deleted_of: dict[str, int] = {}
    added_of: dict[str, int] = {}
    for p in files:
        added, deleted, commits = _git_numstat(root, p)
        if added == 0:
            continue
        lines = len(p.read_text(encoding="utf-8", errors="replace").splitlines())
        if not is_growth_eligible(p, commits, lines):
            continue
        rows.append((deleted / added, str(p), commits, lines))
        deleted_of[str(p)] = deleted
        added_of[str(p)] = added
    ratios = [r for r, _, _, _ in rows]
    stats = {
        "median": quantile(ratios, 0.5),
        "p25": quantile(ratios, 0.25),
        "p75": quantile(ratios, 0.75),
        "cut": quantile(ratios, 0.25),
        "population": len(rows),
        # CONTEXT, not a finding: a near-monotonic file must still be visible to a reader.
        # nguoi doc, du tieu chi tuyet doi `deleted == 0` khong bat chung.
        "lowest": [(round(r, 3), pth) for r, pth, _, _ in sorted(rows)[:5]],
    }
    out = []
    for ratio, path, commits, lines in rows:
        # An ABSOLUTE criterion derived from the law, not a relative ranking:
        # `doc-organization.md` §12 requires the text of a narrowed law to be DELETED. A file that
        # has never deleted a line is a measurable violation, and a CLOSABLE one - one later commit
        # deleting one line ends it. A quantile cut, by contrast, always flags exactly 25% of the
        # population however clean the corpus is.
        if deleted_of[path] == 0:
            out.append({
                "signal": "growth",
                "paths": [path],
                "lines": [],
                "text": f"delete/add={ratio:.2f}",
                "detail": f"{path} has never deleted a line - added={added_of[path]} deleted=0 "
                          f"commits={commits} lines={lines} (phan bo: median={stats['median']:.2f} p25={stats['p25']:.2f})",
            })
    return out, stats
