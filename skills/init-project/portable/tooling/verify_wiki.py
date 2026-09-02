#!/usr/bin/env python3
"""Gate for the wiki tier: it checks LINKS, never truth.

This gate does not know whether a claim is true and does not pretend to. It answers exactly
one question: is everything an edge points at still there — and does every edge carry at least
one readable evidence item, even where that item's content goes unconfirmed (stored-data /
absent / running-system, R8).

root = the directory holding `wiki/` (that is `.agent-workspace/`, the parent of the directory
holding this file).
"""
import re
import secrets
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ALPHABET = "abcdefghijkmnpqrstuvwxyz23456789"     # l/o/0/1 dropped - too easy to misread

EVIDENCE_ITEM_RE = re.compile(r"^(located|absent|stored-data|running-system):\s*(.*)$", re.S)
KV_RE = re.compile(r"(\w[\w-]*)=(`[^`]*`|\"[^\"]*\"|\S+)")
# GFM requires only ONE dash per separator cell; demanding {2,} would make a perfectly legal
# `|-|-|-|-|-|` table read as no table at all, turning the whole cluster into 0 edges (I2).
SEP_CELL_RE = re.compile(r"^:?-+:?$")
# `<br>` is not the only legal spelling — `<br/>` and `<br />` are equally valid evidence-item
# boundaries (I3).
BR_RE = re.compile(r"<br\s*/?>", re.I)
# `rg` prints "<path>:<line>:<content>". On Windows a path carries a drive letter ("C:\..."),
# so split(":", 2) would cut right after the drive — match the first ":<digits>:" pair instead
# of counting colons.
RG_LINE_RE = re.compile(r"^(.+?):(\d+):(.*)$", re.S)
# The mandatory columns of an edge table, in order.
HEADER_COLS = ["id", "claim", "class", "confidence", "evidence"]
# A block inside a code fence is ILLUSTRATION, never a table of the cluster. This tier will
# carry a page explaining the format with a sample edge table; without skipping fences that
# sample becomes the first table and the REAL edge table below it is never inspected.
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


class GitError(Exception):
    """A git command R9 needs returned a real error code (bad ref, bad path, ...)."""


def _split_row(line):
    """Split a markdown table line '| a | b | c |' into a list of trimmed cells.

    A `\|` inside a cell is a LITERAL (escaped) pipe, not a column boundary — split on a
    negative lookbehind, then unescape within each cell.
    """
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", inner)]


def _is_separator_row(cells):
    return bool(cells) and all(SEP_CELL_RE.match(c.strip()) for c in cells)


def _is_edge_header(cells):
    """The header matches the 5 canonical names EXACTLY, in order (a 6th column is ignored)."""
    return [c.strip().lower() for c in cells[:5]] == HEADER_COLS


def _cluster_note(message, kind):
    """A FILE-level note, not an edge — id=None keeps it out of `_iter_ids`."""
    return {
        "id": None,
        "claim": None,
        "class": None,
        "confidence": None,
        "evidence": [],
        "cluster_note": message,
        "note_kind": kind,
    }


def _second_edge_table_notes(blocks):
    """A table AFTER the first whose header matches the edge header EXACTLY is an explicit error.

    A cluster may hold only ONE edge table and it must be the first. Without this rule a second
    edge table with a perfect header is swallowed whole: no evidence check, no path/anchor
    check, no duplicate-id check, and its ids never reach `_all_ids`, so `--new-id` can hand the
    same id out again. The comparison here is EXACT MATCH — the same comparison used for the
    first table, not some looser inferred threshold.
    """
    return [
        _cluster_note(
            f"table {i} of the cluster also carries the edge header — a cluster may hold "
            "only ONE edge table and it must be the first table of the file",
            "second_edge_table",
        )
        for i, b in enumerate(blocks[1:], start=2)
        if _is_edge_header(b[0])
    ]


