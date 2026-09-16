#!/usr/bin/env python3
"""Check or set only the independent Codex product's version mirrors."""
import argparse
import json
import re
import sys
from pathlib import Path
from product_files import checked, write_atomic, skill_metadata

SEMVER = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?")


def run(root: Path, command: str, version: str | None):
    root, version_file, mapping, bundle = skill_metadata(root)
    support = checked(Path(__file__).resolve().parent)
    manifest = checked(support / "plugin.json")
    meta = json.loads(manifest.read_text(encoding="utf-8"))
    if meta.get("name") != "codex-genome":
        raise ValueError("The script's support directory is not the Codex product.")
    canonical = version if command == "set" else version_file.read_text(encoding="utf-8").strip()
    if canonical is None or not SEMVER.fullmatch(canonical):
        raise ValueError("A valid semantic version is required.")
    # The bundle map is a distribution mirror, not a deployed project manifest.
    records = [(manifest, meta), (mapping, bundle)]
    if command == "check":
        drift = [str(p) for p, data in records if data.get("version") != canonical]
        if drift:
            raise ValueError("Codex version mismatch: " + ", ".join(drift))
    else:
        for path, data in records:
            data["version"] = canonical
            write_atomic(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        write_atomic(version_file, canonical + "\n")
    print(f"Codex version {canonical}: {command} complete.")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "sync", "set"], default="check", nargs="?")
    parser.add_argument("version", nargs="?")
    parser.add_argument("--skill-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        run(args.skill_root, args.command, args.version)
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")
