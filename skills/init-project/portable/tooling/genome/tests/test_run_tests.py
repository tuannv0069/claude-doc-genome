#!/usr/bin/env python3
"""Exercise the group's test runner on temporary test folders.

The cases cover a passing folder, a failing file, a selection by name and an
empty folder, which must be reported as nothing run and not as success."""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import run_tests as R  # noqa: E402
from lib.console import use_utf8_output  # noqa: E402
from support import check, fails  # noqa: E402

use_utf8_output()





def quiet(tests_dir: Path, root: Path, names: list[str]) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return R.run(tests_dir, root, names)


with tempfile.TemporaryDirectory() as t:
    root = Path(t)
    tests = root / "tests"
    tests.mkdir()
    check(quiet(tests, root, []) == 2, "case 1: an empty test folder was not reported as nothing run")

    (tests / "test_good.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    check(quiet(tests, root, []) == 0, "case 2: a passing folder did not return 0")

    (tests / "test_bad.py").write_text("import sys\nsys.exit(1)\n", encoding="utf-8")
    check(quiet(tests, root, []) == 1, "case 3: a failing test file did not return 1")
    check(quiet(tests, root, ["test_good"]) == 0, "case 4: selecting the passing file by name did not return 0")
    check(quiet(tests, root, ["test_bad.py"]) == 1, "case 5: selecting the failing file with its extension did not return 1")
    check(quiet(tests, root, ["test_absent"]) == 2, "case 6: a name that matches no file was not reported as nothing run")

    check(quiet(tests, root, ["test_good", "test_absent"]) == 2,
          "case 8: a named test that does not exist was dropped silently beside one that does")

    (tests / "helper.py").write_text("import sys\nsys.exit(1)\n", encoding="utf-8")
    check(quiet(tests, root, ["test_good"]) == 0 and len(R.select(tests, [])) == 2,
          "case 7: a file without the test_ prefix was collected as a test")

for f in fails:
    print("FAIL:", f)
print(f"{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
