#!/usr/bin/env python3
"""Check role routing and the section read by checking roles.

The gate verifies that registered roles exist, that optional handoff references
resolve, and that each role exposes its checking criteria in section 6. It does
not impose a document length, a fixed section count, or a style for examples.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROLES = Path(".agent-workspace/guide/roles")
HEADER_CELLS = ["work type", "primary role", "checking roles"]
ROLE_NAME = re.compile(r"^[a-z][a-z0-9-]*$")
BACKTICKED = re.compile(r"`([a-z][a-z0-9-]*)`")
SECTION = re.compile(r"^#{1,6}\s+§(\d+)\b", re.M)
REQUIRED = [6]


def parse_router(index_path: Path) -> tuple[list[dict], list[str]]:
    """Read the router table(s). Returns (rows, problems).

    More than one table may carry the header — §1 holds the genome roles, §1a the project
    roles — and rows from both are collected. A changed format becomes a problem and NEVER a
    silent zero rows: a gate that cannot read its input is a failure OF THE GATE
    (`verification-gate-design.md` §1).
    """
    problems: list[str] = []
    rows: list[dict] = []
    header_ok = False
    for i, line in enumerate(index_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if [c.lower() for c in cells] == HEADER_CELLS:
            header_ok = True
            continue
        if not header_ok:
            continue
        if cells and set("".join(cells)) <= set("-: "):
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


def check_tree(roles: Path) -> list[str]:
    index = roles / "index.md"
    if not index.is_file():
        return [f"{index}: router not found — the gate cannot derive its scope"]
    rows, problems = parse_router(index)
    if not rows:
        return problems or [f"{index}: the router table parsed no row — the gate refuses to run empty"]

    registered = {r["primary"] for r in rows} | {c for r in rows for c in r["checking"]}
    on_disk = {p.stem for p in roles.glob("*.md") if p.name != "index.md"}

    for name in sorted(registered - on_disk):
        problems.append(f"{index}: role `{name}` has no file on disk")
    for name in sorted(on_disk - registered):
        problems.append(f"{roles / (name + '.md')}: role file appears in no router row")

    for p in sorted(roles.glob("*.md")):
        if p.name == "index.md":
            continue
        problems.extend(check_file(p, registered))
    return problems


def main(argv: list[str]) -> int:
    if "--file" in argv:
        target = Path(argv[argv.index("--file") + 1])
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
    sys.exit(main(sys.argv[1:]))
