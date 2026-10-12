"""What the wiki gate does not check, stated so that a green result is not over-read.

Called by the entry point, which prints these notices beside the result.
"""
from pathlib import Path

from wiki.cluster import parse_cluster


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