def _parse_evidence_item(raw):
    """One evidence item: a `located:` / `absent:` / `stored-data:` / `running-system:`
    prefix, then the body.

    `located:` carries `path:line` in the first backtick pair, then an ``anchor=`...` `` pair.
    `absent:` / `stored-data:` / `running-system:` carry `key=value` pairs; a value wrapped in
    backticks or quotes is unwrapped. With no pair at all the whole body is kept as `reason`.
    A body matching no prefix becomes `kind: "malformed"` and is NEVER dropped silently — the
    caller (`check_tier`) is what decides whether that is an error.
    """
    m = EVIDENCE_ITEM_RE.match(raw.strip())
    if not m:
        return {"kind": "malformed", "raw": raw.strip()}
    kind, body = m.group(1), m.group(2).strip()
    ev = {"kind": kind}
    if kind == "located":
        backticks = re.findall(r"`([^`]*)`", body)
        if backticks:
            pathline = backticks[0]
            path, sep, line = pathline.rpartition(":")
            if sep:
                ev["path"], ev["line"] = path, line
            else:
                ev["path"] = pathline
        m2 = re.search(r"anchor=`([^`]*)`", body)
        if m2:
            ev["anchor"] = m2.group(1)
        return ev
    kvs = list(KV_RE.finditer(body))
    if kvs:
        for km in kvs:
            key, val = km.group(1), km.group(2)
            if val[:1] in ("`", '"') and val[-1:] == val[:1] and len(val) >= 2:
                val = val[1:-1]
            ev[key] = val
    else:
        ev["reason"] = body
    return ev


def _iter_table_blocks(text):
    """Group consecutive '|...' lines into independent table blocks.

    Every line between a pair of fences (``` or ~~~) is skipped: that is illustration, not a
    table of the cluster. An unclosed fence swallows the rest of the file — the file then has
    no table at all, and "cluster has no edge table" is reported rather than passing silently.
    """
    block = []
    fence = None
    for raw_line in text.splitlines() + [""]:
        m = FENCE_RE.match(raw_line)
        if m:
            marker = m.group(1)[0]
            if fence is None:
                if block:
                    yield block
                block = []
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is not None:
            continue
        s = raw_line.strip()
        if s.startswith("|"):
            block.append(_split_row(s))
            continue
        if block:
            yield block
        block = []


def _parse_cluster_text(text):
    """The core of `parse_cluster` — it takes TEXT directly and reads no file.

    Split out from `parse_cluster` so R9 (`_ids_at`) can read a cluster's content at a different
    git ref (`git show <ref>:<path>`) through exactly the path `check_tier` uses, rather than
    through a parallel regex that might read `id` differently (both sides of a comparison must
    be in the same unit, `verification-gate-design.md` §1).

    The edge table is the FIRST table of the file — a convention of the format, not an inference
    (`parse_cluster` carries the full statement of the convention). That leaves no grey area:
    the first table's header must match exactly, and no table after it is inspected.

    Three situations produce a pseudo-edge carrying a `cluster_note` (id=None) instead of being
    skipped silently — `check_tier` decides whether they become errors: a first table whose
    header does not match, a file with no table at all, and a table AFTER the first that also
    carries the edge header (`_second_edge_table_notes`).

    A file whose first table has a mismatched header yields NO id. The first cell of a label row
    is not an id, and a fabricated id like that makes `check_merge` cry wolf about an "edge
    disappeared in the merge" the moment the author fixes the column order. That file is already
    red on its header; its ids are UNKNOWN, and the gate declares that rather than guessing.
    Duplicate-id checking for that file waits until the header is fixed.
    """
    blocks = [
        b for b in _iter_table_blocks(text)
        if len(b) >= 2 and _is_separator_row(b[1])
    ]
    if not blocks:
        return [_cluster_note("cluster has no edge table", "empty_cluster")]

    extra = _second_edge_table_notes(blocks)
    block = blocks[0]
    rows = block[2:]
    if not _is_edge_header(block[0]):
        header_read = " | ".join(c.strip() for c in block[0])
        return [
            _cluster_note(
                f"the first table of the cluster does not carry the edge header (read as: {header_read!r})"
                " — the first table of the file must be the edge table; move auxiliary tables below it",
                "header_mismatch",
            )
        ] + extra

    edges = list(extra)
    for cells in rows:
        if len(cells) < 5:
            # A missing mandatory cell is an error the GATE reports, not a row it skips: the
            # edge is still created (with its "id" if present) so that id still reaches
            # seen_ids/_all_ids — otherwise `new_id` could hand out the very id a broken row
            # is holding.
            padded = cells + [""] * (5 - len(cells))
            id_, claim, cls, confidence, evidence_cell = padded[0:5]
            edges.append(
                {
                    "id": id_,
                    "claim": claim,
                    "class": cls,
                    "confidence": confidence,
                    "evidence": [],
                    "row_error": f"row has only {len(cells)}/5 columns",
                }
            )
            continue
        id_, claim, cls, confidence, evidence_cell = cells[0:5]
        items = [
            _parse_evidence_item(x) for x in BR_RE.split(evidence_cell) if x.strip()
        ]
        edges.append(
            {
                "id": id_,
                "claim": claim,
                "class": cls,
                "confidence": confidence,
                "evidence": items,
            }
        )
    return edges


