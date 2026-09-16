"""Exercise the built product as an external consumer, including its version boundary."""
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2]
SCRIPTS = SOURCE / "scripts/codex"
SKILL = SOURCE / "skills/init-codex-genome"


def version_fixture(root):
    """Copy only support scripts, and construct independent Codex metadata."""
    support = root / "scripts/codex"
    shutil.copytree(SCRIPTS, support, ignore=shutil.ignore_patterns("__pycache__"))
    metadata = support / "plugin.json"
    metadata.write_text(json.dumps({"name": "codex-genome", "version": "1.0.0"}), encoding="utf-8")
    skill = root / "skills/init-codex-genome"
    (skill / "bundle").mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: init-codex-genome\n---\n", encoding="utf-8")
    version = skill / "VERSION"
    version.write_text("1.0.0\n", encoding="utf-8")
    mapping = skill / "bundle/bundle-map.json"
    mapping.write_text(json.dumps({"product": "codex-genome", "schema_version": 1,
                                   "version": "1.0.0", "files": []}), encoding="utf-8")
    return support, skill, metadata, mapping, version


class PackagingTests(unittest.TestCase):
    def test_external_package_initializes_without_source_checkout(self):
        with tempfile.TemporaryDirectory(prefix="codex-genome-package-") as temporary:
            root = Path(temporary)
            output = root / "phân phối có dấu"
            built = subprocess.run([sys.executable, str(SCRIPTS / "package.py"),
                                    "--skill-root", str(SKILL), "--output", str(output)],
                                   capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
            plugin = output / "plugins/codex-genome"
            self.assertFalse((plugin / ".claude").exists())
            self.assertFalse((plugin / "CLAUDE.md").exists())
            self.assertFalse((plugin / ".agents").exists())
            self.assertEqual([p.name for p in (plugin / "skills").iterdir()], ["init-codex-genome"])
            self.assertEqual((plugin / "VERSION").read_bytes(), (SKILL / "VERSION").read_bytes())
            wrapper = plugin / "skills/init-codex-genome/scripts/genome.py"
            for link in re.findall(r"\]\(([^)]+)\)", (plugin / "README.md").read_text(encoding="utf-8")):
                self.assertTrue((plugin / link).is_file(), link)
            target = root / "project thử nghiệm"
            target.mkdir()
            command = [sys.executable, str(wrapper), "init", "--project", str(target)]
            proposed = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(proposed.returncode, 0, proposed.stdout + proposed.stderr)
            plan = json.loads(proposed.stdout)
            self.assertFalse((target / "AGENTS.md").exists())
            applied = subprocess.run(command + ["--apply", "--plan-hash", plan["plan_hash"]],
                                     cwd=root, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            tool = target / ".agent-workspace/tooling/genome.py"
            checked = subprocess.run([sys.executable, str(tool), "verify", "--project", str(target)],
                                     cwd=root, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            # A build must not replace an existing artifact or its edits.
            sentinel = output / "keep.txt"
            sentinel.write_text("local artifact edit", encoding="utf-8")
            again = subprocess.run([sys.executable, str(SCRIPTS / "package.py"),
                                    "--skill-root", str(SKILL), "--output", str(output)],
                                   capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(again.returncode, 0)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "local artifact edit")

    def test_version_changes_only_explicit_product(self):
        with tempfile.TemporaryDirectory(prefix="codex-genome-version-") as temporary:
            root = Path(temporary)
            parent_version = root / "VERSION"
            parent_version.write_text("5.0.0\n", encoding="utf-8")
            support, skill, metadata, mapping, version = version_fixture(root)
            script = support / "sync-version.py"
            changed = subprocess.run([sys.executable, str(script), "set", "1.2.3", "--skill-root", str(skill)],
                                     cwd=root, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(changed.returncode, 0, changed.stdout + changed.stderr)
            self.assertEqual(json.loads(metadata.read_text())['version'], "1.2.3")
            self.assertEqual(json.loads(mapping.read_text())['version'], "1.2.3")
            self.assertEqual(version.read_text(), "1.2.3\n")
            self.assertEqual(parent_version.read_text(), "5.0.0\n")
            refused = subprocess.run([sys.executable, str(script), "set", "1.2.4", "--skill-root", str(root)],
                                     capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(refused.returncode, 0)
            self.assertEqual(parent_version.read_text(), "5.0.0\n")

    def test_version_rejects_hardlinked_metadata_without_changing_any_mirror(self):
        with tempfile.TemporaryDirectory(prefix="codex-genome-linked-version-") as temporary:
            root = Path(temporary)
            support, skill, metadata, mapping, version = version_fixture(root)
            outside = root / "other-product.json"
            before = json.dumps({"name": "codex-genome", "version": "1.0.0"})
            outside.write_text(before, encoding="utf-8")
            metadata.unlink()
            os.link(outside, metadata)
            result = subprocess.run([sys.executable, str(support / "sync-version.py"), "set", "1.2.3", "--skill-root", str(skill)], capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(outside.read_text(encoding="utf-8"), before)
            self.assertEqual(version.read_text(), "1.0.0\n")
            self.assertEqual(json.loads(mapping.read_text())['version'], "1.0.0")

    def test_package_refuses_recursive_destination_before_creating_it(self):
        # The proposed destination is inside the actual source skill. Rejection
        # must happen before creating any source artifact or starting a copy.
        destination = SKILL / "recursive-output-test"
        self.assertFalse(destination.exists())
        result = subprocess.run([sys.executable, str(SCRIPTS / "package.py"), "--skill-root", str(SKILL), "--output", str(destination)], capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("inside the skill", result.stderr)
        self.assertFalse(destination.exists())

    def test_wrong_skill_identity_is_refused_without_writes(self):
        with tempfile.TemporaryDirectory(prefix="codex-genome-identity-") as temporary:
            root = Path(temporary)
            support, skill, metadata, mapping, version = version_fixture(root)
            (skill / "SKILL.md").write_text("---\nname: init-project\n---\n", encoding="utf-8")
            output = root / "package"
            for script, arguments in (("sync-version.py", ["set", "9.9.9"]),
                                      ("package.py", ["--output", str(output)])):
                result = subprocess.run([sys.executable, str(support / script),
                                         *arguments, "--skill-root", str(skill)],
                                        capture_output=True, text=True, encoding="utf-8")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("init-codex-genome", result.stderr)
            self.assertFalse(output.exists())
            self.assertEqual(version.read_text(), "1.0.0\n")
            self.assertEqual(json.loads(metadata.read_text())['version'], "1.0.0")
            self.assertEqual(json.loads(mapping.read_text())['version'], "1.0.0")


if __name__ == "__main__":
    unittest.main()
