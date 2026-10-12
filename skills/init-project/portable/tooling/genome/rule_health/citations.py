"""Finding `file.md §N` citations and resolving the file each one names.

Called by `dead.py` and `drift.py`, which judge the same citations in two ways.
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from rule_health.scope import FROZEN

PTR = re.compile(r"`?([A-Za-z0-9_\-./]+\.md)`?\s*`?\s*§\s*([0-9]+(?:\.[0-9]+)*[a-z]?)")
ANCHOR = re.compile(r"(?:^|\n)\s*(?:#{1,6}\s*)?(?:\*\*)?§\s*([0-9]+(?:\.[0-9]+)*[a-z]?)")


def _anchors(text: str) -> set[str]:
    return {m.group(1) for m in ANCHOR.finditer(text)}


def _index_by_name(root: Path) -> dict:
    """Index from file name -> path, EXCLUDING frozen archives.

    `.agent-workspace/worktrees/**` and `.agent-workspace/tasks/**` are snapshots of a closed
    round (`lesson-capture.md` §8: an old name in there is not a dead pointer). Scale: an archive
    can hold thousands of .md files against a few hundred live ones, so folding it in would make
    every common file name "ambiguous".

    """
    out: dict = defaultdict(list)
    for p in root.rglob("*.md"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if any(rel.startswith(f) for f in FROZEN):
            continue
        out[p.name].append(p)
    return out


def _resolve_target(root: Path, src: Path, target: str,
                    by_name: dict) -> tuple[Path | None, bool]:
    """Return (path, used_fallback). Keyed on the PATH first; the file name is only a fallback."""
    cand = (src.parent / target).resolve()
    if cand.exists():
        return cand, False
    cand = (root / target).resolve()
    if cand.exists():
        return cand, False
    # Match on the citation's PATH SUFFIX, not on the file name alone. A citation resolved by
    # `index.md` alone shatters into a dozen candidates and then reports a missing anchor on a file
    # the author never meant - throwing away a relative path is throwing away a decidable answer.
    # trinh bay nhu phep phan giai.
    want = target.replace("\\", "/").lstrip("./")
    hits = [c for c in by_name.get(Path(target).name, [])
            if str(c).replace("\\", "/").endswith(want)]
    if len(hits) > 1:
        # A human resolves it by DIRECTORY CONTEXT: a standard belonging to one axis citing
        # `content-rules.md` means that axis's copy, not another axis's. Measure that context by the
        # length of the shared path prefix, and call it ambiguous only when two candidates TIE.
        def _shared(c):
            a = str(src.parent).replace("\\", "/").split("/")
            b = str(c.parent).replace("\\", "/").split("/")
            n = 0
            for x, y in zip(a, b):
                if x != y:
                    break
                n += 1
            return n
        best = max(_shared(c) for c in hits)
        top = [c for c in hits if _shared(c) == best]
        if len(top) == 1:
            return top[0], True
    if len(hits) == 1:
        return hits[0], True
    if len(hits) > 1:
        return None, True
    return None, False
