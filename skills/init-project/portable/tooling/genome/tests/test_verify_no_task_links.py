#!/usr/bin/env python3
"""Exercise the task-workspace citation gate with temporary trees.

A bare mention of the workspace, a placeholder component and a glob must pass;
a concrete component must fail, in either slash form, once per occurrence; the
structural exemptions must hold exactly as the gate's docstring states them;
and inside a git work tree the gate must read untracked files that are not
ignored while never reading the ignored workspace."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import verify_no_task_links as V  # noqa: E402
from lib.console import use_utf8_output  # noqa: E402

use_utf8_output()

fails: list[str] = []
cases = 0


def check(cond: bool, msg: str) -> None:
    global cases
    cases += 1
    if not cond:
        fails.append(msg)


def build(tmp: Path, files: dict[str, str | bytes]) -> Path:
    """Write a fake project tree; return its root."""
    d = Path(tempfile.mkdtemp(dir=tmp))
    for rel, content in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_text(content, encoding="utf-8")
    return d


with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    if V.repo_root(tmp) is not None:
        print("SKIP - the system temp directory lies inside a git work tree; the walk-path cases would not run as designed")
        sys.exit(2)

    # --- no false alarm: naming the location is allowed ------------------
    d = build(tmp, {
        "CLAUDE.md": "Place working files under `.agent-workspace/tasks/<task-slug>/`.\n",
        "guide.md": "The project ignores `.agent-workspace/tasks/` and `.agent-workspace/tasks/**`.\n",
        ".gitignore": ".agent-workspace/tasks/\n",
        "note.md": 'The owner said "không link tới .agent-workspace\\tasks".\n',
    })
    check(V.check(d) == [], f"case 1: clean tree reported: {V.check(d)}")

    # --- a concrete component fails, with the file and line ---------------
    d = build(tmp, {
        "docs/readme.md": "Intro.\nSee `.agent-workspace/tasks/research-x/findings.md`.\n",
    })
    got = V.check(d)
    check(len(got) == 1 and got[0].startswith("docs/readme.md:2:"),
          f"case 2: concrete forward-slash path not reported as expected: {got}")

    d = build(tmp, {"docs/readme.md": "See .agent-workspace\\tasks\\pv-Bu0xNDLNORU\\review.md\n"})
    got = V.check(d)
    check(len(got) == 1 and "pv-Bu0xNDLNORU" in got[0],
          f"case 3: concrete backslash path not reported: {got}")

    d = build(tmp, {"a.md": "x .agent-workspace/tasks/one/ and .agent-workspace/tasks/two/\n"})
    got = V.check(d)
    check(len(got) == 2, f"case 4: two citations on one line must give two findings: {got}")

    d = build(tmp, {"a.md": "xem .agent-workspace/tasks/kiểm-chứng-khung/findings.md\n"})
    got = V.check(d)
    check(len(got) == 1 and "kiểm-chứng-khung" in got[0],
          f"case 5: a non-ASCII slug must be reported in full: {got}")

    # --- structural exemptions ------------------------------------------
    d = build(tmp, {
        ".agent-workspace/lessons/write-docs.md":
            "- record: cited `.agent-workspace/tasks/pv-Bu0xNDLNORU/` which is gone. seen: 1\n",
    })
    check(V.check(d) == [], f"case 6: lesson store body should be exempt: {V.check(d)}")

    d = build(tmp, {
        ".agent-workspace/decisions/2026-09/2026-09-22-rule-x.md":
            "---\nclass: rule\nsubject: docs/a.md\nanchor: docs/b.md\n---\n\n"
            "because: it cited `.agent-workspace/tasks/pv-Bu0xNDLNORU/`.\n",
    })
    check(V.check(d) == [], f"case 7: decision body should be exempt: {V.check(d)}")

    d = build(tmp, {
        ".agent-workspace/decisions/2026-09/2026-09-22-rule-x.md":
            "---\nclass: rule\nsubject: docs/a.md\n"
            "anchor: .agent-workspace/tasks/research-x/findings.md\n---\n\ndecided: x\n",
    })
    got = V.check(d)
    check(len(got) == 1 and ":4:" in got[0],
          f"case 8: decision anchor pointing at the workspace must fail: {got}")

    d = build(tmp, {
        ".agent-workspace/decisions/2026-09/2026-09-22-rule-x.md":
            "﻿---\nclass: rule\nsubject: docs/a.md\n"
            "anchor: .agent-workspace/tasks/research-x/findings.md\n---\n\ndecided: x\n",
    })
    got = V.check(d)
    check(len(got) == 1 and ":4:" in got[0],
          f"case 9: a byte-order mark must not hide the frontmatter: {got}")

    d = build(tmp, {
        ".agent-workspace/decisions/2026-09/2026-09-22-rule-x.md":
            "# no frontmatter\n\nsee .agent-workspace/tasks/research-x/findings.md\n",
    })
    got = V.check(d)
    check(len(got) == 1 and ":3:" in got[0],
          f"case 10: a decision entry without frontmatter is checked in full: {got}")

    d = build(tmp, {
        ".agent-workspace/tooling/genome/tests/test_something.py":
            'put(root, ".agent-workspace/tasks/task/notes.md", "x")\n',
        ".agent-workspace/tooling/genome/verify_no_task_links.py":
            'CONCRETE = r".agent-workspace/tasks/x"\n',
    })
    check(V.check(d) == [], f"case 11: test fixtures and the gate itself are exempt: {V.check(d)}")

    # --- the ignored workspace itself is never read on the walk path ------
    d = build(tmp, {
        ".agent-workspace/tasks/research-x/findings.md": "see .agent-workspace/tasks/research-x/plan.md\n",
        "ok.md": "nothing here\n",
    })
    check(V.check(d) == [], f"case 12: files inside the task workspace are not input on the walk path: {V.check(d)}")

    # --- encodings ------------------------------------------------------
    d = build(tmp, {"img.png": b"\x89PNG\r\n\x1a\n\xff\xfe.agent-workspace/tasks/x", "ok.md": "fine\n"})
    check(V.check(d) == [], f"case 13: a binary file is skipped: {V.check(d)}")

    d = build(tmp, {"doc.md": "see .agent-workspace/tasks/x/".encode("utf-16"), "ok.md": "fine\n"})
    got = V.check(d)
    check(len(got) == 1 and "not valid UTF-8" in got[0],
          f"case 14: a text file the gate cannot read is reported, not skipped: {got}")

    # --- an empty input is a gate failure, never a pass -------------------
    d = build(tmp, {})
    got = V.check(d)
    check(len(got) == 1 and "refuses" in got[0], f"case 15: empty tree must not pass: {got}")

    # --- inside a git work tree: tracked + untracked, never ignored -------
    if shutil.which("git"):
        d = build(tmp, {
            ".gitignore": ".agent-workspace/tasks/\n",
            "tracked.md": "clean\n",
            ".agent-workspace/tasks/research-x/findings.md": "see .agent-workspace/tasks/research-x/plan.md\n",
        })
        git = ["git", "-C", str(d)]
        subprocess.run(git + ["init", "-q"], check=True, capture_output=True)
        subprocess.run(git + ["add", ".gitignore", "tracked.md"], check=True, capture_output=True)
        check(V.repo_root(d) is not None, "case 16: repo_root must find the temporary work tree")
        check(V.check(d) == [], f"case 16: tracked clean tree with an ignored workspace must pass: {V.check(d)}")
        (d / "new.md").write_text("see .agent-workspace/tasks/research-x/findings.md\n", encoding="utf-8")
        got = V.check(d)
        check(len(got) == 1 and got[0].startswith("new.md:1:"),
              f"case 17: an untracked file not yet added must be read: {got}")
        sub = d / "docs"; sub.mkdir()
        check(V.repo_root(sub) == V.repo_root(d), "case 18: repo_root from a subdirectory resolves to the work tree")
    else:
        print("note: git not on PATH; cases 16–18 (git work tree) not run")

if fails:
    print(f"{len(fails)} failure(s) in {cases} check(s):")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print(f"OK - verify_no_task_links: {cases} checks hold")
