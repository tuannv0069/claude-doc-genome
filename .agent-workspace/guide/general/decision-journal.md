---
scope: portable
---

# Decision journal

The journal records reasons and choices that a diff cannot reconstruct. It complements version history without repeating a record of the files changed.

## §1 Admission test

Before adding an entry, ask whether version history alone could reconstruct the conclusion. If it could, do not duplicate that history. If the conclusion depends on an alternative that was rejected, an accepted limitation, or another decision that leaves no sufficient trace in the diff, record it under one of the classes in §2.

## §2 Decision classes

| Class | What it records |
|---|---|
| `choice` | The selected approach, a viable alternative that was rejected, and the reason for that choice. |
| `scope` | A decision that some work is outside the task or does not apply, when that decision leaves no diff. |
| `debt` | A known limitation accepted for delivery, together with the condition that permits or requires resolving it. |
| `rule` | A change to a governing requirement and the reasoning behind the change. |
| `review` | The conclusion on a review comment when the response traces to a governing requirement, including the established cause and the requirement affected. |

A review entry is the authoritative record of its root-cause classification. Working notes and the response to the reviewer must agree with it. If later evidence changes the conclusion, supersede the entry under §8.

## §3 Entry data

Each decision has its own Markdown file. Its YAML metadata includes `class`, `subject`, and `anchor`. The subject identifies an existing repository-relative path and can include a stable section. The anchor identifies the evidence or commit supporting the decision. Add `supersedes` only when the entry replaces a previous decision, using that entry's identifier.

The body contains a nonempty `decided:` field. Use `because:`, `rejected:`, or `unlocked by:` when that information applies. These labels identify decision data for the journal's verifier; their values can contain the explanation the decision requires.

Do not edit or delete a historical entry to change its conclusion. Add a new entry that supersedes it. Progress, test output, and descriptions of the current file contents belong in working records or version history.

## §4 Location and identifiers

The journal router is `.agent-workspace/decisions/index.md`. Entries live in a year-month directory beneath `.agent-workspace/decisions/` and use the filename pattern `YYYY-MM-DD-<class>-<slug>.md`. The identifier is the filename without its extension.

One file per decision avoids competing sessions appending to the same file. If the subject is later renamed, keep the historical path in the entry; the verifier can follow the rename through version history.

## §5 When to write

Apply the admission test when changing a law, answering a review comment that affects a law, or deciding scope, accepted debt, or a rejected alternative. Write an admitted decision during the same turn in which it is made, while its evidence and reasoning remain available.

A law includes a rule, guide, role, lesson-store requirement, or deliverable standard. A minor wording edit does not need a journal entry when its entire meaning is already recoverable from the diff.

## §6 When to read

Before changing a law, search the journal for its subject and read any standing decision that could conflict with the proposed change. Understand the earlier reason before reversing the decision.

Search by repository-relative path and relevant stable section. A search result is a candidate record; use the supersession relationships to determine whether it still governs the subject.

## §7 Subagents

A subagent returns the decisions it made or identified together with their evidence. The orchestrator reconciles those results and writes any journal entries. Subagents do not write competing entries independently for the same coordinated task.

## §8 Lifecycle

An entry is standing until a later entry supersedes it. The older entry then remains as history. Closing an accepted debt is also recorded by a later debt entry that supersedes the earlier one and states how the condition was satisfied.

Read the subject's entries and their supersession relationships to find the current decision. A newer timestamp alone does not establish that an unrelated entry replaced an earlier decision.

## §9 Volume and archive

The project sets its per-shard volume threshold in the journal router's `cap:` metadata. A warning invites examination of whether the journal is recording decisions or duplicating routine history; it is not a limit on the length of a decision's explanation.

Use `archive_decisions.py --year YYYY` to inspect archive candidates. Only superseded entries are eligible. Review the proposed moves under the task's authorization before applying them. An old but standing decision remains active, including when its subject was renamed.

## §10 Relationship to current guidance

Decision records preserve history; rules and guides state the requirements currently in force. Keep the two responsibilities separate. Do not copy an entry's change history into the body of the requirement it describes.
