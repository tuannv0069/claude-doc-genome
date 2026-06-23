# init-project — Claude Code plugin

> One-shot **Claude Code plugin** that bootstraps an AI-agent documentation system — `CLAUDE.md` + `.claude/rules/` + `docs/agent-guide/` — then lets the project self-maintain.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.7.0-blue.svg)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757.svg)](https://docs.claude.com/en/docs/claude-code)
[![Marketplace](https://img.shields.io/badge/marketplace-claude--doc--genome-555.svg)](#install)

<!-- Demo: drop a GIF here once recorded, e.g. ![demo](docs/demo.gif) -->

`init-project` deploys a battle-tested documentation standard for AI agents — the `CLAUDE.md` + `.claude/rules/` + `docs/agent-guide/` trio — plus a skill-authoring toolkit (`skill-designer`, `skill-writer`, `skill-writer-auditor`, `document-writer`). After the one-time seed, the project grows its own documentation using the deployed standard. `init` runs once; later you can opt into `update` to pull newer portable files from the bundle — a safe 3-way merge that never overwrites your local edits.

Keywords: Claude Code plugin · AI agent documentation · CLAUDE.md scaffolding · agent rules · prompt/skill standards.

## Requirements

- Claude Code, a recent version with plugin/marketplace support.
- A git repository for the target project (recommended; the skill writes into it).

## Install

```
/plugin marketplace add tuannv0069/claude-doc-genome
/plugin install init-project@claude-doc-genome
```

## Use

```
/init-project
```

The skill scans the project's stack, interviews for unscannable values, copies the portable bundle, renders the templates, generates optional module rules, writes a manifest, and verifies the result.

## Modes

| command | runs where | action |
|---|---|---|
| `/init-project` | a new project | deploy the standard (one-shot seed) |
| `/init-project check` | the bundle's home repo | report drift between the bundle and the live files |
| `/init-project promote` | the bundle's home repo | consolidate proven live changes back into the bundle |
| `/init-project update` | an initialized project | pull newer portable files from the bundle (safe 3-way merge; skips local edits) |

## Updating

`init` seeds once; the project then evolves on its own. When the bundle ships newer portable files, opt into them:

```
/init-project update
```

It compares the bundle against your files three ways (manifest ↔ live ↔ bundle): missing files are added, untouched files are updated, and any file you edited locally is reported as a **conflict and left untouched** — promote your change upstream or merge it by hand. Rendered files (`CLAUDE.md`, `index.md`, project-authored guides) are never overwritten.

## Philosophy

The documentation system is modeled as a **neural network**: files are neurons, links (triggers, router entries, `§ID` pointers) are synapses, and a file with no links is dead content. Five principles drive the design:

- **Context economy** — only pre-decision guardrails load every turn; everything else is one trigger line away, read on demand.
- **Growth from evidence** — no directory tree is pre-built; structure grows from real stimulus.
- **Bounded conduction** — knowledge routes through `router → hub → file`; work products route by naming convention.
- **Self-healing** — link-integrity on every change plus periodic orphan/dead-link audit.
- **Heredity** — the portable bundle is a genome seeded once per project; proven patterns are promoted back into the genome.

## What gets deployed

| group | content |
|---|---|
| rules | `doc-organization`, `critical-thinking`, `file-reading`, `claude-md-standards`, `skill-md-standards`, `rule-writing-standards`, `subagent-standards` |
| agent-guide | `five-why`, `markdown`, `mermaid`, `orchestration-policy` |
| skills | `skill-designer`, `skill-writer`, `document-writer` |
| agents | `skill-writer-auditor` |
| templates | `CLAUDE.md`, `agent-guide/index.md`, `docs/index.md` |

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Author

**Tuấn Nguyễn** — author of the skill and its documentation-architecture philosophy.

## License

[MIT](LICENSE) © 2026 Tuấn Nguyễn
