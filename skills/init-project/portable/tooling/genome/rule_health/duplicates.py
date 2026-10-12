"""The duplication signal: text units that say the same thing in two places.

Called by the entry point with the units of `units.py`.
"""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from pathlib import Path

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
