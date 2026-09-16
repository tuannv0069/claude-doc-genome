---
scope: portable
---

# Recording decisions that a diff cannot explain

## §1 Decide whether a record is needed

Before changing a rule, guide, role or lesson requirement, responding to a review comment, or deciding scope, debt or a rejected alternative, inspect existing decisions about that subject. Search by subject path and relevant section, then follow supersession links to identify the standing decision.

Create a record when the reasoning cannot be reconstructed from the diff: a viable alternative was rejected, a limitation was accepted, work was excluded, or a governing requirement changed for a reason the edit alone does not preserve. Routine progress and test output belong in task evidence. A wording correction with no changed requirement does not automatically need a journal entry.

## §2 Classify the decision

Use `choice` for a selected approach and a rejected viable alternative, `scope` for work explicitly excluded or judged inapplicable, `debt` for a known limitation and its resolution condition, `rule` for a governing requirement change, and `review` for a review conclusion that traces to a governing requirement. A review record owns its root-cause classification; later responses and working notes must agree with it or supersede it with new evidence.

## §3 Store the reason and evidence

Each decision has a file under `.agent-workspace/decisions/YYYY-MM/`, named `YYYY-MM-DD-<class>-<slug>.md`. The filename without its extension is the identifier. YAML fields `class`, `subject` and `anchor` identify its category, repository-relative subject and supporting evidence. An optional `supersedes` field identifies the earlier decision replaced.

Begin the frontmatter with `scope: project`, as required for project-owned genome records. The decision-specific fields follow it; they do not replace that portability declaration.

The body includes a nonempty `decided:` value. Add `because:`, `rejected:` and `unlocked by:` when they carry relevant reasoning. These are journal data fields rather than a prose format for other documents. A subject may include a stable section. Preserve a historical subject path after a later rename rather than rewriting the record as though it had always named the new file.

## §4 Preserve the lifecycle

Write an admitted record in the same turn as the decision. Do not edit an old decision to reverse it; add a later record that explicitly supersedes it. A newer timestamp alone does not replace another entry. Resolve accepted debt with a superseding record describing how its condition was satisfied.

The active rule states the current requirement; the journal preserves reasons and history. Coordinated executors return candidate decisions to the parent, which owns reconciliation and writing. This avoids conflicting records for the same shared choice.

## §5 Archive only resolved history

The project may set a shard-volume review threshold in the decision router. It is a signal to inspect whether records duplicate routine history, not a limit on how fully a decision may be explained. Archive only superseded entries through a reviewed move that preserves identifiers and references. Old standing decisions remain active. Do not assume a verifier has followed renames or validated evidence unless its actual checks establish that result.
