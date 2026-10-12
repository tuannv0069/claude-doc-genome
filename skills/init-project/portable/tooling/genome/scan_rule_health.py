#!/usr/bin/env python3
"""Report possible duplication, drift, growth, and broken references.

The scan reads the live instruction trees and any additional paths declared by
rules. Findings need interpretation. The scan updates its ledger of scanned
files; it does not rewrite the instructions or enforce a writing style.

Reads: rules, skills, agents, guides and lesson stores under `--root`, and their version history.
Prints: the report of open findings. Changes: `.agent-workspace/rule-health/ledger.json`.
Arguments: `--root <dir>`, `--paths <files>` to scan those files and a few stale ones, `--rotate <n>`.
Exit status: 0 when the scan ran, with or without open findings; 1 when the ledger is unreadable
or invalid; 2 when the scan scope is empty. `guide/general/rule-health.md` §1 explains the report.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lib.console import use_utf8_output
from lib.git import run_git
from lib.project import caller_path, enter_project_root
from rule_health.dead import signal_dead
from rule_health.drift import signal_drift
from rule_health.duplicates import signal_dup
from rule_health.growth import signal_growth
from rule_health.ledger import _fp_path, ledger_problems, load_ledger, open_findings, save_ledger
from rule_health.report import render_report
from rule_health.scope import resolve_scope, scope_findings
from rule_health.units import rule_lines

use_utf8_output()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="the tree to scan (default: the project root)")
    ap.add_argument("--paths", nargs="*", default=None)
    ap.add_argument("--rotate", type=int, default=3)
    args = ap.parse_args(argv)
    root = (caller_path(args.root) if args.root else Path(".")).resolve()

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
        touched = {_fp_path(caller_path(p).resolve(), root) for p in args.paths}
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

    stamp = run_git(["rev-parse", "HEAD"], root).stdout.strip()
    for p in chosen:
        ledger["last_scanned"][_fp_path(p, root)] = stamp
    save_ledger(root, ledger)

    return 0


if __name__ == "__main__":
    enter_project_root()
    sys.exit(main())
