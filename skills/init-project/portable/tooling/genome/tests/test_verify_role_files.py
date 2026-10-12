#!/usr/bin/env python3
"""Exercise role routing and checking sections with temporary role trees.

The cases verify missing or unregistered files, unresolved handoffs and the
group-folder layout. They also establish that additional headings and prose
examples remain valid."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import verify_role_files as V  # noqa: E402
from lib.console import use_utf8_output  # noqa: E402
from support import check, fails  # noqa: E402

use_utf8_output()


HEADER = "| work type | primary role | checking roles |\n|---|---|---|\n"




def role(name: str = "developer", drop: int | None = None, extra: int | None = None,
         no_pair: int | None = None, handoff: str = "qa") -> str:
    """A role file that satisfies every rule, minus whatever the caller breaks."""
    out = ["---", "scope: project", "---", "", f"# {name.title()}", ""]
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
        # a bare name goes into the default group; a name containing "/" places the file
        # exactly there, so the layout cases can put it anywhere
        target = d / (f"{name}.md" if "/" in name else f"work/{name}.md")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
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
    check(V.check_file(d / "work" / "developer.md", set()) == [],
          "case 2: --file mode reported a problem on a valid role file")

    # a second table (another work group) contributes its rows too
    second = ("\n### §1.2 second group\n\n" + HEADER
              + row("translating a sentence", "comtor"))
    roles2 = dict(clean, comtor=role("comtor", handoff="qa"))
    d = build(tmp, roles2, clean_rows, second_table=second)
    check(V.check_tree(d) == [],
          "case 3: a role registered only in the second table was not accepted")

    # an empty second table (header only) must not break the parse
    d = build(tmp, clean, clean_rows, second_table="\n### §1.2 second group\n\n" + HEADER)
    check(V.check_tree(d) == [], "case 4: an empty second table broke the parse")

    # --- rule 1: router role must have a file ---------------------------
    d = build(tmp, clean, clean_rows + [row("planning", "project-manager")])
    check(any("has no file in a group folder" in p for p in V.check_tree(d)),
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

    # Section 6 is a routing interface. Other headings and examples may evolve.
    d = build(tmp, dict(clean, developer=role("developer", drop=6)), clean_rows)
    check(any("§6 missing" in p for p in V.check_tree(d)),
          "case 8: missing checking criteria were not caught")
    d = build(tmp, dict(clean, developer=role("developer", extra=8)), clean_rows)
    check(V.check_tree(d) == [], "case 9: an additional section was rejected")
    d = build(tmp, dict(clean, developer=role("developer", no_pair=3)), clean_rows)
    check(V.check_tree(d) == [], "case 10: prose examples were rejected")
    d = build(tmp, dict(clean, developer=role("developer", drop=4)), clean_rows)
    check(V.check_tree(d) == [], "an optional section was incorrectly required")
    d = build(tmp, dict(clean, developer=role("developer").replace("## §", "### §")), clean_rows)
    check(V.check_tree(d) == [], "heading depth was incorrectly treated as role data")

    # --- layout: every role sits in exactly one group folder -------------
    d = build(tmp, {"developer": clean["developer"], "other/qa": clean["qa"]}, clean_rows)
    check(V.check_tree(d) == [], "case 16: roles spread over two groups were rejected")

    d = build(tmp, {"developer": clean["developer"], "./qa": clean["qa"]}, clean_rows)
    check(any("not inside a group folder" in p for p in V.check_tree(d)),
          "case 17: a role file directly under the router folder was not caught")

    # the role template beside the router is not a role: no row, no §6, no group folder
    d = build(tmp, clean, clean_rows)
    (d / "_template.md").write_text("# [Role name]\n\n## §7 Handoffs\n\n`nobody`\n", encoding="utf-8")
    check(V.check_tree(d) == [], "case 21: the role template beside the router was treated as a role")

    # the same name inside a group folder is an ordinary role file and must be registered
    d = build(tmp, dict(clean, **{"work/_template": clean["qa"]}), clean_rows)
    check(any("appears in no router row" in p for p in V.check_tree(d)),
          "case 22: a `_template.md` inside a group folder escaped the router check")

    # a role does not check its own result
    d = build(tmp, clean, clean_rows + [row("fixing a defect", "developer", "qa, developer")])
    check(any("checking role for its own row" in p for p in V.check_tree(d)),
          "case 23: a role named as its own checking role was not caught")

    d = build(tmp, dict(clean, **{"other/developer": clean["developer"]}), clean_rows)
    check(any("is also used by" in p for p in V.check_tree(d)),
          "case 18: one role name in two groups was not caught")

    d = build(tmp, dict(clean, **{"work/deep/security": role("security")}), clean_rows)
    check(any("nested inside a group" in p for p in V.check_tree(d)),
          "case 19: a folder nested inside a group was not caught")

    d = build(tmp, {"developer": clean["developer"], "Bad_Group/qa": clean["qa"]}, clean_rows)
    check(any("must be kebab-case" in p for p in V.check_tree(d)),
          "case 20: a group folder with a non-kebab-case name was not caught")

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
