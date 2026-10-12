"""One way to run git and read its output as text.

Used by the tools that read version history. The output is always decoded as
UTF-8: git writes file content and names in UTF-8, while the host's preferred
encoding may be a legacy code page, and decoding with that would corrupt every
non-ASCII character.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


def run_git(args: list[str], cwd: Path | str, timeout: float | None = None) -> subprocess.CompletedProcess:
    """Run `git <args>` in `cwd` and return the completed process.

    `args` does not include "git". The caller decides what a non-zero return code
    means; this function raises only what `subprocess.run` raises, such as git
    missing from the path or the timeout expiring.
    """
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(cwd), timeout=timeout,
    )
