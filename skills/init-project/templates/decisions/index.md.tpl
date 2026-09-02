---
scope: project
cap: {{DECISION_CAP}}
---

<critical>
scope: router of the decision journal — where an entry lives, its shape, how to query it.
never: list entries here | edit or delete an entry | record what `git log` reconstructs
always: one decision one file | read the law before writing an entry — `.agent-workspace/guide/general/decision-journal.md`
</critical>

# Decision journal

git holds what changed. This journal holds what a diff cannot reconstruct: the option not taken, the scope call, the debt accepted on purpose, the law that turned out wrong.

## §1 What is admitted

Five classes, admission test, entry shape → `guide/general/decision-journal.md` §1-§3.

`cap:` in the frontmatter is this project's per-shard entry ceiling — the gate reads that line (§9). Above it the gate warns: entries are recording what git already holds.

## §2 Layout

```
YYYY-MM/YYYY-MM-DD-<class>-<slug>.md   standing entries
archive/YYYY/                          entries a later entry superseded
```

## §3 Queries

| question | command |
|---|---|
| decision history of a file or a law | `rg -l "subject: <path>" .agent-workspace/decisions --glob '!archive/**'` |
| every decision of one class | `rg -l "^class: rule" .agent-workspace/decisions` |
| what overturned this entry | `rg -l "supersedes: <id>" .agent-workspace/decisions` |
| current state of a subject | grep the subject, read backwards, stop at the first entry nothing supersedes |

## §4 Gate

```
python .agent-workspace/tooling/verify_decision_log.py
python .agent-workspace/tooling/archive_decisions.py --year YYYY
```

A seeded journal — this router alone, no shard directory — passes with zero entries. An entry is written when a decision is made, never upfront (`decision-journal.md` §5).
