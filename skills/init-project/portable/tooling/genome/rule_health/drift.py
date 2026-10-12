"""The drift signal: a cited section that changed after the citing file was last committed.

Reads version history. Called by the entry point.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from lib.git import run_git
from rule_health.citations import PTR, _index_by_name, _resolve_target

HEADING = re.compile(r"^\s*#{1,6}\s*§\s*([0-9]+(?:\.[0-9]+)*[a-z]?)\b")


def section_body(text: str, sid: str) -> str:
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        m = HEADING.match(ln)
        if m and m.group(1) == sid:
            start = i + 1
            break
    if start is None:
        return ""
    body = []
    for ln in lines[start:]:
        if HEADING.match(ln):
            break
        body.append(ln)
    return "\n".join(body)


def same_body(a: str, b: str) -> bool:
    return a.split() == b.split()


def _git_show(root: Path, rev: str, path: Path) -> str:
    rel = str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    r = run_git(["show", f"{rev}:{rel}"], root)
    return r.stdout if r.returncode == 0 else ""


def _last_commit(root: Path, path: Path) -> str:
    rel = str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    return run_git(["log", "-1", "--format=%H", "--", rel], root).stdout.strip()


def signal_drift(files: list[Path], root: Path) -> list[dict]:
    by_name = _index_by_name(root)

    out = []
    for src in files:
        c_s = _last_commit(root, src)
        if not c_s:
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        for lineno, raw in enumerate(text.splitlines(), 1):
            for m in PTR.finditer(raw):
                target, sec = m.group(1), m.group(2)
                tp, _ = _resolve_target(root, src, target, by_name)
                if tp is None or tp == src:
                    continue
                then = section_body(_git_show(root, c_s, tp), sec)
                now = section_body(tp.read_text(encoding="utf-8", errors="replace"), sec)
                if not then or not now:
                    continue
                if same_body(then, now):
                    continue
                out.append({
                    "signal": "drift",
                    "paths": [str(src), str(tp)],
                    "target_sha256": hashlib.sha256(now.encode("utf-8")).hexdigest(),
                    "lines": [lineno],
                    "text": raw.strip(),
                    "detail": f"drift {target} §{sec} changed after commit {c_s[:8]}",
                })
    return out
