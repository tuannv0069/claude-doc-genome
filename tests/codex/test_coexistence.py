"""Integration boundary: the Codex adapter reuses a Claude-created genome workspace."""
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

CLAUDE = Path(__file__).resolve().parents[2]
SKILL = CLAUDE / "skills/init-codex-genome"
NODE = shutil.which("node")
spec = importlib.util.spec_from_file_location(
    "codex_deployment", SKILL / "bundle/portable/.agent-workspace/tooling/genome.py"
)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def snapshot_shared(root):
    result = {}
    prefixes = tuple(f".agent-workspace/{name}/" for name in ("guide", "lessons", "decisions", "wiki"))
    for file in root.rglob("*"):
        if file.is_file():
            relative = file.relative_to(root).as_posix()
            if relative.startswith(prefixes):
                result[relative] = file.read_bytes()
    return result


def snapshot_codex_adapter(root):
    result = {}
    for file in root.rglob("*"):
        if not file.is_file():
            continue
        relative = file.relative_to(root).as_posix()
        if relative == "AGENTS.md" or relative.startswith((".agent-workspace/rules/", ".codex/")) or relative == ".agent-workspace/tooling/genome.py":
            result[relative] = file.read_bytes()
    return result


def snapshot_claude_adapter(root):
    result = {}
    for file in root.rglob("*"):
        if not file.is_file():
            continue
        relative = file.relative_to(root).as_posix()
        if relative == "CLAUDE.md" or relative.startswith(".claude/") or (
            relative.startswith(".agent-workspace/tooling/") and relative != ".agent-workspace/tooling/genome.py"
        ):
            result[relative] = file.read_bytes()
    return result


