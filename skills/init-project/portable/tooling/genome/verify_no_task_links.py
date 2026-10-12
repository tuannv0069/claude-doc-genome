#!/usr/bin/env python3
"""Fail when a committed file cites a concrete path under the task workspace.

`.agent-workspace/tasks/` is ignored by version control and may be deleted at
any time, so a committed file that links, cites or anchors to a path inside it
points at something the next reader cannot open (`doc-organization.md` §10).

Unit measured (`verification-gate-design.md` §1): one line of one text file
that version control tracks or would add — tracked files plus untracked files
not covered by the ignore rules, so that a file about to be committed for the
first time is read too. A line is reported for every occurrence of the task
workspace path followed by a concrete component, such as
`.agent-workspace/tasks/pv-Bu0xNDLNORU/`. Naming the location itself is
allowed: a bare `.agent-workspace/tasks/`, a placeholder component such as
`<task-slug>`, or a glob such as `**` passes, because the rule bans citing a
disposable file, not naming the place where disposable files live.

Structural exemptions, each because the file's job is to hold the path:
- a lesson store under `.agent-workspace/lessons/` — an append-only record
  that cites the path as evidence of the incident it describes;
- the body of a decision entry under `.agent-workspace/decisions/` — history
  that must not be edited; its `subject:` and `anchor:` frontmatter lines are
  still checked, because an anchor pointing at the workspace was the original
  defect, and an entry without frontmatter is checked in full;
- a `test_*.py` file and this gate itself, which contain the pattern as code.

A file with a text extension that is not valid UTF-8 is reported, because the
gate cannot read it; a file with any other extension that is not UTF-8 is
taken to be binary and skipped. A UTF-8 byte-order mark is accepted. Outside a
git work tree the gate walks the directory and skips the ignored workspace
directories by name. The gate cannot tell a link from a mention inside the
same sentence, and it cannot see a path that was paraphrased instead of
written.

Reads: every tracked file and every untracked file that is not ignored.
Prints: one line for each citation found, or one OK line. Changes nothing.
Exit status: 0 when no file cites the task workspace, 1 when one does or no file could be read."""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from lib.console import use_utf8_output
from lib.project import enter_project_root

use_utf8_output()

CONCRETE = re.compile(r"\.agent-workspace[/\\]tasks[/\\]([^\s/\\`'\"<>()\[\]|*]+)")
FRONTMATTER_LOCATOR = re.compile(r"^(subject|anchor):")
SKIP_DIRS_ANYWHERE = {".git", "node_modules", "__pycache__"}
WORKSPACE_STATE_DIRS = {"tasks", "worktrees"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".tpl", ".py", ".mjs",
                 ".js", ".ts", ".tsx", ".css", ".html", ".csv", ".toml", ".ini"}
SELF = Path(__file__).name


def repo_root(start: Path) -> Path | None:
    """The git work tree containing `start`, or None outside one."""
    try:
        out = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8", "replace").strip()
        return Path(out) if out else None
    except (OSError, subprocess.CalledProcessError):
        return None


def collect_files(root: Path) -> list[Path]:
    """Tracked files plus untracked files that the ignore rules do not cover,
    when `root` is a git work tree; otherwise a walk that skips the workspace
    state directories. Paths are relative to `root`."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others",
             "--exclude-standard"],
            capture_output=True, check=True,
        ).stdout
        names = [n for n in out.decode("utf-8", "replace").split("\0") if n]
        return sorted({Path(n) for n in names})
    except (OSError, subprocess.CalledProcessError):
        pass
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS_ANYWHERE
            and not (rel.name == ".agent-workspace" and d in WORKSPACE_STATE_DIRS)
        ]
        for f in filenames:
            found.append(rel / f)
    return sorted(found)


def exemption(rel: Path) -> str:
    """'' when the file is checked in full, 'locators' when only its frontmatter
    locator lines are checked, 'all' when the file is skipped."""
    parts = rel.as_posix().split("/")
    name = rel.name
    if name == SELF or (name.startswith("test_") and name.endswith(".py")):
        return "all"
    if ".agent-workspace" in parts:
        i = parts.index(".agent-workspace")
        tier = parts[i + 1] if len(parts) > i + 1 else ""
        if tier == "lessons":
            return "all"
        if tier == "decisions":
            return "locators"
    return ""


def check(root: Path, files: list[Path] | None = None) -> list[str]:
    files = collect_files(root) if files is None else files
    if not files:
        return [f"{root}: no file to check — the gate refuses to pass an empty input"]
    problems: list[str] = []
    for rel in files:
        mode = exemption(rel)
        if mode == "all":
            continue
        path = root / rel
        if not path.is_file():
            continue
        try:
            text = path.read_bytes().decode("utf-8-sig")
        except UnicodeDecodeError:
            if path.suffix.lower() in TEXT_SUFFIXES:
                problems.append(
                    f"{rel.as_posix()}: not valid UTF-8 — the gate cannot read this text file")
            continue
        lines = text.splitlines()
        if mode == "locators" and not (lines and lines[0].strip() == "---"):
            mode = ""
        in_frontmatter = False
        for i, line in enumerate(lines, 1):
            if mode == "locators":
                if i == 1:
                    in_frontmatter = True
                    continue
                if line.strip() == "---":
                    break
                if not FRONTMATTER_LOCATOR.match(line):
                    continue
            for m in CONCRETE.finditer(line):
                problems.append(
                    f"{rel.as_posix()}:{i}: cites `.agent-workspace/tasks/{m.group(1)}`,"
                    " a path under the disposable task workspace"
                    " — move the content to its work-product destination and point there"
                )
    return problems


def main(argv: list[str]) -> int:
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    root = repo_root(Path.cwd()) or Path.cwd()
    problems = check(root)
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        return 1
    print(f"OK - no committed or to-be-committed file cites a concrete path under"
          f" .agent-workspace/tasks/ ({len(collect_files(root))} file(s) read from {root})")
    return 0


if __name__ == "__main__":
    enter_project_root()
    sys.exit(main(sys.argv[1:]))
