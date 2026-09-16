---
scope: project
cap: {{DECISION_CAP}}
---

# Decision journal

This journal records reasons and choices that a diff cannot reconstruct. Read `.agent-workspace/guide/general/decision-journal.md` before creating or interpreting an entry.

## §1 Admission

The admission test, decision classes and entry schema are defined in `.agent-workspace/guide/general/decision-journal.md` §1, §2 and §3. The project's `cap` value is a review threshold for the number of entries in a shard, as described in that guide's §9; it is not a limit on the length of a decision.

## §2 Layout

Store active entries under `YYYY-MM/YYYY-MM-DD-<class>-<slug>.md`. Archived entries live under `archive/YYYY/`. Use the lifecycle in `.agent-workspace/guide/general/decision-journal.md` §8 to identify which decisions have been superseded.

## §3 Queries

Search a subject with `rg -l "subject: <path>" .agent-workspace/decisions`. Search `supersedes: <id>` to find entries that overturn an earlier decision. Read the resulting chain to determine the current choice; a later date alone does not supersede another entry.

## §4 Tools

Run `python .agent-workspace/tooling/verify_decision_log.py` to validate the journal. Use `python .agent-workspace/tooling/archive_decisions.py --year YYYY` for the archive procedure defined in `.agent-workspace/guide/general/decision-journal.md` §9.

A newly initialized journal contains this router and no entries. Create an entry when there is an actual decision to record.
