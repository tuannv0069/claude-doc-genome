---
scope: portable
---

<critical>
scope: a repeatable procedure is being run with no skill and no subagent owning it — decide whether to package it and propose that to the user.
never: create a skill or agent file without a request or delegated authority, or package a procedure whose trigger, steps and output are not already written down.
note: detect the procedure where it is already written, not by counting runs; one candidate per task, raised at the end.
</critical>

# Recognizing work that can be packaged

This guide helps identify when an existing procedure would benefit from a skill or subagent. It does not authorize creating a new capability without a request or delegated authority. What a packaged artifact must look like is settled by `.claude/rules/skill-md-standards.md` and `.claude/rules/subagent-standards.md`; this guide supplies the other half, when the assistant itself raises the question.

## §1 What qualifies as a capability

A candidate needs a recognizable trigger, an ordered procedure, and a defined output that the procedure creates or changes, such as a file, a set of cells, a diagram or a report shape. A rule with no steps is a rule; steps with no defined output are a habit; steps with no trigger are a one-off.

The output property decides most cases and is the one read carelessly. A glossary, an evidence policy or a routing table can be long, numbered and precise and still produce nothing: the reader leaves with an answer, not with a changed artifact. Packaging one of those wraps a lookup in a workflow and makes it slower to reach.

<rules section="ALWAYS">
- Establish the trigger, the ordered steps and the created or changed output before proposing a package.
</rules>

<rules section="NEVER">
- Count an answer the reader forms in their own head as an output.
- Treat a list of criteria as a procedure because it is numbered.
</rules>

## §2 Recognize a procedure while using its guide

This check runs at the moment the router already sends the assistant into a guide. It is `.claude/rules/doc-organization.md` §8.3 branch 1 read from the other side: that branch asks the question when content is written; this section asks it when the work is done.

<rules section="ALWAYS">
- When the task already requires a guide, check whether that guide describes a trigger, ordered steps and an output.
- When it does, inspect the installed skills and agents to determine whether one already owns the same workflow.
- When no owner exists, retain the guide's file name as the candidate's identity, so that two agents raise the same candidate rather than two.
- Complete the user's current task before raising the proposal under §5.
</rules>

<rules section="NEVER">
- Treat a guide that only states criteria as a candidate; criteria are read, not executed.
- Interrupt the work in hand to build a capability the user did not request.
- Re-propose a candidate whose rejection is already recorded, unless new information changes the earlier reason.
</rules>

<example type="output_test">
input: a guide with fifteen numbered rules that map where each kind of content lives
❌ propose packaging it; the numbered rules look like steps
✅ leave it as a guide; the reader leaves with an answer, and no artifact exists on disk after the run
</example>

<example type="output_test_positive">
input: a guide whose steps end in named cells written into a named workbook, owned by no skill
✅ a candidate; the output exists on disk after the run and can be checked
</example>

### §2.1 No extra run-counting is needed

This recognition step uses the guide already being read. It does not require logging every execution or maintaining an additional registry of routine work. The question is whether the procedure has a stable shape and an owner. An agent that starts logging runs to be sure has replaced a free check with an expensive one.

## §3 A requested sweep for unwritten procedures

The check in §2 cannot see a procedure that is re-derived from scratch each time. That one is found by a sweep over current task records, the lesson router and relevant version history. Three independent instances of the same work provide a useful candidate signal, the same step the lesson ladder uses in `lesson-capture.md` §4; they do not prove that the work has stable steps.

<rules section="ALWAYS">
- Perform the sweep only when requested.
- Group by the action performed, not by the subject name in a task slug.
- Establish the steps, trigger and output of a recurring kind of work before proposing a package.
- Name the one candidate with the clearest repeatable procedure and practical benefit, and stop there.
</rules>

<rules section="NEVER">
- Run the sweep inside an ordinary task; it reads dozens of names to answer a question nobody asked.
- Turn the sweep into a capability backlog.
</rules>

<example type="group_by_action">
input: task slugs `shiteki-rd031` and `fix-comment-kian-orange-9c3b`
❌ count them as two kinds of work because the subjects differ
✅ count them as one kind of work, answering a review comment; the slug names the subject and the round, the work is the same
</example>

## §4 Choose the appropriate form

| the candidate | form |
|---|---|
| ordered steps, one working context, defined output | skill |
| a pass that must run in an independent context, such as verification of another phase's product | subagent |
| a judgment applied at a single point, with no step order | it stays a guide section |
| steps that differ substantially every run | neither; it is not a procedure |

A workflow can need both a skill and an independent check. Treat that as one capability decision and resolve its implementation structure when authoring the approved package.

<rules section="NEVER">
- Package a procedure as a subagent because it is long; length is not isolation.
- Restate what a skill or agent file must contain; the skill and agent standards own that.
</rules>

## §5 Propose and obtain the needed decision

Creation requires the user's request or delegated authority. Authorization already given for creating the capability does not need to be requested again.

<rules section="ALWAYS">
- Raise the proposal after completing the task in which the candidate was noticed.
- State which procedure was identified, how it was found, which form fits, and what repeated manual work it would replace.
- Keep the proposal to a few lines; the design belongs to the build.
- Raise one candidate per task.
- Author an approved skill against `.claude/rules/skill-md-standards.md` and an approved agent against `.claude/rules/subagent-standards.md`.
</rules>

<rules section="NEVER">
- Create a skill or agent file because the candidate looked obvious; the decision is the user's.
- Raise a candidate the same session declined.
</rules>

<example type="proposal">
input: a guide with a fixed trigger, seven ordered sections and a tool that writes defined cells, owned by no skill
❌ write the skill file, then report it; the user never chose to spend the turn
✅ "Candidate: `<guide>.md`, found while using it: trigger, ordered steps and a defined output, with no owner. Proposed form: skill. It would replace reading and following that guide by hand each run. Build it?"
</example>

## §6 Remember a declined proposal

Without a record, the next session spends the same turn on the same candidate and gets the same answer. A changed requirement or new evidence can justify reconsideration; repeating the same proposal without addressing the earlier reason does not.

<rules section="ALWAYS">
- Record a declined candidate, with the reason that should prevent an identical future proposal, in the store selected by `lesson-capture.md` §8.
- Preserve the decision's evidence in that record.
</rules>

## §7 Related guidance

Placement of a workflow follows `.claude/rules/doc-organization.md` §8.3. Learning from repeated failures follows `lesson-capture.md` §4. The skill and agent standards govern the artifacts after the capability has been authorized.
