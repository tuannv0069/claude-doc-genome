---
scope: portable
---

<critical>
scope: choosing the working role for a task, and writing a role file.
core: one primary role per task | checking roles contribute §6 only | the subtask's role travels in the dispatch prompt.
note: §ID append-only (portable) — never renumber; retired sections keep their number.
</critical>

# Role selection

## §1 When this applies

- apply role selection to every task, unconditionally.
- cond → a skill already owns the running flow → that skill decides; role selection does not intrude on it.

## §2 Choosing the role

Match against the work-type table in the hub `roles/index.md`. The six steps below are the matching procedure; the table itself lives only in the hub, never copied here.

1. Name the task about to start by the action it performs, never by the artifact it will change.
2. Scan the work-type column of BOTH tables to the last row before choosing — stopping at the first match hides the second one, and the row it hides is the one naming the lens the task lacked.
   - one row matched → it names the primary role; read that role file in full, and only the role file's §6 of each checking role on it
3. cond → two rows match → the more specific row gives the primary role; the other row's primary becomes a checking role.
   - a project row (hub §1a) outranks a genome row (hub §1)
   - within one table, a row naming a specific artifact or tool outranks a general one
4. cond → no row matches → skip role selection and continue; forcing a near-match wastes a read and misdirects the work.
5. cond → already matched this session and the work type has not changed → do not match again.
6. cond → the user names a role in their message → that role becomes the primary role, overriding the table match.

