# Codex Genome

The complete Codex genome is authored in [skills/init-codex-genome](../../skills/init-codex-genome/SKILL.md). That skill contains the instructions, templates and deployment tool needed to initialize another project. Development tests live in `tests/codex/`, packaging scripts in `scripts/codex/`, and human documentation in `docs/codex/`. None contains another genome source tree.

The Claude and Codex distributions are maintained independently, but they connect their agents to the same project genome. Inside a project, both use `.agent-workspace/` for guidance and accumulated working state. `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.codex/` and each distribution's manifest remain harness-specific.

## Use the skill in a project

Copy the whole `skills/init-codex-genome/` directory to `<project>/.agents/skills/init-codex-genome/`. Python 3.12 or later is required. Open a fresh Codex session in that project and ask:

> Use init-codex-genome to initialize this project's genome.

The skill inspects the project, reviews a deployment plan, applies changes within the user's authorization, and verifies the result. Open a fresh session afterward to check that the installed instructions load. Project-specific information stays outside the managed AGENTS region or in the project's own routers and documents.

The script can also run from a skill stored outside the target project:

```text
python <skill>/scripts/genome.py init --project <absolute-target-project>
```

This command only proposes changes. Review them, then append `--apply --plan-hash <returned-hash>` to apply that plan. Use `update` when `.codex/genome-manifest.json` exists. If another supported adapter already created a complete `.agent-workspace/`, Codex reuses it instead of creating a parallel workspace. Read [adoption guidance](../../skills/init-codex-genome/references/adoption.md) for existing instructions whose ownership is unresolved.

## Maintain the source

Edit the files inside the skill directly. Its `bundle/portable/` directory is the authored source, not a generated copy. Its templates seed project-owned files. After reviewing an edit, refresh the deployment map and check the result:

```text
python skills/init-codex-genome/scripts/genome.py refresh
python skills/init-codex-genome/scripts/genome.py refresh --apply
python skills/init-codex-genome/scripts/genome.py check
python -m unittest discover -s tests/codex
```

These commands run from the repository root. The check materializes a temporary project; the repository keeps no second Codex instruction tree. See [the contribution guide](contributing.md) for development and version maintenance.

## Optional plugin distribution

From the repository root, build a new local marketplace directory:

```text
python scripts/codex/package.py --skill-root skills/init-codex-genome --output <new-marketplace-directory>
codex plugin marketplace add <new-marketplace-directory>
codex plugin add codex-genome@codex-genome-local
```

The built plugin distributes the same skill. Use either that plugin or a project skill copy in a session to avoid duplicate discovery. Building a package does not install it or change user configuration.

## Deployed project layout

The installer creates a managed region in `AGENTS.md`. For a new project it also seeds the shared guidance, roles, lessons, decisions and wiki under `.agent-workspace/`; for a project with a complete genome it uses those files in place. Codex-specific standards and tooling also live under `.agent-workspace/`, while the Codex deployment manifest, lock and journal live under `.codex/`. These are deployed project files, not another source tree in this repository.

The genome governs work and evidence. It does not impose a general writing style on project outputs or configure personal models, permissions, trust, hooks or MCP. See the [workflow coverage map](workflow-obligations.md) and [compatibility evidence](compatibility.md) for scope and tested limits.

## License

Copyright 2026 Tuấn Nguyễn. Distributed under the [MIT License](../../LICENSE).
