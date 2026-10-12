"""The text of the scan report. Called by the entry point."""
from __future__ import annotations


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
