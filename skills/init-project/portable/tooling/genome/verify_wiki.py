#!/usr/bin/env python3
"""Check the wiki's recorded links, evidence fields, and identifiers.

Located evidence is checked against the source path and anchor positions. Other
evidence forms receive schema checks, whose limits are reported to the caller.
The gate does not establish the truth or readability of a claim.

Reads: `.agent-workspace/wiki/` and the source material its router names.
Prints: the number of clusters, the limits of the check, and one `FAIL:` line for each failure.
Arguments: none to check the tier; `--new-id <cluster>` to print an unused identifier;
`--merge-check <ref> <ref> [...]` to check that no identifier of those revisions is missing.
Exit status: 0 when nothing failed, 1 when a check failed, 2 when the arguments are incomplete.
"""
import sys

from lib.project import WORKSPACE, enter_project_root
from wiki.identifiers import check_merge, new_id
from wiki.limits import schema_only_classes, undetected_locator_liveness_checks, unverified_class_checks
from wiki.tier import check_tier


def main(argv):
    if len(argv) >= 2 and argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    root = WORKSPACE

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
    enter_project_root()
    sys.exit(main(sys.argv))
