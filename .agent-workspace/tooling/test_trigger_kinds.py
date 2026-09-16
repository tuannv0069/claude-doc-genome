#!/usr/bin/env python3
"""Check real router contracts without prescribing trigger sentence wording.

The filename is retained for existing callers. The checks now verify that the
root instructions reach the lesson and role routers and that both routers can
be parsed by their consumers. Fixtures exercise missing links and malformed
router data, rather than matching a particular English explanation of §10.
"""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_lesson_router import parse_router as lesson_router
from verify_role_files import parse_router as role_router

TARGETS = {
    ".agent-workspace/lessons/index.md": lesson_router,
    ".agent-workspace/guide/roles/index.md": role_router,
}

def check(root):
    source = root / "CLAUDE.md"
    if not source.is_file(): return ["The root instruction file is missing."]
    text = source.read_text(encoding="utf-8")
    errors = []
    for name, parser in TARGETS.items():
        if name not in text:
            errors.append(f"Root instructions do not reference {name}.")
        path = root / name
        if not path.is_file():
            errors.append(f"Router is missing: {name}")
            continue
        errors.extend(parser(path)[1])
    return errors


def main():
    root = Path(__file__).resolve().parents[2]
    errors = check(root)
    with tempfile.TemporaryDirectory() as folder:
        fixture = Path(folder)
        (fixture / "CLAUDE.md").write_text("Read " + " and ".join(TARGETS) + ".\n", encoding="utf-8")
        headers = ["| file | work type | paired guide | checks |\n|---|---|---|---|\n",
                   "| work type | primary role | checking roles |\n|---|---|---|\n"]
        for name, header in zip(TARGETS, headers):
            path = fixture / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(header, encoding="utf-8")
        if check(fixture): errors.append("Valid router fixtures were rejected.")
        (fixture / "CLAUDE.md").write_text("There is no route here.\n", encoding="utf-8")
        if not check(fixture): errors.append("Missing root references were accepted.")
        (fixture / "CLAUDE.md").write_text("Read " + " and ".join(TARGETS), encoding="utf-8")
        (fixture / next(iter(TARGETS))).write_text("A changed schema.\n", encoding="utf-8")
        if not check(fixture): errors.append("A malformed router was accepted.")
    for error in errors: print("FAIL:", error)
    print(f"{len(errors)} routing failures")
    return 1 if errors else 0

if __name__ == "__main__": sys.exit(main())
