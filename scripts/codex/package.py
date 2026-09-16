#!/usr/bin/env python3
"""Build an isolated local marketplace containing only the Codex product."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from product_files import checked, skill_metadata


def build(skill: Path, output: Path):
    source = checked(Path(__file__).resolve().parents[2])
    skill, version_file, _, mapping = skill_metadata(skill)
    manifest_path = checked(Path(__file__).resolve().parent / "plugin.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("name") != "codex-genome":
        raise ValueError("The source is not the Codex genome product.")
    version = version_file.read_text(encoding="utf-8").strip()
    if manifest.get("version") != version or mapping.get("version") != version:
        raise ValueError("Synchronize Codex version metadata before packaging.")
    output = checked(output)
    if output.exists() or output.is_symlink():
        raise ValueError("Output must be a new directory; existing output is never replaced.")
    if output.is_relative_to(skill):
        raise ValueError("Output cannot be inside the skill being copied.")
    inputs = [manifest_path, *skill.rglob("*")]
    for path in inputs:
        checked(path)
    for name in ("docs/codex/package-readme.md", "LICENSE"):
        if not checked(source / name).is_file():
            raise ValueError(f"Package input is missing: {name}")
    tool = checked(skill / "scripts/genome.py")
    subprocess.run([sys.executable, str(tool), "check"], check=True)
    # Support assets come from this script's product; the payload comes only
    # from the explicit skill. No Claude metadata or live tree is traversed.
    destination = output / "plugins/codex-genome"
    (destination / ".codex-plugin").mkdir(parents=True)
    shutil.copy2(manifest_path, destination / ".codex-plugin/plugin.json")
    shutil.copytree(skill, destination / "skills/init-codex-genome",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for name, target in (("docs/codex/package-readme.md", "README.md"), ("LICENSE", "LICENSE")):
        shutil.copy2(source / name, destination / target)
    shutil.copy2(version_file, destination / "VERSION")
    marketplace = {"name": "codex-genome-local", "interface": {"displayName": "Codex Genome"},
                   "plugins": [{"name": "codex-genome", "source": {"source": "local", "path": "./plugins/codex-genome"},
                                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                                "category": "Productivity"}]}
    (output / ".agents/plugins").mkdir(parents=True)
    (output / ".agents/plugins/marketplace.json").write_text(json.dumps(marketplace, indent=2) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(build(args.skill_root, args.output))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Packaging failed: {error}\n")
