"""Report possible duplication, drift, growth, and broken references.

The scan reads the live instruction trees and any additional paths declared by
rules. Findings need interpretation. The scan updates its ledger of scanned
files; it does not rewrite the instructions or enforce a writing style.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FIXED = ["CLAUDE.md"]


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


import unicodedata

STOP = set(
    "the a an of to in for and or is are be it its this that with on by as not no "
    # The second group is Vietnamese: a project may document in a language other than English,
    # and a stopword that never occurs simply never fires.
    "khong la cua va cho mot duoc thi neu".split())
SEPARATOR = re.compile(r"^\s*\|[\s:|-]+\|\s*$")


def normalize(s: str) -> list[str]:
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"`[^`]*`", " ", s)
    s = re.sub(r"[^\w\s]", " ", s)
    return [w for w in s.split() if len(w) > 2 and w not in STOP]


def _is_table_header(raw: str, next_raw: str = "") -> bool:
    """A header row = a pipe row with a SEPARATOR row directly beneath it.

    Deliberately not a keyword list: a real rule row whose first cell reads `file` / `id` /
    `step` would be dropped silently. Structure is exact where a keyword list is a guess.
    """
    if not raw.lstrip().startswith("|"):
        return False
    return bool(SEPARATOR.match(next_raw))


def rule_lines(text: str) -> list[tuple[int, str, set[str]]]:
    """Read paragraphs, list items and table rows as comparable text units.

    A wrapped paragraph is one unit with the same content as its single-line
    form. Headings, metadata, examples and fenced code are not duplicate rules.
    """
    out, pending = [], []
    start = 0
    fenced = example = metadata = False
    lines = text.splitlines()

    def flush():
        nonlocal pending
        if pending:
            unit = " ".join(pending)
            tokens = set(normalize(unit))
            if tokens:
                out.append((start, unit, tokens))
            pending = []

    for i, raw in enumerate(lines, 1):
        value = raw.strip()
        if i == 1 and value == "---":
            metadata = True
            continue
        if metadata:
            if value == "---": metadata = False
            continue
        if value.startswith(("<example>", "<example ")):
            flush(); example = True; continue
        if value.startswith("</example>"):
            example = False; continue
        if example: continue
        if re.match(r"^(?:`{3,}|~{3,})", value):
            flush(); fenced = not fenced; continue
        if fenced: continue
        if not value or value.startswith(("#", "<", "scope:", "core:", "note:")):
            flush(); continue
        following = lines[i] if i < len(lines) else ""
        if SEPARATOR.match(raw) or _is_table_header(raw, following):
            flush(); continue
        if value.startswith("|"):
            flush(); start = i; pending = [value]; flush(); continue
        if re.match(r"^(?:[-*]|\d+[.)])\s+", value):
            flush(); start = i
            pending = [re.sub(r"^(?:[-*]|\d+[.)])\s+", "", value)]
        else:
            if not pending: start = i
            pending.append(value)
    flush()
    return out


from collections import defaultdict
from itertools import combinations

DUP_MIN = 0.75


def _jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if (a or b) else 0.0


_PKG_CACHE: dict = {}


def _is_packaging_copy(a: str, b: str) -> bool:
    """Two files that are VERBATIM copies of each other -> a packaging relation, not drift.

    One rule copied into TWO different files is real duplication. One FILE copied whole is
    packaging, and `doc-organization.md` §4 allows it.
    """
    if Path(a).name != Path(b).name:
        return False
    key = tuple(sorted((a, b)))
    if key not in _PKG_CACHE:
        try:
            _PKG_CACHE[key] = (Path(a).read_bytes() == Path(b).read_bytes())
        except OSError:
            _PKG_CACHE[key] = False
    return _PKG_CACHE[key]


def _skel_key(toks) -> tuple:
    return tuple(sorted(toks))


def _skeleton_lines(units: dict) -> dict:
    """A line present in the MAJORITY of one directory's files = a TEMPLATE, not a repeated rule.

    `doc-organization.md` §7.1 recognises that an area may hold files that are INSTANCES of one
    template (same §ID skeleton, different subject only). Those skeleton lines are not a copied
    rule - they ARE the template. Measured: 21 files in one standards directory produced 2,600
    "verbatim duplicate" pairs purely by sharing the skeleton. The threshold is the MAJORITY of
    that directory, never a fixed constant.
    """
    from collections import defaultdict as _dd
    per_dir = _dd(list)
    for path in units:
        per_dir[str(Path(path).parent)].append(path)
    skel = _dd(set)
    for d, paths in per_dir.items():
        if len(paths) < 3:
            continue
        cnt = _dd(int)
        for path in paths:
            # Keyed on the NORMALIZED form, not the raw one: `signal_dup` pairs lines by Jaccard
            # over tokens, so two skeleton lines differing only in a code span are still a j=1.0
            # pair even where the raw text differs. Keying on raw would mean this suppression
            # never fires - measured: only 12 of 2,600 pairs were caught.
            for k in {_skel_key(toks) for _, _, toks in units[path]}:
                cnt[k] += 1
        half = len(paths) / 2
        skel[d] = {k for k, n in cnt.items() if n > half}
    return skel


def _instance_groups(units: dict) -> dict:
    """Collapse the INSTANCES of one logical file onto a single representative.

    A file and its bundle copy are TWO INSTANCES of one file, not two files. Without collapsing,
    every real duplicate between file A and file B is reported 4 times - a combinatorial artefact
    of packaging, not 4 defects. Criterion: same file name and rule-line sets overlapping >= 80%.
    Drift between two instances is `/init-project check`'s job (`doc-organization.md` §4).
    """
    from collections import defaultdict as _dd
    by_base = _dd(list)
    for path in units:
        by_base[Path(path).name].append(path)
    rep, drifted = {}, 0
    for _, paths in by_base.items():
        if len(paths) == 1:
            rep[paths[0]] = paths[0]
            continue
        canon = sorted(paths, key=lambda x: (len(x), x))[0]
        base_toks = set()
        for _, _, toks in units[canon]:
            base_toks |= toks
        for path in paths:
            other_toks = set()
            for _, _, toks in units[path]:
                other_toks |= toks
            union = base_toks | other_toks
            same = len(base_toks & other_toks) / len(union) if union else 1.0
            if same >= 0.8:
                rep[path] = canon
                if same < 1.0 and path != canon:
                    drifted += 1
            else:
                rep[path] = path
    return {"rep": rep, "drifted": drifted}


def signal_dup(units: dict, stats: dict | None = None) -> list[dict]:
    groups = _instance_groups(units)
    rep = groups["rep"]
    skel = _skeleton_lines(units)
    flat = []
    for path, rows in units.items():
        # Compare only the REPRESENTATIVE of each instance group.
        if rep.get(path, path) != path:
            continue
        for lineno, raw, toks in rows:
            flat.append((path, lineno, raw, toks))

    df = defaultdict(int)
    for _, _, _, toks in flat:
        for t in toks:
            df[t] += 1
    buckets = defaultdict(list)
    for idx, (_, _, _, toks) in enumerate(flat):
            # Tie-break on the TOKEN itself when df is equal: set iteration order is salted by
            # PYTHONHASHSEED, and 34% of lines have several equally rare candidates - without the
            # tie-break the output differs between processes and the fingerprints stop being stable.
        for t in sorted(toks, key=lambda x: (df[x], x))[:3]:
            buckets[t].append(idx)

    seen, out = set(), []
    skipped = 0
    packaged = 0
    skeleton = 0
    for idxs in buckets.values():
        if len(idxs) > 300:
            # A silent cut reads exactly like a cut that never fires.
            skipped += 1
            continue
        for a, b in combinations(sorted(idxs), 2):
            if (a, b) in seen:
                continue
            seen.add((a, b))
            pa, la, ra, ta = flat[a]
            pb, lb, rb, tb = flat[b]
            if pa != pb and _is_packaging_copy(pa, pb):
                # `doc-organization.md` §4: a packaged copy vs its deployed instance is LEGITIMATE
                # duplication, and it already has its own gate (`/init-project check`).
                packaged += 1
                continue
            j = _jaccard(ta, tb)
            if j < DUP_MIN:
                continue
            _d = str(Path(pa).parent)
            if (Path(pa).parent == Path(pb).parent
                    and _skel_key(ta) in skel.get(_d, set())
                    and _skel_key(tb) in skel.get(_d, set())):
                # A skeleton line of that very directory (§7.1), not a repeated rule.
                skeleton += 1
                continue
            kind = "verbatim duplicate" if j >= 0.999 else "divergent copy"
            out.append({
                "signal": "dup",
                "paths": [pa] if pa == pb else [pa, pb],
                "lines": [la, lb],
                "text": ra,
                "detail": f"{kind} j={j:.2f} | {pa}:{la} <-> {pb}:{lb}",
            })
    if stats is not None:
        stats["dup_buckets_skipped"] = skipped
        stats["dup_pairs_compared"] = len(seen)
        stats["dup_packaging_pairs"] = packaged
        stats["dup_instances_collapsed"] = sum(1 for p, r in rep.items() if p != r)
        stats["bundle_drift_pairs"] = groups["drifted"]
        stats["dup_skeleton_pairs"] = skeleton
    return out


import subprocess

LESSONS_DIR = ".agent-workspace/lessons"
GROWTH_MIN_COMMITS = 4
GROWTH_MIN_LINES = 100


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    return s[min(len(s) - 1, int(len(s) * q))]


def is_growth_eligible(path: Path, commits: int, lines: int) -> bool:
    if LESSONS_DIR in str(path).replace("\\", "/"):
        return False
    return commits >= GROWTH_MIN_COMMITS and lines >= GROWTH_MIN_LINES


def _git_numstat(root: Path, path: Path) -> tuple[int, int, int]:
    out = subprocess.run(
        ["git", "log", "--follow", "--numstat", "--format=%H", "--", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(root)).stdout
    added = deleted = commits = 0
    for ln in out.splitlines():
        parts = ln.split("\t")
        if len(parts) == 3 and parts[0].isdigit():
            added += int(parts[0])
            deleted += int(parts[1])
        elif ln.strip() and "\t" not in ln:
            commits += 1
    return added, deleted, commits


def signal_growth(files: list[Path], root: Path) -> tuple[list[dict], dict]:
    rows = []
    deleted_of: dict[str, int] = {}
    added_of: dict[str, int] = {}
    for p in files:
        added, deleted, commits = _git_numstat(root, p)
        if added == 0:
            continue
        lines = len(p.read_text(encoding="utf-8", errors="replace").splitlines())
        if not is_growth_eligible(p, commits, lines):
            continue
        rows.append((deleted / added, str(p), commits, lines))
        deleted_of[str(p)] = deleted
        added_of[str(p)] = added
    ratios = [r for r, _, _, _ in rows]
    stats = {
        "median": quantile(ratios, 0.5),
        "p25": quantile(ratios, 0.25),
        "p75": quantile(ratios, 0.75),
        "cut": quantile(ratios, 0.25),
        "population": len(rows),
        # CONTEXT, not a finding: a near-monotonic file must still be visible to a reader.
        # nguoi doc, du tieu chi tuyet doi `deleted == 0` khong bat chung.
        "lowest": [(round(r, 3), pth) for r, pth, _, _ in sorted(rows)[:5]],
    }
    out = []
    for ratio, path, commits, lines in rows:
        # An ABSOLUTE criterion derived from the law, not a relative ranking:
        # `doc-organization.md` §12 requires the text of a narrowed law to be DELETED. A file that
        # has never deleted a line is a measurable violation, and a CLOSABLE one - one later commit
        # deleting one line ends it. A quantile cut, by contrast, always flags exactly 25% of the
        # population however clean the corpus is.
        if deleted_of[path] == 0:
            out.append({
                "signal": "growth",
                "paths": [path],
                "lines": [],
                "text": f"delete/add={ratio:.2f}",
                "detail": f"{path} has never deleted a line - added={added_of[path]} deleted=0 "
                          f"commits={commits} lines={lines} (phan bo: median={stats['median']:.2f} p25={stats['p25']:.2f})",
            })
    return out, stats


PTR = re.compile(r"`?([A-Za-z0-9_\-./]+\.md)`?\s*`?\s*§\s*([0-9]+(?:\.[0-9]+)*[a-z]?)")
ANCHOR = re.compile(r"(?:^|\n)\s*(?:#{1,6}\s*)?(?:\*\*)?§\s*([0-9]+(?:\.[0-9]+)*[a-z]?)")
FROZEN = (".git/", ".agent-workspace/worktrees/", ".agent-workspace/tasks/")


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
    rel = str(path.relative_to(root)).replace("\\", "/")
    r = subprocess.run(["git", "show", f"{rev}:{rel}"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(root))
    return r.stdout if r.returncode == 0 else ""


def _last_commit(root: Path, path: Path) -> str:
    rel = str(path.relative_to(root)).replace("\\", "/")
    return subprocess.run(["git", "log", "-1", "--format=%H", "--", rel],
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          cwd=str(root)).stdout.strip()


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


import hashlib
import json

LEDGER = ".agent-workspace/rule-health/ledger.json"
VALID_STATUS = {"fixed", "exempt"}


def _fp_path(p: str, root: Path | None = None) -> str:
    """Repo-relative POSIX form of a path.

    Every ledger key goes through here. An absolute key is machine-specific: it
    misses on a clone, on a renamed directory and in a worktree, so the run
    appends a parallel set instead of updating the existing one.
    """
    s = str(p).replace("\\", "/")
    base = str((root or Path(".")).resolve()).replace("\\", "/")
    # `base` is resolved, so an absolute `p` must be resolved too or the prefix misses:
    # on Windows a temp/8.3 short name and its long form denote one directory and spell
    # it differently, and the key would come out absolute (machine-specific).
    if Path(s).is_absolute():
        try:
            s = str(Path(p).resolve()).replace("\\", "/")
        except OSError:
            pass
    if s.startswith(base):
        s = s[len(base):]
    return s.lstrip("/")


def _is_absolute_key(k: str) -> bool:
    return k.startswith("/") or (len(k) > 1 and k[1] == ":")


def fingerprint(finding: dict) -> str:
    key = "|".join([
        finding["signal"],
        ",".join(sorted(_fp_path(p) for p in finding["paths"])),
        " ".join(normalize(finding.get("text", ""))),
    ])
    if finding.get("target_sha256"):
        key += "|" + finding["target_sha256"]
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def load_ledger(root: Path) -> dict:
    p = root / LEDGER
    if not p.exists():
        return {"entries": {}, "git_cache": {}, "last_scanned": {}}
    data = json.loads(p.read_text(encoding="utf-8"))
    data.setdefault("entries", {})
    data.setdefault("git_cache", {})
    data.setdefault("last_scanned", {})
    # drop keys written by an older revision that used the absolute path
    data["last_scanned"] = {k: v for k, v in data["last_scanned"].items()
                            if not _is_absolute_key(k)}
    return data


def save_ledger(root: Path, data: dict) -> None:
    p = root / LEDGER
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True),
                 encoding="utf-8")


def ledger_problems(ledger: dict) -> list[str]:
    out = []
    for fp, e in ledger.get("entries", {}).items():
        st = e.get("status")
        if st not in VALID_STATUS:
            out.append(f"{fp}: invalid status: {st!r}")
        if st == "exempt" and not e.get("allowed_by"):
            out.append(f"{fp}: an exempt entry has no allowed_by (the §ID that permits it)")
        if st == "exempt" and not e.get("reason"):
            out.append(f"{fp}: an exempt entry has no reason")
    return out


def open_findings(findings: list[dict], ledger: dict) -> list[dict]:
    entries = ledger.get("entries", {})
    return [f for f in findings if fingerprint(f) not in entries]


import argparse


def render_report(findings: list[dict], counts: dict, stats: dict) -> str:
    lines = [
        "== rule-health ==",
        f"denominator: {counts['files']} files, {counts['rule_lines']} text units",
        (f"growth: median={stats['median']:.2f} p25={stats['p25']:.2f} "
         f"p75={stats['p75']:.2f} cut={stats['cut']:.2f} population={stats['population']}"),
        (f"dup: {stats.get('dup_pairs_compared', 0)} pairs compared, "
         f"{stats.get('dup_buckets_skipped', 0)} buckets cut (threshold 300), "
         f"{stats.get('dup_packaging_pairs', 0)} packaging (§4 legitimate), "
         f"{stats.get('dup_instances_collapsed', 0)} instances collapsed, "
         f"{stats.get('bundle_drift_pairs', 0)} bundle drift (/init-project check owns these), "
         f"{stats.get('dup_skeleton_pairs', 0)} template skeleton (§7.1 legitimate)"),
        (f"citations resolvable only BY FILE NAME: "
         f"{stats.get('ambiguous_total', 0)} (context, NOT a finding) "
         f"— most frequent: {stats.get('ambiguous_top', [])}"),
        "growth — the least-deleting files (context, NOT a finding):",
        *[f"    {r:.3f}  {pth}" for r, pth in stats.get("lowest", [])],
        f"open findings: {len(findings)}",
    ]
    for f in findings:
        lines.append(f"  [{f['signal']}] {f['detail']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--paths", nargs="*", default=None)
    ap.add_argument("--rotate", type=int, default=3)
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()

    files, errors = resolve_scope(root)
    if errors:
        for e in errors:
            print(f"DECLARATION ERROR: {e}")
        return 2

    try:
        ledger = load_ledger(root)
    except (ValueError, TypeError, AttributeError, OSError) as error:
        print(f"LEDGER ERROR: {error}")
        return 1
    problems = ledger_problems(ledger)
    if problems:
        for p in problems:
            print(f"LEDGER ERROR: {p}")
        return 1

    if args.paths:
        touched = {_fp_path(Path(p).resolve(), root) for p in args.paths}
        stale = sorted(files, key=lambda p: ledger["last_scanned"].get(_fp_path(p, root), ""))
        chosen = [p for p in files if _fp_path(p, root) in touched]
        chosen += [p for p in stale if _fp_path(p, root) not in touched][:args.rotate]
    else:
        chosen = files

    units = {}
    total_lines = 0
    for p in chosen:
        rows = rule_lines(p.read_text(encoding="utf-8", errors="replace"))
        units[str(p)] = rows
        total_lines += len(rows)

    dup_stats: dict = {}
    findings = scope_findings(root)
    findings += signal_dup(units, dup_stats)
    growth, stats = signal_growth(chosen, root)
    findings += growth
    findings += signal_dead(chosen, root, dup_stats)
    findings += signal_drift(chosen, root)

    opened = open_findings(findings, ledger)
    stats.update(dup_stats)
    print(render_report(opened, {"files": len(chosen), "rule_lines": total_lines}, stats))

    stamp = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", cwd=str(root)).stdout.strip()
    for p in chosen:
        ledger["last_scanned"][_fp_path(p, root)] = stamp
    save_ledger(root, ledger)

    return 0


if __name__ == "__main__":
    sys.exit(main())
