# Existing instructions and legacy installations

## Establish ownership before merging

Read existing `AGENTS.md`, any applicable `AGENTS.override.md`, nested instruction files, project skills and the current manifests. Record which files belong to this project, a previous Codex deployment or another product. A generated marker without a recorded hash does not prove that its contents can be replaced.

The new Codex installer manages only its marked region in `AGENTS.md`, its own ignore entries and files listed in its manifest. Keep project identity, domain rules and unrelated instructions outside that region. Use the dry run's exact before hash when preparing a reviewed adoption file; inspect `init --help` for its supported input format. Read the proposed replacement back before applying it.

For a legacy generated AGENTS file, distinguish project information and domain workflows from the retired shared writing policies. Preserve the former in project-owned instructions. Remove the retired global sentence, length, heading and presentation policies as part of the reviewed merge; do not translate them into the new genome. Keep genuinely output-specific requirements in their owning project rules when they remain applicable.

## Shared workspace and other writers

When `.agent-workspace/` already contains a complete genome, reuse its guides, roles, lessons, decisions and wiki. The Codex manifest records that the shared workspace is reused and does not claim those files. It owns only the Codex adapter files that it actually installs. An incomplete shared workspace is a conflict because filling selected gaps could combine incompatible versions without review.

Files listed in `.claude/init-manifest.json` remain under that installer's update ownership. Shared genome files are consumed in place; harness-specific files are not adopted or deleted through the Codex updater. Unreferenced Markdown may remain without becoming part of the Codex instruction chain.

Inspect hooks, init/update workflows and scripts that can run an old renderer. A renderer that can regenerate AGENTS makes adoption incomplete even if the new installation passes its own hash checks. Retire the identified invocation through a separately scoped migration of its owner, or report the unresolved writer and stop adoption. Do not disable an entire hook or remove unrelated configuration to suppress one call.

## Historical records

Existing lessons, decisions and wiki records under `.agent-workspace/` are already the project's shared history. Do not copy them into a Codex-specific namespace. If records are being migrated from a genuinely separate legacy location, preserve provenance and identifier mapping, check their references, and never overwrite an existing record with the same identifier.

## Local changes during updates

Review the local file, its recorded deployed hash and the candidate bundle before resolving a conflict. Reapply the intended change to the new source or retain a documented project-owned variant as appropriate. Do not edit the manifest's hashes to make unexplained changes appear clean. Template updates need semantic review because the instantiated router may contain project data. Verify the final state before acknowledging a reviewed template revision.

The `--adoption` input is a JSON object keyed by project-relative target path. For an existing AGENTS file without Codex ownership, supply `before_sha256` for the current whole file and `replacement` containing the reviewed project content to keep; the installer appends its new managed region. Do not include managed markers in that replacement.

For an already owned portable file or AGENTS region whose local changes have been reviewed and are intentionally replaced, supply `before_sha256` for the current whole file, `accept_source_sha256` for the exact bundle source and `replace_from_bundle: true`. The installer still preserves AGENTS content outside its managed region. These fields authorize only the examined bytes, not arbitrary later changes. A project variant that should remain different is not resolved by falsely acknowledging the bundle.

For a project-owned seed whose template changed, first perform any needed semantic merge yourself. Acknowledge it with the current target's `before_sha256` and the new template's `accept_template_sha256`. The updater records the review without overwriting the project data. Hashes are SHA-256 of the actual file bytes. Run a fresh dry run with the same adoption file, then apply its returned plan hash.
