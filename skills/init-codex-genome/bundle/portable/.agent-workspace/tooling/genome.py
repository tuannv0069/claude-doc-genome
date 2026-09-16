#!/usr/bin/env python3
"""Codex adapter deployment for the shared project genome. Standard library only."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile

PRODUCT = "codex-genome"
BASE = ".agent-workspace"
MANIFEST = ".codex/genome-manifest.json"
LOCK = ".codex/genome-update-lock.json"
JOURNAL = ".codex/genome-update-journal.json"
BEGIN = "<!-- codex-genome:begin -->"
END = "<!-- codex-genome:end -->"
IGNORE_BEGIN = "# codex-genome:begin"
IGNORE_END = "# codex-genome:end"
RESERVED = re.compile(r"^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?$", re.I)
CORE_RULES = ("agents-md-standards", "codex-agents-standards", "codex-config-standards", "critical-thinking", "doc-organization", "file-reading", "skill-md-standards", "wiki-tier")
CORE_GUIDES = ("bug-report-format", "capability-packaging", "decision-journal", "doc-system-mechanics", "five-why", "fix-impact-analysis", "lesson-capture", "markdown", "mermaid", "orchestration-policy", "review-checklist-method", "role-selection", "rule-health", "task-planning", "verification-gate-design", "worktree")
CORE_ROLES = ("business-analyst", "comtor", "developer", "project-manager", "qa", "security", "tech-lead")
SHARED_PREFIXES = tuple(BASE + "/" + name + "/" for name in ("guide", "lessons", "decisions", "wiki"))
SHARED_ROUTERS = tuple(BASE + "/" + name for name in (
    "guide/index.md", "guide/roles/index.md", "lessons/index.md", "decisions/index.md", "wiki/index.md"
))
SHARED_REQUIRED_ROUTERS = SHARED_ROUTERS[:-1]


class GenomeError(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest() if data is not None else None


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"


def read(path):
    return path.read_bytes() if path.exists() else None


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (ValueError, OSError) as exc:
        raise GenomeError(f"Cannot read JSON {path}: {exc}") from exc


def check_node(path):
    if not path.exists() and not path.is_symlink():
        return
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
        raise GenomeError(f"Symbolic links and reparse points are not supported: {path}")
    if path.is_file() and info.st_nlink != 1:
        raise GenomeError(f"Hard-linked files are not supported: {path}")


def root_path(value):
    path = Path(os.path.abspath(value))
    for ancestor in reversed((path, *path.parents)):
        check_node(ancestor)
    if not path.is_dir():
        raise GenomeError(f"Root must already be a directory: {path}")
    if os.name == "nt" and str(path.resolve()).casefold() != str(path).casefold():
        raise GenomeError(f"Root uses a filesystem alias; provide its canonical path: {path.resolve()}")
    return path


def relative(value):
    if not isinstance(value, str) or "\\" in value:
        raise GenomeError(f"Use a relative forward-slash path: {value!r}")
    parts = value.split("/")
    if not value or PurePosixPath(value).is_absolute() or any(
        not p or p in (".", "..") or p[-1:] in (" ", ".") or
        any(c in p for c in ':<>"|?*') or any(ord(c) < 32 for c in p) or
        "~" in p or RESERVED.match(p) for p in parts
    ):
        raise GenomeError(f"Unsafe or aliased relative path: {value!r}")
    return parts


def safe(root, value):
    path = root
    for part in relative(value):
        if path.is_dir():
            aliases = [p.name for p in path.iterdir() if p.name.casefold() == part.casefold()]
            if aliases and aliases != [part]:
                raise GenomeError(f"Case alias for {value}: {aliases}")
        path = path / part
        check_node(path)
    return path


def allowed(value):
    relative(value)
    if value in ("AGENTS.md", ".gitignore", MANIFEST, LOCK, JOURNAL):
        return
    if not value.startswith(BASE + "/"):
        raise GenomeError(f"Path is outside Codex ownership: {value}")
    if value.startswith((BASE + "/tasks/", BASE + "/worktrees/")):
        raise GenomeError(f"Working data cannot be bundled: {value}")


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    check_node(path)
    fd, temporary = tempfile.mkstemp(prefix=".codex-write-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def package_path(value=None):
    if value:
        root = root_path(value)
        if not safe(root, "bundle/bundle-map.json").is_file():
            raise GenomeError("--package-root must be the init-codex-genome skill directory")
        return root
    for parent in Path(__file__).resolve().parents:
        if (parent / "bundle/bundle-map.json").is_file():
            return root_path(parent)
    raise GenomeError("Cannot locate package; provide --package-root")


def bundle_map(package):
    data = load(safe(package, "bundle/bundle-map.json"))
    if data.get("schema_version") != 1 or data.get("product") != PRODUCT:
        raise GenomeError("Unsupported bundle map")
    if not isinstance(data.get("version"), str) or not isinstance(data.get("files"), list):
        raise GenomeError("Bundle version and file array are required")
    seen = set()
    for entry in data["files"]:
        path = entry.get("path", "")
        allowed(path)
        if path in (MANIFEST, LOCK, JOURNAL):
            raise GenomeError(f"Bookkeeping path cannot be bundled: {path}")
        if path.casefold() in seen:
            raise GenomeError(f"Duplicate bundle target: {path}")
        seen.add(path.casefold())
        if entry.get("kind") not in ("portable", "seed", "region"):
            raise GenomeError(f"Unknown ownership kind: {path}")
        if (path == "AGENTS.md") != (entry["kind"] == "region") or path == ".gitignore":
            raise GenomeError("Only AGENTS.md can be a bundle region; ignore rules are generated")
        source = entry.get("source", "")
        if not source.startswith(("portable/", "templates/")):
            raise GenomeError(f"Invalid bundle source: {source}")
        safe(package, "bundle/" + source)
    if "agents.md" not in seen:
        raise GenomeError("Bundle must include the AGENTS.md region")
    return data


def extract_region(data, begin=BEGIN, end=END):
    text = (data or b"").decode("utf-8-sig")
    if not text.count(begin) and not text.count(end):
        return None
    if text.count(begin) != 1 or text.count(end) != 1 or text.index(begin) > text.index(end):
        raise GenomeError("Managed region markers are malformed or duplicated")
    return text[text.index(begin):text.index(end) + len(end)].encode("utf-8")


def replace_region(data, region, begin=BEGIN, end=END):
    old = extract_region(data, begin, end)
    if old is None:
        prefix = data or b""
        return prefix + (b"\n" if prefix and not prefix.endswith(b"\n") else b"") + region + b"\n"
    return data[:data.index(begin.encode())] + region + data[data.index(end.encode()) + len(end.encode()):]


def manifest(root):
    path = safe(root, MANIFEST)
    if not path.exists():
        return None
    result = load(path)
    if result.get("product") != PRODUCT or result.get("schema_version") != 1 or result.get("status") != "complete":
        raise GenomeError("Unsupported or incomplete project manifest")
    if result.get("shared_workspace", "managed") not in ("managed", "reused"):
        raise GenomeError("Unsupported shared workspace ownership mode")
    for name, entry in result.get("files", {}).items():
        allowed(name)
        if name in (MANIFEST, LOCK, JOURNAL):
            raise GenomeError(f"Manifest cannot own its bookkeeping path: {name}")
        if entry.get("kind") not in ("portable", "seed", "region", "ignore-region"):
            raise GenomeError(f"Unsupported manifest ownership: {name}")
        if entry["kind"] == "region" and name != "AGENTS.md":
            raise GenomeError("Invalid region ownership")
        if entry["kind"] == "ignore-region" and name != ".gitignore":
            raise GenomeError("Invalid ignore ownership")
    return result


def legacy_inventory(root):
    observations, owners, writers = {}, set(), []
    legacy = safe(root, ".claude/init-manifest.json")
    if legacy.is_file():
        observations[".claude/init-manifest.json"] = digest(legacy.read_bytes())
        manifest_data = load(legacy)
        for roster in (manifest_data.get("files", []), manifest_data.get("templates", [])):
            if isinstance(roster, dict):
                owners.update(str(key).replace("\\", "/") for key in roster)
            elif isinstance(roster, list):
                owners.update(item["path"].replace("\\", "/") for item in roster if isinstance(item, dict) and isinstance(item.get("path"), str))
        def visit(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    if isinstance(key, str) and ("/" in key or key == "AGENTS.md"):
                        owners.add(key.replace("\\", "/"))
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)
            elif isinstance(value, str) and ("/" in value or value == "AGENTS.md"):
                owners.add(value.replace("\\", "/"))
        visit(manifest_data)
    candidates = [root / "package.json"]
    for folder in (".claude", ".codex", ".agents", "scripts", ".agent-workspace/tooling"):
        parent = safe(root, folder)
        if parent.is_dir():
            for directory, dirs, files in os.walk(parent, followlinks=False):
                dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "bundle")]
                for d in dirs:
                    check_node(Path(directory) / d)
                candidates.extend(Path(directory) / f for f in files if Path(f).suffix in (".md", ".json", ".toml", ".py", ".ps1", ".sh", ".mjs", ".js"))
    for file in candidates:
        if not file.is_file():
            continue
        rel = file.relative_to(root).as_posix()
        if file.name == "render_codex.py" or rel == BASE + "/tooling/genome.py":
            continue
        safe(root, rel)
        content = file.read_bytes()
        if b"render_codex.py" in content:
            observations[rel] = digest(content)
            writers.append(rel)
    return {"owned_paths": sorted(owners), "renderer_references": sorted(writers), "observations": observations}


def required_bundle(files):
    declared = {entry["path"]: entry for entry in files}
    required = {f"{BASE}/{folder}/{name}.md" for folder, names in (("rules", CORE_RULES), ("guide/general", CORE_GUIDES), ("guide/roles", CORE_ROLES)) for name in names}
    required.add(BASE + "/tooling/genome.py")
    for name in sorted(required):
        if name not in declared or declared[name]["kind"] != "portable":
            raise GenomeError(f"Incomplete core bundle: {name}")
    for router in ("guide/index.md", "guide/roles/index.md", "lessons/index.md", "decisions/index.md", "wiki/index.md"):
        if declared.get(BASE + "/" + router, {}).get("kind") != "seed":
            raise GenomeError(f"Missing project router template: {router}")


def deployment_plan(root, package, mode, adoption=None):
    mapping = bundle_map(package)
    required_bundle(mapping["files"])
    prior = manifest(root)
    if mode == "init" and prior:
        raise GenomeError("Already initialized; use update")
    if mode == "update" and not prior:
        raise GenomeError("No Codex manifest; use init")
    if safe(root, JOURNAL).exists():
        raise GenomeError("Unfinished update exists; run recover before planning another update")
    old = prior.get("files", {}) if prior else {}
    inventory = legacy_inventory(root)
    conflicts = [f"Legacy renderer reference requires separate reviewed migration: {p}" for p in inventory["renderer_references"]]
    warnings = []
    observations = {MANIFEST: digest(read(safe(root, MANIFEST))), **inventory["observations"]}
    shared_expected = set(SHARED_REQUIRED_ROUTERS)
    shared_expected.update(f"{BASE}/guide/general/{name}.md" for name in CORE_GUIDES)
    shared_expected.update(f"{BASE}/guide/roles/{name}.md" for name in CORE_ROLES)
    shared_existing = {name for name in shared_expected if safe(root, name).is_file()}
    reuse_shared = (mode == "init" and shared_existing == shared_expected) or (
        mode == "update" and prior.get("shared_workspace") == "reused"
    )
    if (mode == "init" and shared_existing or reuse_shared) and shared_existing != shared_expected:
        missing = ", ".join(sorted(shared_expected - shared_existing))
        conflicts.append("Existing shared genome workspace is incomplete; resolve its ownership and missing files before adding the Codex adapter: " + missing)
    if reuse_shared:
        warnings.append("Reusing the existing shared genome workspace; Codex will add only its adapter instructions, standards and tooling.")
    for override in ("AGENTS.override.md",):
        data = read(safe(root, override))
        observations[override] = digest(data)
        if data:
            conflicts.append(f"{override} overrides the root AGENTS.md; resolve its integration explicitly before installation")
    for directory, dirs, filenames in os.walk(root, followlinks=False):
        dirs[:] = [name for name in dirs if name not in (".git", "node_modules", ".venv", "venv", ".agent-workspace", ".claude", ".agents", ".codex", "vendor", "dist", "build")]
        for name in list(dirs):
            child = Path(directory) / name
            if child.is_symlink() or getattr(child.lstat(), "st_file_attributes", 0) & 0x400:
                dirs.remove(name)
                warnings.append(f"Nested instruction discovery skipped linked directory: {child.relative_to(root).as_posix()}")
        if Path(directory) == root:
            continue
        for name in ("AGENTS.md", "AGENTS.override.md"):
            if name in filenames:
                path = (Path(directory) / name).relative_to(root).as_posix()
                observations[path] = digest(safe(root, path).read_bytes())
                warnings.append(f"Nested instructions affect sessions started in this subtree; review separately: {path}")
    changes, next_files = [], {}
    def propose(path, before, after, kind):
        observations[path] = digest(before)
        if before != after:
            changes.append({"path": path, "action": "delete" if after is None else "write", "before_sha256": digest(before), "after_sha256": digest(after), "content_base64": base64.b64encode(after).decode() if after is not None else None})
    for entry in mapping["files"]:
        name, kind = entry["path"], entry["kind"]
        target = safe(root, name)
        before = read(target)
        observations[name] = digest(before)
        source = safe(package, "bundle/" + entry["source"]).read_bytes()
        previous = old.get(name)
        review = (adoption or {}).get(name, {})
        reviewed_replacement = review.get("replace_from_bundle") is True and review.get("before_sha256") == digest(before) and review.get("accept_source_sha256") == digest(source)
        if reuse_shared and name.startswith(SHARED_PREFIXES) and previous is None and before is not None:
            continue
        if name in inventory["owned_paths"]:
            conflicts.append(f"Another installer owns {name}; review ownership before Codex adopts it")
            continue
        if previous and previous["kind"] != kind:
            conflicts.append(f"Ownership kind changed for {name}; manual migration required")
            continue
        if kind == "seed":
            if previous and previous.get("source_sha256") != digest(source):
                reviewed = (adoption or {}).get(name, {})
                if reviewed.get("before_sha256") != digest(before) or reviewed.get("accept_template_sha256") != digest(source):
                    conflicts.append(f"Changed template needs review and exact before/source hash acknowledgment: {name}")
                    continue
            after = source if before is None else before
            next_files[name] = {"kind": kind, "sha256": digest(after), "source_sha256": digest(source)}
        elif kind == "region":
            desired = BEGIN.encode() + b"\n" + source.strip() + b"\n" + END.encode()
            region = extract_region(before)
            if previous:
                if digest(region) != previous["sha256"] and not reviewed_replacement:
                    conflicts.append(f"Locally edited AGENTS managed region: {name}")
                    continue
                after = replace_region(before, desired)
            elif before:
                record = (adoption or {}).get("AGENTS.md")
                if not record or record.get("before_sha256") != digest(before) or not isinstance(record.get("replacement"), str):
                    conflicts.append("Existing AGENTS.md needs reviewed adoption with its exact hash and replacement text")
                    continue
                replacement = record["replacement"].encode("utf-8")
                if extract_region(replacement) is not None:
                    conflicts.append("Adoption replacement must contain only retained project content, without managed markers")
                    continue
                after = replace_region(replacement, desired)
            else:
                after = replace_region(before, desired)
            next_files[name] = {"kind": kind, "sha256": digest(desired), "source_sha256": digest(source)}
        else:
            if previous and digest(before) != previous["sha256"] and not reviewed_replacement:
                conflicts.append(f"Locally edited or missing owned file: {name}")
                continue
            if not previous and before is not None:
                conflicts.append(f"Unowned file already exists: {name}")
                continue
            after = source
            next_files[name] = {"kind": kind, "sha256": digest(after), "source_sha256": digest(source)}
        propose(name, before, after, kind)
    ignore = ".gitignore"
    before = read(safe(root, ignore))
    observations[ignore] = digest(before)
    desired = (IGNORE_BEGIN + "\n/" + BASE + "/tasks/\n/" + BASE + "/worktrees/\n/" + LOCK + "\n/" + JOURNAL + "\n" + IGNORE_END).encode()
    current = extract_region(before, IGNORE_BEGIN, IGNORE_END)
    if ignore in inventory["owned_paths"]:
        conflicts.append("Claude manifest owns .gitignore; Codex cannot add or update its region")
    elif current is not None and (ignore not in old or digest(current) != old[ignore]["sha256"]):
        conflicts.append("Unowned or locally edited .gitignore managed region")
    else:
        propose(ignore, before, replace_region(before, desired, IGNORE_BEGIN, IGNORE_END), "ignore-region")
        next_files[ignore] = {"kind": "ignore-region", "sha256": digest(desired)}
    for name, entry in old.items():
        if name in next_files or name in {e["path"] for e in mapping["files"]} or name == ignore:
            continue
        before = read(safe(root, name))
        observations[name] = digest(before)
        if entry["kind"] == "seed":
            warnings.append(f"Retired project-owned seed retained: {name}")
            continue
        if name in inventory["owned_paths"] or entry["kind"] != "portable" or digest(before) != entry["sha256"]:
            conflicts.append(f"Retired file has changed or ownership is unsafe: {name}")
        else:
            propose(name, before, None, entry["kind"])
    result_manifest = {"schema_version": 1, "product": PRODUCT, "version": mapping["version"], "status": "complete", "shared_workspace": "reused" if reuse_shared else "managed", "modules": ["core"], "provenance": {"bundle_sha256": digest(encoded(mapping))}, "unresolved": [], "files": next_files}
    if not conflicts:
        propose(MANIFEST, read(safe(root, MANIFEST)), encoded(result_manifest), "manifest")
    result = {"schema_version": 1, "product": PRODUCT, "operation": mode, "project": str(root), "version": mapping["version"], "changes": changes, "conflicts": conflicts, "warnings": warnings, "observations": observations, "legacy": inventory}
    result["plan_hash"] = digest(encoded(result))
    return result


def lock(root):
    path = safe(root, LOCK)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid()}, stream)
    except FileExistsError as exc:
        raise GenomeError("Another update or stale lock exists; inspect recovery before continuing") from exc
    return path


def apply_plan(root, plan, expected_hash, fail_after=None):
    if not expected_hash or plan["plan_hash"] != expected_hash:
        raise GenomeError("Plan changed or --plan-hash missing; review a fresh dry run")
    if plan["conflicts"]:
        raise GenomeError("Plan has conflicts; no files were applied")
    if not plan["changes"]:
        return {"status": "unchanged", "plan_hash": expected_hash}
    guard = lock(root)
    try:
        for name, expected in plan["observations"].items():
            if digest(read(safe(root, name))) != expected:
                raise GenomeError(f"File changed after planning: {name}")
        entries = []
        for change in plan["changes"]:
            before = read(safe(root, change["path"]))
            entries.append({**change, "before_base64": base64.b64encode(before).decode() if before is not None else None})
        journal = {"schema_version": 1, "product": PRODUCT, "project": str(root), "plan_hash": expected_hash, "entries": entries}
        atomic(safe(root, JOURNAL), encoded(journal))
        for index, entry in enumerate(entries, 1):
            target = safe(root, entry["path"])
            if digest(read(target)) != entry["before_sha256"]:
                raise GenomeError(f"Concurrent modification: {entry['path']}")
            if entry["action"] == "delete":
                target.unlink()
            else:
                atomic(target, base64.b64decode(entry["content_base64"]))
            if fail_after == index:
                raise GenomeError("Injected interruption for recovery verification")
        safe(root, JOURNAL).unlink()
        return {"status": "complete", "version": plan["version"], "changed": len(entries), "warnings": plan["warnings"], "plan_hash": expected_hash}
    finally:
        guard.unlink(missing_ok=True)


def process_alive(pid):
    if os.name == "nt":
        import ctypes
        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
        if not handle:
            return False
        code = ctypes.c_ulong()
        try:
            return not ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(code)) or code.value == 259
        finally:
            ctypes.windll.kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def recovery(root, apply=False, expected=None):
    journal_path = safe(root, JOURNAL)
    lock_path = safe(root, LOCK)
    if lock_path.exists() and process_alive(load(lock_path).get("pid", 0)):
        raise GenomeError("Update lock belongs to a running process")
    journal = load(journal_path) if journal_path.exists() else None
    if journal is not None and (not isinstance(journal, dict) or journal.get("schema_version") != 1 or journal.get("product") != PRODUCT or journal.get("project") != str(root) or not isinstance(journal.get("entries"), list)):
        raise GenomeError("Recovery journal belongs to another project")
    observations = {}
    for entry in (journal or {}).get("entries", []):
        name = entry["path"]
        if name in observations or entry.get("action") not in ("write", "delete"):
            raise GenomeError("Recovery journal has duplicate paths or an invalid action")
        if name != MANIFEST:
            allowed(name)
        for key, hash_key in (("before_base64", "before_sha256"), ("content_base64", "after_sha256")):
            payload = entry[key]
            content = base64.b64decode(payload, validate=True) if isinstance(payload, str) else None
            if payload is not None and not isinstance(payload, str) or digest(content) != entry[hash_key]:
                raise GenomeError(f"Recovery payload hash mismatch: {name}")
        if (entry["action"] == "delete") != (entry["content_base64"] is None):
            raise GenomeError("Recovery action disagrees with its payload")
        value = digest(read(safe(root, name)))
        if value not in (entry["before_sha256"], entry["after_sha256"]):
            raise GenomeError(f"Recovery would overwrite a subsequent edit: {name}")
        observations[name] = value
    result = {"operation": "recover", "project": str(root), "journal_sha256": digest(read(journal_path)), "lock_sha256": digest(read(lock_path)), "observations": observations, "entries": len((journal or {}).get("entries", []))}
    result["plan_hash"] = digest(encoded(result))
    if not apply:
        return result
    if expected != result["plan_hash"]:
        raise GenomeError("Review recovery dry run and pass its --plan-hash")
    if lock_path.exists():
        lock_path.unlink()
    guard = lock(root)
    try:
        for entry in reversed((journal or {}).get("entries", [])):
            target = safe(root, entry["path"])
            if digest(read(target)) != observations[entry["path"]]:
                raise GenomeError("Concurrent modification during recovery")
            before = entry["before_base64"]
            if before is None:
                target.unlink(missing_ok=True)
            else:
                atomic(target, base64.b64decode(before))
        journal_path.unlink(missing_ok=True)
    finally:
        guard.unlink(missing_ok=True)
    return {"status": "recovered", "restored": result["entries"]}


def owned_files(root, folder):
    """Inventory source files without following aliases or runtime bytecode caches."""
    base = safe(root, folder)
    if base.is_dir():
        for directory, dirs, files in os.walk(base, followlinks=False):
            for name in dirs:
                check_node(Path(directory) / name)
            dirs[:] = [name for name in dirs if name != "__pycache__"]
            for name in files:
                file = Path(directory) / name
                safe(root, file.relative_to(root).as_posix())
                yield file


def refreshed_map(package):
    """Describe the authored skill payload; there is no second source tree."""
    version = safe(package, "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", version):
        raise GenomeError("Skill VERSION must contain a semantic release version")
    files = [{"path": "AGENTS.md", "kind": "region", "source": "templates/AGENTS.md"}]
    for short, target in (("guide", "guide"), ("roles", "guide/roles"), ("lessons", "lessons"), ("decisions", "decisions"), ("wiki", "wiki")):
        files.append({"path": f"{BASE}/{target}/index.md", "kind": "seed", "source": f"templates/{short}-index.md"})
    expected_templates = {"bundle/" + entry["source"] for entry in files}
    actual_templates = {p.relative_to(package).as_posix() for p in owned_files(package, "bundle/templates")}
    if actual_templates != expected_templates:
        raise GenomeError("Template inventory differs: " + ", ".join(sorted(actual_templates ^ expected_templates)))
    for file in sorted(owned_files(package, "bundle/portable")):
        path = file.relative_to(package / "bundle/portable").as_posix()
        allowed(path)
        if file.suffix == ".md" and path.startswith((BASE + "/rules/", BASE + "/guide/")):
            if metadata(file.read_text(encoding="utf-8-sig")).get("scope") != "portable":
                raise GenomeError(f"Authored portable Markdown requires scope: portable: {path}")
        elif not (file.suffix == ".py" and path.startswith(BASE + "/tooling/")):
            raise GenomeError(f"Unsupported authored payload file: {path}")
        files.append({"path": path, "kind": "portable", "source": "portable/" + path})
    seen = set()
    for entry in files:
        key = entry["path"].casefold()
        if key in seen:
            raise GenomeError(f"Duplicate authored target: {entry['path']}")
        seen.add(key)
        entry["sha256"] = digest(safe(package, "bundle/" + entry["source"]).read_bytes())
    required_bundle(files)
    return {"schema_version": 1, "product": PRODUCT, "version": version, "files": files}


def materialized_verification(package, mapping):
    """Check the project contract produced by these sources without changing a project."""
    with tempfile.TemporaryDirectory(prefix="codex-source-check-") as directory:
        root = Path(directory)
        for entry in mapping["files"]:
            content = safe(package, "bundle/" + entry["source"]).read_bytes()
            if entry["kind"] == "region":
                content = BEGIN.encode() + b"\n" + content.strip() + b"\n" + END.encode()
            atomic(safe(root, entry["path"]), content)
        return verify(root)


def maintenance(package, command, apply=False):
    package = package_path(package)
    previous = bundle_map(package)
    mapping = refreshed_map(package)
    verification = materialized_verification(package, mapping)
    before = {entry["path"]: entry for entry in previous["files"]}
    after = {entry["path"]: entry for entry in mapping["files"]}
    changes = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
    retired = sorted(set(before) - set(after))
    version_matches = previous["version"] == mapping["version"]
    result = {"operation": command, "drift": changes, "retired": retired,
              "version_matches": version_matches, "verification": verification}
    if verification["status"] != "pass":
        return {**result, "status": "fail", "errors": verification["errors"]}
    differs = previous != mapping
    if command == "refresh" and apply:
        atomic(safe(package, "bundle/bundle-map.json"), encoded(mapping))
        return {**result, "status": "complete", "changed": changes}
    return {**result, "status": "drift" if differs else "pass"}


def markdown_files(root):
    result = []
    agents = safe(root, "AGENTS.md")
    if agents.is_file():
        result.append(agents)
    for folder in ("rules", "guide", "lessons", "decisions", "wiki"):
        directory = safe(root, f"{BASE}/{folder}")
        if directory.is_dir():
            for path, dirs, files in os.walk(directory, followlinks=False):
                for name in dirs:
                    check_node(Path(path) / name)
                for name in files:
                    if name.endswith(".md"):
                        file = Path(path) / name
                        safe(root, file.relative_to(root).as_posix())
                        result.append(file)
    return result


def metadata(text):
    match = re.match(r"^---\s*\n(.*?)\n---(?:\n|$)", text, re.S)
    return {key: value.strip().strip("\"'") for key, value in re.findall(r"^([a-z_]+):[ \t]*([^\n]*)$", match[1] if match else "", re.M)}


def table_rows(text, header):
    rows, active, found = [], False, 0
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            active = False
            continue
        cells = [v.strip().strip("`") for v in line.strip().strip("|").split("|")]
        if cells == header:
            active, found = True, found + 1
        elif active and not all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            if len(cells) != len(header):
                raise GenomeError("Malformed table row for " + ", ".join(header))
            rows.append(cells)
    return found, rows


def typed_records(root, texts):
    errors = []
    def table(name, columns, required=True):
        try:
            count, rows = table_rows(texts.get(name, ""), columns)
            if required and not count:
                errors.append(f"Missing table schema in {name}: {columns}")
            return rows
        except GenomeError as exc:
            errors.append(f"{name}: {exc}")
            return []
    def cycle(graph, label):
        def visit(node, stack, done):
            if node in stack:
                errors.append(f"{label} cycle: {node}")
                return
            if node in done:
                return
            stack.add(node)
            for target in graph.get(node, []):
                visit(target, stack, done)
            stack.remove(node)
            done.add(node)
        done = set()
        for node in graph:
            visit(node, set(), done)
    role_rows = table(BASE + "/guide/roles/index.md", ["work type", "primary role", "checking roles"])
    for name, text in texts.items():
        if name.startswith(BASE + "/guide/roles/") and not name.endswith("/index.md"):
            if not re.search(r"^## §6(?:\s|$)", text, re.M):
                errors.append(f"Role completion section missing: {name} §6")
    lesson_root = BASE + "/lessons/"
    lessons = table(lesson_root + "index.md", ["file", "work type", "paired guide", "checks"])
    graph, registered = {}, set()
    for name, work, paired, checks in lessons:
        path = lesson_root + name
        if name in registered or not work:
            errors.append(f"Duplicate lesson or empty work type: {name}")
        registered.add(name)
        if path not in texts:
            errors.append(f"Registered lesson store missing: {name}")
        targets = [p.strip().strip("`") for p in checks.split(",") if p.strip().strip("`") not in ("", "—", "-")]
        graph[name] = targets
        if paired not in ("", "—", "-"):
            pointer = paired.split("§")[0].strip().strip("`").strip()
            if not (root / pointer).is_file() and not (root / lesson_root / pointer).is_file():
                errors.append(f"Paired guide missing: {name} -> {paired}")
    for name, targets in graph.items():
        for target in targets:
            if target not in registered:
                errors.append(f"Lesson checking reference is not registered: {name} -> {target}")
    cycle(graph, "Lesson checking")
    phases = {"writing", "reviewing", "answering", "building-gate", "orchestrating", "investigating", "operating"}
    for name, text in texts.items():
        if name.startswith(lesson_root) and not name.endswith("/index.md"):
            values = metadata(text)
            critical = re.search(r"<critical>(.*?)</critical>", text, re.S)
            details = dict(re.findall(r"^(scope|phase):\s*([^\n]+)", critical[1] if critical else "", re.M))
            phase = values.get("phase", details.get("phase"))
            if phase not in phases:
                errors.append(f"Invalid lesson phase: {name}")
            if not values.get("work_scope") and not details.get("scope"):
                errors.append(f"Lesson protected action scope missing: {name}")
    decisions, graph = {}, {}
    for name, text in texts.items():
        if not name.startswith(BASE + "/decisions/") or name.endswith("/index.md"):
            continue
        values = metadata(text)
        identifier = Path(name).stem
        if identifier in decisions:
            errors.append(f"Duplicate decision identifier: {identifier}")
        decisions[identifier] = name
        category = values.get("class", "")
        if category not in {"choice", "scope", "debt", "rule", "review"} or not re.fullmatch(r"\d{4}-\d{2}-\d{2}-" + re.escape(category) + r"-[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
            errors.append(f"Decision filename/class mismatch: {name}")
        for field in ("subject", "anchor"):
            if not values.get(field):
                errors.append(f"Decision frontmatter field missing: {name} {field}")
        subject = values.get("subject", "").split("§")[0].strip().strip("`")
        if subject:
            try:
                relative(subject)
            except GenomeError:
                errors.append(f"Decision subject is not repository-relative: {name}")
        if not re.search(r"^decided:\s*\S", text, re.M):
            errors.append(f"Decision has no nonempty decided field: {name}")
        graph[identifier] = [values["supersedes"]] if values.get("supersedes") else []
    for identifier, targets in graph.items():
        for target in targets:
            if target not in decisions:
                errors.append(f"Decision supersedes missing identifier: {identifier} -> {target}")
    cycle(graph, "Decision supersession")
    wiki_root = BASE + "/wiki/"
    wiki = texts.get(wiki_root + "index.md", "")
    classes = table(wiki_root + "index.md", ["class", "required evidence"])
    declared = {name: evidence for name, evidence in classes if name and evidence}
    if len(declared) != len(classes):
        errors.append("Wiki classes contain duplicates or missing evidence obligations")
    claims = set()
    for name, text in texts.items():
        if not name.startswith(wiki_root) or name == wiki_root + "index.md":
            continue
        if metadata(wiki).get("active") != "true":
            errors.append(f"Inactive wiki contains a claim cluster: {name}")
        linked = any(os.path.abspath((root / wiki_root) / target) == str(root / name) for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", wiki))
        if not linked:
            errors.append(f"Wiki cluster is not linked from router: {name}")
        try:
            count, rows = table_rows(text, ["id", "claim", "class", "confidence", "evidence"])
        except GenomeError as exc:
            errors.append(f"{name}: {exc}")
            continue
        if count != 1:
            errors.append(f"Wiki cluster requires one claim table: {name}")
        for identifier, claim, category, confidence, evidence in rows:
            if not identifier or identifier in claims:
                errors.append(f"Duplicate or empty wiki claim identifier: {identifier}")
            claims.add(identifier)
            if not claim or category not in declared or confidence not in ("hypothesis", "sourced"):
                errors.append(f"Invalid wiki claim data: {name} {identifier}")
            if confidence == "sourced" and evidence in ("", "—", "-"):
                errors.append(f"Sourced wiki claim has no evidence: {name} {identifier}")
    return errors


def verify(root, health=False):
    errors, notes = [], []
    files = markdown_files(root)
    texts = {p.relative_to(root).as_posix(): p.read_text(encoding="utf-8-sig") for p in files}
    installed = manifest(root) if safe(root, MANIFEST).is_file() else None
    reused_shared = bool(installed and installed.get("shared_workspace") == "reused")
    if not reused_shared:
        errors.extend(typed_records(root, texts))
    if "AGENTS.md" not in texts:
        errors.append("AGENTS.md is missing")
    elif extract_region(read(root / "AGENTS.md")) is None:
        errors.append("AGENTS.md has no Codex managed region")
    for needed in ("guide/index.md", "guide/roles/index.md", "lessons/index.md", "decisions/index.md", "wiki/index.md"):
        if BASE + "/" + needed not in texts:
            errors.append(f"Missing router: {needed}")
    for folder, roster in (("rules", CORE_RULES), ("guide/general", CORE_GUIDES), ("guide/roles", CORE_ROLES)):
        for name in roster:
            if f"{BASE}/{folder}/{name}.md" not in texts:
                errors.append(f"Missing core file: {folder}/{name}.md")
    for name, text in texts.items():
        if name.startswith(BASE + "/") and not re.match(r"---\s*\nscope: (portable|project)\s*\n", text):
            errors.append(f"Missing scope frontmatter: {name}")
        if reused_shared and name.startswith(SHARED_PREFIXES):
            continue
        for raw, anchor in re.findall(r"`([^`\n]+\.md)`(?:\s+(§[0-9]+(?:\.[0-9]+)*))?", text):
            if any(char in raw for char in ("*", "<", ">")) or raw.startswith(("http", "docs/", "channels/")):
                continue
            candidates = [root / raw, (root / name).parent / raw]
            target = next((p for p in candidates if p.is_file()), None)
            # Project work-product paths are optional, while genome pointers must resolve.
            if target is None:
                if raw.startswith((BASE + "/", "general/", "roles/", "../")) or "/" not in raw and raw not in ("README.md", "CLAUDE.md", "AGENTS.override.md", "SKILL.md"):
                    errors.append(f"Broken Markdown pointer: {name} -> {raw}")
            elif anchor and not re.search(r"^#{1,6}\s+" + re.escape(anchor) + r"(?:\s|[a-z]|$)", target.read_text(encoding="utf-8-sig"), re.M):
                errors.append(f"Missing section: {name} -> {raw} {anchor}")
    if not reused_shared:
        role_index = texts.get(BASE + "/guide/roles/index.md", "")
        for line in role_index.splitlines():
            if not line.startswith("|") or "---" in line or "primary role" in line:
                continue
            cells = [v.strip().strip("`") for v in line.strip("|").split("|")]
            if len(cells) == 3:
                for role in [cells[1], *cells[2].split(",")]:
                    role = role.strip().strip("`")
                    if not role or role in ("—", "-"):
                        continue
                    key = f"{BASE}/guide/roles/{role}.md"
                    if key not in texts or not re.search(r"^## §6\b", texts.get(key, ""), re.M):
                        errors.append(f"Role missing or without completion criteria: {role}")
        lesson_index = texts.get(BASE + "/lessons/index.md", "")
        for name in texts:
            if name.startswith(BASE + "/lessons/") and not name.endswith("/index.md") and Path(name).name not in lesson_index:
                errors.append(f"Lesson not routed: {name}")
    agents = texts.get("AGENTS.md", "")
    for name in CORE_RULES:
        if f"{BASE}/rules/{name}.md" not in agents:
            errors.append(f"Root instruction surface does not route core standard: {name}.md")
    if not reused_shared:
        reachable = {BASE + "/guide/index.md"}
        pending = [(BASE + "/guide/index.md", 0)]
        while pending:
            router, depth = pending.pop()
            for pointer in re.findall(r"`([^`\n]+\.md)`", texts.get(router, "")):
                for candidate in (root / pointer, (root / router).parent / pointer):
                    try:
                        name = Path(os.path.abspath(candidate)).relative_to(root).as_posix()
                    except ValueError:
                        continue
                    if name not in texts or name in reachable or not name.startswith(BASE + "/guide/"):
                        continue
                    reachable.add(name)
                    if name.endswith("/index.md"):
                        if depth >= 1:
                            errors.append(f"Guide routing exceeds one area hub: {name}")
                        else:
                            pending.append((name, depth + 1))
        for name in texts:
            if name.startswith(BASE + "/guide/") and not name.startswith(BASE + "/guide/roles/") and name not in reachable:
                errors.append(f"Guide not routed: {name}")
        for name, text in texts.items():
            if name.startswith(BASE + "/decisions/") and not name.endswith("/index.md"):
                for field in ("class:", "subject:", "anchor:", "decided:"):
                    if field not in text:
                        errors.append(f"Decision missing {field}: {name}")
    for marker in ("lessons/index.md", "guide/roles/index.md", "guide/index.md"):
        if marker not in agents:
            errors.append(f"Root instructions do not reach {marker}")
    if health:
        hashes = {}
        for name, text in texts.items():
            normalized = " ".join(text.split())
            if len(normalized) > 120:
                hashes.setdefault(digest(normalized.encode()), []).append(name)
        notes.extend({"kind": "identical-content", "files": group} for group in hashes.values() if len(group) > 1)
        notes.append({"kind": "review-limit", "message": "Mechanical checks establish reference and schema integrity, not the completeness or quality of workflow guidance."})
    return {"status": "pass" if not errors else "fail", "files": len(files), "errors": sorted(set(errors)), "observations": notes}


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    for command in ("init", "update"):
        sub = commands.add_parser(command)
        sub.add_argument("--project", required=True)
        sub.add_argument("--package-root")
        sub.add_argument("--adoption", help="JSON with AGENTS.md: {before_sha256, replacement}; replacement retains reviewed project text")
        sub.add_argument("--apply", action="store_true")
        sub.add_argument("--plan-hash")
    sub = commands.add_parser("recover")
    sub.add_argument("--project", required=True)
    sub.add_argument("--apply", action="store_true")
    sub.add_argument("--plan-hash")
    for command in ("check", "refresh"):
        sub = commands.add_parser(command)
        sub.add_argument("--package-root")
        if command == "refresh":
            sub.add_argument("--apply", action="store_true")
    for command in ("verify", "health"):
        sub = commands.add_parser(command)
        sub.add_argument("--project", required=True)
    return result


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = parser().parse_args(argv)
    try:
        if args.command in ("init", "update"):
            root = root_path(args.project)
            plan = deployment_plan(root, package_path(args.package_root), args.command, load(Path(args.adoption)) if args.adoption else None)
            result = apply_plan(root, plan, args.plan_hash) if args.apply else plan
        elif args.command == "recover":
            result = recovery(root_path(args.project), args.apply, args.plan_hash)
        elif args.command in ("check", "refresh"):
            result = maintenance(package_path(args.package_root), args.command, getattr(args, "apply", False))
        else:
            result = verify(root_path(args.project), args.command == "health")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("conflicts") or result.get("status") in ("fail", "drift") else 0
    except (GenomeError, OSError, UnicodeError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
