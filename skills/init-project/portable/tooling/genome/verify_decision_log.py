#!/usr/bin/env python3
"""Gate for the decision journal `.agent-workspace/decisions/`.

Law enforced, source: `guide/general/decision-journal.md` §2-§4, §8, §9.

The gate checks the SHAPE of an entry that was written: file name, frontmatter, class,
a `subject` that resolves, `supersedes` pointing at an entry that exists, and a nonempty recorded decision. The gate CANNOT catch a decision that happened and nobody recorded — you cannot
measure what does not exist (the limit is declared in §1 of the law; the backstop is a human
reading `git log` from time to time).

The per-shard entry ceiling is a per-project value, declared as `cap:` in the frontmatter of
`.agent-workspace/decisions/index.md`. Exceeding it is a WARNING, not an error — the cap is a
signal that scope is drifting, not a hard quota.

A freshly seeded journal — the router alone, no shard directory — passes with zero entries.

Reads: the journal under `--dir` and, through git, the history of each entry's subject under `--repo-root`.
Prints: warnings, then the problems found or one OK line. Changes nothing.
Exit status: 0 when no problem was found, with or without warnings; 1 when a problem was found.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from lib.console import use_utf8_output
from lib.decision_entries import SHARD, collect, parse_entry
from lib.git import run_git
from lib.project import caller_path, enter_project_root

use_utf8_output()

CLASSES = ("choice", "scope", "debt", "rule", "review")
NAME = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(" + "|".join(CLASSES) + r")-[a-z0-9][a-z0-9-]*\.md$")
REQUIRED = ("class", "subject", "anchor")


def subject_state(repo_root: Path, subject: str) -> str:
    """`ok` | `renamed` | `missing` — the subject's path, resolved through git history (§4)."""
    path = re.split(r"\s*§", subject, maxsplit=1)[0].strip().strip("`")
    if not path:
        return "missing"
    if (repo_root / path).exists():
        return "ok"
    try:
        out = run_git(["log", "--format=", "--name-only", "--", path], repo_root, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return "missing"
    return "renamed" if out.returncode == 0 and out.stdout.strip() else "missing"


def read_cap(index_path: Path):
    if not index_path.exists():
        return None
    for line in index_path.read_text(encoding="utf-8").splitlines()[:20]:
        m = re.match(r"^cap:\s*(\d+)\s*$", line)
        if m:
            return int(m.group(1))
    return None


def check(decisions: Path, repo_root: Path):
    entries, problems = collect(decisions)
    warnings: list[str] = []
    ids: dict[str, Path] = {}
    superseded_by: list = []

    for path in entries:
        rel = path.relative_to(decisions)
        m = NAME.match(path.name)
        if not m:
            problems.append(f"{rel}: file name does not match `YYYY-MM-DD-<class>-<slug>.md`")
            continue
        year, month, _day, klass = m.groups()
        stem = path.stem
        if stem in ids:
            problems.append(f"{rel}: id collides with {ids[stem].relative_to(decisions)}")
            continue
        ids[stem] = path
        parent = path.parent.name
        if path.parent.parent.name == "archive":
            if parent != year:
                problems.append(f"{rel}: an entry from {year} sits in `archive/{parent}`")
        elif parent != f"{year}-{month}":
            problems.append(f"{rel}: an entry dated {year}-{month} sits in shard `{parent}`")

        fm, body, read_problems = parse_entry(path)
        problems += read_problems
        if read_problems:
            continue
        for key in REQUIRED:
            if not fm.get(key):
                problems.append(f"{rel}: frontmatter has no `{key}:`")
        if fm.get("class") and fm["class"] != klass:
            problems.append(
                f"{rel}: `class: {fm['class']}` differs from the class `{klass}` in the file name")
        if fm.get("supersedes"):
            if fm["supersedes"] == stem:
                problems.append(f"{rel}: `supersedes:` points at itself")
            else:
                superseded_by.append((path, fm["supersedes"]))
        if fm.get("subject"):
            state = subject_state(repo_root, fm["subject"])
            if state == "missing":
                problems.append(
                    f"{rel}: `subject: {fm['subject']}` does not resolve to a real path")
            elif state == "renamed":
                warnings.append(
                    f"{rel}: subject was renamed or deleted and survives only in git history"
                    " — the entry stays as written")
        if not body:
            problems.append(f"{rel}: entry body is empty")
            continue
        # Field labels are data. Paragraph length and list formatting are not.
        match = re.search(
            r"^(?:[-*]\s+)?decided:\s*(.*?)(?=^(?:[-*]\s+)?(?:because|rejected|unlocked by):|\Z)",
            "\n".join(body), re.M | re.S,
        )
        if not match or not match.group(1).strip():
            problems.append(f"{rel}: entry has no nonempty `decided:` field")

    for path, target in superseded_by:
        if target not in ids:
            problems.append(
                f"{path.relative_to(decisions)}: `supersedes: {target}` points at no entry")

    cap = read_cap(decisions / "index.md")
    if cap:
        for shard in sorted(p for p in decisions.iterdir() if p.is_dir() and SHARD.match(p.name)):
            count = len([p for p in shard.iterdir() if p.is_file()])
            if count > cap:
                warnings.append(
                    f"{shard.name}: {count} entries against a declared cap of {cap}"
                    " — re-read the admission test in §1")
    return problems, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", help="the decision-journal directory (default: .agent-workspace/decisions in the project)")
    ap.add_argument("--repo-root", help="repository root used to resolve `subject:` (default: the project root)")
    args = ap.parse_args()

    decisions = caller_path(args.dir) if args.dir else Path(".agent-workspace/decisions")
    repo_root = caller_path(args.repo_root) if args.repo_root else Path(".")
    problems, warnings = check(decisions, repo_root)
    for w in warnings:
        print("  ! ", w)
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        return 1
    total = len(collect(decisions)[0])
    print(f"OK - decision journal: {total} well-formed entry/entries, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    enter_project_root()
    sys.exit(main())
