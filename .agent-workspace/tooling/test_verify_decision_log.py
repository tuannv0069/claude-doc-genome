#!/usr/bin/env python3
"""Test `verify_decision_log.py` against FAKE journals.

The real journal must be green, so running the gate on it only proves the gate does not cry
wolf. The other half — does the gate catch a real defect — is built by mutation: each case
below breaks exactly one of the shape rules the gate enforces.

Both directions are named on purpose (`verification-gate-design.md` §2): the clean cases check
"no false alarm", the mutation cases check "nothing missed".
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_decision_log as V  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

fails: list[str] = []

SUBJECT = "docs/thing.md"


def check(cond: bool, msg: str) -> None:
    if not cond:
        fails.append(msg)


def entry(klass: str = "rule", subject: str = SUBJECT, supersedes: str = "",
          body: list[str] | None = None, frontmatter: bool = True,
          close_frontmatter: bool = True, anchor: str = "a1b2c3d") -> str:
    if not frontmatter:
        return "- decided: something\n"
    lines = ["---", f"class: {klass}"]
    if subject:
        lines.append(f"subject: {subject}")
    if anchor:
        lines.append(f"anchor: {anchor}")
    if supersedes:
        lines.append(f"supersedes: {supersedes}")
    if close_frontmatter:
        lines.append("---")
    lines.append("")
    lines += body if body is not None else ["- decided: the law ships with its gate",
                                            "- because: a gate alone makes the regex the law"]
    return "\n".join(lines) + "\n"


def build(tmp: Path, files: dict[str, str], cap: int | None = None,
          with_subject: bool = True) -> tuple[Path, Path]:
    """Return (journal dir, repo root). `files` maps a path relative to the journal."""
    root = Path(tempfile.mkdtemp(dir=tmp))
    if with_subject:
        (root / "docs").mkdir(parents=True, exist_ok=True)
        (root / SUBJECT).write_text("x", encoding="utf-8")
    d = root / ".agent-workspace" / "decisions"
    d.mkdir(parents=True)
    fm = f"---\nscope: project\ncap: {cap}\n---\n" if cap else "---\nscope: project\n---\n"
    (d / "index.md").write_text(fm + "\n# Decision journal\n", encoding="utf-8")
    for rel, text in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return d, root


with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    GOOD = "2026-09/2026-09-02-rule-ship-gate-with-law.md"

    # --- no false alarm -------------------------------------------------
    d, root = build(tmp, {GOOD: entry()})
    problems, warnings = V.check(d, root)
    check(problems == [], f"case 1: clean entry reported {problems}")
    check(warnings == [], f"case 1b: clean entry warned {warnings}")

    d, root = build(tmp, {})
    check(V.check(d, root)[0] == [], "case 2: seeded-empty journal reported a problem")

    d, root = build(tmp, {GOOD: entry(),
                          "archive/2025/2025-04-11-choice-pick-a.md": entry(klass="choice")})
    check(V.check(d, root)[0] == [], "case 3: a well-placed archived entry reported a problem")

    # --- file name and placement ----------------------------------------
    d, root = build(tmp, {"2026-09/notes.md": entry()})
    check(any("file name does not match" in p for p in V.check(d, root)[0]),
          "case 4: malformed file name was not caught")

    d, root = build(tmp, {"2026-08/2026-09-02-rule-x.md": entry()})
    check(any("sits in shard" in p for p in V.check(d, root)[0]),
          "case 5: entry in the wrong shard was not caught")

    d, root = build(tmp, {"2026-09-02-rule-x.md": entry()})
    check(any("outside a shard" in p for p in V.check(d, root)[0]),
          "case 6: entry at the journal root was not caught")

    d, root = build(tmp, {"september/2026-09-02-rule-x.md": entry()})
    check(any("not a `YYYY-MM` shard" in p for p in V.check(d, root)[0]),
          "case 7: a non-shard directory was not caught")

    d, root = build(tmp, {"archive/2024/2026-09-02-rule-x.md": entry()})
    check(any("sits in `archive/2024`" in p for p in V.check(d, root)[0]),
          "case 8: archived entry under the wrong year was not caught")

    # --- frontmatter ------------------------------------------------------
    d, root = build(tmp, {GOOD: entry(frontmatter=False)})
    check(any("no opening `---`" in p for p in V.check(d, root)[0]),
          "case 9: missing frontmatter was not caught")

    d, root = build(tmp, {GOOD: entry(close_frontmatter=False)})
    check(any("never closed" in p for p in V.check(d, root)[0]),
          "case 10: unclosed frontmatter was not caught")

    d, root = build(tmp, {GOOD: entry(anchor="")})
    check(any("no `anchor:`" in p for p in V.check(d, root)[0]),
          "case 11: missing anchor was not caught")

    d, root = build(tmp, {"2026-09/2026-09-02-rule-x.md": entry(klass="choice")})
    check(any("differs from the class" in p for p in V.check(d, root)[0]),
          "case 12: class disagreeing with the file name was not caught")

    d, root = build(tmp, {GOOD: entry(subject="docs/never-existed.md")}, with_subject=False)
    check(any("does not resolve" in p for p in V.check(d, root)[0]),
          "case 13: unresolvable subject was not caught")

    # --- supersedes -------------------------------------------------------
    d, root = build(tmp, {GOOD: entry(supersedes="2026-01-01-rule-ghost")})
    check(any("points at no entry" in p for p in V.check(d, root)[0]),
          "case 14: dangling supersedes was not caught")

    d, root = build(tmp, {GOOD: entry(supersedes="2026-09-02-rule-ship-gate-with-law")})
    check(any("points at itself" in p for p in V.check(d, root)[0]),
          "case 15: self-referential supersedes was not caught")

    # --- body -------------------------------------------------------------
    d, root = build(tmp, {GOOD: entry(body=[])})
    check(any("body is empty" in p for p in V.check(d, root)[0]),
          "case 16: empty body was not caught")

    d, root = build(tmp, {GOOD: entry(body=["- decided: a"] + [f"- line {i}" for i in range(5)])})
    check(any("the ceiling is 4" in p for p in V.check(d, root)[0]),
          "case 17: an over-long body was not caught")

    d, root = build(tmp, {GOOD: entry(body=["- because: it was late", "- decided: a"])})
    check(any("must be `- decided:`" in p for p in V.check(d, root)[0]),
          "case 18: a body not opening with `- decided:` was not caught")

    d, root = build(tmp, {GOOD: entry(body=["- decided: a", "loose prose"])})
    check(any("`- ` bullets only" in p for p in V.check(d, root)[0]),
          "case 19: a non-bullet body line was not caught")

    # --- cap is a WARNING, never a failure --------------------------------
    many = {f"2026-09/2026-09-0{i}-rule-x{i}.md": entry() for i in range(1, 4)}
    d, root = build(tmp, many, cap=2)
    problems, warnings = V.check(d, root)
    check(problems == [], f"case 20: exceeding the cap must not be an error, got {problems}")
    check(any("declared cap of 2" in w for w in warnings),
          "case 21: exceeding the cap raised no warning")

    # --- missing journal --------------------------------------------------
    gone = Path(tempfile.mkdtemp(dir=tmp)) / "decisions"
    check(any("does not exist" in p for p in V.check(gone, tmp)[0]),
          "case 22: a missing journal directory was not reported")

print(f"{len(fails)} failure(s)")
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
