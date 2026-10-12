"""Reading a wiki cluster file into its edges.

The first table of a cluster is its edge table. Called by `tier.py`,
`identifiers.py` and `limits.py`, so that every check reads a cluster the same way.
"""
import re
from pathlib import Path

EVIDENCE_ITEM_RE = re.compile(r"^(located|absent|stored-data|running-system):\s*(.*)$", re.S)
KV_RE = re.compile(r"(\w[\w-]*)=(`[^`]*`|\"[^\"]*\"|\S+)")
# GFM requires only ONE dash per separator cell; demanding {2,} would make a perfectly legal
# `|-|-|-|-|-|` table read as no table at all, turning the whole cluster into 0 edges (I2).
SEP_CELL_RE = re.compile(r"^:?-+:?$")
# `<br>` is not the only legal spelling — `<br/>` and `<br />` are equally valid evidence-item
# boundaries (I3).
BR_RE = re.compile(r"<br\s*/?>", re.I)
# The mandatory columns of an edge table, in order.
HEADER_COLS = ["id", "claim", "class", "confidence", "evidence"]
# A block inside a code fence is ILLUSTRATION, never a table of the cluster. This tier will
# carry a page explaining the format with a sample edge table; without skipping fences that
# sample becomes the first table and the REAL edge table below it is never inspected.
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def _split_row(line):
    r"""Split a markdown table line '| a | b | c |' into a list of trimmed cells.

    An escaped pipe belongs to the cell's content. Split only at unescaped
    boundaries, then restore literal pipes inside each cell.
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
