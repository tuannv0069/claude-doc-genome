---
scope: portable
---

<critical>
scope: the decision journal — which decisions are recorded, when an entry is written, how it is read back and retired.
core: five classes only | grep before changing a law | write in the same turn as the decision | entry append-only — superseded, never edited
note: §ID append-only (portable) — never renumber; retired sections keep their number.
</critical>

# Decision journal

git holds what changed. The journal holds what a diff cannot reconstruct: the option not taken, the branch judged out of scope, the debt accepted on purpose, the law that turned out wrong.

## §1 Admission test

One question decides every candidate: **delete the entry — can `git log` still reconstruct the conclusion?**

- reconstructable → do not write
- not reconstructable → write it under one of the five classes (§2)

Volume is controlled here, not by archiving. A shard past the project's cap (§9) means entries are recording diffs.

## §2 The five classes

| class | records | admitted when |
|---|---|---|
| `choice` | option taken, option rejected, the reason | two viable approaches existed |
| `scope` | a thing judged out of scope or not applicable | the work leaves no diff |
| `debt` | the gap accepted + the condition that unlocks it | a known limit ships on purpose |
| `rule` | a law changed: what it says now, what it stopped saying | any law file is edited |
| `review` | reviewer comment answered: conclusion + root-cause class + law touched | the fix traces to a rule |

A `review` entry holds the **authoritative** root-cause class. The working record under `.agent-workspace/tasks/` and the answer written back to the reviewer are working copies — they lose to the entry.

## §3 Entry — one decision, one file

```markdown
---
class: rule
subject: .claude/rules/doc-organization.md §12
supersedes: 2026-08-11-rule-doc-org-tier-order
anchor: lessons/<store>.md · a1b2c3d
---
- decided: law ships with its artifacts and its gate in one commit
- because: a gate landing alone makes the regex the law
- rejected: gate first, law after — nobody reading the standards can find the rule
```

<rules section="ALWAYS">
- `subject` → a repo-relative path that exists, `§ID` optional
- `anchor` → the evidence or commit the decision rests on
- body → `decided:` first, 4 lines maximum
- `supersedes` → id of the entry this one overturns; omit when it overturns none
</rules>

<rules section="NEVER">
- edit or delete an entry — a wrong entry is corrected by a later entry that supersedes it
- record progress, verification steps, or what a file now contains — git, the evidence ledger and the status tracker own those
</rules>

## §4 Location and id

```
.agent-workspace/decisions/index.md                              router: entry shape + query patterns
.agent-workspace/decisions/YYYY-MM/YYYY-MM-DD-<class>-<slug>.md  one entry
.agent-workspace/decisions/archive/YYYY/                         retired entries
```

id = file name without extension. One file per entry — parallel sessions and worktrees never append to the same file.

Renamed subject → the gate resolves the old path through `git log --follow`; the entry stays as written.

## §5 When to write

cond → about to edit a law file (`.claude/rules/**`, `.agent-workspace/guide/**`, role files, lesson stores, a deliverable-standard file), to write an answer to a reviewer comment, or to declare a scope call / accepted debt / rejected option in any artifact
→ write the entry in the same turn.

The condition is the agent's own next action on a named object, decided before that call — never a judgment about how significant the decision felt.

## §6 When to read

cond → about to change a law → grep the journal for that subject first.

```bash
rg -l "subject: <path>" .agent-workspace/decisions --glob '!archive/**'
```

A standing entry that decided the opposite is read before the law is reversed again.

## §7 Subagents

<rules section="ALWAYS">
- subagent → return its decisions as `decisions:` blocks in its report; write no entry
- orchestrator → merge the returned blocks and write the entries when the fan-out returns
</rules>

A subagent does not inherit the project index file, and its context dies at return — an unwritten decision dies with it.

## §8 Lifecycle

| state | reached by | reads as |
|---|---|---|
| standing | default | the current decision for that subject |
| superseded | a later entry names its id in `supersedes` | historical |
| closed | a later `debt` entry supersedes it | historical |

Read a subject backwards; stop at the first entry no later entry supersedes.

## §9 Volume and archive

- project declares the per-shard entry cap in `cap:` of its own `.agent-workspace/decisions/index.md`; the gate warns above it
- year boundary → `archive_decisions.py --year YYYY`; it lists what it will move and asks before moving
- archivable = an entry some later entry supersedes — a closed `debt` is closed by superseding it; nothing else moves, and a live subject whose path was renamed stays

## §10 Relation to the no-history law

A journal entry is a record file, not a document. The ban on writing change history into a file's body governs rules, guides, standards and deliverables; it does not reach `.agent-workspace/decisions/`. Nothing in the journal is copied back into the file it describes.

<critical_recap>
1. admission test — `git log` reconstructs it → do not write it
2. write in the same turn as the decision; read before reversing a law
3. entries are append-only — supersede, never edit
4. subagents report decisions, the orchestrator writes them
5. archive only what a later entry supersedes
</critical_recap>
