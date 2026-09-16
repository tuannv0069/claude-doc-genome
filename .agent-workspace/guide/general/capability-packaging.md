---
scope: portable
---

# Recognizing work that can be packaged

This guide helps identify when an existing procedure would benefit from a skill or subagent. It does not authorize creating a new capability without a request or delegated authority.

## §1 What qualifies as a capability

A candidate needs a recognizable trigger, an ordered procedure, and a defined output that the procedure creates or changes. All three must be established before proposing a package.

A glossary, evidence policy, or routing table can be useful without being a workflow. Reading it may answer a question, but that alone does not produce the kind of output that warrants a skill. A list of criteria also does not become a procedure merely because it is numbered.

## §2 Recognize a procedure while using its guide

When the task already requires a guide, check whether that guide describes a trigger, steps, and an output. If it does, inspect the installed skills and agents to determine whether one already owns the same workflow.

If no owner exists, retain the guide's identity as a packaging candidate. Complete the user's current task before raising an optional packaging proposal. Do not interrupt the work to build a capability the user did not request.

Do not re-propose a candidate whose rejection is already recorded, unless new information changes the earlier reason.

### §2.1 No extra run-counting is needed

This recognition step uses the guide already being read. It does not require logging every execution or maintaining an additional registry of routine work. The question is whether the procedure has a stable shape and an owner.

## §3 A requested sweep for unwritten procedures

Only perform a broader discovery sweep when requested. Examine current task records, the lesson router, and relevant version history for recurring kinds of work that have no owning skill or agent.

Group by the action performed, not by the subject name in a task slug. Three independent instances of the same work provide a useful candidate signal. They do not prove that the work has stable steps; establish those steps, its trigger, and its output before proposing a package.

Prioritize the candidate with the clearest repeatable procedure and practical benefit. Respect the requested sweep scope rather than turning an ordinary task into a capability backlog.

## §4 Choose the appropriate form

Use a skill for a repeatable sequence that can run in one working context and produce a defined output. Use a subagent when the work needs an independent context, such as verification of another phase's product.

Keep a criterion in a guide when it is a judgment applied at one point. Do not package work whose steps differ substantially every time. Length alone does not justify a subagent.

A workflow can need both a skill and an independent check. Treat that as one capability decision and resolve its implementation structure when authoring the approved package.

## §5 Propose and obtain the needed decision

For an optional proposal, explain which procedure was identified, how it was found, which form fits, and what repeated manual work it would replace. Raise it after completing the task in which it was noticed.

Creation requires the user's request or delegated authority. Authorization already given for creating the capability does not need to be requested again. Author the resulting skill or agent against `.claude/rules/skill-md-standards.md` or `.claude/rules/subagent-standards.md`, respectively.

## §6 Remember a declined proposal

Record the declined candidate and the reason that should prevent an identical future proposal. Use the store selected by `lesson-capture.md` §8 and preserve the decision's evidence.

A changed requirement or new evidence can justify reconsideration. Repeating the same proposal without addressing the earlier reason does not.

## §7 Related guidance

Placement of a workflow follows `.claude/rules/doc-organization.md` §8.3. Learning from repeated failures follows `lesson-capture.md` §4. The skill and agent standards govern the artifacts after the capability has been authorized.
