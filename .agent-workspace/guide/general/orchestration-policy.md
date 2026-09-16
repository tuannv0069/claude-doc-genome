---
scope: portable
---

# Coordinating work across agents

This guide covers tasks whose coordination is not already owned by a skill. Its purpose is to preserve responsibility, context, and verifiable results across work boundaries.

## §1 When this applies

Use the coordination procedure for work divided across files, agents, or dependent phases. A small isolated task can remain with the current agent when delegation would add no useful independence or capacity.

For research, avoid delegating material the current agent already knows merely to repeat the reading. The persistence requirements in §6 still apply. A skill that owns a workflow determines its own coordination procedure.

## §2 Coordination and execution

The coordinating agent owns the task's scope, plan, assignments, integration, and final verification. An executor owns the bounded result assigned to it.

Delegate independent multi-file implementation when an executor can work from a self-contained plan and the coordination cost is justified. Keep a small change in the current context when an additional agent would need to reread the same material for little benefit. A difficult change can remain with the coordinating agent or receive an executor with suitable capability.

Do not assign overlapping edits without an explicit ownership arrangement. An agent that can produce a result still needs to know which files it owns and which decisions belong to another participant.

## §3 Select capability for the reasoning required

Choose model capability and reasoning effort from the difficulty of the assignment, the consequences of an error, and the interfaces it crosses. A subtle condition in one file can demand more reasoning than a mechanical change across many files.

Do not force a difficult task onto a weaker executor and rely on repeated repair rounds to compensate. Conversely, a mechanical task does not need maximum effort merely because the overall project is large. Use only model choices supported and authorized in the current environment.

## §4 Persist the working state

Before delegation, save the plan in `.agent-workspace/tasks/<task-slug>/`. Include the requested outcome, targets, ownership, dependencies, acceptance criteria, and verification. Keep that file current when the plan changes.

Executors and reviewers should be able to resume from this saved state without relying on the coordinating agent's memory. Keep evidence and intermediate artifacts in the same task workspace. Redirect a skill's temporary output there when its default location would scatter task state elsewhere.

Do not place temporary working state among finished project documents, or inside a disposable worktree whose removal would erase the only copy. Finished work products belong at the location selected under `.claude/rules/doc-organization.md` §11.

## §5 Task-workspace lifecycle

Use one workspace directory for each task and keep it separate from other active tasks. The project ignores `.agent-workspace/tasks/` and `.agent-workspace/worktrees/` in version control; curated guides, lessons, and intended deliverables have separate lifetimes.

When a task closes, first preserve anything that must outlive it. A reusable method belongs in the lesson store, a project fact belongs in a work product, and an approved governing requirement belongs in its guide. Then remove the closed task's disposable state when doing so cannot lose unfinished or untransferred work.

Do not treat an old task plan as the current plan for a new task. If task state is retained because the work remains active, its status must accurately describe that state.

## §6 Persist research while it is happening

When research passes its third file read or search, or when it is delegated, save the developing findings in the task workspace. Do this during the work so context loss cannot erase the only record before the final answer.

Keep source locations, established facts, unresolved questions, and the next dependency in that record. Transfer findings with lasting project value to their durable destination before closing the task.

A lookup that already resolves a single fact does not need a separate research artifact.

## §7 Use independence when it is the point of delegation

An independent reader can inspect what the author did not consider. Use one when the work requires an absence check, a comparison of the finished result with its source, or a challenge to a consequential claim.

Give that reader the requirements, artifact, and scope needed for the check. Avoid supplying the author's conclusion as the premise the reviewer is expected to confirm.

This use of delegation differs from assigning several agents to repeat the same search for speed. The useful result is an independent assessment, not duplicated reading.
