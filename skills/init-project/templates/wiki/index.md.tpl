---
scope: project
source_root: {{WIKI_SOURCE_ROOT}}
---

# Wiki index

The wiki records established claims about this project's subject material. Its data contracts and evidence requirements are defined in `.claude/rules/wiki-tier.md`.

The `source_root` value is resolved relative to this router's directory, `.agent-workspace/wiki/`. Each `located` evidence item uses a path relative to that source root.

## §1 Subjects

| subject | holds | status |
|---|---|---|
{{WIKI_SUBJECTS}}

A subject with status `growing` accepts new claims. A `frozen` subject remains available for reading but receives no additions. A subject marked `not opened` has no recorded claims yet.

## §2 Project configuration

Declare the extension points required by `.claude/rules/wiki-tier.md` §7 here.

| extension point | this project declares |
|---|---|
| subject list | The subjects are listed in §1. |
| claim classes and required evidence | The allowed classes and their evidence requirements are listed in §2.1. |
| subject material | {{WIKI_SUBJECT_MATERIAL}} |
| search procedure | If source files need additional encodings, declare them in the optional `source_encodings` frontmatter field. Otherwise the locator check uses its defaults. |
| locator root | The `source_root` frontmatter field identifies the material root relative to this router. |
| conservation checkpoint | {{WIKI_MERGE_CHECKPOINT}} |

### §2.1 Claim classes

The `class` field of a claim must use a token from this table. An evidence column marked `required` identifies a source that must be present before the claim can be considered sourced.

| class | what the claim states | {{WIKI_EVIDENCE_AXES}} |
{{WIKI_CLASS_SEPARATOR}}
{{WIKI_CLAIM_CLASSES}}

Evidence forms are defined in `.claude/rules/wiki-tier.md` §4. Use `located` for source text, `stored-data` for stored data, `running-system` for runtime evidence, and `absent` for a measured absence.

## §3 Clusters

Create a cluster when an investigation first reaches its lookup topic, following `.claude/rules/wiki-tier.md` §2. Register it below with a Markdown link whose target is relative to `.agent-workspace/wiki/`. The verification tool reads Markdown links here as cluster declarations, so do not add example links to nonexistent clusters.

| subject | cluster | lookup topic |
|---|---|---|

## §4 Verification

Run `python .agent-workspace/tooling/verify_wiki.py` to validate the wiki. Use `--new-id <cluster>` to allocate an identifier and `--merge-check <ref> <ref>` to check conservation across at least two Git references.
