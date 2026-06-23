# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.7.0] - 2026-06-23

### Added

- `update` mode now WARNs when a template (`.tpl`) changed in the bundle since deploy. Rendered phenotype files (`CLAUDE.md`, `index.md`) are still never overwritten — slots hold project-specific values — but the user is told to re-render manually instead of the change being silently dropped (`scripts/update.mjs`).
- `init-manifest.json` records a `templates[]` array (`.tpl` path + sha at deploy time); `update` compares it against the current bundle to detect template drift. Manifests predating this field warn conservatively (`cannot prove unchanged`) until the next init (`skills/init-project/SKILL.md` step 6).

## [1.4.0] - 2026-06-19

### Added

- `update` mode — pull newer portable files into an initialized project via a safe 3-way merge (`manifest ↔ live ↔ bundle`) that never overwrites local edits (`scripts/update.mjs`).
- `scripts/sync-version.mjs` — single-source version sync across `VERSION`, the plugin manifests, and the README badge, with a `check` mode (exits non-zero on drift).
- Drift guards: a `version-sync` CI workflow and a `.githooks/pre-commit` hook.
- `Releasing` guide in `CONTRIBUTING.md` with a SemVer-for-the-bundle policy.

### Changed

- `doc-organization.md`: an on-demand file defaults to a router entry only; an always-loaded trigger is earned via an interception test plus user confirmation in both outcomes.

## [1.3.0] - 2026-06-18

### Added

- Initial public release of the `init-project` Claude Code plugin.
- One-shot deploy of the agent documentation standard: `CLAUDE.md` + `.claude/rules/` (7 portable rules) + `docs/agent-guide/` (4 portable guides).
- Skill-authoring toolkit: `skill-designer`, `skill-writer`, `skill-writer-auditor`, `document-writer`.
- Three modes: `init` (seed a new project), `check` (drift report), `promote` (consolidate live changes into the bundle).
- Templates for `CLAUDE.md`, `agent-guide/index.md`, and `docs/index.md`.

[Unreleased]: https://github.com/tuannv0069/claude-doc-genome/compare/v1.4.0...HEAD
[1.4.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.4.0
[1.3.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.3.0
