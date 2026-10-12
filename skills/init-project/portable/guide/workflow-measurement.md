---
scope: portable
---

<critical>
scope: designing or redesigning a workflow, meaning a fixed sequence of steps that the assistant runs from a start to an end and will run again in the same form.
never: finish a workflow design that defines no run record for its steps, or write an estimated time or token count into a run record as a measured one.
note: time means active working time and excludes waiting; token counts come from the usage record of the environment that ran the step; analysing the records is separate work from keeping them.
</critical>

# Measuring the time and token cost of a workflow

A workflow that is run many times incurs its cost in time and tokens on every run, and nobody can tell which step to change without figures for each step. A total for the whole run shows that a workflow is expensive but does not show where. This guide makes the per-step record part of the workflow's design, so that the figures exist from the first run and do not have to be reconstructed afterwards.

## §1 When this applies

A workflow here is a sequence of steps with a fixed order, a defined start and a defined end, which the assistant is expected to run again in the same form. The body of a skill, a script that coordinates several agents, a guide procedure and a staged production process, such as editing a video or delivering a code change, are all workflows. A plan written for one task under `task-planning.md` §4 is not a workflow, because it is not run again.

Designing a workflow means writing its steps for the first time. Redesigning one means adding, removing, reordering, splitting or merging steps. Rewording a step without changing what it does is neither.

<rules section="ALWAYS">
- Define the run record of §3 in the same change that designs a workflow.
- Define the run record of an existing workflow in the change that redesigns it.
</rules>

<rules section="NEVER">
- Leave the run record of a newly designed workflow to be defined after the workflow has gone into use.
- Apply this guide to a plan for a single task.
</rules>

<example type="redesign">
input: an existing skill with no run record; one change fixes a typo in step 3, and a later change splits step 3 into two steps
❌ define the run record in the typo fix, or split the step without defining one
✅ leave the typo fix as it is, and define the run record in the change that splits the step
</example>

## §2 What the design states

The step is the unit of measurement, so the design has to make each step recognizable in the record and say how its figures are obtained. The record measures the assistant's work. A step that a person performs still appears in it, so that the sequence stays complete.

<rules section="ALWAYS">
- Give each step a stable identifier for the run record to use.
- Keep a step's identifier when the wording of the step changes.
- State for each step who performs it: the main agent, a delegated agent, a script or tool, or a person.
- State for each step the event that marks its start and the event that marks its end.
- State for each step where its time and its token counts come from, using the sources in §4.
- State where the run record is stored, using §5.
- Mark the time and token fields of a step performed by a person as not applicable.
</rules>

<rules section="NEVER">
- Put two steps under one identifier when one of them could be changed without the other.
- Reuse the identifier of a removed step for a different step.
</rules>

<example type="step_granularity">
input: a workflow that researches a topic, drafts a script, reviews the draft and revises it
❌ one identifier, `write-script`, covering all four; the record shows that the script was expensive but not which part of it
✅ four identifiers, `research`, `draft`, `review` and `revise`, each with its own line in the record
</example>

## §3 The run record

One run is one pass through the workflow from its start to its end. The record holds one line for each execution of a step, with these fields:

| field | content |
|---|---|
| workflow | The workflow's identifier and the version or date of its design. |
| run | The identifier of the run. |
| step | The step's identifier from §2. |
| performer | The main agent, a delegated agent, a script or tool, or a person. |
| model | The model that did the work, when a model did it. |
| start, end | The times at which the step started and ended. |
| active time | The working time defined in §4. |
| tokens | The counts in the types the source reports, such as input, output, cache write and cache read. |
| outcome | Completed, failed, or run again because a later step sent it back. |
| source | Where the time and token figures came from, and the reason for any figure that is missing. |

Rework is exactly what someone tuning a workflow needs to see, and a line that is overwritten hides it. Token types stay separate because each type has its own price, and the prices in force when the record is analysed are not known when it is written. Some environments make a step's token counts readable only after the step, or the whole run, has ended.

