#!/usr/bin/env python3
"""Run every test of this tool group and report which ones failed.

Reads: the `test_*.py` files in `tests/` beside this file. Each is run as its own
process from the project root, because the tests are scripts that exit non-zero on failure.
Prints: one line for each test file with its result, then the output of each failing file.
Arguments: optional test file names, with or without `.py`, to run only those.
Exit status: 0 when every test passed, 1 when a test failed, 2 when no test file was found
or a named test file does not exist.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from lib.console import use_utf8_output
from lib.project import PROJECT_ROOT

use_utf8_output()

GROUP = Path(__file__).resolve().parent


def select(tests_dir: Path, names: list[str]) -> list[Path]:
    """Return the test files to run: all of them, or the ones named."""
    found = sorted(tests_dir.glob("test_*.py"))
    if not names:
        return found
    wanted = {name.removesuffix(".py") for name in names}
    return [path for path in found if path.stem in wanted]


def run(tests_dir: Path, root: Path, names: list[str]) -> int:
    tests = select(tests_dir, names)
    missing = sorted({name.removesuffix(".py") for name in names} - {path.stem for path in tests})
    for name in missing:
        print(f"{name}: no such test file in {tests_dir}", file=sys.stderr)
    if missing or not tests:
        print(f"{tests_dir}: nothing was run", file=sys.stderr)
        return 2
    failed: list[tuple[Path, str]] = []
    for path in tests:
        done = subprocess.run([sys.executable, str(path)], cwd=root, capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
        print(f"{'ok  ' if done.returncode == 0 else 'FAIL'} {path.name}")
        if done.returncode != 0:
            failed.append((path, done.stdout + done.stderr))
    for path, output in failed:
        print(f"\n--- {path.name} ---\n{output.rstrip()}")
    print(f"\n{len(tests) - len(failed)} of {len(tests)} test file(s) passed")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    return run(GROUP / "tests", PROJECT_ROOT, argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
