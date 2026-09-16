---
name: init-project
description: Set up a new Claude Code project's documentation system when the user asks to initialize project docs, deploy the documentation standard, khởi tạo bộ tài liệu agent, or run /init-project. Use update for an initialized project. Use check and promote only in the genome's source repository to compare and synchronize its live files and distribution bundle. This skill does not author individual skills or project deliverables.
---

# Initialize the project documentation system

## §1 Purpose and boundaries

This skill installs reusable workflow guidance and the project-specific indexes that make it reachable. A project is initialized once, then maintains its own instructions and can request later bundle updates. Existing project requirements remain owned by the project throughout installation and maintenance.

Locate this skill's installed directory before reading the bundle or running a maintenance script. Paths beginning with `portable/` and `templates/` below are relative to the skill directory. The `scripts/` directory is at the plugin repository root. Never make a deployed project's guidance depend on a path inside the plugin installation.

Keep temporary scans, plans and verification output in `.agent-workspace/tasks/<task-slug>/` in the target project. Place finished project deliverables in their project-owned work-product area.

## §2 Modes

| Invocation | Target | Responsibility |
|---|---|---|
| `/init-project` | A project that has not been initialized | Install the bundle, merge project indexes and verify the result. |
| `/init-project update` | An initialized project | Bring in a newer bundle while preserving local changes and updating project-owned routing. |
| `/init-project check` | The genome source repository | Compare portable live files with their bundle copies and report drift. |
| `/init-project promote` | The genome source repository | Synchronize reviewed live changes into the bundle. |

Do not rerun initialization over an initialized project as a substitute for resolving an update. Check and promote require the source repository's live deployment; without that deployment, there is no trusted live side to compare.

## §3 Distribution map

Copy portable files without changing their contents. Templates are project-owned after rendering, so they require a different update procedure.

| Bundle group | Project destination |
|---|---|
| `portable/rules/` | `.claude/rules/` |
| `portable/guide/` | `.agent-workspace/guide/general/` |
| `portable/roles/` | `.agent-workspace/guide/roles/` |
| `portable/tooling/` | `.agent-workspace/tooling/` |
| `portable/skills/` | `.claude/skills/` |
| `portable/agents/` | `.claude/agents/` |

The role router `index.md` is a template, not a portable role. Empty optional skill or agent groups do not require placeholder files. A project's own tools, roles, skills and agents are not automatically eligible for promotion.

| Template | Rendered destination |
|---|---|
| `templates/CLAUDE.md.tpl` | `CLAUDE.md` |
| `templates/guide/index.md.tpl` | `.agent-workspace/guide/index.md` |
| `templates/docs/index.md.tpl` | `docs/index.md` |
| `templates/lessons/index.md.tpl` | `.agent-workspace/lessons/index.md` |
| `templates/roles/index.md.tpl` | `.agent-workspace/guide/roles/index.md` |
| `templates/decisions/index.md.tpl` | `.agent-workspace/decisions/index.md` |
| `templates/wiki/index.md.tpl` | `.agent-workspace/wiki/index.md` |

Render the docs index when the project has a work-product category to register. Render the wiki index only when the wiki module applies. The remaining indexes are part of the core deployment. The manifest tracks template source hashes even when an optional rendered index is not needed yet.

## §4 Initialize a project

### Establish the project facts

Inspect the project's existing instructions, repository structure, runtime configuration and documentation. Determine which values are supported by those sources and which still need the user's input. Identify any existing files that would receive template content before writing them.

Use the available evidence and the user's stated preferences to fill the template slots. Ask only about necessary information that remains unresolved, such as ownership boundaries or a wiki source root. Do not invent a port, language choice or source directory. If a value cannot be established, preserve an explicit TODO and report that the corresponding setup is incomplete.

Select optional modules using §7. A module needs evidence from the project or the user's request; uncertainty alone does not justify adding it.

### Install the shared files

Create the required destinations in §3, then copy the bundle's portable files into them. Preserve existing local files that differ from the incoming content until their differences have been reviewed. Installation must not silently erase project work.

When a complete project genome already exists under `.agent-workspace/`, reuse its guide, role, lesson, decision and wiki files instead of copying or rendering another set over them. Install only the Claude-specific adapter, rules, skills, agents and non-conflicting tooling. Verify that every shared portable file and required router named in §3 exists; a partial workspace requires reviewed migration rather than selective filling. This is the deployed collaboration space for every supported agent, not a Codex-owned foreign tree.

Add `.agent-workspace/tasks/` and `.agent-workspace/worktrees/` to the project's ignore rules without replacing its existing ignore entries. These locations hold working state and temporary checkouts rather than distributed guidance.

### Merge the project indexes

Render the applicable templates using the established project values. When a target already exists, merge the new structure with its existing requirements instead of replacing the file. Preserve release procedures, scope boundaries, domain requirements and other project-owned facts unless the user has authorized changing them.

The lesson and role templates need no slot values. The decision index needs the project's entry-count review threshold. The wiki index needs the material root, subjects, claim classes, evidence axes and conservation checkpoint. Fill `WIKI_CLASS_SEPARATOR` with a Markdown table delimiter row containing one cell for each of the two fixed columns and each evidence axis. Check that every claim-class row has the same number of cells. Validate those values against the evidence model in `.claude/rules/wiki-tier.md` before accepting the wiki setup.

