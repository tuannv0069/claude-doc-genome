"""The check of the whole wiki tier: router, clusters, evidence fields and anchors.

Called by the entry point. Needs `rg` (ripgrep) on the path to find anchors.
"""
import re
import subprocess
from collections import defaultdict
from pathlib import Path

from wiki.cluster import _iter_ids, parse_cluster

# `rg` prints "<path>:<line>:<content>". On Windows a path carries a drive letter ("C:\..."),
# so split(":", 2) would cut right after the drive — match the first ":<digits>:" pair instead
# of counting colons.
RG_LINE_RE = re.compile(r"^(.+?):(\d+):(.*)$", re.S)


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
