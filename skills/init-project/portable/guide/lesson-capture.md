---
scope: portable
---

<critical>
scope: a working method just failed — a user correction, a repeated failure, a probe that gave a confident wrong answer. Record it so the next run of the same work type does not repeat it.
never: keep a work-method lesson only in harness memory, paste a record into a guide, or promote a record straight into the always-loaded tier.
note: read-back is unconditional and routed by `.agent-workspace/lessons/index.md` §1 alone (§7); the store is chosen by the phase the lesson protects (§8); a method that met its expectation is not a lesson and is routed to `method-review.md` §5 by the table in §1.
</critical>

# Learning from failed working methods

Use this guide when a correction or observed failure reveals a method that should change for future tasks. A lesson is an evidence-backed record of an incident, not an automatically binding new law.

## §1 Choose the right store

Keep raw lesson records separate from curated guidance. A lesson records what happened and what to try instead; a guide states a requirement that has been evaluated for wider use. The destinations hold different content classes and do not overlap; the last row routes a method that succeeded out of this guide, because a success is not a lesson.

| what was learned | store |
|---|---|
| how to perform a kind of work: a query form, a tool choice, a step order, a probe that misled | `.agent-workspace/lessons/<work-type>.md` |
| a fact about the project: a term, a decision, official knowledge | the project's work-product area under `.claude/rules/doc-organization.md` §11 |
| the owner's reaction to, or approval of, a creative passage (a title, a hook, a line of narration) | a taste note in the project's taste store under `creative-work.md` §3 and §5, not a lesson |
| who the user is, or a preference that outlives this project | the memory mechanism available for that purpose |
| a method that met the expectation recorded for it before release | the review record kept with the work product, and the standard that owns the method once it has held twice, under `method-review.md` §5 |

<example type="store_choice">
input: the user says to stop globbing the shared test directory and run only this task's tests
❌ write it to harness memory, where it is invisible to the next agent working in the repository
✅ record it under the work type; distill it into the file-reading rule when it recurs
</example>

## §2 When to capture a lesson

Record the method that made the error likely, rather than a one-off fact about the artifact. For a misleading probe, preserve the query or checking technique that failed. For an incorrect diagnosis, preserve the evidence that made it appear plausible and the evidence that disproved it. Recording is part of the working process, not a separate request.

<rules section="ALWAYS">
- Record a lesson when the user corrects the approach, rejects an output or redirects the method.
- Record a lesson, and escalate under §4, when an existing rule fails to prevent a recurring defect.
- Record the query form when a probe or script answered confidently and proved wrong.
- Record what made the earlier diagnosis look right when a fix disproves it.
- Capture the lesson in the same turn in which the signal appears.
</rules>

<rules section="NEVER">
- Record a one-off fact about the artifact being worked on; that belongs in the work product.
- Add a duplicate record for a lesson that already exists; update its recurrence count instead.
- Ask permission to record; the store is a capture layer, not established truth.
</rules>

## §3 Record content

A record identifies the recognizable situation, the method that failed, why it appeared reasonable, the method that should be tried instead, the supporting evidence, and the recurrence count. Existing records may use `signal`, `❌`, `✅`, `evidence`, and `seen` labels. These are storage conventions, not a required sentence pattern. Promotion under §4 evaluates the scope of the requirement supported by the incidents; the record supplies the evidence for that decision.

<rules section="ALWAYS">
- Use one store per work type, named for the action it protects.
- Register a new store in `.agent-workspace/lessons/index.md` §1 in the same change that creates it.
- Write records in the language of the guide the store pairs with, so that a promotion is a copy rather than a translation.
- When a new lesson protects an action outside the store's declared scope, widen that scope or select a more appropriate store.
- Preserve the meaning and source of quoted evidence.
</rules>

<example type="file_name">
input: naming the store for lessons about reading legacy source
❌ `legacy-source.md` names the subject and matches no trigger
✅ `read-legacy-source.md` names the action the trigger fires on
</example>

## §4 Escalation

Prose can be skipped; a failing check cannot. Distill the supported requirement from the incidents rather than copying the entire record into a guide, and preserve the records as evidence.

| recurrence | action |
|---|---|
| first occurrence | a record under §3 |
| second occurrence | evaluate whether the lesson becomes a requirement with a stable identifier in the guide for that work type; the record stays |
| third occurrence, or a condition a program can decide reliably at any count | build a verification mechanism that fails on the defect; the requirement stays as the human-readable reason |

<rules section="NEVER">
- Promote a lesson directly into the always-loaded tier merely because it recurred; placement follows `.claude/rules/doc-organization.md` §8.2 and §8.3.
- Ship a check that fires on legitimate work; an unreliable gate replaces an unreliable habit.
- Copy record text into a guide; distill it to the requirement it supports.
</rules>

<example type="escalation">
input: the same wrong query form has now cost three passes
❌ append a third near-identical record; the store grows and the next run repeats it anyway
✅ record the third occurrence and write the check that fails on that form, keeping the requirement as the reason
</example>

