"""The project root, found from this file's own location.

Used by the entry points, so that a tool gives the same result whatever directory
it is started from. The location is fixed by the layout of a tool group:
`<root>/.agent-workspace/tooling/<group>/lib/project.py`.
"""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
WORKSPACE = PROJECT_ROOT / ".agent-workspace"
# The directory the tool was started from; `enter_project_root` records it before leaving.
_caller_dir = Path.cwd()


def enter_project_root() -> Path:
    """Make the project root the working directory and return it.

    The tools name their default inputs relative to the project root and print
    those relative paths in their findings; changing directory keeps both.
    """
    global _caller_dir
    _caller_dir = Path.cwd()
    os.chdir(PROJECT_ROOT)
    return PROJECT_ROOT


def caller_path(value: str) -> Path:
    """A path given as an argument, as the person who typed it meant it.

    A relative path is relative to the directory the tool was started from, which
    is no longer the working directory once `enter_project_root` has run. Started
    from the project root, the path is returned unchanged, so findings keep the
    short relative form.
    """
    path = Path(value)
    if path.is_absolute() or _caller_dir.resolve() == PROJECT_ROOT:
        return path
    return _caller_dir / path