<rules section="ALWAYS">
- Write one line for each execution of a step, with the fields in the table above.
- Write a field that has no value as not measured or not applicable, as §2 and §4 direct.
- Write the line, with its start and end times, when the step ends.
- Add token counts that the usage record makes available only later to the same line as soon as they can be read.
- Write a new line when a step is run again within the same run.
- Keep the token types separate as the source reports them.
- Record a step that failed or was abandoned with the time and the tokens it used.
</rules>

<rules section="NEVER">
- Overwrite the line of an earlier execution with the figures of a later one.
- Add the token types up into one number in the record.
- Store an amount of money in place of the token counts.
- Put the content of the work, such as a prompt, a draft or a credential, into the record.
</rules>

<example type="rerun">
input: the review step sends the draft back, and the revise step runs a second time in the same run
❌ replace the first `revise` line with the combined time and tokens of both attempts
✅ keep the first `revise` line, and add a second `revise` line with its own times, tokens and outcome
</example>

## §4 Where the figures come from

The assistant cannot sense how much time has passed or how many tokens it has used. Environments differ in what they record: a coding harness may write a session transcript with a timestamp and a usage block for each model response and report the total tokens and duration of a delegated agent in that agent's result, as Claude Code does; a direct API call returns its usage in the response; a script can time itself. Such a record is an optional dependency under `.claude/rules/doc-organization.md` §9.

Active time is the time during which work is being done for the step. When steps run in parallel, each has its own active time, so the active times of a run can add up to more than the time the run took.

<rules section="ALWAYS">
- Take the start and end times from the system clock or from the timestamps in the environment's usage record.
- Take the token counts from the usage record of the environment that ran the step.
- Check in the installed environment that the usage record exists and what its fields mean before a design relies on it.
- Count as active time the time the model spends generating and the time a tool, a script or a delegated agent spends working for the step.
- Leave out of active time the time spent waiting for a person, the time between sessions, and any pause in which nothing is working for the step, such as waiting out a rate limit.
- Record the active time of a step that a wait interrupted as the sum of its working intervals.
- When the environment keeps no usage record for a step, write the token fields as not measured and give the reason in the source field.
</rules>

<rules section="NEVER">
- Write a time or a token count from the assistant's own impression of how long a step took or how much it used.
- Fill a missing figure with an estimate, with an average of earlier runs or with a count worked out from the length of the text.
- Assume that a usage record found in one environment exists in another.
</rules>

<example type="missing_usage">
input: a step runs inside a tool that reports its duration but no token usage
❌ work out a token count from the length of the tool's output and write it in the record
✅ write the duration, write the token fields as not measured, and note in the source field that the tool reports no usage
</example>

<example type="active_time">
input: a step starts at 10:00, waits from 10:05 to 10:40 for the owner's approval, and ends at 10:50
❌ record an active time of fifty minutes
✅ record an active time of fifteen minutes, the sum of the two working intervals
</example>

## §5 Where the record is kept

A run record is data about how the work went. It is neither guidance nor the deliverable that the run produced, and it is useful only when the runs of one workflow can be read side by side. The project decides where its records are kept and whether they are committed.

<rules section="ALWAYS">
- Name one location for each workflow's records in the workflow's design, inside the project's work-product area or at the place the project's own instructions name.
- Write every run of a workflow to that location in the same machine-readable, append-only format, such as JSON Lines.
</rules>

<rules section="NEVER">
- Keep the only copy of a run record in the task workspace, which is removed when the task closes under `orchestration-policy.md` §5.
- Write a run record into an installed skill package, which `.claude/rules/skill-md-standards.md` §4 keeps free of task output.
</rules>

## §6 Checking the record on the first run

The record of the first run shows at once whether a step has no line, whether a source returned nothing, and whether waiting time has been counted as active time. The first run can be a trial or the first real use; a workflow that costs money or needs an approval to run is not run only to test its record.

Reading the records, comparing runs, finding the expensive step and deciding what to change is separate work, done when the project owner asks for it. The record says what a step cost and nothing about what the step contributed to the result.

<rules section="ALWAYS">
- After the first run of a newly designed or redesigned workflow, confirm that the record has a line for every step that ran, with figures from the sources the design names.
- Correct the design when the first run shows a missing line or a figure from the wrong source.
</rules>
