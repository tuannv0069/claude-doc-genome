"""The dead-reference signal: a citation whose file or section does not exist.

Called by the entry point.
"""
from __future__ import annotations

from pathlib import Path

from rule_health.citations import PTR, _anchors, _index_by_name, _resolve_target


def signal_dead(files: list[Path], root: Path,
                stats: dict | None = None) -> list[dict]:
    by_name = _index_by_name(root)

    out = []
    ambiguous: list[str] = []
    for src in files:
        text = src.read_text(encoding="utf-8", errors="replace")
        in_fence = in_example = False
        for lineno, raw in enumerate(text.splitlines(), 1):
            s = raw.strip()
            if s.startswith("```"):
                in_fence = not in_fence
                continue
            if s.startswith("<example"):
                in_example = True
                continue
            if s.startswith("</example>"):
                in_example = False
                continue
            if in_fence or in_example:
                continue
            for m in PTR.finditer(raw):
                target, sec = m.group(1), m.group(2)
                tp, fallback = _resolve_target(root, src, target, by_name)
                if tp is None and fallback:
                    # NOT a finding: nothing is dead, the citation merely omits the path segment
                    # that would disambiguate it. Counted, and reported as context.
                    ambiguous.append(f"{src}:{lineno} -> {target} §{sec}")
                    continue
                if tp is None:
                    kind = "path_missing"
                    suffix = ""
                elif tp.stat().st_size == 0:
                    kind = "target_empty"
                    suffix = " (fallback-by-name)" if fallback else ""
                elif sec not in _anchors(tp.read_text(encoding="utf-8", errors="replace")):
                    kind = "sid_missing"
                    suffix = " (fallback-by-name)" if fallback else ""
                else:
                    continue
                out.append({
                    "signal": "dead",
                    "paths": [str(src)],
                    "lines": [lineno],
                    "text": s,
                    "detail": f"{kind} {target} §{sec}{suffix}",
                })
    if stats is not None:
        from collections import Counter as _C
        stats["ambiguous_total"] = len(ambiguous)
        stats["ambiguous_top"] = _C(
            a.split("-> ")[1].split(" §")[0] for a in ambiguous).most_common(5)
    return out
