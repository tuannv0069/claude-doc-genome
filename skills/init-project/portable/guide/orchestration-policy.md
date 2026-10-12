---
scope: portable
---

<critical>
scope: a multi-step or multi-agent task that no skill owns, where the main model coordinates the work directly.
never: keep the only copy of a plan or of research findings in the conversation; write it to the task workspace while working.
note: delegate execution across many files; keep research and small edits inline; escalate hard reasoning instead of repairing a weak executor.
</critical>

# Coordinating work across agents

This guide covers tasks whose coordination is not already owned by a skill. Its purpose is to preserve responsibility, context, and verifiable results across work boundaries.

## §1 When this applies

Use the coordination procedure for work divided across files, agents, or dependent phases. A small isolated task can remain with the current agent when delegation would add no useful independence or capacity. A skill that owns a workflow determines its own coordination procedure.

<rules section="ALWAYS">
- Apply §2 to §4 to a task that edits several files or dispatches an agent.
- Apply §6 to research and investigation even when nothing is delegated and no file changes.
</rules>

<rules section="NEVER">
- Delegate material the current agent already knows merely to have it read again.
</rules>

## §2 Coordination and execution

The coordinating agent owns the task's scope, plan, assignments, integration, and final verification. An executor owns the bounded result assigned to it. An agent that can produce a result still needs to know which files it owns and which decisions belong to another participant.

<rules section="ALWAYS">
- Delegate independent multi-file implementation when an executor can work from a self-contained plan and the coordination cost is justified.
- Keep a small change in the current context when an additional agent would need to reread the same material for little benefit.
- Keep a difficult change with the coordinating agent, or give it to an executor with suitable capability.
- Give each executor an explicit ownership arrangement before assigning edits that could overlap.
</rules>

<rules section="NEVER">
- Delegate a search, a reading or an analysis to a subagent when the coordinating agent already holds the context.
- Block a small inline edit behind a subagent whose spawn and rereading cost exceeds the edit.
</rules>

<example type="delegation">
input: apply a multi-file change across several modules
✅ dispatch an implementer with the saved plan; the coordinating agent verifies the result
❌ the coordinating agent edits every file itself
</example>

<example type="inline_edit">
input: fix three files already in context, fewer than fifty lines of edits in total
✅ edit inline; the context is already warm and nothing needs rereading
❌ spawn an implementer that must reread all three files and their dependencies
</example>

<example type="inline_research">
input: investigate the root cause of a recurring defect by searching, reading and reasoning
✅ the coordinating agent searches, reads the relevant sections and reasons over the findings inline
❌ spawn three subagents to search in parallel, each rereading overlapping files
</example>

## §3 Select capability for the reasoning required

Choose model capability and reasoning effort from the difficulty of the assignment, the consequences of an error, and the interfaces it crosses. A subtle condition in one file can demand more reasoning than a mechanical change across many files.

An agent that is dispatched without a named model takes whatever the environment gives it by default, which in many environments is the coordinating agent's own model. Routine work then runs at the price of the hardest work in the task. The table below sorts work into three capability tiers. The tier names are the same in every project; the project's entry point maps each tier to a model and to effort levels that its environment supports. Environments differ in where effort is set: some accept it with each dispatch, and others read it only from the definition of the agent being dispatched.

| tier | work that belongs to it | reasoning effort |
|---|---|---|
| standard | Work with a definite answer or a complete plan: locating files or code, converting a format, running checks and reporting the result, applying a change that is already specified, implementing from a detailed specification, summarizing sources, drafting a document from established facts, reviewing against an existing checklist. | medium for locating, converting, running checks and applying a specified change; high for the rest |
| strong | Work that needs judgment, or in which an error is costly: a design, a root-cause investigation, a change to a governing rule, writing or reviewing creative text, verifying a fact, an independent review of strong-tier work. | high |
| highest | The hardest reasoning, where a wrong result is costly, hard to detect and hard to reverse: a decision on architecture or method that many later steps depend on, or a problem that a strong-tier attempt has failed to solve. | high, and above high only for a problem that a high-effort attempt has failed to solve |

<rules section="ALWAYS">
- Select the tier from the table by the hardest part of the assignment.
- Select effort from the reasoning difficulty; the number of files is a signal, not the measure.
- Split a mixed batch across agents by difficulty rather than assigning one effort to all of it.
- Name the model in every dispatch, taken from the project's mapping of the tiers, unless the agent's own definition already fixes its model.
- Set the reasoning effort of every dispatch from the same row of the table as its model, in the dispatch itself where the environment accepts it there and otherwise through an agent definition that carries that effort.
- Use only model and effort choices supported and authorized in the current environment.
- Move an assignment up one tier after an executor at the current tier has failed it once.
- Give an independent reviewer a tier at least as high as the tier that produced the work under review.
- State in the plan or the dispatch why the strong tier is not enough whenever the highest tier is selected.
- Lower the tier of a workflow step only after a run at the lower tier has passed that step's verification, and compare the cost of the two tiers from the run records of `workflow-measurement.md` §3.
</rules>

