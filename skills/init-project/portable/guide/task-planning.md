---
scope: portable
---

<critical>
scope: planning and verifying any task that changes an artifact or produces a deliverable; a question answered without changing anything needs no plan.
never: promise correctness without naming the evidence, or hand an executor a subtask whose required behavior is still undefined.
note: scale the depth to consequence and reversibility (§2.1); design verification with the work (§3.4); check the result independently of its author (§3.6); a skill that owns the planning workflow governs §6 to §8.
</critical>

# Planning work and verifying its result

A plan connects the requested outcome to the work that will produce it and the evidence that will show whether it succeeded.

## §1 When this applies

When an installed skill owns the planning workflow, use that workflow. The principles of proportional effort, verification, and scope control in §2 through §4 still apply. Sections §6 through §8 provide the fallback planning method when no skill owns it.

<rules section="ALWAYS">
- Use this procedure for work that changes an artifact or produces a deliverable.
</rules>

<rules section="NEVER">
- Write a separate plan for a question that can be answered without changing anything.
</rules>

## §2 Two independent choices

Choose the depth of planning from the consequence and reversibility of the change. Choose the evidence and deliverable from the nature of the task. A different artifact type does not automatically require more ceremony.

### §2.1 Scale the depth

For a small, isolated, reversible change, the plan can remain part of the immediate work. Shared contracts, migration, broad reuse, ownership boundaries, or costly irreversible actions justify a fuller plan.

<rules section="ALWAYS">
- For a small, isolated, reversible change, establish the intended result, make the change, and check it against the source.
- For work with several dependent steps or files, record the targets, dependencies, acceptance criteria, and checks before execution.
- For a change with shared contracts, migration, broad reuse, ownership boundaries, or costly irreversible actions, add an independent review before implementation.
- When the risk is uncertain, investigate the uncertainty.
</rules>

<rules section="NEVER">
- Treat the largest possible process as the default when the risk is merely unknown.
</rules>

### §2.2 Choose the relevant evidence

An investigation relies on source evidence and distinguishes observed or traced claims from inference. A design relies on requirements and constraints. Code changes rely on the specification and relevant execution checks. A migration compares the state before and after the change. Documentation relies on source facts and the needs of its intended reader.

<rules section="ALWAYS">
- For a task spanning several types, account for the highest-consequence part.
</rules>

<rules section="NEVER">
- Change the depth of planning merely because the output has another file extension.
</rules>

## §3 Principles

### §3.1 Plan before execution

<rules section="ALWAYS">
- Establish the intended outcome and the steps needed to reach it before editing, with the amount of planning matched to §2.1.
</rules>

### §3.2 Establish a shared understanding

Explicit instructions and decisions already given are authorization for the work they cover.

<rules section="ALWAYS">
- Check the user's goal, constraints, and assumptions under `.claude/rules/critical-thinking.md`.
- Ask when a missing answer changes the work materially.
</rules>

### §3.3 Decide where the output belongs

<rules section="ALWAYS">
- Select the destination and discovery point before creating an artifact, using `.claude/rules/doc-organization.md` §8.3 for placement.
</rules>

### §3.4 Design verification with the work

<rules section="ALWAYS">
- For each result, identify the evidence that could show it is wrong and how that evidence will be obtained.
</rules>

<rules section="NEVER">
- Defer the verification strategy until the implementation is complete.
</rules>

### §3.5 Make acceptance assessable

<rules section="ALWAYS">
- Connect each criterion to the task's purpose and source evidence.
- Use execution or structural checks for mechanically decidable requirements.
- For a judgment that requires domain expertise, identify the intended reader or evaluator and the reasons they should be able to assess.
</rules>

<rules section="NEVER">
- Replace a domain judgment with a word count, a fixed layout, or another easy measurement that does not establish the required quality.
</rules>

### §3.6 Check the result independently

The author's explanation of why the work is correct does not replace a comparison with the source.

<rules section="ALWAYS">
- For work beyond a small isolated change, have an independent agent or human compare the result with the task's source evidence.
- For a small change, use a direct self-check against its source, such as reopening the edited section or running the relevant behavior.
- State any limit when an independent check required for the task cannot be performed.
</rules>

