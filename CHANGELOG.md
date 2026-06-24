# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.8.0] - 2026-06-24

### Changed

- `skill-designer` and `skill-writer` are now model-invocable — removed `disable-model-invocation: true` from both SKILL.md frontmatter so the agent can self-invoke them, not only the user via slash command (`skills/init-project/portable/skills/skill-designer/SKILL.md`, `skills/init-project/portable/skills/skill-writer/SKILL.md`).
- Rewrote both skills' `description` to the `skill-md-standards` frontmatter spec: open with "Use when…", add concrete trigger phrases, keep the scope boundary. With model-invocation enabled the description is the matcher, so trigger accuracy now matters.

## [1.7.1] - 2026-06-24

### Changed

- Plugin renamed from `init-project` to `claude-doc-genome` so it no longer displays as `init-project:init-project`; the skill keeps its `/init-project` command (now shown as `claude-doc-genome:init-project`). Install command is now `/plugin install claude-doc-genome@claude-doc-genome` (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`).
- Branding unified to `claude-doc-genome` across `README.md`, `CLAUDE.md`, and `CONTRIBUTING.md` for product/plugin references; skill name, `/init-project` commands, and `skills/init-project/` paths unchanged.

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

[Unreleased]: https://github.com/tuannv0069/claude-doc-genome/compare/v1.8.0...HEAD
[1.8.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.8.0
[1.7.1]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.7.1
[1.7.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.7.0
[1.4.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.4.0
[1.3.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.3.0