<rules section="NEVER">
- Dispatch an agent without a named model and leave it to take the environment's default.
- Leave the reasoning effort of a dispatched agent to the coordinating session's setting when the environment offers a way to set it.
- Force a difficult task onto a weaker executor and rely on repeated repair rounds to compensate.
- Raise a mechanical task to maximum effort merely because the overall project is large.
- Select the highest tier for work that the strong tier handles.
- Use a model below the one the project maps to the standard tier unless the user chooses it for that dispatch.
</rules>

<example type="effort_not_scope">
input: a one-file change touching tricky conditional logic
✅ high effort; the difficulty is high although the scope is small
❌ medium effort because only one file changes
</example>

<example type="tier_selection">
input: a task needs a list of every file that imports one module, and a decision on how to split that module
❌ dispatch both to agents with no model named; both run on the coordinating agent's model
✅ dispatch the file listing at the standard tier and the split decision at the strong tier, each with the model and the effort the project maps to its tier
</example>

## §4 Persist the working state

Executors and reviewers should be able to resume from saved state without relying on the coordinating agent's memory. Finished work products belong at the location selected under `.claude/rules/doc-organization.md` §11.

<rules section="ALWAYS">
- Before delegation, save the plan in `.agent-workspace/tasks/<task-slug>/` with the requested outcome, targets, ownership, dependencies, acceptance criteria, and verification.
- Keep that file current when the plan changes; a stale plan is worse than none.
- Keep evidence and intermediate artifacts in the same task workspace.
- Redirect a skill's temporary output to the task workspace when its default location would scatter task state elsewhere.
</rules>

<rules section="NEVER">
- Place temporary working state among finished project documents.
- Scatter working files outside `.agent-workspace/tasks/`, such as the repository root or `docs/`.
- Store the plan inside a disposable worktree whose removal would erase the only copy.
</rules>

<example type="persistence">
input: coordinate a two-step review and fix over many findings
✅ write the plan to a file in the task workspace; agents and verification rounds read it back
❌ keep the mapping of findings to agents only in the conversation
</example>

## §5 Task-workspace lifecycle

Use one workspace directory for each task and keep it separate from other active tasks. The project ignores `.agent-workspace/tasks/` and `.agent-workspace/worktrees/` in version control; curated guides, lessons, and intended deliverables have separate lifetimes.

<rules section="ALWAYS">
- Name the directory by the task, never by date, and never share it between tasks.
- When a task closes, first preserve anything that must outlive it: a reusable method goes to the lesson store, a project fact to a work product, an approved governing requirement to its guide.
- Remove the closed task's disposable state once doing so cannot lose unfinished or untransferred work.
- When task state is retained because the work remains active, keep its status accurate.
</rules>

<rules section="NEVER">
- Treat an old task plan as the current plan for a new task.
- Keep a folder in case it is useful later; that is a promotion decision avoided, not state preserved.
</rules>

<example type="lifecycle">
input: the review-and-fix task just merged; its folder holds the plan and a probe script that finally worked
❌ leave the folder; the next agent finds the plan and works from a plan that already shipped
✅ promote the probe technique into the lesson store, then delete the folder
</example>

## §6 Persist research while it is happening

Research changes no file, so its product tends to end up in the reply alone. That is the one place context loss can erase mid-task, and the one place a later session cannot reach. The reading was expensive; repeating it is the only way to recover it.

<rules section="ALWAYS">
- When research passes its third file read or search, or when it is delegated, save the developing findings in the task workspace during the work.
- Keep source locations, established facts, unresolved questions, and the next dependency in that record.
- Transfer findings with lasting project value to their durable destination before closing the task.
</rules>

<rules section="NEVER">
- Defer the write to the end of a long investigation; context loss lands mid-task, and then there is nothing left to write.
- Create a research artifact for a lookup that already resolves a single fact.
</rules>

<example type="research_persistence">
input: compare two subsystems' guides against each other, six files read
❌ the full comparison appears in the reply only, so the next session starts from zero and pays the six reads again
✅ the table is written to `.agent-workspace/tasks/<task-slug>/findings.md` as it is built; the reply gives the verdict and the path
</example>

## §7 Use independence when it is the point of delegation

An independent reader can inspect what the author did not consider. This differs from assigning several agents to repeat the same search for speed: the useful result is an independent assessment, not duplicated reading. The coordinating agent having read the artifact is what makes this delegation necessary, not what makes it redundant.

<rules section="ALWAYS">
- Delegate to an unprimed reader when the work requires an absence check, a comparison of the finished result with its source, or a challenge to a consequential claim.
- Give that reader the requirements, artifact, and scope needed for the check.
</rules>

<rules section="NEVER">
- Supply the author's conclusion as the premise the reviewer is expected to confirm.
- Cite this section for a search the coordinating agent could run itself; that is the double reading §2 forbids.
- Spawn parallel readers over the same files for speed and call it independent review.
</rules>

<example type="fresh_attention">
input: the coordinating agent has just written a rule file and needs to know what is missing from it
❌ the author lists the gaps; it cannot see what it never thought of, and that blind spot is the defect
✅ a subagent that has read only the requirement set and the file reports what the requirements demand and the file lacks
</example>
