"""Exercise ownership boundaries and persisted state through the independent tool."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
SKILL = REPO / "skills/init-codex-genome"
TOOL = SKILL / "bundle/portable/.agent-workspace/tooling/genome.py"
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("genome", TOOL)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def put(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content.encode() if isinstance(content, str) else content)


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


class Deployment(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex-genome-")
        self.base = Path(self.temp.name)
        self.project = self.base / "Dự án có dấu"
        self.package = self.base / "external package"
        self.project.mkdir()
        self.portable = g.BASE + "/rules/work.md"
        self.seed = g.BASE + "/lessons/index.md"
        self.mapping = {"schema_version": 1, "product": g.PRODUCT, "version": "1.0.0", "files": [
            {"path": "AGENTS.md", "kind": "region", "source": "templates/AGENTS.md"},
            {"path": self.portable, "kind": "portable", "source": "portable/" + self.portable, "live": self.portable},
            {"path": self.seed, "kind": "seed", "source": "templates/lessons-index.md"},
        ]}
        put(self.package / "bundle/templates/AGENTS.md", "Read project guidance before changing it.\n")
        put(self.package / "bundle/templates/lessons-index.md", "Project lessons.\n")
        put(self.package / ("bundle/portable/" + self.portable), "Original portable rule.\n")
        for folder, roster in (("rules", g.CORE_RULES), ("guide/general", g.CORE_GUIDES), ("guide/roles", g.CORE_ROLES), ("tooling", ("genome",))):
            for name in roster:
                path = f"{g.BASE}/{folder}/{name}." + ("py" if folder == "tooling" else "md")
                self.mapping["files"].append({"path": path, "kind": "portable", "source": "portable/" + path, "live": path})
                put(self.package / ("bundle/portable/" + path), "Core fixture source\n")
        for name in ("guide/index.md", "guide/roles/index.md", "decisions/index.md", "wiki/index.md"):
            path = g.BASE + "/" + name
            source = "templates/" + name
            self.mapping["files"].append({"path": path, "kind": "seed", "source": source})
            put(self.package / ("bundle/" + source), "Project router\n")
        self.save_map()

    def tearDown(self):
        self.temp.cleanup()

    def save_map(self):
        put(self.package / "bundle/bundle-map.json", g.encoded(self.mapping))

    def plan(self, mode="init", adoption=None):
        return g.deployment_plan(self.project, self.package, mode, adoption)

    def install(self):
        plan = self.plan()
        self.assertFalse(plan["conflicts"])
        return g.apply_plan(self.project, plan, plan["plan_hash"])

    def test_dry_run_no_writes_and_apply_repeated_update_stable(self):
        before = snapshot(self.project)
        plan = self.plan()
        self.assertEqual(snapshot(self.project), before)
        g.apply_plan(self.project, plan, plan["plan_hash"])
        deployed = snapshot(self.project)
        update = self.plan("update")
        self.assertEqual(update["changes"], [])
        g.apply_plan(self.project, update, update["plan_hash"])
        self.assertEqual(snapshot(self.project), deployed)

    def test_existing_project_requires_exact_review_and_preserves_outside_bytes(self):
        old = b"\xef\xbb\xbf# Human project\r\nKeep this.\r\n"
        put(self.project / "AGENTS.md", old)
        put(self.project / ".gitignore", b"existing\r\n")
        self.assertTrue(self.plan()["conflicts"])
        adoption = {"AGENTS.md": {"before_sha256": g.digest(old), "replacement": old.decode("utf-8")}}
        plan = self.plan(adoption=adoption)
        self.assertFalse(plan["conflicts"])
        g.apply_plan(self.project, plan, plan["plan_hash"])
        self.assertTrue((self.project / "AGENTS.md").read_bytes().startswith(old))
        self.assertTrue((self.project / ".gitignore").read_bytes().startswith(b"existing\r\n"))
        put(self.project / "AGENTS.md", (self.project / "AGENTS.md").read_bytes() + b"\r\nOutside after\r\n")
        self.mapping["version"] = "2.0.0"
        self.save_map()
        plan = self.plan("update")
        g.apply_plan(self.project, plan, plan["plan_hash"])
        self.assertTrue((self.project / "AGENTS.md").read_bytes().endswith(b"\r\nOutside after\r\n"))

    def test_local_edit_conflict_is_atomic_and_version_not_advanced(self):
        self.install()
        put(self.project / self.portable, "Local edit")
        self.mapping["version"] = "2.0.0"
        self.save_map()
        before = snapshot(self.project)
        plan = self.plan("update")
        self.assertTrue(plan["conflicts"])
        with self.assertRaises(g.GenomeError):
            g.apply_plan(self.project, plan, plan["plan_hash"])
        self.assertEqual(snapshot(self.project), before)
        self.assertEqual(g.manifest(self.project)["version"], "1.0.0")

    def test_managed_region_local_edits_block_but_seeds_preserve_user_text(self):
        self.install()
        put(self.project / self.seed, "User-owned lesson index")
        plan = self.plan("update")
        g.apply_plan(self.project, plan, plan["plan_hash"])
        self.assertEqual((self.project / self.seed).read_text(), "User-owned lesson index")
        put(self.project / "AGENTS.md", (self.project / "AGENTS.md").read_text().replace("Read project", "Changed project"))
        self.assertTrue(self.plan("update")["conflicts"])

    def test_template_change_blocks_until_exact_acknowledgment(self):
        self.install()
        source = b"New template"
        put(self.package / "bundle/templates/lessons-index.md", source)
        self.assertTrue(self.plan("update")["conflicts"])
        review = {self.seed: {"before_sha256": g.digest((self.project / self.seed).read_bytes()), "accept_template_sha256": g.digest(source)}}
        plan = self.plan("update", review)
        self.assertFalse(plan["conflicts"])
        g.apply_plan(self.project, plan, plan["plan_hash"])
        self.assertEqual((self.project / self.seed).read_bytes(), b"Project lessons.\n")

    def test_retirement_requires_unmodified_owned_file(self):
        self.install()
        self.mapping["files"] = [e for e in self.mapping["files"] if e["path"] != self.portable]
        self.save_map()
        plan = self.plan("update")
        self.assertTrue(any(e["action"] == "delete" for e in plan["changes"]))
        put(self.project / self.portable, "User edit after plan")
        with self.assertRaises(g.GenomeError):
            g.apply_plan(self.project, plan, plan["plan_hash"])
        self.assertTrue(self.plan("update")["conflicts"])
        put(self.project / self.portable, "Original portable rule.\n")
        plan = self.plan("update")
        g.apply_plan(self.project, plan, plan["plan_hash"])
        self.assertFalse((self.project / self.portable).exists())

    def test_review_hash_changes_when_bundle_or_project_changes(self):
        plan = self.plan()
        put(self.package / "bundle/templates/AGENTS.md", "Different instructions")
        revised = self.plan()
        with self.assertRaises(g.GenomeError):
            g.apply_plan(self.project, revised, plan["plan_hash"])
        self.assertEqual(snapshot(self.project), {})

    def test_truncated_bundle_cannot_install_or_retire_existing_core(self):
        self.install()
        before = snapshot(self.project)
        self.mapping["files"] = [entry for entry in self.mapping["files"] if entry["path"] != g.BASE + "/rules/critical-thinking.md"]
        self.save_map()
        with self.assertRaises(g.GenomeError):
            self.plan("update")
        self.assertEqual(snapshot(self.project), before)

    def test_explicit_local_resolution_is_bound_to_both_target_and_source(self):
        self.install()
        put(self.project / self.portable, "User merged version")
        source = (self.package / ("bundle/portable/" + self.portable)).read_bytes()
        review = {self.portable: {"before_sha256": g.digest(b"User merged version"), "accept_source_sha256": g.digest(source), "replace_from_bundle": True}}
        plan = self.plan("update", review)
        self.assertFalse(plan["conflicts"])
        put(self.project / self.portable, "Later local edit")
        self.assertTrue(self.plan("update", review)["conflicts"])
        put(self.project / self.portable, "User merged version")
        put(self.package / ("bundle/portable/" + self.portable), "Later source")
        self.assertTrue(self.plan("update", review)["conflicts"])
        put(self.package / ("bundle/portable/" + self.portable), source)
        plan = self.plan("update", review)
        g.apply_plan(self.project, plan, plan["plan_hash"])
        self.assertEqual((self.project / self.portable).read_bytes(), source)

    def test_interrupted_update_recovers_original_bytes_then_retries(self):
        self.install()
        before = snapshot(self.project)
        put(self.package / ("bundle/portable/" + self.portable), "New portable rule")
        self.mapping["version"] = "2.0.0"
        self.save_map()
        plan = self.plan("update")
        with self.assertRaises(g.GenomeError):
            g.apply_plan(self.project, plan, plan["plan_hash"], fail_after=1)
        with self.assertRaises(g.GenomeError):
            self.plan("update")
        recovery = g.recovery(self.project)
        g.recovery(self.project, True, recovery["plan_hash"])
        self.assertEqual(snapshot(self.project), before)
        plan = self.plan("update")
        g.apply_plan(self.project, plan, plan["plan_hash"])
        self.assertEqual(g.manifest(self.project)["version"], "2.0.0")

    def test_recovery_refuses_to_overwrite_post_failure_edit(self):
        plan = self.plan()
        with self.assertRaises(g.GenomeError):
            g.apply_plan(self.project, plan, plan["plan_hash"], fail_after=1)
        put(self.project / "AGENTS.md", "Later human edit")
        with self.assertRaises(g.GenomeError):
            g.recovery(self.project)
        self.assertEqual((self.project / "AGENTS.md").read_text(), "Later human edit")

    def test_corrupt_recovery_payload_is_rejected_before_replay(self):
        plan = self.plan()
        with self.assertRaises(g.GenomeError):
            g.apply_plan(self.project, plan, plan["plan_hash"], fail_after=1)
        journal = g.load(self.project / g.JOURNAL)
        journal["entries"][0]["before_base64"] = "Y29ycnVwdA=="
        put(self.project / g.JOURNAL, g.encoded(journal))
        before = snapshot(self.project)
        with self.assertRaises(g.GenomeError):
            g.recovery(self.project)
        self.assertEqual(snapshot(self.project), before)

    def test_live_lock_blocks_second_writer_and_recovery(self):
        plan = self.plan()
        guard = g.lock(self.project)
        try:
            with self.assertRaises(g.GenomeError):
                g.apply_plan(self.project, plan, plan["plan_hash"])
            with self.assertRaises(g.GenomeError):
                g.recovery(self.project)
        finally:
            guard.unlink()

    def test_escape_windows_alias_hardlink_and_case_alias_are_rejected(self):
        for path in ("../outside", "C:/outside", "a/../b", "a\\b", "a./b", "NUL/file", "foo:bar", "SHORT~1/a", "/absolute"):
            with self.subTest(path=path), self.assertRaises(g.GenomeError):
                g.safe(self.project, path)
        put(self.project / "Case.txt", "keep")
        with self.assertRaises(g.GenomeError):
            g.safe(self.project, "case.txt")
        outside = self.base / "outside"
        put(outside, "keep")
        os.link(outside, self.project / "hard")
        with self.assertRaises(g.GenomeError):
            g.safe(self.project, "hard")

    def test_symlink_is_rejected_when_host_allows_creation(self):
        outside = self.base / "outside-dir"
        outside.mkdir()
        try:
            os.symlink(outside, self.project / "link", target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"Host cannot create symlink: {exc}")
        with self.assertRaises(g.GenomeError):
            g.safe(self.project, "link/file")

    def test_malicious_manifest_cannot_retire_claude_files(self):
        self.install()
        value = g.manifest(self.project)
        value["files"][".claude/rules/keep.md"] = {"kind": "portable", "sha256": "abc"}
        put(self.project / g.MANIFEST, g.encoded(value))
        with self.assertRaises(g.GenomeError):
            self.plan("update")

    def test_legacy_ownership_and_active_renderer_block_adoption(self):
        put(self.project / ".claude/init-manifest.json", json.dumps({"version": "4.0.0", "harness": "both", "files": [{"path": self.portable, "sha256": "abc"}, {"path": ".codex/rules/old.md", "sha256": "abc"}]}))
        put(self.project / ".claude/skills/update/SKILL.md", "Run python .agent-workspace/tooling/render_codex.py")
        plan = self.plan()
        self.assertTrue(any("Another installer owns" in c for c in plan["conflicts"]))
        self.assertTrue(any("renderer" in c for c in plan["conflicts"]))
        self.assertIn(".codex/rules/old.md", plan["legacy"]["owned_paths"])

    def test_existing_complete_workspace_is_reused_across_codex_updates(self):
        claude_files = []
        for entry in self.mapping["files"]:
            if entry["path"].startswith(g.SHARED_PREFIXES):
                source = self.package / ("bundle/" + entry["source"])
                put(self.project / entry["path"], source.read_bytes())
                claude_files.append({"path": entry["path"], "sha256": g.digest(source.read_bytes())})
        put(self.project / ".claude/init-manifest.json", json.dumps({"version": "5.0.0", "files": claude_files}))

        plan = self.plan()
        self.assertFalse(plan["conflicts"], plan["conflicts"])
        self.assertTrue(any("shared genome workspace" in warning for warning in plan["warnings"]))
        g.apply_plan(self.project, plan, plan["plan_hash"])
        installed = g.manifest(self.project)
        self.assertEqual(installed["shared_workspace"], "reused")
        self.assertFalse(any(name.startswith(g.SHARED_PREFIXES) for name in installed["files"]))

        lesson = self.project / self.seed
        put(lesson, "Shared lesson changed by another agent.\n")
        update = self.plan("update")
        self.assertFalse(update["conflicts"], update["conflicts"])
        g.apply_plan(self.project, update, update["plan_hash"])
        self.assertEqual(lesson.read_text(), "Shared lesson changed by another agent.\n")

    def test_reused_core_workspace_receives_missing_optional_wiki_seed(self):
        claude_files = []
        wiki = g.BASE + "/wiki/index.md"
        for entry in self.mapping["files"]:
            if entry["path"].startswith(g.SHARED_PREFIXES) and entry["path"] != wiki:
                source = self.package / ("bundle/" + entry["source"])
                put(self.project / entry["path"], source.read_bytes())
                claude_files.append({"path": entry["path"], "sha256": g.digest(source.read_bytes())})
        put(self.project / ".claude/init-manifest.json", json.dumps({"version": "5.0.0", "files": claude_files}))

        plan = self.plan()
        self.assertFalse(plan["conflicts"], plan["conflicts"])
        g.apply_plan(self.project, plan, plan["plan_hash"])
        self.assertTrue((self.project / wiki).is_file())
        installed = g.manifest(self.project)
        self.assertIn(wiki, installed["files"])
        self.assertFalse(any(name.startswith(g.SHARED_PREFIXES) and name != wiki for name in installed["files"]))

    def test_foreign_owned_root_gitignore_cannot_be_modified(self):
        put(self.project / ".gitignore", "Claude-owned ignore")
        put(self.project / ".claude/init-manifest.json", json.dumps({"files": [{"path": ".gitignore", "sha256": "abc"}]}))
        plan = self.plan()
        self.assertTrue(any("owns .gitignore" in c for c in plan["conflicts"]))
        self.assertFalse(any(e["path"] == ".gitignore" for e in plan["changes"]))

    def test_nested_instructions_are_reported_observed_and_preserved(self):
        put(self.project / "subproject/AGENTS.override.md", "Nested instructions")
        plan = self.plan()
        self.assertTrue(any("subproject/AGENTS.override.md" in w for w in plan["warnings"]))
        self.assertIn("subproject/AGENTS.override.md", plan["observations"])
        g.apply_plan(self.project, plan, plan["plan_hash"])
        self.assertEqual((self.project / "subproject/AGENTS.override.md").read_text(), "Nested instructions")

    @unittest.skipUnless(os.name == "nt", "Windows directory junction")
    def test_windows_junction_never_writes_to_referent(self):
        outside = self.base / "outside-junction"
        outside.mkdir()
        put(outside / "keep.txt", "untouched")
        junction = self.project / ".agent-workspace"
        env = {**os.environ, "CODEX_TEST_JUNCTION": str(junction), "CODEX_TEST_REFERENT": str(outside)}
        result = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", "New-Item -ItemType Junction -Path $env:CODEX_TEST_JUNCTION -Target $env:CODEX_TEST_REFERENT | Out-Null"], env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        try:
            with self.assertRaises(g.GenomeError):
                self.plan()
            self.assertEqual(snapshot(outside), {"keep.txt": b"untouched"})
        finally:
            os.rmdir(junction)

    def test_sparse_legacy_generated_label_never_establishes_ownership(self):
        put(self.project / ".claude/init-manifest.json", '{"version":"4.0.0","harness":"both","files":[]}')
        put(self.project / "AGENTS.md", "<!-- generated by renderer -->\nLegacy project text")
        self.assertTrue(self.plan()["conflicts"])

    def test_override_blocks_completion_without_modifying_override(self):
        put(self.project / "AGENTS.override.md", "Existing override")
        plan = self.plan()
        self.assertTrue(any("overrides" in c for c in plan["conflicts"]))
        self.assertEqual((self.project / "AGENTS.override.md").read_text(), "Existing override")

    def test_unrelated_config_and_history_remain_byte_identical(self):
        for path in (".codex/config.toml", ".codex/agents/existing.toml", ".agents/skills/other/SKILL.md", ".agent-workspace/lessons/history.md", ".agent-workspace/decisions/old.md", ".agent-workspace/wiki/fact.md"):
            put(self.project / path, "Existing user content\n")
        before = snapshot(self.project)
        self.install()
        after = snapshot(self.project)
        self.assertTrue(all(after[p] == value for p, value in before.items()))

    def test_cli_root_explicit_and_external_package_from_three_directories(self):
        for cwd in (REPO, Path(__file__).resolve().parent, self.base):
            result = subprocess.run([sys.executable, str(TOOL), "init", "--project", str(self.project), "--package-root", str(self.package)], cwd=cwd, capture_output=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["project"], str(self.project))
        result = subprocess.run([sys.executable, str(TOOL), "init"], cwd=self.project, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(snapshot(self.project), {})


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex-gate-source-")
        self.root = Path(self.temp.name)
        plan = g.deployment_plan(self.root, SKILL, "init")
        g.apply_plan(self.root, plan, plan["plan_hash"])

    def tearDown(self):
        self.temp.cleanup()

    def source_texts(self):
        return {p.relative_to(self.root).as_posix(): p.read_text(encoding="utf-8-sig") for p in g.markdown_files(self.root)}

    def test_role_semantic_prose_requires_only_the_routed_completion_section(self):
        texts = self.source_texts()
        path = g.BASE + "/guide/roles/editor.md"
        texts[path] = "---\nscope: project\n---\n# Project editor\n\nAssess whether a source script serves its audience. Read the approved brief and script together. Check unsupported claims against evidence; the project owns voice and audience expectations. Resolve material ambiguity before accepting the script.\n\n## §6 Completion criteria\n\nEvery substantive claim needs support and the script must meet the approved brief.\n"
        self.assertEqual(g.typed_records(self.root, texts), [])
        texts[path] = texts[path].replace("## §6 Completion criteria", "## Completion criteria")
        self.assertTrue(any("Role completion section missing" in e for e in g.typed_records(self.root, texts)))

    def test_lesson_contract_checks_phase_links_cycles_and_schema(self):
        texts = self.source_texts()
        root = g.BASE + "/lessons/"
        texts[root + "index.md"] = "| file | work type | paired guide | checks |\n|---|---|---|---|\n| a.md | Writing | — | b.md |\n| b.md | Review | — | a.md |\n"
        texts[root + "a.md"] = "---\nscope: project\nphase: invented\nwork_scope: Writing artifacts\n---\n# Lesson\n"
        errors = g.typed_records(self.root, texts)
        self.assertTrue(any("cycle" in e for e in errors))
        self.assertTrue(any("phase" in e for e in errors))
        self.assertTrue(any("store missing" in e for e in errors))
        texts[root + "index.md"] = "| file | work | check |\n|---|---|---|"
        self.assertTrue(any("Missing table schema" in e for e in g.typed_records(self.root, texts)))

    def test_decision_body_cannot_substitute_for_required_frontmatter(self):
        texts = self.source_texts()
        path = g.BASE + "/decisions/2026-09/2026-09-16-choice-example.md"
        texts[path] = "---\nscope: project\n---\nclass: choice\nsubject: AGENTS.md\nanchor: request\ndecided: A choice\n"
        self.assertTrue(any("frontmatter" in e for e in g.typed_records(self.root, texts)))
        texts[path] = "---\nscope: project\nclass: choice\nsubject: AGENTS.md\nanchor: user request\nsupersedes: 2026-09-15-choice-missing\n---\ndecided: Kept project content\n"
        self.assertTrue(any("supersedes missing" in e for e in g.typed_records(self.root, texts)))
        texts[path] = texts[path].replace("supersedes: 2026-09-15-choice-missing\n", "")
        self.assertEqual(g.typed_records(self.root, texts), [])

    def test_wiki_checks_declared_classes_identifiers_and_sourced_evidence(self):
        texts = self.source_texts()
        wiki = g.BASE + "/wiki/"
        texts[wiki + "index.md"] = "---\nscope: project\nactive: true\n---\n[Topic](subject/topic.md)\n\n| class | required evidence |\n|---|---|\n| fact | Source locator |\n"
        texts[wiki + "subject/topic.md"] = "---\nscope: project\n---\n| id | claim | class | confidence | evidence |\n|---|---|---|---|---|\n| F1 | Claim | fact | sourced | — |\n| F1 | Claim two | unknown | sourced | locator |\n"
        errors = g.typed_records(self.root, texts)
        self.assertTrue(any("no evidence" in e for e in errors))
        self.assertTrue(any("Duplicate" in e for e in errors))
        self.assertTrue(any("Invalid wiki" in e for e in errors))
        texts[wiki + "subject/topic.md"] = texts[wiki + "subject/topic.md"].replace("sourced | —", "hypothesis | —").replace("F1 | Claim two | unknown", "F2 | Claim two | fact")
        self.assertEqual(g.typed_records(self.root, texts), [])

    def test_guide_router_cycles_do_not_make_orphan_areas_reachable(self):
        with tempfile.TemporaryDirectory(prefix="codex-router-") as directory:
            root = Path(directory)
            for name, content in self.source_texts().items():
                put(root / name, content)
            put(root / g.BASE / "guide/a/index.md", "---\nscope: project\n---\n`../b/index.md`\n")
            put(root / g.BASE / "guide/b/index.md", "---\nscope: project\n---\n`../a/index.md`\n`leaf.md`\n")
            put(root / g.BASE / "guide/b/leaf.md", "---\nscope: portable\n---\n# Leaf\n")
            errors = g.verify(root)["errors"]
            self.assertTrue(any("Guide not routed" in e and "guide/b/leaf.md" in e for e in errors))

    def test_gate_detects_missing_extra_and_out_of_scope_files(self):
        with tempfile.TemporaryDirectory(prefix="codex-gate-") as directory:
            root = Path(directory)
            put(root / "AGENTS.md", g.BEGIN + "\nRead `.agent-workspace/guide/index.md`. Read `.agent-workspace/guide/roles/index.md`. Read `.agent-workspace/lessons/index.md`.\n" + g.END)
            for name in ("guide/index.md", "guide/roles/index.md", "lessons/index.md", "decisions/index.md", "wiki/index.md"):
                put(root / g.BASE / name, "---\nscope: project\n---\n# Empty router\n")
            put(root / ".claude/rules/broken.md", "`missing.md`")
            baseline = g.verify(root)["errors"]
            self.assertTrue(any("Missing core file" in e for e in baseline))
            self.assertFalse(any(".claude" in e for e in baseline))
            put(root / g.BASE / "guide/general/new.md", "---\nscope: portable\n---\n# Guide\n`missing.md`\n")
            put(root / g.BASE / "lessons/new.md", "---\nscope: project\n---\n# Lesson\n")
            errors = g.verify(root)["errors"]
            self.assertTrue(any("not routed" in e for e in errors))
            self.assertTrue(any("Broken Markdown" in e for e in errors))


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex-maintenance-")
        self.root = Path(self.temp.name)
        self.package = self.root / "standalone skill"
        shutil.copytree(SKILL, self.package, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        self.rule = g.BASE + "/rules/critical-thinking.md"
        # Every test receives only the skill. No repository or live authoring tree exists.
        self.assertEqual(g.maintenance(self.package, "refresh", True)["status"], "complete")

    def tearDown(self):
        self.temp.cleanup()

    def test_direct_source_and_template_edits_refresh_only_metadata(self):
        for relative in ("portable/" + self.rule, "templates/AGENTS.md"):
            path = self.package / "bundle" / relative
            put(path, path.read_bytes() + b"\nA reviewed source change.\n")
        before = snapshot(self.package)
        self.assertEqual(g.maintenance(self.package, "check")["status"], "drift")
        result = g.maintenance(self.package, "refresh")
        self.assertIn(self.rule, result["drift"])
        self.assertIn("AGENTS.md", result["drift"])
        self.assertEqual(snapshot(self.package), before)
        self.assertEqual(g.maintenance(self.package, "refresh", True)["status"], "complete")
        after = snapshot(self.package)
        self.assertEqual([p for p in before if before[p] != after[p]], ["bundle/bundle-map.json"])
        self.assertEqual(g.maintenance(self.package, "check")["status"], "pass")
        self.assertTrue(all("live" not in entry for entry in g.bundle_map(self.package)["files"]))

    def test_optional_source_addition_and_retirement_have_no_second_copy(self):
        extra = g.BASE + "/rules/additional.md"
        path = self.package / ("bundle/portable/" + extra)
        put(path, "---\nscope: portable\n---\n# An additional operational rule\n")
        self.assertEqual(g.maintenance(self.package, "check")["status"], "drift")
        self.assertEqual(g.maintenance(self.package, "refresh", True)["status"], "complete")
        path.unlink()
        result = g.maintenance(self.package, "refresh", True)
        self.assertEqual(result["retired"], [extra])
        self.assertEqual(g.maintenance(self.package, "check")["status"], "pass")

    def test_refresh_refuses_missing_core_unsafe_files_and_unrouted_guides(self):
        rule = self.package / ("bundle/portable/" + self.rule)
        content = rule.read_bytes()
        rule.unlink()
        before = snapshot(self.package)
        with self.assertRaises(g.GenomeError):
            g.maintenance(self.package, "refresh", True)
        self.assertEqual(snapshot(self.package), before)
        put(rule, content)
        extra = self.package / "bundle/portable/unexpected.txt"
        put(extra, "Unowned source")
        with self.assertRaises(g.GenomeError):
            g.maintenance(self.package, "refresh", True)
        extra.unlink()
        extra = self.package / ("bundle/portable/" + g.BASE + "/guide/deployment/task.md")
        put(extra, "---\nscope: portable\n---\n# A guide without a router\n")
        before = snapshot(self.package)
        result = g.maintenance(self.package, "refresh", True)
        self.assertEqual(result["status"], "fail")
        self.assertTrue(any("Guide not routed" in e for e in result["errors"]))
        self.assertEqual(snapshot(self.package), before)

    def test_refresh_refuses_missing_template_and_linked_source(self):
        template = self.package / "bundle/templates/wiki-index.md"
        content = template.read_bytes()
        template.unlink()
        with self.assertRaises(g.GenomeError):
            g.maintenance(self.package, "refresh", True)
        put(template, content)
        outside = self.root / "outside.md"
        put(outside, "---\nscope: portable\n---\n# Outside source\n")
        linked = self.package / ("bundle/portable/" + g.BASE + "/rules/linked.md")
        os.link(outside, linked)
        with self.assertRaises(g.GenomeError):
            g.maintenance(self.package, "refresh", True)
        self.assertEqual(outside.read_bytes(), b"---\nscope: portable\n---\n# Outside source\n")

    def test_skill_version_is_canonical_and_refresh_records_it(self):
        put(self.package / "VERSION", "1.2.3\n")
        before = snapshot(self.package)
        self.assertFalse(g.maintenance(self.package, "check")["version_matches"])
        self.assertEqual(snapshot(self.package), before)
        g.maintenance(self.package, "refresh", True)
        self.assertEqual(g.bundle_map(self.package)["version"], "1.2.3")
        put(self.package / "VERSION", "not a release\n")
        with self.assertRaises(g.GenomeError):
            g.maintenance(self.package, "refresh", True)

    def test_version_prerelease_build_and_leading_zero_boundaries(self):
        put(self.package / "VERSION", "1.2.3-rc.1+build.7\n")
        result = g.maintenance(self.package, "refresh", True)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(g.bundle_map(self.package)["version"], "1.2.3-rc.1+build.7")
        self.assertEqual(g.maintenance(self.package, "check")["status"], "pass")
        for version in ("01.2.3", "1.02.3", "1.2.03"):
            with self.subTest(version=version):
                put(self.package / "VERSION", version + "\n")
                before = snapshot(self.package)
                with self.assertRaises(g.GenomeError):
                    g.maintenance(self.package, "refresh", True)
                self.assertEqual(snapshot(self.package), before)

    def test_absent_core_metadata_can_be_rebuilt_only_with_actual_core_payload(self):
        mapping = g.bundle_map(self.package)
        mapping["files"] = [entry for entry in mapping["files"] if entry["path"] != self.rule]
        put(self.package / "bundle/bundle-map.json", g.encoded(mapping))
        self.assertEqual(g.maintenance(self.package, "check")["status"], "drift")
        self.assertEqual(g.maintenance(self.package, "refresh", True)["status"], "complete")
        self.assertIn(self.rule, {entry["path"] for entry in g.bundle_map(self.package)["files"]})
        put(self.package / "bundle/bundle-map.json", g.encoded(mapping))
        (self.package / ("bundle/portable/" + self.rule)).unlink()
        before = snapshot(self.package)
        with self.assertRaises(g.GenomeError):
            g.maintenance(self.package, "refresh", True)
        self.assertEqual(snapshot(self.package), before)

    def test_copied_skill_cli_initializes_updates_and_verifies_without_repository(self):
        wrapper = self.package / "scripts/genome.py"
        project = self.root / "Dự án độc lập"
        project.mkdir()
        def run(*args):
            result = subprocess.run([sys.executable, str(wrapper), *args], cwd=project, capture_output=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return json.loads(result.stdout)
        self.assertEqual(run("check")["status"], "pass")
        plan = run("init", "--project", str(project))
        run("init", "--project", str(project), "--apply", "--plan-hash", plan["plan_hash"])
        self.assertEqual(run("verify", "--project", str(project))["status"], "pass")
        rule = self.package / ("bundle/portable/" + self.rule)
        put(rule, rule.read_bytes() + b"\nA revised source rule.\n")
        run("refresh", "--apply")
        plan = run("update", "--project", str(project))
        run("update", "--project", str(project), "--apply", "--plan-hash", plan["plan_hash"])
        self.assertEqual((project / self.rule).read_bytes(), rule.read_bytes())
        self.assertEqual(run("verify", "--project", str(project))["status"], "pass")
        for args in (("promote",), ("verify", "--source-root", str(project))):
            result = subprocess.run([sys.executable, str(wrapper), *args], cwd=project, capture_output=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