def parse_cluster(path):
    """Read a cluster file from disk: the FIRST table is the edge table; return its edges.

    Convention of the cluster format: the first markdown table of the file IS the edge table,
    and its header must be exactly `id | claim | class | confidence | evidence`. Every table
    after it is auxiliary and is never inspected by the gate; a cluster wanting an auxiliary
    table first must reorder, and the gate says so the moment the author does.

    Two consequences of the convention, themselves laws of the format: a cluster may hold only
    ONE edge table, so a table after the first carrying the exact edge header is an explicit
    error (`_second_edge_table_notes`) rather than an auxiliary table; and a table inside a code
    fence is illustration and never counts as a table of the cluster (`_iter_table_blocks`).

    Declared, not inferred, because no signal separates `table | column | type | null |
    description` from `iD_ | clam | clss | confidance | evidance`, and none separates a table
    ABOUT evidence from a table CARRYING evidence.

    The evidence column splits on `<br>` / `<br/>` / `<br />`, each part being one evidence item
    (`_parse_evidence_item`). Returns `list[dict]`, each dict holding
    "id"/"claim"/"class"/"confidence"/"evidence".
    """
    text = Path(path).read_text(encoding="utf-8")
    return _parse_cluster_text(text)


def _rg_batch(anchors, root, encodings=()):
    """One pass for the WHOLE BATCH of anchors, plus one pass per encoding the project declares.
    A pass costs ~18s regardless of how many patterns it carries, so looping once per anchor is
    wrong by an order of magnitude.

    `encodings` = `source_encodings:` in the router frontmatter (`wiki-tier.md` §7). The
    encodings of the source material are a PROJECT value: hardcoding them into the gate would
    end its portability (`doc-organization.md` §9). Undeclared → exactly one default pass.

    `-uu`: `rg` respects `.gitignore` by default — a file that is ignored but still on disk (a
    build artifact, say) is visible to `Path.exists()` and invisible to `rg`, and the gate then
    cries wolf about an "anchor no longer found" on an anchor that never moved (C5).
    """
    hits = defaultdict(set)          # anchor -> {(path, line)}
    if not anchors:
        return hits
    pat_args = []
    for a in anchors:
        pat_args += ["-e", re.escape(a)]
    for enc in [["-E", e] for e in encodings] + [[]]:
        proc = subprocess.run(
            ["rg", "-n", "--no-heading", "-uu", *enc, *pat_args, str(root)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        for line in proc.stdout.splitlines():
            m = RG_LINE_RE.match(line)
            if not m:
                continue
            path, lineno, body = m.group(1), m.group(2), m.group(3)
            for a in anchors:
                if a in body:
                    # de-duplicate by (path, line): the plain pass returns the same position
                    # as the mojibake string, and sort -u cannot collapse those
                    hits[a].add((path.replace("\\", "/"), int(lineno)))
    return hits


def check_tier(root):
    """root = the directory holding `wiki/`. Returns a list of error messages; empty = green."""
    root = Path(root)
    wiki = root / "wiki"
    errors = []
    if not wiki.exists():
        return []  # no wiki tier yet - green, no cluster

    router = wiki / "index.md"
    on_disk = {
        p.relative_to(wiki).as_posix()
        for p in wiki.rglob("*.md")
        if p.name != "index.md"
    }
    if not router.exists():
        if on_disk:
            return [f"wiki/index.md router missing although {len(on_disk)} cluster(s) exist"]
        return []  # tier not bootstrapped: no router, no cluster - green

    rtext = router.read_text(encoding="utf-8")
    m = re.search(r"^source_root:\s*(\S+)", rtext, re.M)
    if not m:
        return ["the router does not declare source_root"]
    src_root = (wiki / m.group(1)).resolve()
    me = re.search(r"^source_encodings:\s*(.+)$", rtext, re.M)
    src_encodings = [t.strip() for t in re.split(r"[,\s]+", me.group(1).strip(" []"))
                     if t.strip()] if me else []

    listed = set(re.findall(r"\]\((\S+?\.md)\)", rtext))
    for orphan in sorted(on_disk - listed):
        errors.append(f"orphan cluster, no router row: {orphan}")
    for dead in sorted(listed - on_disk):
        errors.append(f"router row points at a file that does not exist: {dead}")

    edges, seen_ids = [], {}
    for f in sorted(wiki.rglob("*.md")):
        if f.name == "index.md":
            continue
        rel = f.relative_to(wiki).as_posix()
        file_edges = parse_cluster(f)
        for e in file_edges:
            e["_source"] = rel
        # ONE reading path for all three id checks - tier-wide duplicates here, `new_id` (R5)
        # and `check_merge` (R9) through `_all_ids`/`_ids_at`. Both sides of one comparison must
        # be in the same unit (`verification-gate-design.md` §1): an id sitting in a first table
        # with a mismatched header is still an id already taken, so all three see it.
        for id_ in _iter_ids(file_edges):
            if id_ in seen_ids:
                errors.append(f"tier-wide duplicate id: {id_} ({rel}, {seen_ids[id_]})")
            seen_ids[id_] = rel
        edges.extend(file_edges)

    # anchor -> path -> edge_id -> {recorded lines}. Keyed by BOTH path (R7: compare within the
    # file, not across the tree - the same text in ANOTHER file is a fact about the codebase, not
    # a defect of this edge) AND by edge_id (never merged tier-wide): two edges citing the same
    # anchor+path must not mask each other - an edge that recorded one position short must go red
    # ON ITS OWN, even where another edge recorded that anchor fully in the same file (`want`
    # belongs to EACH edge; `got` - the real positions rg found - belongs to the file and is
    # shared by every edge citing that anchor+path).
    wanted = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    for e in edges:
        if e.get("cluster_note"):
            # A file-level note becomes an error only for a file THE ROUTER DECLARES as a
            # cluster. A file the router never mentions is already red as an "orphan cluster";
            # catching it a second time for its content would be two errors for one cause, and
            # inconsistent with an orphan file holding only auxiliary tables - that one takes
            # exactly one error.
            if e["_source"] in listed:
                errors.append(f"{e['cluster_note']} ({e['_source']})")
            continue
        if e.get("row_error"):
            errors.append(f"row is missing columns ({e['row_error']}): id={e['id'] or '<empty>'}")

        valid_evidence = [
            ev for ev in e["evidence"]
            if ev.get("kind") in ("located", "absent", "stored-data", "running-system")
        ]
        if not valid_evidence:
            errors.append(f"edge carries no valid evidence item: {e['id']}")

        for ev in e["evidence"]:
            kind = ev.get("kind")
            if kind == "malformed":
                errors.append(
                    "evidence item is unreadable / malformed (no located/absent/stored-data/"
                    f"running-system): {e['id']}"
                )
                continue
            if kind == "stored-data":
                if ev.get("anchor"):
                    errors.append(f"stored-data carries an anchor (forbidden): {e['id']}")
                miss_sd = [k for k in ("dataset", "object", "field", "query") if not ev.get(k)]
                if miss_sd:
                    errors.append(f"stored-data is missing field {miss_sd}: {e['id']}")
                continue
            if kind == "running-system":
                # An observation on the running system. The gate NEVER opens the running
                # system - it checks at schema level like stored-data/absent, and declares that
                # in `schema_only_classes` (R8). `anchor` is forbidden for the same reason as
                # stored-data: an anchor is a drift probe on a SOURCE FILE, and an observation
                # has no file position to drift.
                if ev.get("anchor"):
                    errors.append(f"running-system carries an anchor (forbidden): {e['id']}")
                miss_rs = [k for k in ("account", "screen", "observed") if not ev.get(k)]
                if miss_rs:
                    errors.append(f"running-system is missing field {miss_rs}: {e['id']}")
                continue
            if kind == "absent":
                miss_ab = [k for k in ("query", "scope", "expected") if not ev.get(k)]
                if miss_ab:
                    errors.append(f"absent is missing field {miss_ab}: {e['id']}")
                continue
            if kind != "located":
                continue
            miss = [k for k in ("path", "line", "anchor") if not ev.get(k)]
            if miss:
                errors.append(f"located is missing key {miss}: {e['id']}")
                continue
            p = (src_root / ev["path"])
            if not p.exists():
                errors.append(f"dead path: {ev['path']} ({e['id']})")
                continue
            try:
                lineno = int(ev["line"])
            except ValueError:
                errors.append(f"located line is not a number: {ev['line']!r} ({e['id']})")
                continue
            resolved = p.resolve().as_posix()
            wanted[ev["anchor"]][resolved][e["id"]].add(lineno)

    found = _rg_batch(list(wanted), src_root, src_encodings)
    for anchor, per_path in wanted.items():
        # One `rg` pass for the WHOLE BATCH of anchors (_rg_batch unchanged, 2-pass untouched)
        # - the positions found span the whole tree; filter down to EACH item own `path`
        # before comparing sets, so a position in another file never becomes a "surplus" (R7).
        all_got = {(str(Path(p).resolve().as_posix()), n) for p, n in found.get(anchor, set())}
        for path, per_edge in per_path.items():
            got = {(p, n) for (p, n) in all_got if p == path}
            # Compare EACH edge separately against the file `got` - never merge several
            # edges `want` before comparing, so edge A recording fully cannot mask edge B
            # recording short on the same anchor.
            for edge_id, want_lines in per_edge.items():
                want = {(path, n) for n in want_lines}
                if not got:
                    errors.append(f"anchor no longer found: {anchor!r} (edge {edge_id})")
                    continue
                for extra in sorted(got - want):
                    errors.append(f"anchor matches extra positions never recorded {extra}: {anchor!r} (edge {edge_id})")
                for gone in sorted(want - got):
                    errors.append(f"anchor drifted, no longer at {gone}: {anchor!r} (edge {edge_id})")
    return errors


def _iter_ids(edges):
    """The module ONLY id-reading path - `check_tier`, `_all_ids` and `_ids_at` all come
    through here, so the three id checks cannot read in different units.

    Only a row of a readable edge table has an id. A file-level note pseudo-edge carries
    id=None, and a file whose first table has a mismatched header yields no row at all - the ids
    of a broken file are unknown, not the first cell of its first row.
    """
    for e in edges:
        if e.get("id"):
            yield e["id"]


def _all_ids(root):
    ids = set()
    for f in Path(root, "wiki").rglob("*.md"):
        if f.name == "index.md":
            continue
        ids.update(_iter_ids(parse_cluster(f)))
    return ids


def new_id(cluster, root):
    """R5: machine-allocated, never derived from content, unique tier-wide.

    People do not invent 5 random characters: a string a human or an LLM makes up skews the
    distribution and collides far sooner than real randomness.
    """
    taken = _all_ids(root)
    while True:
        cand = f"{cluster}-" + "".join(secrets.choice(ALPHABET) for _ in range(5))
        if cand not in taken:
            return cand


def _run_git(args, cwd, what):
    """`args` does NOT include "git" - this function adds it, along with
    `-c core.quotePath=false` (C-quoting of non-ASCII file names is on by default;
    `ls-tree`/`show` must both turn it off, or a name `ls-tree` wrapped in quotes goes straight
    into `show` and the path no longer matches).

    `returncode != 0` is an error, with no exception: `ls-tree`/`show`/`rev-parse` (unlike `git
    grep`, which was dropped from this module) have no "1 means no match but still valid" - a
    pathspec matching nothing in `ls-tree` still returns 0 with empty stdout (measured
    directly). Tolerating code 1 would only turn a real git failure into a silent `[]`, exactly
    the shape of the C3 defect just closed.
    """
    out = subprocess.run(
        ["git", "-c", "core.quotePath=false", *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(cwd),
    )
    if out.returncode != 0:
        raise GitError(f"{what} failed ({out.returncode}): {out.stderr.strip()}")
    return out.stdout


def _repo_context(root):
    """(repo_root, prefix) of `root` within the git tree containing it.

    The relpath is NOT computed with `os.path.relpath` - on Windows, `root` (a `Path` the caller
    built, possibly in 8.3 short-name form) and `git rev-parse --show-toplevel` (always
    normalized) can name the SAME directory while spelling it differently, which makes relpath
    produce a path that "escapes" the repo when it does nothing of the sort. `git rev-parse
    --show-prefix` asks git itself, run with `cwd=root`, so it is right regardless of short or
    long names, symlinks or worktrees.
    """
    top = _run_git(["rev-parse", "--show-toplevel"], root, "git rev-parse --show-toplevel").strip()
    prefix = _run_git(["rev-parse", "--show-prefix"], root, "git rev-parse --show-prefix").strip()
    return Path(top), prefix


def _ids_at(ref, root):
    """Read the tier id set at a git ref - through EXACTLY the path `check_tier` uses
    (`parse_cluster`/`_parse_cluster_text`), never a parallel hand-rolled regex (C4): the old
    `_ids_at` demanded padding whitespace around each cell (`| id |`), so a row written
    `|id|claim|...|` - valid to `parse_cluster` - slipped past it.

    `-z` plus splitting on NUL: a non-ASCII file name (the project domain here is Japanese) run
    through a plain `--name-only` (no `-z`) is C-quoted into an octal string in double quotes;
    feeding that straight into `git show <ref>:<quoted string>` makes the path stop matching -
    `show` then reports a path that does not exist on a perfectly healthy merge.
    """
    root = Path(root)
    repo_root, prefix = _repo_context(root)
    pathspec = f"{prefix}wiki" if prefix else "wiki"
    listing = _run_git(
        ["ls-tree", "-r", "-z", "--name-only", ref, "--", pathspec],
        repo_root, f"git ls-tree {ref}",
    )
    ids = set()
    for relpath in listing.split("\0"):
        relpath = relpath.strip()
        if not relpath or Path(relpath).name == "index.md":
            continue
        text = _run_git(["show", f"{ref}:{relpath}"], repo_root, f"git show {ref}:{relpath}")
        ids.update(_iter_ids(_parse_cluster_text(text)))
    return ids


def check_merge(root, parents):
    """R9: an id present in ANY parent branch must be present in the merge result.

    This is the "missing" direction. All six checks in check_tier belong to the "surplus"
    direction, so an edge lost in a merge leaves the gate perfectly green. A ref or path that
    cannot be read is a FAILURE OF THIS CHECK, not "the tier is empty at that ref" - say so,
    never degrade it into green.
    """
    here = _all_ids(root)
    errors = []
    for ref in parents:
        try:
            ids_at_ref = _ids_at(ref, root)
        except GitError as exc:
            errors.append(f"check_merge could not read ref {ref!r}: {exc}")
            continue
        for missing in sorted(ids_at_ref - here):
            errors.append(f"edge disappeared in the merge: {missing} (present at {ref})")
    return errors


def schema_only_classes(root):
    """R8, widened to the `absent` and `running-system` classes: return the messages that
    declare which evidence classes are checked at SCHEMA level only (all fields present) with
    their content never re-confirmed.

    A separate function - this declaration must not be reachable only from `main()`; a caller
    using this module as a library (never touching the CLI) needs to see exactly the same
    declaration.
    """
    root = Path(root)
    wiki = root / "wiki"
    counts = {"stored-data": 0, "absent": 0, "running-system": 0}
    if wiki.exists():
        for p in wiki.rglob("*.md"):
            if p.name == "index.md":
                continue
            for e in parse_cluster(p):
                for ev in e["evidence"]:
                    k = ev.get("kind")
                    if k in counts:
                        counts[k] += 1
    notices = []
    if counts["stored-data"]:
        notices.append(
            f"stored-data: {counts['stored-data']} item(s) — schema only "
            "(dataset/object/field/query all present), content NOT checked"
        )
    if counts["absent"]:
        notices.append(
            f"absent: {counts['absent']} item(s) - schema only (query/scope/expected all "
            "present), the query is NOT re-run to confirm the absence"
        )
    if counts["running-system"]:
        notices.append(
            f"running-system: {counts['running-system']} item(s) — schema only "
            "(account/screen/observed all present), the running system is NOT re-opened to observe again"
        )
    return notices


def unverified_class_checks(root):
    """R8 on the `class` axis: the gate checks NOTHING on this axis and must SAY SO.

    Two distinct limits, never merged into one: (a) the `class` cell value is not matched
    against the class vocabulary the project declares - a made-up class name still passes; (b)
    the set of evidence forms an edge carries is not matched against the sources its class
    requires - an edge missing a REQUIRED source can still read `sourced` with the gate green.

    The class vocabulary is a human law; staying silent about it turns the gate into the
    "passing on a proxy" that R8 itself forbids. A separate function for the same reason as
    `schema_only_classes`: a caller using the module as a library must still see the
    declaration.
    """
    root = Path(root)
    wiki = root / "wiki"
    n = 0
    if wiki.exists():
        for p in wiki.rglob("*.md"):
            if p.name == "index.md":
                continue
            n += sum(1 for e in parse_cluster(p) if e.get("id"))
    if not n:
        return []
    return [
        f"class: {n} edge(s) — the `class` cell is NOT matched against the class vocabulary the "
        "project declares; a class name that exists nowhere still passes",
        f"class: {n} edge(s) — the evidence forms an edge carries are NOT matched against the "
        "sources its class requires; an edge missing a required source still passes",
    ]


def undetected_locator_liveness_checks(root):
    """R8 at the locator (§8, row 3): the gate does NOT know which files under `source_root`
    are dead/superseded and which are live, and it must SAY SO - for the same reason
    `unverified_class_checks` is not merged into the `class` declaration: two different axes,
    two different declarations.

    Anchor scoping (R7) confirms the right position inside the very file `path` names; it does
    NOT confirm that file is the one actually in force - a `located` item anchored,
    syntactically perfectly, into a dead copy sitting beside the live one passes exactly like
    the live one. The real backstop is R3 at the deliverable boundary, not this gate (F8,
    accepting the loss of the old mechanism incidental catch).
    """
    root = Path(root)
    wiki = root / "wiki"
    n = 0
    if wiki.exists():
        for p in wiki.rglob("*.md"):
            if p.name == "index.md":
                continue
            for e in parse_cluster(p):
                if not e.get("id"):
                    continue
                if any(ev.get("kind") == "located" for ev in e.get("evidence", [])):
                    n += 1
    if not n:
        return []
    return [
        f"locator: {n} edge(s) carry `located` evidence — the gate does NOT know which files under "
        "`source_root` are dead/superseded and which are live; an edge anchored into a dead copy "
        "beside the live one passes exactly like the live one (the backstop is R3 at the "
        "deliverable boundary, not this gate)",
    ]


def main(argv):
    root = Path(__file__).resolve().parent.parent  # .agent-workspace/

    if len(argv) >= 2 and argv[1] == "--new-id":
        if len(argv) < 3:
            print("usage: verify_wiki.py --new-id <cluster>", file=sys.stderr)
            return 2
        print(new_id(argv[2], root))
        return 0

    if len(argv) >= 2 and argv[1] == "--merge-check":
        if len(argv) < 4:
            print("usage: verify_wiki.py --merge-check <ref> <ref> [...]", file=sys.stderr)
            return 2
        errors = check_merge(root, argv[2:])
        for e in errors:
            print("FAIL:", e)
        print(f"{len(errors)} fail")
        return 1 if errors else 0

    wiki = root / "wiki"
    cluster_files = (
        [p for p in wiki.rglob("*.md") if p.name != "index.md"] if wiki.exists() else []
    )

    errors = check_tier(root)
    print(f"clusters: {len(cluster_files)}")
    for notice in schema_only_classes(root):
        print(notice)
    for notice in unverified_class_checks(root):
        print(notice)
    for notice in undetected_locator_liveness_checks(root):
        print(notice)
    for e in errors:
        print("FAIL:", e)
    print(f"{len(errors)} fail")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
