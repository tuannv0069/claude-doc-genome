---
scope: portable
---

<critical>
scope: the decision journal — which decisions are recorded, when an entry is written, how it is read back and superseded.
never: edit or delete a historical entry, or record what version history can reconstruct by itself.
note: search the journal before changing a law; write an admitted decision in the same turn it is made; a wrong entry is corrected by a later entry that supersedes it.
</critical>

# Decision journal

The journal records reasons and choices that a diff cannot reconstruct. It complements version history without repeating a record of the files changed.

## §1 Admission test

One question decides every candidate: if the entry were deleted, could version history alone reconstruct the conclusion?

<rules section="ALWAYS">
- Before adding an entry, ask whether version history alone could reconstruct the conclusion, and skip the entry when it could.
- Record the conclusion under one of the classes in §2 when it depends on a rejected alternative, an accepted limitation, or another decision that leaves no sufficient trace in the diff.
- Skip an entry for choosing among creative drafts or options and for revising creative text for taste; `creative-work.md` §8 covers those.
</rules>

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

Each decision has its own Markdown file. The labels `decided:`, `because:`, `rejected:` and `unlocked by:` identify decision data for the journal's verifier; their values can contain the explanation the decision requires.

<rules section="ALWAYS">
- Give the YAML metadata `class`, `subject` and `anchor`, where `subject` identifies an existing repository-relative path with an optional stable section and `anchor` identifies the evidence or commit supporting the decision.
- Add `supersedes` only when the entry replaces a previous decision, using that entry's identifier.
- Write a nonempty `decided:` field in the body, and add `because:`, `rejected:` or `unlocked by:` when that information applies.
</rules>

<rules section="NEVER">
- Edit or delete a historical entry to change its conclusion; add a new entry that supersedes it.
- Record progress, test output or descriptions of the current file contents; those belong in working records or version history.
</rules>

## §4 Location and identifiers

The journal router is `.agent-workspace/decisions/index.md`. Entries live in a year-month directory beneath `.agent-workspace/decisions/` and use the filename pattern `YYYY-MM-DD-<class>-<slug>.md`. The identifier is the filename without its extension.

One file per decision avoids competing sessions appending to the same file. If the subject is later renamed, keep the historical path in the entry; the verifier can follow the rename through version history.

## §5 When to write

A law includes a rule, guide, role, lesson-store requirement, or deliverable standard. A minor wording edit does not need a journal entry when its entire meaning is already recoverable from the diff.

<rules section="ALWAYS">
- Apply the admission test when changing a law, answering a review comment that affects a law, or deciding scope, accepted debt, or a rejected alternative.
- Write an admitted decision during the same turn in which it is made, while its evidence and reasoning remain available.
</rules>

## §6 When to read

Search by repository-relative path and relevant stable section. A search result is a candidate record; the supersession relationships determine whether it still governs the subject.

<rules section="ALWAYS">
- Before changing a law, search the journal for its subject and read any standing decision that could conflict with the proposed change.
- Understand the earlier reason before reversing the decision.
</rules>

## §7 Subagents

Subagents do not write competing entries independently for the same coordinated task.

<rules section="ALWAYS">
- A subagent returns the decisions it made or identified together with their evidence.
- The orchestrator reconciles those results and writes any journal entries.
</rules>

## §8 Lifecycle

An entry is standing until a later entry supersedes it. The older entry then remains as history. Closing an accepted debt is also recorded by a later debt entry that supersedes the earlier one and states how the condition was satisfied.

Read the subject's entries and their supersession relationships to find the current decision. A newer timestamp alone does not establish that an unrelated entry replaced an earlier decision.

## §9 Volume and archive

The project sets its per-shard volume threshold in the journal router's `cap:` metadata. A warning invites examination of whether the journal is recording decisions or duplicating routine history; it is not a limit on the length of a decision's explanation.

Use `archive_decisions.py --year YYYY` to inspect archive candidates. Only superseded entries are eligible. Review the proposed moves under the task's authorization before applying them. An old but standing decision remains active, including when its subject was renamed.

## §10 Relationship to current guidance

Decision records preserve history; rules and guides state the requirements currently in force. Keep the two responsibilities separate.

<rules section="NEVER">
- Copy an entry's change history into the body of the requirement it describes.
</rules>
