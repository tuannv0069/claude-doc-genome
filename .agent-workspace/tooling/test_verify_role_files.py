#!/usr/bin/env python3
"""Test `verify_role_files.py` against FAKE role trees.

The real tree must be green once the work is done, so running the gate on it only proves the
gate does not cry wolf. The other half — does the gate catch a real defect — is built by
mutation: each case below breaks exactly one of the rules the gate enforces.

Both directions are named on purpose (`verification-gate-design.md` §2): the clean-tree cases
check "no false alarm", the mutation cases check "nothing missed".
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_role_files as V  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

fails: list[str] = []

HEADER = "| work type | primary role | checking roles |\n|---|---|---|\n"


def check(cond: bool, msg: str) -> None:
    if not cond:
        fails.append(msg)


def role(name: str = "developer", drop: int | None = None, extra: int | None = None,
         no_pair: int | None = None, handoff: str = "qa") -> str:
    """A role file that satisfies every rule, minus whatever the caller breaks."""
    out = ["---", "scope: portable", "---", "", f"# {name.title()}", ""]
    for n in range(1, 8):
        if n == drop:
            continue
        out.append(f"## §{n} section {n}")
        if n in (1, 3, 5) and n != no_pair:
            out.append("- ✅ a concrete example")
            out.append("- ❌ the shape that fails")
        if n == 7:
            out.append(f"- what this role does not decide, handed to `{handoff}`")
        out.append("")
    if extra:
        out.append(f"## §{extra} an extra section")
        out.append("")
    return "\n".join(out)


def build(tmp: Path, roles: dict[str, str], rows: list[str],
          header: str = HEADER, second_table: str = "") -> Path:
    d = Path(tempfile.mkdtemp(dir=tmp))
    (d / "index.md").write_text(
        "## §1 router\n\n" + header + "".join(rows) + second_table, encoding="utf-8")
    for name, text in roles.items():
        (d / f"{name}.md").write_text(text, encoding="utf-8")
    return d


def row(work: str, primary: str, checking: str = "") -> str:
    return f"| {work} | {primary} | {checking} |\n"


with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    clean = {"developer": role("developer", handoff="qa"),
             "qa": role("qa", handoff="developer")}
    clean_rows = [row("writing code", "developer", "qa"),
                  row("reviewing an artifact", "qa", "developer")]

    # --- no false alarm -------------------------------------------------
    d = build(tmp, clean, clean_rows)
    check(V.check_tree(d) == [], "case 1: clean tree reported a problem")

    d = build(tmp, clean, clean_rows)
    check(V.check_file(d / "developer.md", set()) == [],
          "case 2: --file mode reported a problem on a valid role file")

    # a second table (§1a project roles) contributes its rows too
    second = ("\n## §1a project roles\n\n" + HEADER
              + row("translating a sentence", "comtor"))
    roles2 = dict(clean, comtor=role("comtor", handoff="qa"))
    d = build(tmp, roles2, clean_rows, second_table=second)
    check(V.check_tree(d) == [],
          "case 3: a role registered only in the second table was not accepted")

    # an empty second table (header only) must not break the parse
    d = build(tmp, clean, clean_rows, second_table="\n## §1a project roles\n\n" + HEADER)
    check(V.check_tree(d) == [], "case 4: an empty second table broke the parse")

    # --- rule 1: router role must have a file ---------------------------
    d = build(tmp, clean, clean_rows + [row("planning", "project-manager")])
    check(any("has no file on disk" in p for p in V.check_tree(d)),
          "case 5: router role with no file was not caught")

    # --- rule 1 reverse: file must appear in the router ------------------
    d = build(tmp, dict(clean, security=role("security", handoff="qa")), clean_rows)
    check(any("appears in no router row" in p for p in V.check_tree(d)),
          "case 6: role file absent from the router was not caught")

    # --- rule 2: §7 handoff must be a known role -------------------------
    d = build(tmp, {"developer": role("developer", handoff="architect"),
                    "qa": role("qa", handoff="developer")}, clean_rows)
    check(any("hands off to `architect`" in p for p in V.check_tree(d)),
          "case 7: §7 handoff to an unknown role was not caught")

    # --- rule 3: the seven-section frame ---------------------------------
    d = build(tmp, dict(clean, developer=role("developer", drop=4)), clean_rows)
    check(any("§4 missing" in p for p in V.check_tree(d)),
          "case 8: a missing section was not caught")

    d = build(tmp, dict(clean, developer=role("developer", extra=8)), clean_rows)
    check(any("outside the fixed §1-§7 frame" in p for p in V.check_tree(d)),
          "case 9: a section outside the frame was not caught")

    # --- rule 4: ✅/❌ pair in §1, §3, §5 --------------------------------
    d = build(tmp, dict(clean, developer=role("developer", no_pair=3)), clean_rows)
    check(any("§3 has no ✅/❌ pair" in p for p in V.check_tree(d)),
          "case 10: a section missing its ✅/❌ pair was not caught")

    # --- router format is a contract -------------------------------------
    d = build(tmp, clean, ["| writing code | developer |\n"] + clean_rows[1:])
    check(any("needs 3" in p for p in V.check_tree(d)),
          "case 11: row with the wrong cell count was not caught")

    d = build(tmp, clean, [row("writing code", "`developer`", "qa")] + clean_rows[1:])
    check(any("must be exactly one kebab-case role name" in p for p in V.check_tree(d)),
          "case 12: a backticked primary role was not caught")

    d = build(tmp, clean, [row("writing code", "developer", "`qa`")] + clean_rows[1:])
    check(any("not role names" in p for p in V.check_tree(d)),
          "case 13: a backticked checking role was not caught")

    d = build(tmp, clean, clean_rows,
              header="| work type | role | checkers |\n|---|---|---|\n")
    check(any("header row" in p for p in V.check_tree(d)),
          "case 14: a changed header was not caught")

    # --- missing router ---------------------------------------------------
    empty = Path(tempfile.mkdtemp(dir=tmp))
    check(any("router not found" in p for p in V.check_tree(empty)),
          "case 15: missing router was not reported")

print(f"{len(fails)} failure(s)")
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
