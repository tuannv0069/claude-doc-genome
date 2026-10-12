#!/usr/bin/env python3
"""Check role routing and the section read by checking roles.

The gate verifies that registered roles exist, that optional handoff references
resolve, and that each role exposes its checking criteria in section 6. It does
not impose a document length, a fixed section count, or a style for examples.

Reads: `.agent-workspace/guide/roles/`, or one role file with `--file <path>`.
Prints: the problems found, or one OK line. Changes nothing.
Exit status: 0 when nothing is wrong, 1 when a problem was found or the router could not be read.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from lib.console import use_utf8_output
from lib.markdown_table import is_separator, row_cells
from lib.project import caller_path, enter_project_root

use_utf8_output()

ROLES = Path(".agent-workspace/guide/roles")
HEADER_CELLS = ["work type", "primary role", "checking roles"]
ROLE_NAME = re.compile(r"^[a-z][a-z0-9-]*$")
BACKTICKED = re.compile(r"`([a-z][a-z0-9-]*)`")
SECTION = re.compile(r"^#{1,6}\s+§(\d+)\b", re.M)
REQUIRED = [6]
# The router and the role template sit beside the group folders and are not roles
# (`role-selection.md` §6).
NOT_ROLES = {"index.md", "_template.md"}


def parse_router(index_path: Path) -> tuple[list[dict], list[str]]:
    """Read the router table(s). Returns (rows, problems).

    More than one table may carry the header — the router keeps one table per work group —
    and rows from every table are collected. A changed format becomes a problem and NEVER a
    silent zero rows: a gate that cannot read its input is a failure OF THE GATE
    (`verification-gate-design.md` §1).
    """
    problems: list[str] = []
    rows: list[dict] = []
    header_ok = False
    for i, line in enumerate(index_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = row_cells(line)
        if [c.lower() for c in cells] == HEADER_CELLS:
            header_ok = True
            continue
        if not header_ok:
            continue
        if is_separator(cells):
            continue
        if len(cells) != 3:
            problems.append(
                f"{index_path}:{i}: row has {len(cells)} cells, the router table needs 3"
                " — the format changed and the gate cannot read this row correctly")
            continue
        if not ROLE_NAME.match(cells[1]):
            problems.append(
                f"{index_path}:{i}: `primary role` cell is {cells[1]!r},"
                " it must be exactly one kebab-case role name")
            continue
        checking = [c.strip() for c in cells[2].split(",") if c.strip()]
        bad = [c for c in checking if not ROLE_NAME.match(c)]
        if bad:
            problems.append(
                f"{index_path}:{i}: `checking roles` cell holds entries that are not role names: {bad}")
            continue
        if cells[1] in checking:
            problems.append(
                f"{index_path}:{i}: role `{cells[1]}` is named as a checking role for its own row")
            continue
        rows.append({"work": cells[0], "primary": cells[1], "checking": checking})
    if not header_ok:
        problems.append(
            f"{index_path}: header row `| {' | '.join(HEADER_CELLS)} |` not found"
            " — the table format changed")
    return rows, problems


def sections(text: str) -> dict[int, str]:
    """Return {section number: section body}, body running from its heading to the next."""
    marks = [(int(m.group(1)), m.start()) for m in SECTION.finditer(text)]
    out: dict[int, str] = {}
    for idx, (num, start) in enumerate(marks):
        end = marks[idx + 1][1] if idx + 1 < len(marks) else len(text)
        out[num] = text[start:end]
    return out


def check_file(path: Path, known: set[str]) -> list[str]:
    """Check the role section contract and any declared handoff targets."""
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    secs = sections(text)
    for n in REQUIRED:
        if n not in secs:
            problems.append(f"{path}: §{n} missing")
    if known:
        for target in BACKTICKED.findall(secs.get(7, "")):
            if target not in known:
                problems.append(
                    f"{path}: §7 hands off to `{target}`, a role absent from the router")
    return problems


def role_files(roles: Path) -> tuple[dict[str, Path], list[str]]:
    """Return ({role name: file}, problems) for the group layout `roles/<group>/<name>.md`.

    The router and the role template beside it are skipped. A role file outside a group folder, a folder nested inside a group, a group name that is
    not kebab-case and one role name used in two groups are all layout problems: the router
    names a role by its file stem alone, so the name must identify exactly one file.
    """
    problems: list[str] = []
    found: dict[str, Path] = {}
    for p in sorted(roles.rglob("*")):
        rel = p.relative_to(roles)
        if p.is_dir():
            if len(rel.parts) > 1:
                problems.append(f"{p}: folder nested inside a group; roles live one level below the router")
            elif not ROLE_NAME.match(p.name):
                problems.append(f"{p}: group folder name must be kebab-case")
            continue
        if p.suffix != ".md" or rel.as_posix() in NOT_ROLES:
            continue
        if len(rel.parts) == 1:
            problems.append(f"{p}: role file is not inside a group folder")
            continue
        if len(rel.parts) > 2:
            continue  # the nested folder is already reported
        if p.stem in found:
            problems.append(f"{p}: role name `{p.stem}` is also used by {found[p.stem]}")
            continue
        found[p.stem] = p
    return found, problems


def check_tree(roles: Path) -> list[str]:
    index = roles / "index.md"
    if not index.is_file():
        return [f"{index}: router not found — the gate cannot derive its scope"]
    rows, problems = parse_router(index)
    if not rows:
        return problems or [f"{index}: the router table parsed no row — the gate refuses to run empty"]

    registered = {r["primary"] for r in rows} | {c for r in rows for c in r["checking"]}
    files, layout = role_files(roles)
    problems.extend(layout)

    for name in sorted(registered - set(files)):
        problems.append(f"{index}: role `{name}` has no file in a group folder")
    for name in sorted(set(files) - registered):
        problems.append(f"{files[name]}: role file appears in no router row")

    for name in sorted(files):
        problems.extend(check_file(files[name], registered))
    return problems


def main(argv: list[str]) -> int:
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if "--file" in argv:
        target = caller_path(argv[argv.index("--file") + 1])
        if not target.is_file():
            print(f"{target}: file not found")
            return 1
        problems = check_file(target, set())
        label = str(target)
    else:
        problems = check_tree(ROLES)
        label = str(ROLES)
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        return 1
    print(f"OK - {label}: role routing and checking sections are valid")
    return 0


if __name__ == "__main__":
    enter_project_root()
    sys.exit(main(sys.argv[1:]))
