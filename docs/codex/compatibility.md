# Compatibility and observed behavior

## Tested baseline

The implementation was developed on Windows with Python 3.12.10 and `codex-cli 0.154.0-alpha.6.2`. This is the observed client, not an inferred minimum supported version. The bundled Python tools require Python 3.12 or later and do not require an API key, MCP server or Claude installation.

Local prompt-construction fixtures observed root and child AGENTS loading, per-directory override selection, project fallback filenames, and a combined project-document byte limit. Separate config fixtures observed root and nested project settings, CLI overrides and rejection of untrusted project configuration. Skill metadata in `.agents/skills` was visible from a nested working directory; its body was not included until selected.

On this CLI, explicitly untrusted projects also omitted the synthetic AGENTS marker while project skill metadata still appeared. The installer does not grant trust. Check the effective instructions after the user has made the normal client trust decision. Discovery of a skill name alone does not establish that project instructions or the skill body are active.

Run the optional non-model platform probe with:

```text
python scripts/codex/probe-platform.py --output <new-temporary-directory>
```

It creates a synthetic Codex home and Git fixture, uses only artificial config values, and saves selected markers rather than raw prompts or private configuration. It does not copy account credentials or alter the real user configuration. The output directory must be new so a previous fixture cannot affect the result.

## Optional capabilities

Two live custom-agent probes did not produce a spawn event or the marker defined only in the agent file, including a run with `agents.enabled=true`. The prompt renderer also accepted a fixture containing invalid agent TOML without diagnosing it. These observations do not certify custom-agent registration or prove that every Codex client lacks it. Therefore this release does not install custom-agent definitions or make them necessary for the core workflow. Roles remain usable by the main agent; delegation uses an actually available tool when appropriate.

The core does not configure hooks, execution-policy rules, model settings or MCP. Optional integrations need their own project-specific validation and ownership. A file's presence is not evidence that the host executed it.

## Plugin distribution

The supported packaging path uses `.codex-plugin/plugin.json` and the packaged `skills/` directory. A local isolated-home probe successfully registered a marketplace, installed the compatibility plugin and listed it as enabled on the baseline CLI. The builder copies the authored skill from `skills/init-codex-genome/` into that plugin layout; no runtime source sharing with Claude is involved.

The source checkout and generated distribution serve different discovery paths. Use one copy of `init-codex-genome` in a project session. Packaging itself does not modify account settings or install a plugin globally.

## Limits of the evidence

CLI prompt construction, command execution and structural validation are distinct checks. A model's successful action in a fresh CLI session is evidence for that session, not a guarantee for every future response. Fresh desktop UI loading, IDE, remote and cloud behavior require separate observations. The development environment does not expose an authorized native desktop test surface, so this product does not claim desktop UI certification from CLI results.

The implementation reports in the repository record the exact executed checks and remaining client limits. A copy of `skills/init-codex-genome/` remains usable without those reports or this development support directory.
