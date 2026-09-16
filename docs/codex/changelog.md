# Changelog

## Unreleased — 1.0.0

### Source organization

- The complete genome is authored directly in `skills/init-codex-genome/`, including its canonical version. Development tests, tools and documentation live under `tests/codex/`, `scripts/codex/` and `docs/codex/`; the root `codex/` directory has been removed.
- Removed the duplicate live instruction tree and its promotion workflow. Skill-local `check` and `refresh` validate sources and maintain deployment metadata without copying from another authoring tree.
- Corrected the deployed architecture so Claude Code and Codex use the same `.agent-workspace/`. Codex-specific deployment records now live under `.codex/`.

### Added

- Codex adapter for the shared project instruction network, with action-triggered guidance, role and lesson routing, decisions and evidence requirements.
- A self-contained initialization and maintenance skill, portable bundle and project templates.
- Separate adapter ownership, explicit target roots, managed AGENTS content and preservation of shared project-genome files.
- Independent verification, deployment tests, packaging and version maintenance.

The product does not include a shared output-style policy. Its source release and maintenance lifecycle is independent from the Claude distribution; the deployed project genome is shared.
