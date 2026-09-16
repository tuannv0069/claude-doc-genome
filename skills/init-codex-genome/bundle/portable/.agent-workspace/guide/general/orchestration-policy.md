---
scope: portable
---

# Coordinating execution and preserving task state

## §1 Keep responsibility explicit

The coordinating assistant owns scope, assignments, dependencies, integration and final verification. An executor owns the bounded result it is assigned. A skill with an established coordination procedure owns that sequence; this guide supplies the fallback when no skill does.

## §2 Use delegation for useful independence

Delegate independent implementation when the task permits it, the assignment is self-contained and the benefit exceeds the context and coordination cost. Keep a small change or an already-understood investigation in the current context when delegation would mainly duplicate reading. Respect client and task restrictions on subagents.

Use an independent reader for consequential absence checks, comparisons with source evidence and challenges to assumptions. Give that reader the requirements and artifact without making the author's conclusion the premise to confirm. If an independent reader is unavailable, report the limitation in the resulting acceptance evidence.

Choose supported capability from the reasoning difficulty and consequences of the assignment. Do not force difficult reasoning onto a weaker executor merely because the edit is small. Do not override models or effort universally.

## §3 Define ownership before dispatch

Assign non-overlapping edits or explicitly agree how shared files are coordinated. Provide the root directory, exact targets, sources, interfaces and checks. Pass the applicable role and lesson paths; the child may not receive the parent's context. Ask an executor to return decisions and lesson candidates so the coordinator can reconcile shared records.

Do not treat a child completion message as integration evidence. Inspect returned artifacts, check the interface with adjacent work and run the acceptance checks appropriate to the combined result.

## §4 Persist developing work

Before delegating or editing more than three files, save a plan under `.agent-workspace/tasks/<task-slug>/`. Record outcome, ownership, dependencies, acceptance evidence and current status. When research passes its third read or search, or is delegated, persist sources, findings, open questions and the next dependency there while the work is still underway.

Keep task evidence outside installed skills and disposable checkouts. A delegate or future session must be able to resume from the saved state. Do not reuse a closed task's plan as if it governed newly requested work.

## §5 Close without losing useful work

Ignore `.agent-workspace/tasks/` and `.agent-workspace/worktrees/` in version control. Before removing closed task state, transfer durable deliverables, accepted requirements and reusable lessons to their proper owners. Inspect the exact paths and retain unfinished or untransferred work.

Clean only the task storage covered by the current work and preserve records or artifacts that another active task still needs. Follow `worktree.md` §3 for isolated checkout cleanup.

## §6 Preserve research before context is lost

The third read or search, or the first delegated research pass, is the checkpoint for writing sources and developing findings under `.agent-workspace/tasks/<task-slug>/`. Record enough context for another supported agent to continue from the same evidence. This checkpoint applies to the shared project workspace; it does not create a harness-specific research store.
