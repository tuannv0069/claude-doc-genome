---
name: init-codex-genome
description: Connect Codex to a project's shared genome, initialize that genome when absent, update Codex-owned adapter files, or maintain the Codex distribution in this skill. Use for requests to install or maintain the Codex project instruction system, not for ordinary project work or creating an unrelated skill.
---

# Initialize and maintain the Codex genome

This skill owns the Codex distribution and adapter. A project has one genome workspace under `.agent-workspace/`; Claude Code and Codex use that same guidance, roles, lessons, decisions, wiki and task state. Harness-specific instructions, configuration and deployment records remain separate. The project's requirements and deliverables remain project-owned.

## Establish the operation

Identify the target project from the request and the current workspace. Resolve it to an absolute path before running a command. Use authorization already given in the conversation. Ask only if the intended project, a material merge decision or authority for the proposed change remains unresolved.

Find this skill's actual directory from the skill path supplied by Codex. Run its `scripts/genome.py` by absolute path. The script finds the bundle in this installed skill; it does not assume the user's project contains the source repository. Python 3.12 or later is required.

Use `init` when the project has no `.codex/genome-manifest.json`. Use `update` when that manifest already exists. If a complete shared genome workspace is already present, `init` reuses it and installs only the Codex adapter, Codex standards and Codex tooling. A previous generated Codex installation without the new manifest requires adoption under [references/adoption.md](references/adoption.md), not an ordinary update.

## Install or update a project

Inspect the project's existing instructions, overrides, configuration and workflows before deciding what to merge. Establish its real purpose and verification commands from its sources; do not invent project facts to fill a template. Read the selected bundle templates and the deployment plan to understand the proposed changes.

Run a dry run first:

```text
python <skill>/scripts/genome.py init --project <absolute-project-path>
python <skill>/scripts/genome.py update --project <absolute-project-path>
```

Review the returned operations, conflicts and inventory. The two commands are alternatives for the states described above. Do not infer ownership from a familiar directory name or a generated-file comment. Resolve existing root instructions or local changes through the procedure in [references/adoption.md](references/adoption.md). Preserve project configuration and other skills; the core needs no model, permissions, trust, hook or MCP changes.

When the plan is within the user's authorization and has no unresolved conflict, rerun the same operation with `--apply --plan-hash <hash-from-dry-run>`. This binds the write to the state that was reviewed. If the hash changes, inspect the new state and plan before applying it. Do not ask the user to confirm an already authorized clean installation merely because the tool separates planning from writing.

Keep project context outside the managed region of `AGENTS.md`. After installation, inspect the shared routers and add project facts, domain roles and discovery links only where evidence establishes them. An empty lesson or decision store is valid. Do not copy the source repository's incident history into a new project.

Run the installed tool's `verify --project <absolute-project-path>`, inspect the result, and confirm that the manifest's completed version matches the installed bundle. When updating, compare the final diff with the requested changes and confirm that preserved local content is intact. Open a fresh Codex session to verify effective instruction and skill loading; a successful file copy alone does not establish model behavior. State any remaining validation limit.

## Maintain the source product

This skill contains the only authored Codex distribution: portable bootstrap files under `bundle/portable/`, project seeds under `bundle/templates/` and the deployment map under `bundle/bundle-map.json`. Edit those sources directly. Use [references/maintenance.md](references/maintenance.md) for `check`, metadata refresh and verification. These operations act on this skill and do not synchronize a second authoring tree or import the Claude distribution.

## Interrupted operations

Do not remove a transaction or lock merely to make an error disappear. Inspect the reported recovery state and the `recover --help` procedure before resuming. Preserve evidence of a conflict and verify the resulting files after recovery. Stop dependent writes if ownership or the latest file state cannot be established.

This workflow does not authorize a commit, push, publication or deployment into another project beyond the user's request.
