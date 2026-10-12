"""Reading the rows of a router table.

Used by the gates that read a router as data: the lesson router and the role
router. A router cell never contains a pipe character, so a row is split at
every pipe. A table whose cells may hold an escaped pipe, such as a wiki
cluster, needs its own splitter and does not use this one.
"""
from __future__ import annotations


def row_cells(line: str) -> list[str]:
    """Split one table line `| a | b |` into its trimmed cells."""
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    """True for the delimiter row under a header, such as `|---|:--|`."""
    return bool(cells) and set("".join(cells)) <= set("-: ")
