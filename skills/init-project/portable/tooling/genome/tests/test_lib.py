#!/usr/bin/env python3
"""Exercise the shared library of this group: table rows, git output and the project root.

The git case writes non-ASCII text into a temporary repository and reads it back while the
host's preferred encoding is forced to a legacy code page, because decoding git output with
that encoding is the failure `lib/git.py` exists to prevent."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import git, markdown_table, project  # noqa: E402
from lib.console import use_utf8_output  # noqa: E402
from support import check, fails  # noqa: E402

use_utf8_output()

# --- markdown_table ---------------------------------------------------------
check(markdown_table.row_cells("| a | b  |  c |") == ["a", "b", "c"], "row_cells: cells were not trimmed and split")
check(markdown_table.row_cells("  | one |  |") == ["one", ""], "row_cells: an empty cell was dropped")
check(markdown_table.is_separator(markdown_table.row_cells("|---|:--|--:|")), "is_separator: a delimiter row was not recognized")
check(not markdown_table.is_separator(markdown_table.row_cells("| a | - |")), "is_separator: a data row was taken for a delimiter row")
check(not markdown_table.is_separator([]), "is_separator: no cells at all was taken for a delimiter row")

# --- project ----------------------------------------------------------------
check((project.PROJECT_ROOT / ".agent-workspace" / "tooling").is_dir(),
      f"PROJECT_ROOT does not hold .agent-workspace/tooling: {project.PROJECT_ROOT}")
check(project.WORKSPACE == project.PROJECT_ROOT / ".agent-workspace", "WORKSPACE is not the workspace of PROJECT_ROOT")

started_in = Path.cwd()
with tempfile.TemporaryDirectory() as elsewhere:
    os.chdir(elsewhere)
    try:
        entered = project.enter_project_root()
        check(entered == project.PROJECT_ROOT and Path.cwd() == project.PROJECT_ROOT,
              "enter_project_root: the working directory is not the project root")
        check(project.caller_path("notes/a.md") == Path(elsewhere) / "notes" / "a.md",
              "caller_path: a relative argument was not kept relative to the starting directory")
        absolute = str(Path(elsewhere) / "b.md")
        check(project.caller_path(absolute) == Path(absolute), "caller_path: an absolute argument was changed")
        project.enter_project_root()
        check(project.caller_path("notes/a.md") == Path("notes/a.md"),
              "caller_path: started from the project root, a relative argument was rewritten")
    finally:
        os.chdir(started_in)

# --- git --------------------------------------------------------------------
with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    text = "Tiếng Việt: “đọc nguồn trước”.\n"
    (root / "note.md").write_text(text, encoding="utf-8")
    for args in (["init", "-q"], ["add", "note.md"],
                 ["-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-q", "-m", "note"]):
        subprocess.run(["git", "-c", "core.hooksPath=", *args], cwd=root, check=True, capture_output=True)
    with patch("subprocess._text_encoding", return_value="cp1252"):
        shown = git.run_git(["show", "HEAD:note.md"], root)
    check(shown.returncode == 0 and shown.stdout == text, "run_git: UTF-8 content was decoded with the host's encoding")
    missing = git.run_git(["show", "HEAD:absent.md"], root)
    check(missing.returncode != 0 and missing.stderr != "", "run_git: a failing command did not return its code and message")

for failure in fails:
    print("FAIL:", failure)
print(f"{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
