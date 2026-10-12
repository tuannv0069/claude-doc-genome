#!/usr/bin/env python3
"""Exercise the archive command on a temporary journal.

Only an entry that another entry supersedes may move, and only from a shard of the
year asked for. The move itself is checked on files, outside a git work tree."""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import archive_decisions as A  # noqa: E402
from lib.console import use_utf8_output  # noqa: E402
from support import check, fails  # noqa: E402

use_utf8_output()


def entry(decisions: Path, shard: str, stem: str, supersedes: str = "") -> Path:
    path = decisions / shard / f"{stem}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    extra = f"supersedes: {supersedes}\n" if supersedes else ""
    path.write_text(f"---\nclass: rule\nsubject: a.md\nanchor: test\n{extra}---\n\ndecided: something\n", encoding="utf-8")
    return path


with tempfile.TemporaryDirectory() as folder:
    decisions = Path(folder) / "decisions"
    old = entry(decisions, "2031-01", "2031-01-05-rule-old")
    entry(decisions, "2031-02", "2031-02-01-rule-new", supersedes="2031-01-05-rule-old")
    standing = entry(decisions, "2031-01", "2031-01-09-rule-standing")
    other_year = entry(decisions, "2030-12", "2030-12-30-rule-older")
    entry(decisions, "2031-03", "2031-03-01-rule-newer", supersedes="2030-12-30-rule-older")

    check(A.superseded_ids(decisions) == {"2031-01-05-rule-old", "2030-12-30-rule-older"},
          "case 1: the superseded identifiers were not read from the entries")
    picked = A.candidates(decisions, "2031")
    check(picked == [old], f"case 2: the candidates of 2031 are not the one superseded entry of that year: {picked}")
    check(A.candidates(decisions, "2029") == [], "case 3: a year with no shard produced candidates")

    with patch.object(sys, "argv", ["archive_decisions.py", "--year", "2031", "--dir", str(decisions)]), \
            patch.object(sys, "stdin", io.StringIO("")), \
            contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        status = A.main()
    check(status == 2 and old.is_file(), "case 6: no answer on standard input did not exit 2 with the entry left in place")

    moved = A.move(picked, decisions, "2031")
    check(moved == 1 and (decisions / "archive" / "2031" / old.name).is_file() and not old.exists(),
          "case 4: the superseded entry was not moved into the archive of its year")
    check(standing.is_file() and other_year.is_file(), "case 5: a standing entry or an entry of another year was moved")

for failure in fails:
    print("FAIL:", failure)
print(f"{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
