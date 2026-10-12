"""Which files the scan reads.

The corpus is the fixed instruction trees plus every glob a rule declares in its
`paths:` frontmatter. Called by the entry point, and by `citations.py` for the
list of frozen trees.
"""
from __future__ import annotations

import re
from pathlib import Path

FIXED = ["CLAUDE.md"]
# Snapshots of closed work: never part of the live corpus.
FROZEN = (".git/", ".agent-workspace/worktrees/", ".agent-workspace/tasks/")


def _frontmatter_paths(text: str) -> list[str]:
    """Read path globs from the leading metadata block, not prose examples."""
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        return []
    out, inside = [], False
    for line in match.group(1).splitlines():
        if line.strip() == "paths:":
            inside = True
            continue
        if inside:
            item = re.match(r'\s+-\s+(?:"([^\"]+)"|([^\s]+))\s*$', line)
            if item:
                out.append(item.group(1) or item.group(2))
            else:
                inside = False
    return out


def _rule_paths(root: Path) -> tuple[list[str], list[str]]:
    """Union of `paths:` across every file in .claude/rules/. Returns (globs, declaring file names)."""
    globs, sources = [], []
    rules_dir = root / ".claude" / "rules"
    for f in sorted(rules_dir.glob("*.md")) if rules_dir.is_dir() else []:
        got = _frontmatter_paths(f.read_text(encoding="utf-8", errors="replace"))
        if got:
            globs += got
            sources.append(f.name)
    return globs, sources


def _expand(root: Path, glob: str) -> list[Path]:
    # pathlib < 3.13: a bare trailing "**" matches directories only, not the
    # files inside them (files need an explicit final "*" segment). Normalize
    # so "dir/**" recurses into files the same way on every stdlib version.
    pattern = glob + "/*" if glob.endswith("**") else glob
    return [p for p in root.glob(pattern) if p.is_file() and p.suffix == ".md"]


def resolve_scope(root: Path) -> tuple[list[Path], list[str]]:
    errors: list[str] = []
    declared, _sources = _rule_paths(root)
    globs = [".claude/rules/**/*.md", ".claude/skills/**/*.md", ".claude/agents/**/*.md",
             ".agent-workspace/guide/**/*.md", ".agent-workspace/lessons/**/*.md", *declared]

    files: list[Path] = []
    for name in FIXED:
        p = root / name
        if p.exists():
            files.append(p)
    for g in globs:
        files += _expand(root, g)

    # The same FROZEN rule already applied in `_index_by_name`: a frozen archive is not a live
    # corpus (`lesson-capture.md` §8). Drop it in one place and forget it in the other and the
    # scope swallows the whole archive, manufacturing thousands of phantom duplicate pairs.
    files = [f for f in files
             if not any(str(f.relative_to(root)).replace("\\", "/").startswith(x)
                        for x in FROZEN)]
    files = sorted(set(files))
    if not files:
        errors.append("scan scope is EMPTY - that is a declaration failure, not clean")
    return files, errors


def scope_findings(root: Path) -> list[dict]:
    """Report declared paths that currently match no file."""
    out = []
    declared, _ = _rule_paths(root)
    for g in declared:
        if not _expand(root, g):
            out.append({
                "signal": "dead",
                "paths": [g],
                "lines": [],
                "text": g,
                "detail": f"paths_no_match a declared `paths:` glob matches no file: {g}",
            })
    return out
