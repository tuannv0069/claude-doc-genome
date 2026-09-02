#!/usr/bin/env python3
"""Gate for the decision journal `.agent-workspace/decisions/`.

Law enforced, source: `guide/general/decision-journal.md` §2-§4, §8, §9.

The gate checks the SHAPE of an entry that was written: file name, frontmatter, class,
a `subject` that resolves, `supersedes` pointing at an entry that exists, and a body short
enough. The gate CANNOT catch a decision that happened and nobody recorded — you cannot
measure what does not exist (the limit is declared in §1 of the law; the backstop is a human
reading `git log` from time to time).

The per-shard entry ceiling is a per-project value, declared as `cap:` in the frontmatter of
`.agent-workspace/decisions/index.md`. Exceeding it is a WARNING, not an error — the cap is a
signal that scope is drifting, not a hard quota.

A freshly seeded journal — the router alone, no shard directory — passes with zero entries.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CLASSES = ("choice", "scope", "debt", "rule", "review")
NAME = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(" + "|".join(CLASSES) + r")-[a-z0-9][a-z0-9-]*\.md$")
SHARD = re.compile(r"^\d{4}-\d{2}$")
ARCHIVE_YEAR = re.compile(r"^\d{4}$")
BODY_MAX = 4
REQUIRED = ("class", "subject", "anchor")


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


def subject_state(repo_root: Path, subject: str) -> str:
    """`ok` | `renamed` | `missing` — the subject's path, resolved through git history (§4)."""
    path = re.split(r"\s*§", subject, maxsplit=1)[0].strip().strip("`")
    if not path:
        return "missing"
    if (repo_root / path).exists():
        return "ok"
    try:
        out = subprocess.run(
            ["git", "log", "--format=", "--name-only", "--", path],
            cwd=repo_root, capture_output=True, text=True, timeout=60,
        )
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
        if len(body) > BODY_MAX:
            problems.append(f"{rel}: entry body is {len(body)} lines, the ceiling is {BODY_MAX}")
        if not body[0].startswith("- decided:"):
            problems.append(f"{rel}: the first body line must be `- decided:`")
        for ln in body:
            if not ln.startswith("- "):
                problems.append(f"{rel}: the entry body takes `- ` bullets only: {ln!r}")

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
    ap = argparse.ArgumentParser(description="Decision journal gate")
    ap.add_argument("--dir", default=".agent-workspace/decisions",
                    help="the decision-journal directory")
    ap.add_argument("--repo-root", default=".", help="repo root, used to resolve `subject:`")
    args = ap.parse_args()

    decisions, repo_root = Path(args.dir), Path(args.repo_root)
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
    sys.exit(main())
