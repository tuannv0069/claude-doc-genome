---
scope: portable
---

<critical>
scope: choosing the working role for a task, establishing and defining a role, and delegating a subtask's role.
never: follow a role clause over a governing project rule, or carry the dispatching agent's role over to a subagent.
note: one primary role per task; a checking role contributes only its §6; the selection is stated in the reply before the first substantive step.
</critical>

# Selecting a working role

A role provides a task-specific perspective, evidence standard, and completion check. It does not set the project's output style.

## §1 When this applies

Consult the role router when starting a task. When a skill owns the running workflow, use the role selection that workflow defines. A role for creative work also follows `creative-work.md` §7.

## §2 Choose the role from the action

The work-type tables live only in `.agent-workspace/guide/roles/index.md`; this section is the matching procedure. Stopping at the first matching row hides the second one, and the hidden row is usually the one naming the perspective the task lacked.

<rules section="ALWAYS">
- Identify the action about to be performed, then read every work-group table in `.agent-workspace/guide/roles/index.md` to the last row before choosing a match.
- Read the primary role in full and, for each checking role, only its §6 completion criteria.
- When two applicable rows differ in specificity, use the more specific primary role and add the other primary role as a checking perspective; a row identifying a specific task or artifact takes precedence over a general row.
- Before the first substantive step of the task, state the selection in the reply: the primary role and the checking roles whose §6 was read, or, when no row matched, the rows considered and why the action falls outside them.
- Write that statement from the router just read, so that an omitted or inferred lookup is visible to a reader who did not watch the reading, and repeat it only when the work type changes and a new lookup is made.
- Give precedence to a role explicitly selected by the user over the router.
</rules>

<rules section="NEVER">
- Force a role onto a task when no row matches; continue without one.
- Repeat the lookup while the work type is unchanged.
- Read a checking role's §1 through §5; two full sets of decision criteria and detail levels serve no one.
</rules>

<example type="two_rows_match">
input: writing a document section that states which permissions may reach a screen; the section-writing row and the authorization row both match
❌ stop at the section-writing row because it matched first; the security perspective the section most needed is left out
✅ read to the last row of both tables, take the more specific row's role as primary and the other's as a checking role
</example>

<example type="name_by_action">
input: about to edit `screen-032-basic-design.md` to add a validation rule
❌ match the work type by the file name, a basic design document
✅ match the work type by the action, writing content that describes system behaviour, then look up that row
</example>

## §3 Define a role by its responsibility

A role should explain what it examines, which questions guide its decisions, how it resolves competing criteria, what level of detail it covers, what evidence it accepts, and where its responsibility ends. Those meanings matter; they do not require a fixed number of sections or a prescribed sentence pattern. Existing stable section identifiers remain valid under `.claude/rules/doc-organization.md` §2, and additional sections can be added when they serve the role.

Completion criteria identify conditions that would leave the assigned work unresolved. They can be explained without a fixed negative-state formula. A role's criteria govern its task, not every task in the project.

<rules section="ALWAYS">
- Write a role file from the template `.agent-workspace/guide/roles/_template.md`, with `scope: project` in its frontmatter.
- Open every role with a `<critical>` block of two lines: a `scope:` line naming the kind of work the role wears and a `core:` line naming the one thing the role exists to protect.
- Keep §6 in every role for completion criteria, because checking-role selection reads that section directly.
- When §7 identifies handoffs, mark receiving role names with backticks so the role verifier can resolve them, and use only names of roles that exist in the router.
</rules>

<rules section="NEVER">
- Put backticks around a file name or a term in a handoff line; the marker is a data convention for the receiving role only.
</rules>

## §4 Delegate the subtask's role

This section is the single source of the subagent role-dispatch rule; a flow that dispatches a subagent refers here rather than repeating it. A subagent does not inherit the coordinating agent's always-loaded surface.

<rules section="ALWAYS">
- Resolve the role for the delegated action, not the coordinating agent's own action.
- Pass the primary role's file path with the subtask so its executor can read the governing perspective.
- Assign one primary role per subtask.
- When no role applies, state in the dispatch that the lookup found no match, so the executor does not infer a missing assignment.
</rules>

<rules section="NEVER">
- Carry the dispatching agent's own role over to the subagent.
- Load additional full role files into a dispatch merely to imply thoroughness.
- Leave the role field blank when no role matched.
</rules>

<example type="no_role_matched">
input: dispatching a subagent to rename a file across the repository
❌ omit the role line from the prompt because none of the work-type rows fit
✅ write that no role matched in the prompt, so the subagent and its reviewer both see that the check ran and found nothing
</example>

## §5 Add a role when the project needs one

Every role belongs to the project that uses it. The genome distributes the role template and no role, because a fixed set of roles is too many for one project and too few for another. A project adds a role when work appears that no existing role covers, or when one part of the work needs a different policy from the role that currently covers it.

<rules section="ALWAYS">
- Establish a new role under §8 before writing it, and define it under §3.
- Place a new role in the group folder of the work it serves, creating the group's folder and its table in `.agent-workspace/guide/roles/index.md` when no existing group fits, and register the role in that table in the same change that creates it.
- When one part of the work needs a different policy from the role that covers it, create a separate role for that part and route its work types to the new role.
- When a role is deleted or renamed, update its router entries and every handoff that refers to it in the same change.
</rules>

## §6 Router data contract

The role router and the role folders are read as data by `verify_role_files.py`. Changing the table's shape or the folder layout without updating the parser breaks the gate, and changing the parser without updating this section makes the code the law instead of this file.

