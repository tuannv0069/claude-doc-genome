---
scope: project
source_root: {{WIKI_SOURCE_ROOT}}
---

# Wiki tier — router

Law of the tier (edge format, R1–R10, extension points): `.claude/rules/wiki-tier.md`.
Gate: `python .agent-workspace/tooling/verify_wiki.py` — `--new-id <cluster>` allocates an `id`,
`--merge-check <ref> <ref> [...]` runs the R9 conservation check at merge time (two refs minimum).

`source_root` in this file's frontmatter is the project's material root, resolved **relative to the
directory holding this file** (`.agent-workspace/wiki/`); every `path` of a `located` item is written
relative to it.

## §1 Subjects

| subject | holds | status |
|---|---|---|
{{WIKI_SUBJECTS}}

`growing` — new edges are written into this subject. `frozen` — nothing more is added, existing
edges still answer. `not opened` — the subject has no edge yet.

## §2 Extension points — what this project declares

The six `wiki-tier.md` §7 requires:

| extension point | this project declares |
|---|---|
| subject list | the table in §1 above |
| claim classes + the evidence each one requires | §2.1 below — a **closed** list; the `class` cell takes one of those tokens and nothing else |
| subject material | {{WIKI_SUBJECT_MATERIAL}} |
| search procedure | `source_encodings:` in this file's frontmatter — extra text encodings the locator check must decode besides the default. Material is single-encoding → omit the key entirely |
| locator root | `source_root:` in this file's frontmatter, resolved relative to the directory holding this router |
| conservation checkpoint | {{WIKI_MERGE_CHECKPOINT}} |

### §2.1 Claim classes

A **closed** list. `required` = R2 will not promote an edge to `sourced` until it carries evidence
from that source.

| class | what the claim states | {{WIKI_EVIDENCE_AXES}} |
|---|---|---|
{{WIKI_CLAIM_CLASSES}}

Which evidence form carries which source (`wiki-tier.md` §4): source text → `located` · stored data
→ `stored-data` · running system → `running-system` · a measured absence → `absent`.

## §3 Clusters

A cluster is created at the moment an investigation touches its lookup topic (`wiki-tier.md` §2),
and registers one row here in the same commit.

A cluster row must be a **markdown link** whose target is the cluster path relative to the `wiki/`
directory (`<subject>/<cluster>.md`) — the gate reads every `.md` link in this file as one cluster
declaration. The row's shape lives in `wiki-tier.md` §2: a sample link written here would be read as
a cluster that does not exist, because the gate's link scan does not honour code fences.

| subject | cluster | lookup topic |
|---|---|---|
