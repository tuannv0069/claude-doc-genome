---
scope: portable
---

# Learning from failed working methods

Use this guide when a correction or observed failure reveals a method that should change for future tasks. A lesson is an evidence-backed record of an incident, not an automatically binding new law.

## §1 Choose the right store

A lesson about how to perform work belongs in `.agent-workspace/lessons/<work-type>.md`. A fact about the project belongs in the project's work-product area under `.claude/rules/doc-organization.md` §11. A user identity or preference that outlives the project belongs in the memory mechanism available for that purpose.

Keep raw lesson records separate from curated guidance. A lesson records what happened and what to try instead; a guide states a requirement that has been evaluated for wider use.

## §2 When to capture a lesson

Record a repeatable method failure when the user corrects the approach or rejects an output, when an existing rule fails to prevent a recurring defect, when a probe produces a confidently wrong answer, or when a fix disproves the earlier diagnosis.

Record the method that made the error likely, rather than a one-off fact about the artifact. For a misleading probe, preserve the query or checking technique that failed. For an incorrect diagnosis, preserve the evidence that made it appear plausible and the evidence that disproved it.

Capture the lesson in the same turn. If the same lesson already exists, update its recurrence count instead of adding a duplicate. This recording is part of the working process and does not require a separate permission request.

## §3 Record content

Use one store per work type, named for the action it protects. Register the store in `.agent-workspace/lessons/index.md` §1 when it is created.

A record identifies the recognizable situation, the method that failed, why it appeared reasonable, the method that should be tried instead, the supporting evidence, and the recurrence count. Existing records may use `signal`, `❌`, `✅`, `evidence`, and `seen` labels. These are storage conventions, not a required sentence pattern.

Promotion evaluates the scope of the requirement supported by the incidents under §4. The record supplies evidence for that decision.

If a new lesson protects an action outside the store's declared scope, adjust the store's scope or select a more appropriate store. Preserve the meaning and source of quoted evidence.

## §4 Escalation

The first occurrence produces a record. On recurrence, evaluate whether the lesson should become a requirement in the guide for that work type. A third occurrence is a reason to build a verification mechanism when the condition can be decided reliably by a program. A mechanically decidable failure can justify that mechanism earlier.

Distill the supported requirement from the incidents rather than copying the entire record into a guide. Preserve the records as evidence. A check should fail on the demonstrated defect and pass on legitimate work; otherwise it replaces an unreliable habit with an unreliable gate.

Do not promote a lesson directly into the always-loaded tier merely because it recurred. Placement still follows `.claude/rules/doc-organization.md` §8.2 and §8.3.

## §5 Making a store reachable

The primary entry point is the lesson router described in §7. When a work type already has a paired guide, that guide can also link to its store for a reader arriving through the guide. A store without a paired guide needs only its router registration.

Split a store when its contents protect different work types, not merely because the file has grown. Keep its live references correct after a move.

## §6 Related procedures

Use `five-why.md` §2 when the record cannot yet explain the failed method. Use `.claude/rules/doc-organization.md` §1 to distinguish a record from a rule or project fact, and its §8.3 when promoting new guidance.

## §7 Lookup and delegation

At the start of a task, consult `.agent-workspace/lessons/index.md` §1. Match the action about to be performed against the router's work types. Read every matching store and the stores named in its `checks` cell. Follow only that one additional hop.

When no row matches, continue without forcing a near match. Do not repeat the lookup while the task and work type remain unchanged. A new action that matches another work type requires the corresponding lookup.

Register each store only in this router. The unconditional task-start lookup already makes it reachable, so a new store does not need a separate always-loaded trigger.

When delegating work, pass the matched store paths and their one-hop checks to the subagent. In coordinated work, subagents return candidate lesson records and the orchestrator writes them, avoiding concurrent edits to the same store.

The router has the columns `file`, `work type`, `paired guide`, and `checks`. The verifier reads these columns as data. Work-type descriptions identify actions; store names in `checks` identify existing stores.

## §8 Select the phase being protected

Choose the store by asking which phase would avoid the failure on its next run. When a review discovers a writing-method defect, record the lesson for writing. If the review technique itself failed, record it for reviewing.

Each store declares `scope:` and `phase:` in its `<critical>` metadata block. The phase values are `writing`, `reviewing`, `answering`, `building-gate`, `orchestrating`, `investigating`, and `operating`. A store that requires separate phases should be split accordingly. A store may instead declare the protected action as `work_scope:` and the phase as `phase:` in its frontmatter; the verifier accepts either form so that one shared `.agent-workspace/` can be checked by every supported agent. Use one form consistently within a store; the frontmatter `scope:` field classifies portability and is not the protected action.

If both the producing and inspecting phases are affected, store the lesson once with the producing phase and let the inspecting phase reach it through `checks`. Keep that relationship acyclic.

When a record moves, preserve its recurrence count. Existing readers can be redirected with a `[[wikilink]]` rather than a duplicate record. Do not rewrite frozen task history to replace old store names; maintain the references in guidance that remains live.