<rules section="NEVER">
- read a checking role's role-file §1 through §5 — colliding detail level (role file's §4) and decision criteria (role file's §3) between two full roles serves no one
</rules>

<example type="two_rows_match">
input: writing a document section that states which permissions may reach a screen — the section-writing row and the authorization row both match
❌ stop at the section-writing row because it matched first — the authorization row never enters, and the security lens the section most needed is the one left out
✅ scan to the last row of both tables, then apply the order below

input: answering a reviewer's comment on a sentence that describes a processing branch — the comment row and the branch-description row both match
❌ read both primary role files in full — two detail levels (role file's §4) and two sets of decision criteria (role file's §3) at once
✅ the comment row is the more specific one → its role is primary, read in full; the branch-description row's role drops to a checking role, read only its §6
</example>

<example type="name_by_action">
input: about to edit `screen-032-basic-design.md` to add a validation rule
❌ match the work type by the file name "basic design document"
✅ match the work type by the action — "writing content that describes system behaviour" — then look up that row
</example>

## §3 Writing a role file

A role file has exactly seven sections — call them **the role file's §1 through §7** below, to keep them distinct from this file's own §1–§7.

```markdown
---
scope: portable
---

<critical>
scope: <the kind of work this role wears> — one line
core: <the one thing this role exists to protect>
</critical>

# <Role>

## §1 Perspective — the unit this role counts
## §2 Priority questions
## §3 Decision criteria
## §4 Level of detail — where this role stops
## §5 Evidence — what counts as known
## §6 Not done until
## §7 Out of scope — handed to
```

Add no section beyond §7 and drop none; a retired section keeps its number and gains a bare `(retired)` marker (`doc-organization.md` §9). The `scope:` line inside `<critical>` is the only place that states the role's mission — never add a separate MISSION section.

Per-section content, and the form that fails it:

| role file's § | must contain | fails as |
|---|---|---|
| §1 | the countable unit this role judges by; paired with ✅/❌ | an attitude adjective, e.g. "looks at the big picture" |
| §2 | 3–6 questions, each answerable from the artifact itself | rhetorical questions; questions with no source to answer them |
| §3 | each criterion as `<condition> → what wins`; states the order when two criteria collide | a flat list of values with no stated winner |
| §4 | the unit where this role stops, e.g. "down to the screen", "down to the branch condition", "down to each data case" | "reasonably detailed", "as needed" |
| §5 | which sources count as known to this role; which sources are only a hypothesis | "must have evidence" with no source named |
| §6 | 3–4 lines shaped as "`<broken state>` still present → not done" | a checklist of "did X happen" ticks |
| §7 | what this role does not decide, naming the receiving role; the receiving role must exist in the router table; backticks mark the receiving role's name and nothing else, e.g. `` `qa` `` | "out of scope beyond this role" with no named receiver |

<rules section="ALWAYS">
- abstract clause in the role file's §1, §3, §5 → pair it with ✅/❌
- role file's §3 → state which criterion wins when two collide
- role file's §6 → write each line as a broken state, never as a completed-action tick
- role file's §7 → wrap only a receiving role's name in backticks; write a file name or a term plain
</rules>

Cap every role file at 90 lines, with no floor — shorter is not a defect; never pad a file with extra lines to reach a target length. cond → the first role file written satisfies every constraint in the table above and still exceeds 90 lines → stop, report the overrun to the user, propose a new cap; never raise the cap silently and never cut content to fit the old one.

## §4 Dispatching a subagent

This section is the single source of the subagent role-dispatch rule; any flow that dispatches a subagent points here rather than repeating it.

<rules section="ALWAYS">
- resolve the SUBTASK's role before dispatch, not the dispatching agent's own role
- pass the resolved role file's path inside the dispatch prompt text — a subagent does not inherit the parent's always-loaded surface
- assign exactly one primary role per dispatch
- cond → no role matched the subtask → state "no role matched" in the prompt text
</rules>

<rules section="NEVER">
- carry the dispatching agent's own role over to the subagent
- attach a checking role to a dispatch prompt alongside the primary role
- leave the role field blank when no role matched
</rules>

<example type="no_role_matched">
input: dispatching a subagent to rename a file across the repo
❌ omit the role line from the prompt because none of the work-type rows fit
✅ write `role: no role matched` in the prompt, so the subagent and its reviewer both see the check ran and found nothing
</example>

## §5 Adding a new role

| situation | action |
|---|---|
| a project needs a domain role outside software development, e.g. BrSE, DBA, SRE | create `roles/<role>.md` with `scope: project`, using the §3 frame; add its row to `roles/index.md` in the same commit |
| a project-scoped role proves useful across every project | promote it into the genome via `/init-project promote`; change its frontmatter to `scope: portable` |
| a portable role should behave differently on one project | never edit the portable file — `/init-project check` will report the drift; create a separate project-scoped role instead and repoint the router row to it |

<rules section="ALWAYS">
- new role's role-file §7 → name a role that exists in the router table
- delete a role → fix every role-file §7 that pointed to it, in the same commit (`doc-organization.md` link-integrity law)
</rules>

## §6 The router table format

The router table (`roles/index.md` §1) is a contract read by a machine gate (`verify_role_files.py`); it is stated here as law because the gate enforces it — changing the shape below without updating the gate breaks the gate, and changing the gate without updating this section makes the regex the law instead of this file.

- exactly three cells per data row
- the header row matches `| work type | primary role | checking roles |`, case-insensitively — the gate lowercases both sides before comparing
- the `primary role` cell holds exactly one role name, kebab-case, not wrapped in backticks
- the `checking roles` cell holds role names separated by commas, not wrapped in backticks; it may be empty
- every role name in either cell names a file that exists under `roles/` (kebab-case, matching that file's stem with no extension)
- every file under `roles/` other than `index.md` is named by at least one data row, in either cell

<rules section="NEVER">
- wrap a role name in the router table in backticks — the gate parses the raw cell text
- widen a data row past three cells, or split `checking roles` on anything but a comma
</rules>

## §7 A role file against the rest of the project's documentation

A role file states how one role reasons; it never states what this project's documentation system permits.

<rules section="ALWAYS">
- role file's §3, §5 or §6 collides with a guide or an always-loaded rule → the project's rule wins, and the work proceeds under it
- collision found → fix the role file, or create a `scope: project` role carrying the project's rule and repoint the router row to it (§5)
- collision reported → name the colliding clause and the rule's `§ID` in the same report; an unnamed collision is read as a role-file clause by the next agent
</rules>

<rules section="NEVER">
- follow a role file's clause over a guide or an always-loaded rule that says otherwise
- edit a `scope: portable` role file to carry one project's rule — the project-scoped replacement is the route (§5)
</rules>

<example type="role_clause_loses">
input: a role file's §5 treats a fact read from the system under analysis as a hypothesis until an outside party confirms it, while the project's evidence guide names the sources the team already holds as sufficient
❌ follow the role file, and record the fact as unknown pending an outside answer
✅ follow the project's guide, then fix the role file or route the row to a `scope: project` role
</example>

<critical_recap>
1. role selection runs unconditionally, except inside a flow a skill already owns.
2. one primary role per task; a checking role contributes only its role-file §6.
3. a subtask gets its OWN role, never its dispatching agent's; exactly one primary role, no checking role, and "no role matched" is written out, never left blank.
4. a role file is always seven sections, capped at 90 lines with no floor, and never edited on the portable copy to fit one project.
5. the router table's three-cell, plain-text-role-name shape is a gate contract, not a style choice — changing it changes what the gate can read.
</critical_recap>
