#!/usr/bin/env python3
"""Check that every tool group has the shape `guide/general/tooling.md` §2 to §5 defines.

Reads: `.agent-workspace/tooling/`: the router, each group's index and each group's files.
Prints: one line for each problem, with the path, what is wrong and what to change.
Arguments: none.
Exit status: 0 when every group has the shape, 1 when a problem was found, 2 when the
tooling folder or its router does not exist.

Checked in any language: the router and the group folders name each other; a group has an
index; entry points and index rows name each other; folders are one level deep; a tool's
folder does not share its entry point's name. Checked for Python files only: imports sit at
the top of a file, and a call goes downward (entry point, tool's folder, `lib/`).
The gate cannot judge whether a file holds one responsibility.
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

from lib.console import use_utf8_output
from lib.markdown_table import is_separator, row_cells
from lib.project import enter_project_root

use_utf8_output()

# Relative to the project root, which the entry point enters before checking.
TOOLING = Path(".agent-workspace/tooling")
IGNORED = {"__pycache__"}
RESERVED_FOLDERS = {"lib", "tests"}
BACKTICKED = re.compile(r"^`([^`]+)`$")


def first_cells(index: Path) -> list[str]:
    """The backticked first cell of every table row in an index, without the backticks."""
    names = []
    for line in index.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = row_cells(line)
        if is_separator(cells):
            continue
        match = BACKTICKED.match(cells[0]) if cells else None
        if match:
            names.append(match.group(1))
    return names


def visible(folder: Path) -> list[Path]:
    return sorted(p for p in folder.iterdir() if p.name not in IGNORED and not p.name.startswith("."))


def imported_names(path: Path) -> tuple[list[str], list[int]]:
    """Top-level module names a Python file imports, and the lines of imports that
    follow other code at module level. A file that does not parse reports nothing here."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return [], []
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.append(node.module.split(".")[0])
    late: list[int] = []
    code_seen = False
    for index, node in enumerate(tree.body):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if code_seen:
                late.append(node.lineno)
            continue
        is_docstring = (index == 0 and isinstance(node, ast.Expr)
                        and isinstance(getattr(node, "value", None), ast.Constant))
        if not is_docstring:
            code_seen = True
    return names, late


def check_group(group: Path) -> list[str]:
    problems: list[str] = []
    index = group / "index.md"
    items = visible(group)
    entries = [p for p in items if p.is_file() and p.name != "index.md"]
    folders = [p for p in items if p.is_dir()]
    tool_folders = [p for p in folders if p.name not in RESERVED_FOLDERS]

    if not index.is_file():
        problems.append(f"{group}: the group has no index.md — add one with a row for each tool")
    else:
        rows = [name for name in first_cells(index) if "/" not in name]
        for entry in entries:
            if entry.name not in rows:
                problems.append(f"{entry}: the entry point has no row in {index} — add its row")
        for name in rows:
            if not (group / name).is_file():
                problems.append(f"{index}: a row names `{name}`, which is not a file of the group"
                                " — remove the row or restore the file")

    if entries and not (group / "tests").is_dir():
        problems.append(f"{group}: the group has tools and no tests/ folder — add tests/ with a test for each tool")

    entry_stems = {p.stem for p in entries}
    for folder in folders:
        if folder.name in entry_stems:
            problems.append(f"{folder}: the folder shares its name with an entry point"
                            " — name it after what the tool works on")
        for inner in visible(folder):
            if inner.is_dir() and not (folder.name == "tests" and inner.name == "fixtures"):
                problems.append(f"{inner}: a folder inside {folder.name}/ — a group is one level deep; move its files up")

    folder_names = {p.name for p in tool_folders}
    users: dict[str, set[str]] = {name: set() for name in folder_names}
    for path in [p for p in entries if p.suffix == ".py"]:
        names, late = imported_names(path)
        for line in late:
            problems.append(f"{path}:{line}: an import follows other code — move it to the top of the file,"
                            " or move the part that needs it to its own file")
        for name in names:
            if name in entry_stems and name != path.stem:
                problems.append(f"{path}: imports the entry point `{name}` — move the shared code to lib/")
            if name in folder_names:
                users[name].add(path.name)
    for name, used_by in sorted(users.items()):
        if len(used_by) > 1:
            problems.append(f"{group / name}: imported by {', '.join(sorted(used_by))}"
                            " — a tool's folder serves one tool; move the shared code to lib/")

    for folder in [p for p in folders if p.name != "tests"]:
        for path in sorted(folder.glob("*.py")):
            names, late = imported_names(path)
            for line in late:
                problems.append(f"{path}:{line}: an import follows other code — move it to the top of the file")
            for name in names:
                if name in entry_stems:
                    problems.append(f"{path}: imports the entry point `{name}` — a call goes downward only")
                elif name in folder_names and name != folder.name:
                    where = "lib/ does not import a tool" if folder.name == "lib" else "a tool does not import another tool"
                    problems.append(f"{path}: imports `{name}` — {where}; move the shared code to lib/")
    return problems


def check(tooling: Path) -> tuple[list[str], bool]:
    """Return (problems, readable). `readable` is False when there is nothing to check."""
    router = tooling / "index.md"
    if not tooling.is_dir() or not router.is_file():
        return [f"{router}: the tool router does not exist — the gate cannot derive its scope"], False
    problems: list[str] = []
    groups = []
    for item in visible(tooling):
        if item.is_dir():
            groups.append(item)
        elif item.name != "index.md":
            problems.append(f"{item}: a file directly under the tooling folder — place it in a group")
    listed = {name.rstrip("/") for name in first_cells(router) if name.endswith("/") and name.count("/") == 1}
    on_disk = {group.name for group in groups}
    for name in sorted(on_disk - listed):
        problems.append(f"{router}: the group `{name}/` has no row — add its row")
    for name in sorted(listed - on_disk):
        problems.append(f"{router}: a row names the group `{name}/`, which does not exist — remove the row")
    for group in groups:
        problems += check_group(group)
    return problems, True


def main(argv: list[str]) -> int:
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    problems, readable = check(TOOLING)
    if not readable:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 2
    if problems:
        print(f"{len(problems)} problem(s):")
        for problem in problems:
            print("  -", problem)
        return 1
    print("OK - every tool group has the shape tooling.md defines")
    return 0


if __name__ == "__main__":
    enter_project_root()
    sys.exit(main(sys.argv[1:]))