Create project-specific optional guidance only for confirmed modules. Give each new guide a router entry and determine whether it also needs a pre-action trigger according to `.claude/rules/doc-organization.md` §10. Keep the trigger and its target in the same change.

### Record and verify the deployment

After the files and indexes are correct, generate their manifest with:

```sh
node <plugin-root>/scripts/init-manifest.mjs --project <project-root> --modules <comma-separated-modules>
```

When §4 reused an existing shared genome, add `--reuse-shared-workspace`. The manifest then records only the files this Claude adapter installed and updates continue to leave the shared files under their existing updater ownership.

The manifest records the installed bundle version, file hashes, template source hashes and selected modules. Generate hashes from the actual installed files; do not invent them or use a manifest refresh to conceal unreviewed differences.

Run the verification in §8. Initialization is complete only when required values are resolved, routing works and the deployed gates accept the installed artifacts. A copied tool that fails against its copied data is a deployment problem to investigate, not proof that the tool should be ignored.

## §5 Check and promote in the source repository

Compare every portable file in §3 with its live counterpart using content hashes. Check both directions so that a removed file or a new candidate is visible. Distinguish project-owned additions from portable changes; a filename alone does not establish ownership.

For a wording or behavior change, edit the live source first and verify it there. Promote the reviewed content into the matching bundle path. If a portable file is removed or renamed, update its referrers and migration handling in the same change. Keep project-owned routers out of the portable copy operation.

Template and skill-body edits are made directly in their source files. They are not recovered by copying the live project phenotype back into the templates, because that would distribute project-specific values.

When preparing a version change, use `node scripts/sync-version.mjs set X.Y.Z`. A removed or renamed portable contract requires a major version; additive compatible content requires a minor version; wording corrections without contract changes require a patch version. Version preparation does not authorize a commit, push, tag or release.

## §6 Update an initialized project

Run the updater from its installed plugin location. It finds the bundle relative to its own script, while `--project` selects the project to update.

```sh
node <plugin-root>/scripts/update.mjs --project <project-root>
```

Review additions, updates, retired files, local conflicts and template changes before applying them. The updater compares the new bundle, current project files and hashes recorded at deployment. A local edit is preserved when it cannot be identified as the unchanged deployed copy. Retired portable files can be removed automatically only when manifest ownership and the current hash prove that they are unchanged genome files.

Resolve conflicts by comparing their actual content. Merge useful local changes or promote them upstream when appropriate. Do not replace a locally edited file merely to obtain a clean status. Unknown or legacy paths need an explicit ownership review rather than automatic deletion.

Merge changed templates into their project-owned targets manually, preserving slot values and project requirements. Remove references to retired files, add routes for new guides and roles, and create any required storage roots. A portable copy alone does not make a new guide reachable.

Apply the reviewed portable changes with:

```sh
node <plugin-root>/scripts/update.mjs --apply --project <project-root>
```

After reviewing and merging all template changes, acknowledge their source hashes with:

```sh
node <plugin-root>/scripts/update.mjs --apply --acknowledge-templates --project <project-root>
```

The acknowledgement records a completed manual template review; it does not perform the merge. Do not use it to dismiss unhandled template changes. The updater keeps the previous completed version while conflicts or unacknowledged template changes remain. Read the complete report rather than using the version field alone to judge success.

Finally, run §8 against the resulting project and verify both new and removed references. Do not rerun the manifest generator solely to make conflicts disappear.

## §7 Optional modules

| Module | Evidence that it is relevant | Project-owned result |
|---|---|---|
| Runtime | The project runs a development server, as shown by its scripts or runtime configuration. | Write a local runtime guide describing the actual startup, ports and shutdown procedure. |
| Browser tests | The project contains an installed browser test tool, its configuration or an existing test suite. | Write guidance for that tool and connect it to the tasks that run those tests. |
| Wiki | The project investigates external subject material and needs established claims preserved across tasks. | Render the wiki index using the project's material root, claim classes and evidence requirements. |

A project can add a skipped module later when evidence of the need appears. Detailed Git or release policies also belong to the project. Only a pattern proven useful across projects becomes a candidate for the portable bundle.

## §8 Verification and completion

Check that each distributed file reached the destination in §3, portable content matches the bundle, metadata is valid and template slots have been resolved. Confirm that root triggers resolve to real files and that each guide or role is reachable through the appropriate router. Check that retired files no longer have active referrers.

Run these tools from the target project root:

```sh
python .agent-workspace/tooling/verify_lesson_router.py
python .agent-workspace/tooling/verify_role_files.py
python .agent-workspace/tooling/verify_decision_log.py
python .agent-workspace/tooling/verify_wiki.py
python .agent-workspace/tooling/test_trigger_kinds.py
```

Run the paired tests for each changed verification tool. Read `.agent-workspace/guide/general/rule-health.md` before using `scan_rule_health.py`; its report requires interpretation and does not certify every aspect of the project.

A fresh lesson store and decision journal are valid with no entries. A project without the wiki module may have no wiki directory. Missing required data in an enabled module remains incomplete work.

Record which checks actually ran and any unresolved setup. Completion requires the installed content, routing and manifest to agree; a command that exits successfully is only one part of that evidence.