@unittest.skipUnless(NODE and (CLAUDE / "scripts/deployment-map.mjs").is_file(), "Shared-workspace suite requires the Claude source product and Node.js")
class SharedWorkspace(unittest.TestCase):
    def mapping(self):
        script = "import {bundleFiles,TEMPLATES,isSharedPath} from './scripts/deployment-map.mjs'; console.log(JSON.stringify({files:[...bundleFiles(process.cwd())].map(([target,source])=>[target,source,isSharedPath(target)]),templates:TEMPLATES.map(([template,target])=>[template,target,isSharedPath(target)])}));"
        result = subprocess.run([NODE, "--input-type=module", "-e", script], cwd=CLAUDE, capture_output=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_codex_reuses_claude_workspace_and_both_updaters_preserve_the_other_adapter(self):
        mapping = self.mapping()

        with tempfile.TemporaryDirectory(prefix="genome-shared-") as temporary:
            root = Path(temporary)
            project = root / "project"
            project.mkdir()
            package = root / "codex-package"
            shutil.copytree(SKILL, package)

            for target, source, _shared in mapping["files"]:
                destination = project / target
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
            for template, target, _shared in mapping["templates"]:
                destination = project / target
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(CLAUDE / "skills/init-project/templates" / template, destination)
            recorded = subprocess.run(
                [NODE, str(CLAUDE / "scripts/init-manifest.mjs"), "--project", str(project)],
                cwd=root, capture_output=True, encoding="utf-8"
            )
            self.assertEqual(recorded.returncode, 0, recorded.stderr)

            shared_before = snapshot_shared(project)
            plan = g.deployment_plan(project, package, "init")
            self.assertFalse(plan["conflicts"], plan["conflicts"])
            self.assertTrue(any("Reusing the existing shared genome workspace" in item for item in plan["warnings"]))
            g.apply_plan(project, plan, plan["plan_hash"])

            self.assertEqual(snapshot_shared(project), shared_before)
            manifest = g.manifest(project)
            self.assertEqual(manifest["shared_workspace"], "reused")
            self.assertFalse(any(path.startswith(g.SHARED_PREFIXES) for path in manifest["files"]))
            self.assertIn(".agent-workspace/guide/", (project / "CLAUDE.md").read_text(encoding="utf-8"))
            self.assertIn(".agent-workspace/guide/", (project / "AGENTS.md").read_text(encoding="utf-8"))

            adapter_before = snapshot_codex_adapter(project)
            updated = subprocess.run(
                [NODE, str(CLAUDE / "scripts/update.mjs"), "--project", str(project), "--apply"],
                cwd=root, capture_output=True, encoding="utf-8"
            )
            self.assertEqual(updated.returncode, 0, updated.stderr + updated.stdout)
            self.assertEqual(snapshot_codex_adapter(project), adapter_before)

            codex_update = g.deployment_plan(project, package, "update")
            self.assertFalse(codex_update["conflicts"], codex_update["conflicts"])
            g.apply_plan(project, codex_update, codex_update["plan_hash"])
            self.assertEqual(snapshot_shared(project), shared_before)

            verified = g.verify(project)
            self.assertEqual(verified["status"], "pass", verified["errors"])

    def test_claude_reuses_codex_workspace_without_replacing_shared_files(self):
        mapping = self.mapping()
        with tempfile.TemporaryDirectory(prefix="genome-shared-reverse-") as temporary:
            root = Path(temporary)
            project = root / "project"
            project.mkdir()
            package = root / "codex-package"
            shutil.copytree(SKILL, package)

            plan = g.deployment_plan(project, package, "init")
            self.assertFalse(plan["conflicts"], plan["conflicts"])
            g.apply_plan(project, plan, plan["plan_hash"])
            shared_before = snapshot_shared(project)

            for target, source, shared in mapping["files"]:
                if shared:
                    continue
                destination = project / target
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
            for template, target, shared in mapping["templates"]:
                if shared:
                    continue
                destination = project / target
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(CLAUDE / "skills/init-project/templates" / template, destination)
            claude_root = project / "CLAUDE.md"
            claude_root.write_text(re.sub(r"\{\{[^}]+\}\}", "", claude_root.read_text(encoding="utf-8")), encoding="utf-8")
            recorded = subprocess.run(
                [NODE, str(CLAUDE / "scripts/init-manifest.mjs"), "--project", str(project), "--reuse-shared-workspace"],
                cwd=root, capture_output=True, encoding="utf-8"
            )
            self.assertEqual(recorded.returncode, 0, recorded.stderr)
            self.assertEqual(snapshot_shared(project), shared_before)

            claude_manifest = json.loads((project / ".claude/init-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(claude_manifest["sharedWorkspace"], "reused")
            self.assertFalse(any(path["path"].startswith(".agent-workspace/guide/") for path in claude_manifest["files"]))
            self.assertIn(".agent-workspace/guide/", (project / "CLAUDE.md").read_text(encoding="utf-8"))
            self.assertIn(".agent-workspace/guide/", (project / "AGENTS.md").read_text(encoding="utf-8"))

            linted = subprocess.run(
                [NODE, str(CLAUDE / "scripts/doc-lint.mjs"), "--quiet"],
                cwd=project, capture_output=True, encoding="utf-8"
            )
            self.assertEqual(linted.returncode, 0, linted.stderr + linted.stdout)
            for script in ("verify_lesson_router.py", "verify_role_files.py", "verify_decision_log.py", "verify_wiki.py"):
                checked = subprocess.run(
                    [sys.executable, str(project / ".agent-workspace/tooling" / script)],
                    cwd=project, capture_output=True, encoding="utf-8"
                )
                self.assertEqual(checked.returncode, 0, script + "\n" + checked.stderr + checked.stdout)

            codex_before = snapshot_codex_adapter(project)
            updated = subprocess.run(
                [NODE, str(CLAUDE / "scripts/update.mjs"), "--project", str(project), "--apply"],
                cwd=root, capture_output=True, encoding="utf-8"
            )
            self.assertEqual(updated.returncode, 0, updated.stderr + updated.stdout)
            self.assertEqual(snapshot_codex_adapter(project), codex_before)
            self.assertEqual(snapshot_shared(project), shared_before)

            claude_before = snapshot_claude_adapter(project)
            codex_update = g.deployment_plan(project, package, "update")
            self.assertFalse(codex_update["conflicts"], codex_update["conflicts"])
            g.apply_plan(project, codex_update, codex_update["plan_hash"])
            self.assertEqual(snapshot_claude_adapter(project), claude_before)
            self.assertEqual(snapshot_shared(project), shared_before)


if __name__ == "__main__":
    unittest.main()
