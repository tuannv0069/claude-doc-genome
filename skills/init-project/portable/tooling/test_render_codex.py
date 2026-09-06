#!/usr/bin/env python3
"""Test `render_codex.py` against FAKE repositories.

Running the renderer on the real repo only proves it does not cry wolf. The other half — does the
gate catch a real defect — is built by mutation: each case below breaks exactly one thing.

Three invariants are pinned, and they fail in different ways (`verification-gate-design.md` §2):
nothing MISSING (a target absent or stale), nothing EXTRA (a target whose source is gone), and no
reference reaching outside the set. The third is the one that reads perfectly in review and
resolves to nothing on a machine that deployed only one platform, so it gets the most cases.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_codex as R  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

fails: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        fails.append(msg)


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def lines(*rows: str) -> str:
    return "\n".join(rows) + "\n"


ALWAYS_RULE = lines("---", "scope: portable", "---", "",
                    "<critical>", "scope: a guardrail held every turn", "</critical>", "",
                    "- never skip the check")

SCOPED_RULE = lines("---", "paths:", '  - ".claude/rules/**"', '  - "**/CLAUDE.md"',
                    "scope: portable", "---", "",
                    "<critical>", "target: a rule file", "</critical>", "",
                    "- one rule, one location")

CLAUDE_MD = lines("# fake", "", "## stack", "- none", "",
                  "## ALWAYS",
                  "- rules live in `.claude/rules/`, skills in `.claude/skills/`",
                  "- the plugin manifest is `.claude-plugin/plugin.json`",
                  "- format law is `claude-md-standards.md`; agents follow `subagent-standards.md`")


def build(tmp: Path, claude_md: str = CLAUDE_MD, skills: tuple[str, ...] = ("alpha",),
          agents: tuple[str, ...] = ("auditor",), authored: dict[str, str] | None = None) -> Path:
    """A repo that renders clean, minus whatever the caller then breaks."""
    root = Path(tempfile.mkdtemp(dir=tmp))
    write(root / "CLAUDE.md", claude_md)
    write(root / ".claude/rules/always-one.md", ALWAYS_RULE)
    write(root / ".claude/rules/scoped-one.md", SCOPED_RULE)
    # both of these describe a mechanism the other platform does not have
    write(root / ".claude/rules/claude-md-standards.md", SCOPED_RULE)
    write(root / ".claude/rules/subagent-standards.md", SCOPED_RULE)
    for s in skills:
        write(root / f".claude/skills/{s}/SKILL.md",
              lines("---", f"name: {s}", "description: >", f"  does {s} things",
                    "  outside `.claude/**`", "---", "", f"# {s}",
                    "read `.claude/skills/other/SKILL.md` for the rest"))
    for a in agents:
        write(root / f".claude/agents/{a}.md",
              lines("---", f"name: {a}", 'description: audits "things" and \\ more', "---", "",
                    f"# {a}", "inspect `.claude/agents/` and report"))
    for rel, text in (authored or {}).items():
        write(root / rel, text)
    return root


with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)

    # ---- clean: apply then check is silent -------------------------------
    root = build(tmp)
    R.apply_tree(root)
    problems = R.check_tree(root)
    check(problems == [], f"case 1: clean tree reported {problems[:3]}")
    check(R.apply_tree(root) == [], "case 2: a second apply reported changes")

    agents_md = (root / "AGENTS.md").read_text(encoding="utf-8")

    # ---- the always-loaded tier is carried IN the chain, in full ---------
    check("## rule: always-one.md" in agents_md, "case 3: the always-loaded rule was not inlined")
    check("- never skip the check" in agents_md,
          "case 4: the always-loaded rule's body text is missing from the chain")
    check("## rule: scoped-one.md" not in agents_md,
          "case 5: a path-scoped rule was inlined; it should stay a file with a trigger")

    # ---- a path-scoped rule earns a trigger line, globs rewritten -------
    check("→ MUST Read `.codex/rules/scoped-one.md`" in agents_md,
          "case 6: the path-scoped rule got no trigger line")
    check("`.codex/rules/**`" in agents_md and "`**/AGENTS.md`" in agents_md,
          "case 7: the trigger line's globs were not rewritten")

    # ---- nothing reaches across ----------------------------------------
    for rel in ("AGENTS.md", ".codex/rules/always-one.md",
                ".agents/skills/alpha/SKILL.md", ".codex/agents/auditor.toml"):
        body = (root / rel).read_text(encoding="utf-8")
        check(".claude/" not in body, f"case 8: {rel} still names a .claude/ path")
        check("CLAUDE.md" not in body, f"case 9: {rel} still names the other root index")

    # `.claude-plugin/` is a fact about the repository, not a pointer into the other set
    check(".claude-plugin/plugin.json" in agents_md,
          "case 10: `.claude-plugin/` was rewritten or dropped; it is neither platform's genome set")

    # ---- an unmirrored rule's NAME is rewritten, never left dangling ----
    check("agents-md-standards.md" in agents_md and "claude-md-standards.md" not in agents_md,
          "case 11: a reference to the unmirrored format standard was not renamed")
    check("codex-agents-standards.md" in agents_md and "subagent-standards.md" not in agents_md,
          "case 12: a reference to the unmirrored agent standard was not renamed")
    check(not (root / ".codex/rules/claude-md-standards.md").exists()
          and not (root / ".codex/rules/subagent-standards.md").exists(),
          "case 13: a platform-specific standard was mirrored anyway")

    # ---- generated content is complete, never a pointer ------------------
    skill = (root / ".agents/skills/alpha/SKILL.md").read_text(encoding="utf-8")
    check("# alpha" in skill, "case 14: the skill stub carries no body")
    check("description: does alpha things outside `.codex/**`" in skill,
          f"case 15: the folded description was not flattened and rewritten: {skill.splitlines()[2]}")
    toml = (root / ".codex/agents/auditor.toml").read_text(encoding="utf-8")
    check("# auditor" in toml and "developer_instructions" in toml,
          "case 16: the agent definition carries no body")
    check('audits \\"things\\" and \\\\ more' in toml,
          f"case 17: TOML escaping failed: {toml.splitlines()[2]}")

    # ---- the cap is shipped and covers the chain ------------------------
    cfg = (root / ".codex/config.toml").read_text(encoding="utf-8")
    check("project_doc_max_bytes" in cfg, "case 18: no size cap was shipped")
    limit = int(cfg.split("project_doc_max_bytes = ")[1].split("\n")[0])
    check(len(agents_md.encode("utf-8")) < limit, "case 19: the rendered chain exceeds its own cap")

    # ---- nothing MISSING ------------------------------------------------
    (root / ".codex/rules/always-one.md").unlink()
    check(any(p.startswith("missing:") for p in R.check_tree(root)),
          "case 20: a deleted generated rule was not reported missing")
    R.apply_tree(root)
    write(root / "AGENTS.md", "hand written\n")
    check(any(p.startswith("stale:") for p in R.check_tree(root)),
          "case 21: a hand-edited AGENTS.md was not reported stale")
    R.apply_tree(root)

    # ---- nothing EXTRA --------------------------------------------------
    write(root / ".agents/skills/ghost/SKILL.md", lines("---", "name: ghost", "---"))
    check(any(p.startswith("orphan:") and "ghost" in p for p in R.check_tree(root)),
          "case 22: an orphan skill was not reported")
    R.apply_tree(root)
    check(not (root / ".agents/skills/ghost").exists(),
          "case 23: apply did not remove the orphan and its directory")

    root2 = build(tmp, skills=("alpha", "beta"))
    R.apply_tree(root2)
    shutil.rmtree(root2 / ".claude/skills/beta")
    check(any("beta" in p for p in R.check_tree(root2)),
          "case 24: a deleted source skill left its target unreported")
    R.apply_tree(root2)
    check(not (root2 / ".agents/skills/beta").exists(), "case 25: beta's target survived")
    check((root2 / ".agents/skills/alpha/SKILL.md").is_file(),
          "case 26: removing beta also removed alpha")

    # ---- a rule authored for this platform alone is left alone ----------
    own = lines("---", "paths:", '  - ".codex/agents/**"', "scope: portable", "---", "",
                "<critical>", "target: a subagent definition", "</critical>", "",
                "- one agent, one job")
    root3 = build(tmp, authored={".codex/rules/codex-agents-standards.md": own})
    R.apply_tree(root3)
    check((root3 / ".codex/rules/codex-agents-standards.md").read_text(encoding="utf-8") == own,
          "case 27: an authored platform-only rule was overwritten by the renderer")
    check(R.check_tree(root3) == [],
          f"case 28: an authored rule was reported as a problem: {R.check_tree(root3)[:2]}")
    a3 = (root3 / "AGENTS.md").read_text(encoding="utf-8")
    check("→ MUST Read `.codex/rules/codex-agents-standards.md`" in a3,
          "case 29: an authored platform-only rule got no trigger line, so nothing reaches it")

    # ---- the leak check actually fires ----------------------------------
    check(R.leaks("x.md", "see `.claude/rules/a.md`") != [],
          "case 30: a cross-reference was not detected")
    check(R.leaks("x.md", "see `.claude-plugin/plugin.json`") == [],
          "case 31: `.claude-plugin/` was flagged as a cross-reference")
    check(any("dangling" in p for p in R.leaks("x.md", "per `subagent-standards.md`")),
          "case 32: a reference to an unmirrored rule was not flagged as dangling")

    # ---- frontmatter helpers --------------------------------------------
    check(R.paths_globs(SCOPED_RULE) == [".claude/rules/**", "**/CLAUDE.md"],
          f"case 33: paths_globs returned {R.paths_globs(SCOPED_RULE)}")
    check(R._one_line("> folded  value") == "folded value",
          "case 34: a folded YAML scalar marker leaked into the value")

    # ---- no root index is a setup failure, never a silent clean pass ----
    empty = Path(tempfile.mkdtemp(dir=tmp))
    check(R.check_tree(empty) == ["CLAUDE.md not found — nothing to render from"],
          "case 35: a repo with no root index did not report a setup failure")

print(f"{len(fails)} failure(s)")
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