Roles are grouped by the kind of work they serve, such as software development or content creation, so that a reader can tell from the path which work a role belongs to. A role that serves several groups, such as work planning, belongs to `general/`. The router keeps one table for each group, and a table lists the work types of that group; a row may name a primary or checking role from another group.

<rules section="ALWAYS">
- Keep each role file at `.agent-workspace/guide/roles/<group>/<role-name>.md`, one level below the router, in a kebab-case group folder.
- Give every role a name that is unique across all groups, because the router identifies a role by its file name alone.
- Use the columns `work type`, `primary role`, and `checking roles`, with exactly three cells per data row.
- Put one kebab-case role name without backticks in the primary cell.
- Fill the checking cell with comma-separated kebab-case role names without backticks, and leave it empty only for a work type that produces no result for another role to check.
- Make every name in either cell identify an existing role file, and make every role file reachable through at least one row.
- Keep the role template at `.agent-workspace/guide/roles/_template.md`, beside the router; it is not a role, has no row, and is the only file allowed there besides the router.
- Change the parser and its test together with any change to this shape.
</rules>

<rules section="NEVER">
- Wrap a role name in the router table in backticks; the gate parses the raw cell text.
- Widen a data row past three cells, or separate checking roles with anything but a comma.
- Name a row's primary role in the same row's checking cell.
- Put a role file directly beside the router or in a folder nested inside a group.
- Register the role template in a router row, or edit it to hold one project's role.
</rules>

## §7 Relationship to project requirements

A role describes how to reason about a class of work. It does not override a governing project requirement or expand the user's authorization.

<rules section="ALWAYS">
- When a role conflicts with a project rule or guide, apply the governing requirement and continue the work under it.
- When reporting a conflict, identify the conflicting role clause and the rule's source section in the same report.
- Correct the role's clause when the conflict shows that the clause is wrong for the project, or route that part of the work to a separate role under §5.
</rules>

<rules section="NEVER">
- Follow a role clause over a guide or an always-loaded rule that says otherwise.
- Turn a software-specific criterion into an obligation for creative work merely because both products are files.
</rules>

<example type="role_clause_loses">
input: a role's §5 treats a fact read from the system under analysis as a hypothesis until an outside party confirms it, while the project's evidence guide names the sources the team already holds as sufficient
❌ follow the role and record the fact as unknown pending an outside answer
✅ follow the project's guide, then correct the role's clause or route the row to a separate role
</example>

## §8 Establish a role from researched practice

A role written from a language model's recollection of a job title is fluent and cannot be checked: it reproduces what the title is commonly said to do, and nobody can tell which sentence came from practice. A role is therefore built from sources that have been opened, and the research covers the content of each role as well as the list of names, because a name with unresearched content is still the model's memory.

The sources describe teams of people, while a role here is a working perspective that an agent takes for a task. The research supplies the responsibilities of the work, the checks between them and the decisions the work ends in. An agent can plan and coordinate work and can make an approval, a decision of taste, a spending decision or a release decision, so those responsibilities become roles like any other. What an agent is able to do and what it has been authorized to decide are different matters, and the authority comes from the user.

The role research record is a work product. It lives in the project's research category, or in a `docs/role-research/` category registered in `docs/index.md` when the project has no research category.

<rules section="ALWAYS">
- Before proposing or writing a role, research how practitioners of that kind of work organize it: the stages of the work, the responsibility held at each stage, which responsibility checks which, and where decisions are made.
- Research in the same pass how that kind of work is run with AI agents: how the responsibilities are divided among agents, which checks are kept independent, and where a person approves.
- Open each source and write its locator into the role research record before relying on it, together with the responsibilities, checks and decisions it supports.
- Record in the role research record any question for which no usable source was found.
- Derive the proposed roles from the responsibilities found in the work, including the ones that plan and coordinate it and the ones that approve, decide questions of taste, spend or release.
- Give every role that produces a result at least one checking role other than itself.
- Leave a researched responsibility out of the proposal only when the project has no work of that kind, and list it with that reason when presenting the proposal.
- Present the proposal to the user with, for each role, its name, the work types it is primary for, the roles that check it and the sources behind it, and let the user select, rename, merge or add roles.
- Ask the user, for each decision a selected role's work ends in, whether the role decides or recommends and waits for a named person, and write the answer in §3 of that role.
- Write each selected role with every statement about the practice taken from the role research record and every statement about the project taken from the project's own sources, and name both in §8 of the role.
- Have a reader who did not write the role compare it with the role research record, under `orchestration-policy.md` §7, before the role is used.
- When no search or browsing tool is available and the user supplies no sources, say so before presenting the proposal, mark the basis of each affected role as `unverified`, and report the role setup as incomplete.
</rules>

<rules section="NEVER">
- Present a role list or a role's content recalled from the model's memory as researched.
- Leave a planning, coordinating or deciding responsibility out of the proposal on the ground that an agent performs the work.
- Assume a decision authority that the user has not stated.
- Let a role check a result that the same role produced.
</rules>

<example type="researched_role">
input: the project's main work is producing a podcast, and the roles are about to be proposed
❌ list producer, host, editor and sound engineer from memory and write each one's criteria as the model remembers the job
✅ open practitioners' published workflows and material on agent-run production, record which responsibility each source supports, propose roles from those responsibilities with their checking roles, and ask who decides the release
</example>

<example type="decision_authority">
input: the selected roles include one whose work ends in publishing a finished piece
❌ write that the role publishes when its checks pass, because an agent can run the publishing command
✅ ask the user whether this role publishes or recommends and waits, and write the answer and the named person in §3 of the role
</example>