### §3.7 Give each part the guidance it needs

<rules section="ALWAYS">
- Identify the governing requirements for each subtask through the project instructions and guide router.
- Pass the relevant paths and stable sections with the subtask.
</rules>

<rules section="NEVER">
- Assume that an executor sees the parent's full context.
</rules>

## §4 Execution sequence and return paths

### §4.1 Establish the outcome

Establish the intended outcome and resolve material uncertainty about scope.

### §4.2 Choose the approach and destination

Choose an approach and output location within the user's authorization.

### §4.3 Define the work and its checks

Define the subtasks, their dependencies, and their verification.

### §4.4 Save the plan

Persist the plan where executors and reviewers can retrieve it.

### §4.5 Review the plan

Review the plan before costly or broadly affecting work. Use an independent review when a wrong plan would create substantial migration, ownership, or compatibility risk.

### §4.6 Resolve gaps

Resolve gaps in the plan so each part can be executed and evaluated.

### §4.7 Execute and verify

A plan is not an additional permission barrier when the user has already authorized implementation.

<rules section="ALWAYS">
- Execute the authorized work and verify each resulting artifact against the plan and its sources.
- Return to an earlier step when new evidence disproves an assumption.
- When the intended work is infeasible, outside authority, or incompatible with a governing constraint, stop the dependent action, explain the issue, and continue independent work that remains valid.
</rules>

<rules section="NEVER">
- Request a new decision for anything but an unresolved choice or an action outside the existing authorization.
</rules>

## §5 Common planning failures

A plan is incomplete when it omits a required outcome, leaves dependencies implicit, or promises correctness without naming evidence. It is also ineffective when it imposes a large process on an isolated change or ignores an owning skill.

Review of the plan cannot stand in for review of the completed artifact. The two checks evaluate different things.

## §6 Subtask contracts

Each subtask must contain enough information for an executor who sees only that assignment.

### §6.1 Choose meaningful boundaries

File count alone does not define a boundary.

<rules section="ALWAYS">
- Group work into units that produce independently assessable results.
- Keep setup, configuration, and documentation with the behavior they enable when they cannot sensibly be accepted separately.
- Split a task where a reviewer could reject one result while accepting another.
</rules>

### §6.2 Information an executor needs

These are information requirements for a handoff, not a required presentation template.

<rules section="ALWAYS">
- Identify the exact target paths and whether each will be created, changed, or removed.
- State what the subtask consumes and produces, including exact interface names and values when another part depends on them.
- Include acceptance criteria, verification, governing guidance, and the reasoning effort the work requires.
</rules>

### §6.3 Resolve placeholders before execution

"Handle errors" does not specify the error condition, the expected response, or the evidence of correctness.

<rules section="ALWAYS">
- When a needed fact remains unknown, identify how and when it will be resolved.
- Accept a reference to another subtask only when the referenced material is available to the executor and defines the needed content.
</rules>

<rules section="NEVER">
- Hand an executor a duty whose required behavior is still undefined.
- Mark a dependent implementation step ready before the fact it depends on is available.
</rules>

<example type="placeholder">
input: a subtask that must respond to a failed upstream call
❌ handle errors
✅ when the upstream call returns a non-success status, retry once after two seconds, then return the status to the caller unchanged; the test asserts the retry count and the returned status
</example>

## §7 Review the plan against the source

This check improves the plan; the independent result check in §3.6 still follows execution.

<rules section="ALWAYS">
- Before execution, map each requested outcome to the work that produces it.
- Check for unresolved placeholders, inconsistent names, missing producers, and consumers scheduled before their inputs exist.
- Revise the plan when the check finds a gap.
</rules>

## §8 Explore design alternatives when needed

<rules section="ALWAYS">
- Read the existing artifact and its constraints before proposing a different approach.
- Compare viable alternatives when the source does not already determine the solution, explain the tradeoff that matters to the stated goal, and recommend an approach based on the evidence.
- Ask for a decision when it belongs to the user and has not been delegated.
</rules>

<rules section="NEVER">
- Create alternatives solely to reach a fixed count.
- Seek another confirmation for a choice already made.
</rules>
