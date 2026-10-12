"""Console setup shared by the tools of this group.

Used by every entry point and test that prints paths or text which may hold
characters outside the console's default code page.
"""
from __future__ import annotations

import sys


def use_utf8_output() -> None:
    """Make standard output accept any character; one it cannot encode is replaced.

    A Windows console defaults to a legacy code page, and printing a finding that
    quotes non-ASCII text would otherwise raise instead of reporting the finding.
    """
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
