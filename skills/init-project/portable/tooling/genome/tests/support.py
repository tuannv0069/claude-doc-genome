"""What the tests of this group share: the list of failed checks and the function that adds to it.

A test file imports `check` and `fails`, calls `check` once for each case, and prints
its own summary from `fails` before exiting non-zero when the list is not empty.
"""
from __future__ import annotations

fails: list[str] = []


def check(condition: bool, message: str) -> None:
    """Record `message` when `condition` is false."""
    if not condition:
        fails.append(message)
