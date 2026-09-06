#!/usr/bin/env python3
"""Test `render_codex.py` against FAKE repositories.

Running the renderer on the real repo only proves it does not cry wolf. The other half — does
the gate catch a real defect — is built by mutation: each case below breaks exactly one thing
the gate is supposed to see.

Both directions are named on purpose (`verification-gate-design.md` §2): the clean cases check
"no false alarm"; the missing/stale cases check the nothing-MISSING direction; the orphan cases
check the nothing-EXTRA direction, which is the one a deleted source exercises.
"""
from __future__ import annotations

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


def build(tmp: Path, claude_md: str = "# fake\n\n## stack\n- none\n",
          skills: tuple[str, ...] = ("alpha",),
          agents: tuple[str, ...] = ("auditor",)) -> Path:
    """A repo that renders clean, minus whatever the caller then breaks."""
    root = Path(tempfile.mkdtemp(dir=tmp))
    write(root / "CLAUDE.md", claude_md)
    write(root / ".claude/rules/always-one.md",
          "---\nscope: portable\n---\n\n<critical>\nscope: a guardrail\n</critical>\n")
    write(root / ".claude/rules/scoped-one.md",
          '---\npaths:\n  - "**/x.md"\nscope: portable\n---\n\n<critical>\ntarget: x.md\n</critical>\n')
    for s in skills:
        write(root / f".claude/skills/{s}/SKILL.md",
              f"---\nname: {s}\ndescription: does {s} things\n---\n\n# {s}\nbody\n")
    for a in agents:
        write(root / f".claude/agents/{a}.md",
              f"---\nname: {a}\ndescription: audits things\n---\n\n# {a}\nbody\n")
    return root


with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)

    # --- clean: apply then check is silent ---------------------------------
    root = build(tmp)
    R.apply_tree(root)
    check(R.check_tree(root) == [], f"case 1: clean tree reported {R.check_tree(root)}")
    check((root / "AGENTS.md").is_file(), "case 2: AGENTS.md was not written")
    check((root / ".agents/skills/alpha/SKILL.md").is_file(), "case 3: skill stub was not written")
    check((root / ".codex/agents/auditor.toml").is_file(), "case 4: agent stub was not written")

    # --- apply is idempotent ----------------------------------------------
    check(R.apply_tree(root) == [], "case 5: a second apply reported changes")

    # --- the header names the always-loaded tier, not the scoped one -------
    agents_md = (root / "AGENTS.md").read_text(encoding="utf-8")
    always, scoped = R.rule_tiers(root)
    check([p.name for p in always] == ["always-one.md"],
          f"case 6: always-loaded split wrong: {[p.name for p in always]}")
    check([p.name for p in scoped] == ["scoped-one.md"],
          f"case 7: path-scoped split wrong: {[p.name for p in scoped]}")
    check("a guardrail" in agents_md, "case 8: the always-loaded rule's label is missing")
    # a rule path must be repo-relative: an absolute path resolves on the rendering machine
    # only, and the file it points at is unreachable for every other reader of the repo
    check("`.claude/rules/always-one.md`" in agents_md and str(root) not in agents_md,
          "case 8b: a rule path was not written repo-relative")
    check(agents_md.endswith("## stack\n- none\n"),
          "case 9: the CLAUDE.md body was not carried verbatim to the end")

    # --- nothing MISSING: a deleted target -------------------------------
    (root / ".agents/skills/alpha/SKILL.md").unlink()
    check(any(p.startswith("missing:") for p in R.check_tree(root)),
          "case 10: a deleted stub was not reported missing")
    R.apply_tree(root)

    # --- nothing MISSING: a hand-edited target ---------------------------
    write(root / "AGENTS.md", "hand written\n")
    check(any(p.startswith("stale:") for p in R.check_tree(root)),
          "case 11: a hand-edited AGENTS.md was not reported stale")
    R.apply_tree(root)

    # --- nothing EXTRA: a stub whose source is gone ----------------------
    write(root / ".agents/skills/ghost/SKILL.md", "---\nname: ghost\n---\n")
    problems = R.check_tree(root)
    check(any(p.startswith("orphan:") and "ghost" in p for p in problems),
          f"case 12: an orphan stub was not reported: {problems}")
    R.apply_tree(root)
    check(not (root / ".agents/skills/ghost").exists(),
          "case 13: apply did not remove the orphan stub's directory")

    # --- a deleted source removes its stub, and only its stub ------------
    root2 = build(tmp, skills=("alpha", "beta"))
    R.apply_tree(root2)
    import shutil
    shutil.rmtree(root2 / ".claude/skills/beta")
    check(any("beta" in p for p in R.check_tree(root2)),
          "case 14: a deleted source skill left its stub unreported")
    R.apply_tree(root2)
    check(not (root2 / ".agents/skills/beta").exists(), "case 15: beta's stub survived")
    check((root2 / ".agents/skills/alpha/SKILL.md").is_file(),
          "case 16: removing beta also removed alpha")

    # --- the byte cap is counted, not estimated --------------------------
    fat = build(tmp, claude_md="# fake\n\n" + ("x" * (R.DOC_MAX_BYTES + 10)) + "\n")
    check(any(str(R.DOC_MAX_BYTES) in p for p in R.check_tree(fat)),
          "case 17: an AGENTS.md over project_doc_max_bytes was not flagged")

    # --- frontmatter: a folded description becomes one line --------------
    fm = R.parse_frontmatter("---\nname: x\ndescription: line one\n  line two\n---\nbody\n")
    check(fm.get("description") == "line one line two",
          f"case 18: folded description parsed as {fm.get('description')!r}")

    # --- a description with a quote survives TOML rendering --------------
    src = root / ".claude/agents/quoted.md"
    write(src, '---\nname: quoted\ndescription: says "hi" to \\ everyone\n---\n')
    toml = R.render_agent_stub(src, "quoted", src.relative_to(root).as_posix())
    check('\\"hi\\"' in toml and "\\\\ everyone" in toml,
          f"case 19: TOML escaping failed: {toml.splitlines()[2]}")

    # --- no CLAUDE.md is a setup failure, never a silent clean pass -------
    empty = Path(tempfile.mkdtemp(dir=tmp))
    check(R.check_tree(empty) == ["CLAUDE.md not found — nothing to render from"],
          "case 20: a repo with no CLAUDE.md did not report a setup failure")

print(f"{len(fails)} failure(s)")
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
