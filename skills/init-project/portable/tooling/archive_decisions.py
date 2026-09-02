#!/usr/bin/env python3
"""Hot/cold cut of the decision journal — `guide/general/decision-journal.md` §9.

Moves into `archive/YYYY/` exactly the entries a LATER entry has superseded. A standing entry
stays where it is however old it gets: it is still the current answer for its subject. A
renamed subject does NOT end an entry's life (§9).

The operation is hard to undo, so it prints the list and asks before moving; `--yes` skips
the question.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_decision_log import SHARD, collect, parse_entry  # noqa: E402


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
        done = subprocess.run(["git", "mv", str(path), str(dest)], capture_output=True, text=True)
        if done.returncode != 0:
            path.replace(dest)
    for shard in sorted(p for p in decisions.iterdir() if p.is_dir() and SHARD.match(p.name)):
        if shard.name.startswith(year) and not any(shard.iterdir()):
            shard.rmdir()
    return len(paths)


def main() -> int:
    ap = argparse.ArgumentParser(description="Move superseded entries into the archive")
    ap.add_argument("--year", required=True, help="year of the shards to sweep, as YYYY")
    ap.add_argument("--dir", default=".agent-workspace/decisions",
                    help="the decision-journal directory")
    ap.add_argument("--yes", action="store_true", help="do not ask, move straight away")
    args = ap.parse_args()

    decisions = Path(args.dir)
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
        answer = input("move them? [y/N] ").strip().lower()
        if answer != "y":
            print("cancelled — nothing moved")
            return 0
    print(f"moved {move(picked, decisions, args.year)} entry/entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
