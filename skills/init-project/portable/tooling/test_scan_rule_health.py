#!/usr/bin/env python3
"""Test `scan_rule_health.py` against FAKE genome trees.

The real repo must produce a report, so running the scan on it only proves it does not crash.
The other half — does it resolve its scope correctly, and does each signal fire where it should
— is built by mutation: each case below breaks exactly one thing.

Both directions are named on purpose (`verification-gate-design.md` §2): the clean cases check
"no false alarm", the mutation cases check "nothing missed".

The scope contract is the part worth pinning hardest. A scan that silently resolves to an empty
or wrong scope reports "0 findings" and reads exactly like a clean corpus.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scan_rule_health as S  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

fails: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        fails.append(msg)


def rule(paths: list[str] | None = None, body: str = "- a rule line\n") -> str:
    if not paths:
        return "---\nscope: portable\n---\n\n" + body
    lines = ["---", "paths:"] + [f'  - "{p}"' for p in paths] + ["scope: portable", "---", "", body]
    return "\n".join(lines)


def build(tmp: Path, rules: dict[str, str], files: dict[str, str] | None = None,
          budget: int | None = 600, with_rws: bool = True, with_claude_md: bool = True) -> Path:
    """A fake genome root. `rules` maps a .claude/rules file name to its text."""
    d = Path(tempfile.mkdtemp(dir=tmp))
    (d / ".claude" / "rules").mkdir(parents=True)
    if with_rws:
        (d / ".claude" / "rules" / "rule-writing-standards.md").write_text(
            rule(["**/CLAUDE.md"]), encoding="utf-8")
    for name, text in rules.items():
        (d / ".claude" / "rules" / name).write_text(text, encoding="utf-8")
    if with_claude_md:
        (d / "CLAUDE.md").write_text("# project\n\n- a rule line\n", encoding="utf-8")
    (d / ".agent-workspace" / "guide").mkdir(parents=True)
    row = f"| always-loaded budget | {budget} lines |\n" if budget is not None else ""
    (d / ".agent-workspace" / "guide" / "index.md").write_text(
        "## §1 placement data\n\n| key | value |\n|---|---|\n" + row, encoding="utf-8")
    for rel, text in (files or {}).items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return d


with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)

    # ---- scope resolution: the contract that matters most --------------
    d = build(tmp, {"a.md": rule([".agent-workspace/guide/general/**"])},
              {".agent-workspace/guide/general/x.md": "- a rule line\n"})
    files, errors = S.resolve_scope(d)
    check(errors == [], f"case 1: a healthy tree reported scope errors: {errors}")
    check(any(p.name == "x.md" for p in files), "case 1b: the declared glob did not reach its file")
    check(any(p.name == "CLAUDE.md" for p in files), "case 1c: the fixed CLAUDE.md entry is missing")

    d = build(tmp, {"a.md": rule([".agent-workspace/guide/general/**"])},
              {".agent-workspace/guide/general/x.md": "- a rule line\n"}, with_rws=False)
    check(any("rule-writing-standards" in e for e in S.resolve_scope(d)[1]),
          "case 2: a missing rule-writing-standards.md was not reported")

    d = build(tmp, {"a.md": rule()}, with_rws=False)
    check(any("paths" in e for e in S.resolve_scope(d)[1]),
          "case 3: no rule declaring `paths:` was not reported")

    # the hard error stays: nothing at all in scope is a declaration failure, never "clean"
    d = build(tmp, {"a.md": rule([".agent-workspace/nowhere/**"])}, with_claude_md=False)
    errors = S.resolve_scope(d)[1]
    check(any("RONG" in e or "empty" in e.lower() for e in errors),
          f"case 4: an entirely empty scope was not reported as an error: {errors}")

    # ---- the fix: one glob matching nothing is a FINDING, not a scope error
    d = build(tmp, {"a.md": rule([".agent-workspace/guide/general/**", ".agent-workspace/wiki/**"])},
              {".agent-workspace/guide/general/x.md": "- a rule line\n"})
    files, errors = S.resolve_scope(d)
    check(errors == [],
          f"case 5: a single zero-match glob still aborted the scan as a scope error: {errors}")
    check(any(p.name == "x.md" for p in files),
          "case 5b: the glob that DID match was dropped along with the one that did not")
    found = S.scope_findings(d)
    check(any("paths_no_match" in f["detail"] and "wiki" in f["detail"] for f in found),
          f"case 6: a zero-match glob produced no finding: {found}")
    check(not any("paths_no_match" in f["detail"] and "guide/general" in f["detail"] for f in found),
          "case 6b: a glob that matched files was still reported as no-match")

    # ---- frozen archives never enter the scope ------------------------
    d = build(tmp, {"a.md": rule(["**"])},
              {".agent-workspace/tasks/some-task/note.md": "- a rule line\n",
               ".agent-workspace/guide/general/x.md": "- a rule line\n"})
    files = S.resolve_scope(d)[0]
    check(not any("tasks" in str(p) for p in files),
          "case 7: a file under .agent-workspace/tasks/ entered the scan scope")

    # ---- naming_prefix fires only on a docs/ glob without the underscore
    d = build(tmp, {"a.md": rule([".agent-workspace/guide/general/**", "docs/spec/**"])},
              {".agent-workspace/guide/general/x.md": "- a rule line\n",
               "docs/spec/s.md": "- a rule line\n"})
    check(any("naming_prefix" in f["detail"] for f in S.scope_findings(d)),
          "case 8: a rule-bearing docs/ folder without the `_` prefix was not reported")

    d = build(tmp, {"a.md": rule([".agent-workspace/guide/general/**", "docs/_spec/**"])},
              {".agent-workspace/guide/general/x.md": "- a rule line\n",
               "docs/_spec/s.md": "- a rule line\n"})
    check(not any("naming_prefix" in f["detail"] for f in S.scope_findings(d)),
          "case 9: a docs/ folder WITH the `_` prefix was wrongly reported")

    # ---- frontmatter parsing and glob expansion ------------------------
    check(S._frontmatter_paths(rule(["a/**", "b/*.md"])) == ["a/**", "b/*.md"],
          "case 10: the `paths:` list was not parsed as written")
    check(S._frontmatter_paths(rule()) == [],
          "case 10b: a rule with no `paths:` yielded paths anyway")

    d = build(tmp, {"a.md": rule(["x/**"])}, {"x/deep/y.md": "- a rule line\n"})
    check([p.name for p in S._expand(d, "x/**")] == ["y.md"],
          "case 11: a trailing `**` glob did not reach the files inside")

    # ---- budget: the only hard gate ------------------------------------
    d = build(tmp, {"a.md": rule()}, budget=None)
    check(any(f["signal"] == "budget" for f in S.signal_budget(d)),
          "case 12: an undeclared always-loaded budget was not reported")

    big = rule(body="- a rule line\n" * 50)
    d = build(tmp, {"a.md": big}, budget=10)
    check(any(f["signal"] == "budget" for f in S.signal_budget(d)),
          "case 13: exceeding the declared budget was not reported")

    d = build(tmp, {"a.md": big}, budget=10_000)
    check(S.signal_budget(d) == [],
          "case 14: a corpus under the declared budget was reported anyway")

    # a path-scoped rule does not spend always-loaded budget
    d = build(tmp, {"a.md": rule(["x/**"], body="- a rule line\n" * 50)}, budget=10)
    check(S.signal_budget(d) == [],
          "case 15: a `paths:`-scoped rule was counted against the always-loaded budget")

    # ---- ledger integrity ----------------------------------------------
    check(S.ledger_problems({"entries": {"aa": {"status": "typo"}}}),
          "case 16: an invalid ledger status was not reported")
    check(S.ledger_problems({"entries": {"aa": {"status": "exempt", "reason": "r"}}}),
          "case 17: an `exempt` entry with no allowed_by was not reported")
    check(S.ledger_problems({"entries": {"aa": {"status": "exempt", "allowed_by": "§4"}}}),
          "case 18: an `exempt` entry with no reason was not reported")
    check(S.ledger_problems({"entries": {"aa": {"status": "fixed"}}}) == [],
          "case 19: a valid `fixed` entry was reported as a problem")

    # ---- ledger keys are repo-relative, never machine-specific ---------
    d = build(tmp, {"a.md": rule()})
    check(not S._is_absolute_key(S._fp_path(str(d / ".claude" / "rules" / "a.md"), d)),
          "case 20: a ledger key came out machine-specific (absolute)")

    # ---- the generated Codex surface is not scanned ---------------------
    # AGENTS.md is rendered from CLAUDE.md, so every shared line is duplication by
    # construction; a `dup` finding there could never be closed (`rule-health.md` §2).
    d = build(tmp, {"a.md": rule()},
              files={"AGENTS.md": "\n".join(["# project", "", "- a rule line", ""]),
                     ".agents/skills/x/SKILL.md": "\n".join(
                         ["---", "name: x", "---", "", "- a rule line", ""])})
    names = S._index_by_name(d)
    check("AGENTS.md" not in names, "case 21: AGENTS.md entered the scan corpus")
    check("SKILL.md" not in names, "case 22: a .agents/ stub entered the scan corpus")

print(f"{len(fails)} failure(s)")
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
