---
scope: portable
---

# Planning work and verifying its result

A plan connects the requested outcome to the work that will produce it and the evidence that will show whether it succeeded.

## §1 When this applies

Use this procedure for work that changes an artifact or produces a deliverable. A question that can be answered without changing anything does not need a separate plan.

When an installed skill owns the planning workflow, use that workflow. The principles of proportional effort, verification, and scope control in §2 through §4 still apply. Sections §6 through §8 provide the fallback planning method when no skill owns it.

## §2 Two independent choices

Choose the depth of planning from the consequence and reversibility of the change. Choose the evidence and deliverable from the nature of the task. A different artifact type does not automatically require more ceremony.

### §2.1 Scale the depth

For a small, isolated, reversible change, establish the intended result, make the change, and check it against the source. The plan can remain part of the immediate work.

For work with several dependent steps or files, record the targets, dependencies, acceptance criteria, and checks before execution. Shared contracts, migration, broad reuse, ownership boundaries, or costly irreversible actions justify a fuller plan and independent review before implementation.

When the risk is uncertain, investigate the uncertainty rather than treating the largest possible process as the default.

### §2.2 Choose the relevant evidence

An investigation relies on source evidence and distinguishes observed or traced claims from inference. A design relies on requirements and constraints. Code changes rely on the specification and relevant execution checks. A migration compares the state before and after the change. Documentation relies on source facts and the needs of its intended reader.

For a task spanning several types, account for the highest-consequence part without changing the depth merely because the output has another file extension.

## §3 Principles

### §3.1 Plan before execution

Establish the intended outcome and the steps needed to reach it before editing. Match the amount of planning to §2.1.

### §3.2 Establish a shared understanding

Check the user's goal, constraints, and assumptions under `.claude/rules/critical-thinking.md`. Ask when a missing answer changes the work materially. Treat explicit instructions and decisions already given as authorization for the work they cover.

### §3.3 Decide where the output belongs

Select the destination and discovery point before creating an artifact. Use `.claude/rules/doc-organization.md` §8.3 for placement.

### §3.4 Design verification with the work

For each result, identify the evidence that could show it is wrong and how that evidence will be obtained. Do not defer the verification strategy until the implementation is complete.

### §3.5 Make acceptance assessable

Connect each criterion to the task's purpose and source evidence. Use execution or structural checks for mechanically decidable requirements. For judgments that require domain expertise, identify the intended reader or evaluator and the reasons they should be able to assess.

Do not replace a domain judgment with a word count, a fixed layout, or another easy measurement that does not establish the required quality.

### §3.6 Check the result independently

For work beyond a small isolated change, have an independent agent or human compare the result with the task's source evidence. The author's explanation of why the work is correct does not replace that comparison.

A small change can use a direct self-check against its source, such as reopening the edited section or running the relevant behavior. State any limit when an independent check required for the task cannot be performed.

### §3.7 Give each part the guidance it needs

Identify the governing requirements for each subtask through the project instructions and guide router. Pass the relevant paths and stable sections with the subtask, rather than assuming that an executor sees the parent's full context.

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

Execute the authorized work and verify each resulting artifact against the plan and its sources.

Return to an earlier step when new evidence disproves an assumption. If the intended work is infeasible, outside authority, or incompatible with a governing constraint, stop the dependent action and explain the issue. Continue independent work that remains valid.

A plan is not an additional permission barrier when the user has already authorized implementation. Request a new decision only for an unresolved choice or action outside that authorization.

## §5 Common planning failures

A plan is incomplete when it omits a required outcome, leaves dependencies implicit, or promises correctness without naming evidence. It is also ineffective when it imposes a large process on an isolated change or ignores an owning skill.

Review of the plan cannot stand in for review of the completed artifact. The two checks evaluate different things.

## §6 Subtask contracts

Each subtask must contain enough information for an executor who sees only that assignment.

### §6.1 Choose meaningful boundaries

Group work into units that produce independently assessable results. Keep setup, configuration, and documentation with the behavior they enable when they cannot sensibly be accepted separately.

Split a task where a reviewer could reject one result while accepting another. File count alone does not define that boundary.

### §6.2 Information an executor needs

Identify the exact target paths and whether each will be created, changed, or removed. State what the subtask consumes and produces, including exact interface names and values when another part depends on them. Include acceptance criteria, verification, governing guidance, and the reasoning effort the work requires.

These are information requirements for a handoff, not a required presentation template.

### §6.3 Resolve placeholders before execution

Do not hand an executor a duty whose required behavior is still undefined. “Handle errors” does not specify the error condition, the expected response, or the evidence of correctness.

If a needed fact remains unknown, identify how and when it will be resolved. Do not mark a dependent implementation step ready until the fact is available. A reference to another subtask is sufficient only when the referenced material is available to the executor and defines the needed content.

## §7 Review the plan against the source

Before execution, map each requested outcome to the work that produces it. Check for unresolved placeholders, inconsistent names, missing producers, and consumers scheduled before their inputs exist.

Revise the plan when the check finds a gap. This check improves the plan; the independent result check in §3.6 still follows execution.

## §8 Explore design alternatives when needed

Read the existing artifact and its constraints before proposing a different approach. Compare viable alternatives when the source does not already determine the solution. Explain the tradeoff that matters to the stated goal and recommend an approach based on the evidence.

Ask for a decision when it belongs to the user and has not been delegated. Do not create alternatives solely to reach a fixed count, or seek another confirmation for a choice already made.
