#!/usr/bin/env python3
"""Exercise the tool-group gate on temporary tooling folders.

One clean tree must pass. Each other case breaks one rule of `tooling.md` §2 to §5
and must be reported; a missing router must be reported as nothing to check."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import verify_tool_groups as V  # noqa: E402
from lib.console import use_utf8_output  # noqa: E402
from support import check, fails  # noqa: E402

use_utf8_output()

ROUTER = "| group | kind of work |\n|---|---|\n| `work/` | checking |\n| `app/tools/` | product |\n"
INDEX = "| entry point | what it does |\n|---|---|\n| `verify_a.py` | checks a |\n| `scan_b.py` | scans b |\n"
ENTRY_A = '"""Check a."""\nimport sys\n\nfrom lib.shared import helper\n\nhelper()\n'
ENTRY_B = '"""Scan b."""\nfrom b_parts.reader import read\nfrom lib.shared import helper\n'


def build(tmp: Path, changes: dict[str, str | None] | None = None, router: str = ROUTER) -> Path:
    """A clean tooling folder with one group, then `changes`: a path mapped to new text, or to None to remove it."""
    tooling = Path(tempfile.mkdtemp(dir=tmp)) / "tooling"
    files = {
        "index.md": router,
        "work/index.md": INDEX,
        "work/verify_a.py": ENTRY_A,
        "work/scan_b.py": ENTRY_B,
        "work/lib/shared.py": '"""Shared."""\n\ndef helper():\n    return 1\n',
        "work/b_parts/reader.py": '"""Read b."""\nfrom lib.shared import helper\n\ndef read():\n    return helper()\n',
        "work/tests/test_verify_a.py": "import sys\nsys.exit(0)\n",
        "work/tests/fixtures/sample.txt": "sample\n",
    }
    files.update(changes or {})
    for name, text in files.items():
        if text is None:
            continue
        path = tooling / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tooling


def reported(tooling: Path, fragment: str) -> bool:
    return any(fragment in problem for problem in V.check(tooling)[0])


with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)

    problems, readable = V.check(build(tmp))
    check(problems == [] and readable, f"case 1: a clean tooling folder reported a problem: {problems}")

    problems, readable = V.check(build(tmp, {"index.md": None}))
    check(bool(problems) and not readable, "case 2: a missing router was not reported as nothing to check")

    check(reported(build(tmp, {"loose.py": "x = 1\n"}), "directly under the tooling folder"),
          "case 3: a file directly under the tooling folder was not caught")
    check(reported(build(tmp, {"other/index.md": "| entry point |\n|---|\n"}), "the group `other/` has no row"),
          "case 4: a group missing from the router was not caught")
    check(reported(build(tmp, router=ROUTER + "| `gone/` | nothing |\n"), "the group `gone/`, which does not exist"),
          "case 5: a router row for a missing group was not caught")
    check(reported(build(tmp, {"work/index.md": None}), "has no index.md"),
          "case 6: a group without an index was not caught")
    check(reported(build(tmp, {"work/fetch_c.py": '"""Fetch c."""\n'}), "has no row in"),
          "case 7: an entry point without an index row was not caught")
    check(reported(build(tmp, {"work/index.md": INDEX + "| `verify_z.py` | gone |\n"}), "a row names `verify_z.py`"),
          "case 8: an index row for a missing entry point was not caught")
    check(reported(build(tmp, {"work/b_parts/deep/more.py": "x = 1\n"}), "a group is one level deep"),
          "case 9: a folder nested inside a tool's folder was not caught")
    check(reported(build(tmp, {"work/scan_b/part.py": "x = 1\n"}), "shares its name with an entry point"),
          "case 10: a tool's folder named like its entry point was not caught")
    check(reported(build(tmp, {"work/verify_a.py": ENTRY_A + "import scan_b\n"}), "imports the entry point `scan_b`"),
          "case 11: one entry point importing another was not caught")
    check(reported(build(tmp, {"work/verify_a.py": ENTRY_A.replace("import sys\n", "import sys\nfrom b_parts.reader import read\n")}),
                   "a tool's folder serves one tool"),
          "case 12: a tool's folder imported by two entry points was not caught")
    check(reported(build(tmp, {"work/lib/shared.py": '"""Shared."""\nfrom b_parts.reader import read\n'}),
                   "lib/ does not import a tool"),
          "case 13: lib/ importing a tool's folder was not caught")
    check(reported(build(tmp, {"work/c_parts/x.py": '"""X."""\nfrom b_parts.reader import read\n',
                               "work/index.md": INDEX}), "a tool does not import another tool"),
          "case 14: one tool's folder importing another was not caught")
    check(reported(build(tmp, {"work/b_parts/reader.py": '"""Read b."""\nX = 1\nimport os\n'}), "an import follows other code"),
          "case 15: an import in the middle of a file was not caught")
    check(reported(build(tmp, {"work/tests/test_verify_a.py": None, "work/tests/fixtures/sample.txt": None}), "no tests/ folder"),
          "case 16: a group with tools and no tests folder was not caught")

    check(reported(build(tmp, {"work/verify_a.py": ENTRY_A + "import os\n"}), "verify_a.py:7: an import follows other code"),
          "case 18: an import in the middle of an entry point was not caught")
    check(reported(build(tmp, {"work/lib/shared.py": '"""Shared."""\nimport scan_b\n'}), "a call goes downward only"),
          "case 19: lib/ importing an entry point was not caught")

    # what must NOT be reported: generated folders, the fixtures folder, an import inside a function
    clean = build(tmp, {"work/__pycache__/x.pyc": "", "work/lib/__pycache__/y.pyc": "",
                        "work/b_parts/reader.py": '"""Read b."""\n\ndef read():\n    import os\n    return os.sep\n'})
    check(V.check(clean)[0] == [], f"case 17: generated folders or a local import were reported: {V.check(clean)[0]}")

for failure in fails:
    print("FAIL:", failure)
print(f"{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
