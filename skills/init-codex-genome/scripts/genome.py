#!/usr/bin/env python3
"""Run the maintenance tool from this installed skill's own bundle."""
from pathlib import Path
import runpy
import sys


def main():
    sys.dont_write_bytecode = True
    package = Path(__file__).resolve().parents[1]
    tool = package / "bundle/portable/.agent-workspace/tooling/genome.py"
    if not tool.is_file():
        raise SystemExit("The skill bundle is incomplete: genome.py is missing.")
    # An installed skill locates only its own bundle, never the target's Git root.
    if len(sys.argv) > 1 and sys.argv[1] in {"init", "update", "check", "refresh"} and "--package-root" not in sys.argv:
        sys.argv.extend(["--package-root", str(package)])
    sys.path.insert(0, str(tool.parent))
    runpy.run_path(str(tool), run_name="__main__")


if __name__ == "__main__":
    main()
