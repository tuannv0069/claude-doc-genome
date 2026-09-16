#!/usr/bin/env python3
"""Check the lesson router, declared phases, and references between stores.

The four router columns and the scope/phase metadata are data contracts. Lesson
records may use complete paragraphs; this gate does not constrain their length
or wording. A correctly seeded router with no stores is valid. The gate cannot
judge whether a declared phase accurately describes the work in a store."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LESSONS = Path(".agent-workspace/lessons")
NAME = re.compile(r"`([a-z0-9-]+\.md)`")
WIKILINK = re.compile(r"\[\[([a-z0-9-]+)\]\]")
PHASES = {"writing", "reviewing", "answering", "building-gate",
          "orchestrating", "investigating", "operating"}
CRIT_OPEN = re.compile(r"^<critical>\s*$", re.M)
CRIT_CLOSE = re.compile(r"^</critical>\s*$", re.M)
HEADER_CELLS = ["file", "work type", "paired guide", "checks"]
FILE_CELL = re.compile(r"^`([a-z0-9-]+\.md)`$")


def parse_router(index_path: Path) -> tuple[list[dict], list[str], bool]:
    """Read the §1 table. Returns (rows, problems, header_ok).

    A changed table format becomes a problem and NEVER a silent zero rows:
    a gate that cannot read its input is a failure OF THE GATE
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
        if cells and set("".join(cells)) <= set("-: "):
            continue
        m = FILE_CELL.match(cells[0]) if cells else None
        if not m:
            continue
        if len(cells) != 4:
            problems.append(
                f"{index_path}:{i}: row has {len(cells)} cells, the router table needs 4"
                " — the format changed and the gate cannot read this row correctly"
            )
            continue
        rows.append(
            {"file": m.group(1), "work_type": cells[1], "guide": cells[2],
             "checks": NAME.findall(cells[3])}
        )
    if not header_ok:
        problems.append(
            f"{index_path}: header row `| {' | '.join(HEADER_CELLS)} |` not found"
            " — the table format changed"
        )
    return rows, problems, header_ok


def scope_status(text: str) -> tuple[str, str, str]:
    """State of a store's <critical> block.

    ('missing', '', '')  — no block at all
    ('no_scope', '', '') — the block is in place but has no scope: line
    ('ok', line, phase)  — valid; `line` is the stripped scope: line, `phase` is the
                           stripped text after `phase:`, or '' when that line is absent
    """
    m = CRIT_OPEN.search(text)
    if not m:
        return ("missing", "", "")
    close = CRIT_CLOSE.search(text, m.end())
    block = text[m.end():close.start()] if close else text[m.end():]
    line = ""
    phase = ""
    for raw in block.splitlines():
        stripped = raw.strip()
        if stripped.startswith("scope:"):
            line = stripped
        elif stripped.startswith("phase:"):
            phase = stripped[len("phase:"):].strip()
    if not line:
        return ("no_scope", "", "")
    return ("ok", line, phase)


def check(lessons: Path) -> list[str]:
    index = lessons / "index.md"
    if not index.is_file():
        return [f"{index}: router not found — the gate cannot derive its scope"]

    rows, problems, header_ok = parse_router(index)
    on_disk = {p.name for p in lessons.glob("*.md") if p.name != "index.md"}

    if not rows:
        # Seeded-empty tier: header present, no row, no store on disk. That is the
        # state init deploys, and it is not a defect. Anything else is.
        if header_ok and not on_disk:
            return problems
        if header_ok:
            problems.append(
                f"{index}: §1 lists no store while {len(on_disk)} store file(s) exist on disk"
            )
        return problems or [f"{index}: §1 parsed no row — the gate refuses to run empty"]

    registered = {r["file"] for r in rows}

    # 1. every `checks` target is a store that exists
    for r in rows:
        for c in r["checks"]:
            if c not in on_disk:
                problems.append(
                    f"{index}: row `{r['file']}` has checks `{c}`, which does not exist on disk"
                )

    # 2. the checks relation has no cycle
    graph = {r["file"]: [c for c in r["checks"] if c in registered] for r in rows}
    color: dict[str, int] = {}

    def walk(node: str, trail: list[str]) -> None:
        color[node] = 1
        for nxt in graph.get(node, []):
            if color.get(nxt) == 1:
                problems.append(f"{index}: checks relation has a cycle: {' -> '.join(trail + [nxt])}")
            elif color.get(nxt, 0) == 0:
                walk(nxt, trail + [nxt])
        color[node] = 2

    for node in graph:
        if color.get(node, 0) == 0:
            walk(node, [node])

    # 3. every store has exactly one row, every row has a file
    for name in sorted(on_disk - registered):
        problems.append(f"{lessons/name}: store has no row in the router §1")
    for name in sorted(registered - on_disk):
        problems.append(f"{index}: row `{name}` has no file on disk")
    seen: dict[str, int] = {}
    for r in rows:
        seen[r["file"]] = seen.get(r["file"], 0) + 1
    for name, n in seen.items():
        if n > 1:
            problems.append(f"{index}: `{name}` has {n} rows, it must have exactly 1")

    # 4. <critical> block present, with scope: and exactly one declared phase
    for name in sorted(on_disk):
        text = (lessons / name).read_text(encoding="utf-8")
        status, _line, phase = scope_status(text)
        if status == "missing":
            problems.append(f"{lessons/name}: no <critical> block")
        elif status == "no_scope":
            problems.append(f"{lessons/name}: <critical> block has no scope: line")
        elif not phase:
            problems.append(
                f"{lessons/name}: <critical> block has no phase: line"
                " — a store must DECLARE its phase"
            )
        elif phase not in PHASES:
            problems.append(
                f"{lessons/name}: phase: {phase!r} is not in the closed set: {sorted(PHASES)}"
            )

    # 5. every [[wikilink]] points at a store that exists
    stems = {n[:-3] for n in on_disk}
    for name in sorted(on_disk):
        for target in WIKILINK.findall((lessons / name).read_text(encoding="utf-8")):
            if target not in stems:
                problems.append(f"{lessons/name}: [[{target}]] points at no store")

    return problems


def main() -> int:
    problems = check(LESSONS)
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        return 1
    rows, _, _ = parse_router(LESSONS / "index.md")
    print(f"OK - lesson router: {len(rows)} row(s), all 5 rules hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
