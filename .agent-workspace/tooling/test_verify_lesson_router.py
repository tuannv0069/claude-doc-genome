#!/usr/bin/env python3
"""Exercise lesson-router contracts with temporary stores.

Valid data must pass regardless of record length or prose style. Each broken
fixture tests a specific missing link, metadata value, or router field."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_lesson_router as V  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

fails: list[str] = []

HEADER = "| file | work type | paired guide | checks |\n|---|---|---|---|\n"


def check(cond: bool, msg: str) -> None:
    if not cond:
        fails.append(msg)


def store(scope: str = "doing the thing", phase: str = "writing",
          body: str = "", critical: bool = True) -> str:
    head = ""
    if critical:
        head = f"<critical>\nscope: {scope}\n" + (f"phase: {phase}\n" if phase else "") + "</critical>\n\n"
    return "---\nscope: project\n---\n\n" + head + (body or "### a lesson\n- seen — 1\n")


def build(tmp: Path, stores: dict[str, str], rows: list[str],
          header: str = HEADER) -> Path:
    """Write a fake lessons tree; return its path."""
    d = Path(tempfile.mkdtemp(dir=tmp))
    (d / "index.md").write_text(
        "## §1 router\n\n" + header + "".join(rows), encoding="utf-8"
    )
    for name, text in stores.items():
        (d / f"{name}.md").write_text(text, encoding="utf-8")
    return d


def row(name: str, work: str = "doing the thing", guide: str = "—",
        checks: str = "—") -> str:
    return f"| `{name}.md` | {work} | {guide} | {checks} |\n"


with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)

    # --- no false alarm -------------------------------------------------
    d = build(tmp, {"write-doc": store()}, [row("write-doc")])
    check(V.check(d) == [], "case 1: clean tree reported a problem")

    d = build(tmp, {"write-doc": store(), "review-doc": store(phase="reviewing")},
              [row("write-doc", checks="`review-doc.md`"), row("review-doc")])
    check(V.check(d) == [], "case 2: valid checks pointer reported a problem")

    d = build(tmp, {}, [])
    check(V.check(d) == [], "case 3: seeded-empty tier (header, no row, no store) must pass")

    # --- rule 1: checks target must exist -------------------------------
    d = build(tmp, {"write-doc": store()}, [row("write-doc", checks="`ghost.md`")])
    check(any("ghost.md" in p for p in V.check(d)),
          "case 4: checks pointing at a missing store was not caught")

    # --- rule 2: no cycle -----------------------------------------------
    d = build(tmp, {"a": store(), "b": store()},
              [row("a", checks="`b.md`"), row("b", checks="`a.md`")])
    check(any("cycle" in p for p in V.check(d)), "case 5: cycle was not caught")

    # --- rule 3: one row per store, both directions ---------------------
    d = build(tmp, {"write-doc": store(), "orphan": store()}, [row("write-doc")])
    check(any("no row in the router" in p for p in V.check(d)),
          "case 6: store on disk with no router row was not caught")

    d = build(tmp, {"write-doc": store()}, [row("write-doc"), row("phantom")])
    check(any("no file on disk" in p for p in V.check(d)),
          "case 7: router row with no file was not caught")

    d = build(tmp, {"write-doc": store()}, [row("write-doc"), row("write-doc")])
    check(any("rows, it must have exactly 1" in p for p in V.check(d)),
          "case 8: duplicated row was not caught")

    # --- rule 4: <critical> with scope: and a legal phase: --------------
    d = build(tmp, {"write-doc": store(critical=False)}, [row("write-doc")])
    check(any("no <critical> block" in p for p in V.check(d)),
          "case 9: missing <critical> was not caught")

    late = ("---\nscope: project\n---\n\n### a lesson\n- seen — 1\n\n"
            "<critical>\nscope: x\nphase: writing\n</critical>\n")
    d = build(tmp, {"write-doc": late}, [row("write-doc")])
    check(V.check(d) == [],
          "case 10: a heading before valid metadata was treated as a schema defect")

    no_scope = ("---\nscope: project\n---\n\n<critical>\nphase: writing\n</critical>\n\n"
                "### a lesson\n- seen — 1\n")
    d = build(tmp, {"write-doc": no_scope}, [row("write-doc")])
    check(any("no scope: line" in p for p in V.check(d)),
          "case 11: <critical> without scope: was not caught")

    d = build(tmp, {"write-doc": store(phase="")}, [row("write-doc")])
    check(any("no phase: line" in p for p in V.check(d)),
          "case 12: <critical> without phase: was not caught")

    d = build(tmp, {"write-doc": store(phase="refactoring")}, [row("write-doc")])
    check(any("not in the closed set" in p for p in V.check(d)),
          "case 13: phase outside the closed set was not caught")

    # --- rule 5: wikilink target must exist -----------------------------
    body = "### a lesson\n- see [[nowhere]]\n- seen — 1\n"
    d = build(tmp, {"write-doc": store(body=body)}, [row("write-doc")])
    check(any("points at no store" in p for p in V.check(d)),
          "case 14: dead [[wikilink]] was not caught")

    # --- gate integrity: a broken table is a gate failure, not 0 rows ---
    d = build(tmp, {"write-doc": store()}, [row("write-doc")],
              header="| file | work type | checks |\n|---|---|---|\n")
    check(any("header row" in p for p in V.check(d)),
          "case 15: missing header row was not caught")

    d = build(tmp, {"write-doc": store()},
              ["| `write-doc.md` | doing the thing | — |\n"])
    check(any("needs 4" in p for p in V.check(d)),
          "case 16: row with the wrong cell count was not caught")

    d = build(tmp, {"write-doc": store()}, [])
    check(any("while 1 store file" in p for p in V.check(d)),
          "case 17: empty router with a store on disk was not caught")

    # --- shared-workspace forms: bare file cells and frontmatter metadata ---
    front = ("---\nscope: project\nwork_scope: doing the thing\nphase: writing\n---\n\n"
             "### a lesson\n- seen — 1\n")
    d = build(tmp, {"write-doc": front, "review-doc": store(phase="reviewing")},
              ["| write-doc.md | doing the thing | — | review-doc.md |\n",
               "| review-doc.md | doing the thing | — | — |\n"])
    check(V.check(d) == [],
          "case 19: bare file cells and frontmatter work_scope/phase were rejected")

    front_no_scope = ("---\nscope: project\nphase: writing\n---\n\n### a lesson\n- seen — 1\n")
    d = build(tmp, {"write-doc": front_no_scope}, [row("write-doc")])
    check(any("no scope: line" in p for p in V.check(d)),
          "case 20: frontmatter phase without work_scope was not caught")

    front_bad_phase = ("---\nscope: project\nwork_scope: doing the thing\nphase: refactoring\n---\n\n"
                       "### a lesson\n- seen — 1\n")
    d = build(tmp, {"write-doc": front_bad_phase}, [row("write-doc")])
    check(any("not in the closed set" in p for p in V.check(d)),
          "case 21: frontmatter phase outside the closed set was not caught")

    d = build(tmp, {"write-doc": store()}, ["| write-doc.md | doing the thing | — | ghost.md |\n"])
    check(any("ghost.md" in p for p in V.check(d)),
          "case 22: bare checks pointer at a missing store was not caught")

    # --- missing router -------------------------------------------------
    empty = Path(tempfile.mkdtemp(dir=tmp))
    check(any("router not found" in p for p in V.check(empty)),
          "case 18: missing router was not reported")

print(f"{len(fails)} failure(s)")
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
