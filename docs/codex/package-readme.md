# Codex Genome

This distribution contains the Codex project adapter and initialization skill. It connects Codex to the project's shared genome, including workflow guidance, roles, lessons, decisions and verification tools. Project requirements and output-specific writing standards remain owned by the project.

## Use the plugin

Install this plugin from its containing local marketplace:

```text
codex plugin marketplace add <marketplace-directory>
codex plugin add codex-genome@codex-genome-local
```

Open a fresh Codex session in the intended project and ask to initialize the Codex genome, or select `init-codex-genome` from the skill catalog. Installing the plugin makes the workflow available; it does not automatically write instructions into every project.

The [initialization skill](skills/init-codex-genome/SKILL.md) explains installation, update and verification. Its script can also be called directly:

```text
python <plugin-directory>/skills/init-codex-genome/scripts/genome.py init --project <absolute-target-project>
```

Python 3.12 or later is required. The command reports a dry-run plan. After reviewing the plan, apply it by adding `--apply --plan-hash <returned-hash>`. Use `update` for a project with an existing Codex manifest. See [existing-file adoption](skills/init-codex-genome/references/adoption.md) before replacing or merging an older instruction system.

Project content outside the managed AGENTS region is preserved. The tool manages only its recorded files and regions. The core does not configure the user's model, trust, permissions, hooks or MCP. A fresh session must verify effective loading in the selected client after installation.

This package is maintained independently from the Claude Code distribution and can bootstrap a project without it. When the project already has a complete `.agent-workspace/`, the Codex adapter reuses that workspace so both agents share working behavior and accumulated records. The skill contains its complete source and can run its own checks and refresh metadata after reviewed edits. Repository development tests and plugin packaging scripts are separate support tools; they are not required for project installation.

The package version is recorded in `VERSION`. Copyright 2026 Tuấn Nguyễn, under the [MIT License](LICENSE).
