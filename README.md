# claude-doc-genome

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.0.0-blue.svg)](CHANGELOG.md)

`claude-doc-genome` is a Claude Code plugin that gives a project a documentation system for AI work. It installs project instructions, reusable workflow rules, guides that are read when needed, and tools that check the relationships between them.

The project owns its requirements, domain knowledge and deliverables. The genome provides the procedures for finding instructions, working from evidence, managing changes and carrying useful lessons forward. It does not prescribe a shared writing style for conversations, scripts or documents.

## Choose the product

The two initialization skills live under `skills/`: [init-project](skills/init-project/SKILL.md) for Claude Code and [init-codex-genome](skills/init-codex-genome/SKILL.md) for Codex. Copy the whole Codex skill into a project's `.agents/skills/` to use it there. That skill is the only authored Codex distribution source; its [documentation](docs/codex/index.md), tests and development tools live under `docs/codex/`, `tests/codex/` and `scripts/codex/`. The Claude product described below keeps its existing source layout, tools and version. Improvements that apply to both are implemented and verified separately; there is no common authoring source or cross-product renderer. After deployment, both adapters use the same `.agent-workspace/` in the project.

## Install and initialize

Add the marketplace and install the plugin in Claude Code:

```text
/plugin marketplace add tuannv0069/claude-doc-genome
/plugin install claude-doc-genome@claude-doc-genome
```

In the target project, run:

```text
/init-project
```

The skill inspects the project, resolves the required settings, copies the portable files, merges project indexes and verifies the deployment. Existing project instructions are preserved during the merge. Node.js is needed for maintenance scripts; the portable verification tools use Python and its standard library. Git provides history and supports the worktree and conservation checks.

## Working with the genome

| Command | Where to use it | What it does |
|---|---|---|
| `/init-project` | A new project | Establishes the documentation system. |
| `/init-project update` | An initialized project | Reviews and applies changes from a newer bundle. |
| `/init-project check` | This source repository | Compares the live genome with its portable bundle. |
| `/init-project promote` | This source repository | Copies reviewed live improvements into the bundle. |

Initialization happens once. Later changes use the update procedure, which compares the new bundle, the current files and the hashes recorded at deployment. It preserves conflicting local edits. An unchanged retired genome file can be removed when the manifest proves its ownership. Project-owned indexes and instructions are merged separately; they are not overwritten by the updater.

The updater reports changed template sources until their changes have been reviewed and acknowledged. It does not report a completed new version while conflicts or unacknowledged templates remain. See the [init skill](skills/init-project/SKILL.md) for the complete procedure.

## What is installed

| Content | Destination | Purpose |
|---|---|---|
| Workflow rules | `.claude/rules/` | Establish source reading, evidence, placement and component contracts. |
| General guides | `.agent-workspace/guide/general/` | Describe planning, review, verification, lessons, decisions and related procedures. |
| Roles | `.agent-workspace/guide/roles/` | Provide working perspectives and completion checks. |
| Verification tools | `.agent-workspace/tooling/` | Check the genome's data and references. |
| Optional skills and agents | `.claude/skills/`, `.claude/agents/` | Hold reusable workflows or delegates that the bundle explicitly includes. |
| Project instructions and indexes | `CLAUDE.md` and the appropriate workspace indexes | Connect shared guidance to the actual project. |

Lessons, decisions and optional wiki claims live under `.agent-workspace/`. Temporary task state and worktrees are ignored by Git. Finished project documents live in the project's work-product area, usually `docs/`.

## How the design works

Each substantive requirement has one source. Routers and references make that source reachable without copying its text into every workflow. Guidance needed before an action is connected to that action; other guidance is read when the task reaches its subject.

Portable files contain reusable procedures. Templates supply the project-specific information and routing that cannot be copied unchanged. A useful improvement is first verified in the live project, then promoted into the bundle when it is appropriate for other projects.

The current rewrite's [design](docs/genome/thiet-ke-goc.md) and [plan](docs/genome/ke-hoach-viet-lai.md) explain the source architecture and the rewrite. The [implementation report](docs/genome/ket-qua-viet-lai.md) records the completed checks and the remaining limits.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for source ownership, verification and release procedures. Changes are recorded in [CHANGELOG.md](CHANGELOG.md).

## Author and license

Tuấn Nguyễn created the skill and its documentation architecture. The project is distributed under the [MIT License](LICENSE).
