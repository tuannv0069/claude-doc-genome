---
scope: portable
---

# Codex project entry instructions

## §1 Define the entry point

Use `AGENTS.md` for the project identity, authority boundaries and obligations needed before the assistant selects further guidance. Keep detailed procedures at their canonical sources and make the condition for reading each source explicit. A path in an index is not evidence that its contents have been loaded.

Codex instruction discovery depends on the client, project root and working directory. Check current official documentation and the installed client's behavior before relying on overrides, fallback filenames or discovery limits. When editing a file in a child directory from the project root, do not assume that the child's AGENTS instructions become active because that file was touched.

## §2 Preserve ownership and effective instructions

The project owns `AGENTS.md`. Genome deployment manages only the region delimited by `<!-- codex-genome:begin -->` and `<!-- codex-genome:end -->`, and records that region's deployed hash. Preserve project content outside it. An existing file without recognized ownership needs an explicit adoption plan rather than replacement.

Inspect applicable ancestor instructions, `AGENTS.override.md`, fallback files and nested instructions before declaring the effective instruction set verified. Do not create an override to silently outrank project guidance. Changes require a fresh Codex session or the client's supported reload mechanism before testing loading.

## §3 Make reading obligations executable

Each trigger identifies the decision signal, the source and the point before which it must be read. Use explicit action triggers for rules selected by the type of artifact being edited, including creation and rename. A standard in `.agent-workspace/rules/` has no automatic loading behavior merely because of its directory name.

Verify that task-start lookups and important action triggers appear in the actual instruction input and cause the required reading in a representative task. Check truncation against the installed client's effective limit. Resolve excessive input by improving routing and scope, not by requiring ungrammatical or compressed writing.

## §4 Verify changes against project behavior

Exercise both a task that matches a changed trigger and nearby work that should not match it. Check from the relevant working directories, including root-to-child edits. A string match confirms that instructions are present; a fresh execution checks whether the intended workflow occurred. Report those two types of evidence separately.
