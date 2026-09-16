"""Filesystem checks for Codex product packaging and version metadata."""
import os
import json
import re
from pathlib import Path
import stat
import tempfile


def skill_metadata(root: Path):
    """Validate the explicit skill before any packaging or metadata write."""
    root = checked(root)
    skill = checked(root / "SKILL.md")
    version = checked(root / "VERSION")
    mapping = checked(root / "bundle/bundle-map.json")
    frontmatter = skill.read_text(encoding="utf-8").split("---", 2)
    if len(frontmatter) != 3 or frontmatter[0].strip() or re.findall(
            r"^name:[ \t]*([^\r\n]+)", frontmatter[1], re.MULTILINE) != ["init-codex-genome"]:
        raise ValueError("--skill-root must identify the init-codex-genome skill.")
    data = json.loads(mapping.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("product") != "codex-genome" or data.get("schema_version") != 1:
        raise ValueError("The skill does not contain the Codex genome bundle.")
    if not version.is_file():
        raise ValueError("The Codex skill must contain its canonical VERSION.")
    return root, version, mapping, data


def checked(path: Path):
    path = Path(os.path.abspath(path))
    for item in reversed((path, *path.parents)):
        if item.parent.is_dir() and item != item.parent:
            aliases = [p.name for p in item.parent.iterdir() if p.name.casefold() == item.name.casefold()]
            if aliases and aliases != [item.name]:
                raise ValueError(f"Case alias is not supported: {item}")
        if not item.exists() and not item.is_symlink():
            continue
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"Linked paths are not supported: {item}")
        if stat.S_ISREG(info.st_mode) and info.st_nlink != 1:
            raise ValueError(f"Hard-linked files are not supported: {item}")
    return path


def write_atomic(path: Path, text: str):
    path = checked(path)
    fd, temporary = tempfile.mkstemp(prefix=".codex-metadata-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        checked(path)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