## §5 Making a store reachable

The primary entry point is the lesson router described in §7. When a work type already has a paired guide, that guide can also link to its store for a reader arriving through the guide. A store without a paired guide needs only its router registration. The store is never loaded on every turn, so it may grow.

<rules section="ALWAYS">
- Read the store before starting the work, not after failing.
- Split a store only when its contents protect different work types, not because the file has grown.
- Keep a store's live references correct after a move.
</rules>

## §6 Related procedures

Use `five-why.md` §2 when the record cannot yet explain the failed method. Use `.claude/rules/doc-organization.md` §1 to distinguish a record from a rule or project fact, and its §8.3 when promoting new guidance. This guide corrects a step inside the method the project already follows; the question of whether that method should remain the method is asked at the review points of `method-review.md` §2, whether or not any lesson was recorded.

## §7 Lookup and delegation

Routing one trigger per work type prices read-back on the always-loaded budget, so a new store's default state would be unreachable. The lookup is unconditional instead: the cost stops growing and registration alone makes a store live. The router has the columns `file`, `work type`, `paired guide`, and `checks`; the verifier reads these columns as data.

<rules section="ALWAYS">
- At the start of a task, consult `.agent-workspace/lessons/index.md` §1 and match the action about to be performed against the router's work types.
- Read every matching store and the stores named in its `checks` cell, following only that one additional hop.
- Before the first substantive step of the task, state the result of the lookup in the reply: each store read and the entries whose situation applies, or, when nothing matched, the router rows considered and why the action falls outside them.
- Write that statement from the files just read; its purpose is to make an omitted or inferred lookup visible to a reader who did not watch the reading, and a statement that could have been written without opening the router does not serve it.
- Cover a task with one statement; repeat it only when a new action matches another work type and requires its own lookup.
- Write a router work-type cell as the action about to be performed, not as a topic name.
- When delegating work, pass the matched store paths and their one-hop checks to the subagent, which may not inherit the always-loaded surface.
- In coordinated work, let subagents return candidate lesson records and let the orchestrator write them, so that concurrent edits to one store do not lose writes.
</rules>

<rules section="NEVER">
- Add a per-work-type always-loaded trigger for a store; the unconditional lookup already reaches it.
- Register a store in a second router; `.agent-workspace/lessons/index.md` §1 is the only one.
- Read a near-miss store because no row matched; a wrong lesson costs more than no lesson.
- Repeat the lookup while the task and work type remain unchanged.
- Make a router condition a task class such as a substantive or complex task; a class needs judgment and fails `.claude/rules/doc-organization.md` §10.
</rules>

<example type="work_type_cell">
input: the router cell for the store about verifying a design before implementing
❌ `design verification`, a topic name the agent must guess its work belongs to
✅ `about to verify a design or write a verification gate`, an action matched against what the agent is doing
</example>

<example type="new_store_cost">
input: a lesson store for a work type that has no guide
❌ a new store, a new `CLAUDE.md` trigger and a new row in the guide router
✅ a new store and one row in `.agent-workspace/lessons/index.md` §1; the unconditional lookup already routes to it
</example>

## §8 Select the phase being protected

A store is chosen by the phase the record protects, never by the task that happened to be running when the record was written. The two coincide for self-contained work; they diverge whenever a task inspects the output of another phase, and that is where records land in the wrong store.

Each store declares `scope:` and `phase:` in its `<critical>` metadata block. The phase values are `writing`, `reviewing`, `answering`, `building-gate`, `orchestrating`, `investigating`, and `operating`. A store may instead declare the protected action as `work_scope:` and the phase as `phase:` in its frontmatter; the verifier accepts either form so that one shared `.agent-workspace/` can be checked by every supported agent. Use one form consistently within a store; the frontmatter `scope:` field classifies portability and is not the protected action.

<rules section="ALWAYS">
- When choosing a store, ask which phase would avoid the failure on its next run, and give the record to that phase's store.
- When a review discovers a writing-method defect, record the lesson for writing; when the review technique itself failed, record it for reviewing.
- When both the producing and inspecting phases are affected, store the lesson once with the producing phase and let the inspecting phase reach it through `checks`.
- Split a store that would need two phase values into two stores.
- Read the matched store plus the stores its `checks` cell names, and no further.
- When a record moves between stores, preserve its recurrence count and redirect existing readers with a `[[wikilink]]` rather than a duplicate record.
</rules>

<rules section="NEVER">
- Let the `checks` relation form a cycle.
- Rewrite frozen task history under `.agent-workspace/tasks/**` or `.agent-workspace/worktrees/**` to replace an old store name; that text records what happened, and references are maintained only in guidance that remains live.
</rules>

<example type="phase_choice">
input: a review pass finds a section whose coverage was scoped from a sibling section instead of from the source
❌ record it in the review store because the review found it; the writer never reads that store before writing, so the next section repeats it
✅ record it in the writing store, and give the review store a `[[wikilink]]` if reviewers also need the signal
</example>
