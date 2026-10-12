#!/usr/bin/env python3
"""Move superseded decisions into the journal archive.

Only an entry named by another entry's supersedes field is eligible. An old
standing decision stays in its shard. The command lists its candidates and
asks before moving them; --yes records the caller's choice to proceed directly.
The journal workflow is defined in guide/general/decision-journal.md, section 9.

Reads: the journal under `--dir`. Prints: the entries that would move. Changes: moves those entries
into `archive/<year>/` after the answer `y`, or at once with `--yes`.
Exit status: 0 when the command ran, moved or not; 1 when the journal does not exist;
2 when it has to ask and standard input gives no answer, or the arguments are invalid."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lib.console import use_utf8_output
from lib.decision_entries import SHARD, collect, parse_entry
from lib.git import run_git
from lib.project import caller_path, enter_project_root

use_utf8_output()


def superseded_ids(decisions: Path) -> set:
    ids = set()
    for path in collect(decisions)[0]:
        fm, _body, _problems = parse_entry(path)
        if fm.get("supersedes"):
            ids.add(fm["supersedes"])
    return ids


def candidates(decisions: Path, year: str) -> list:
    retired = superseded_ids(decisions)
    out = []
    for shard in sorted(p for p in decisions.iterdir() if p.is_dir() and SHARD.match(p.name)):
        if not shard.name.startswith(year):
            continue
        out += sorted(p for p in shard.iterdir() if p.is_file() and p.stem in retired)
    return out


def move(paths: list, decisions: Path, year: str) -> int:
    target = decisions / "archive" / year
    target.mkdir(parents=True, exist_ok=True)
    for path in paths:
        dest = target / path.name
        done = run_git(["mv", str(path), str(dest)], Path.cwd())
        if done.returncode != 0:
            path.replace(dest)
    for shard in sorted(p for p in decisions.iterdir() if p.is_dir() and SHARD.match(p.name)):
        if shard.name.startswith(year) and not any(shard.iterdir()):
            shard.rmdir()
    return len(paths)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", required=True, help="year of the shards to sweep, as YYYY")
    ap.add_argument("--dir", help="the decision-journal directory (default: .agent-workspace/decisions in the project)")
    ap.add_argument("--yes", action="store_true", help="do not ask, move straight away")
    args = ap.parse_args()

    decisions = caller_path(args.dir) if args.dir else Path(".agent-workspace/decisions")
    if not decisions.exists():
        print(f"{decisions}: does not exist")
        return 1

    picked = candidates(decisions, args.year)
    if not picked:
        print(f"{args.year}: no entry has been superseded — nothing to move")
        return 0

    print(f"{len(picked)} entry/entries will move into archive/{args.year}/:")
    for path in picked:
        print("  -", path.relative_to(decisions))
    if not args.yes:
        try:
            answer = input("move them? [y/N] ").strip().lower()
        except EOFError:
            print("no answer on standard input; nothing was moved. Pass --yes to move without asking.",
                  file=sys.stderr)
            return 2
        if answer != "y":
            print("cancelled — nothing moved")
            return 0
    print(f"moved {move(picked, decisions, args.year)} entry/entries")
    return 0


if __name__ == "__main__":
    enter_project_root()
    sys.exit(main())
