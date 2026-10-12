---
paths:
  - ".claude/agents/**"
scope: portable
---

<critical>
scope: creating or editing an agent definition under `.claude/agents/`, a specialist that runs in its own context.
never: grant mutation access an assignment does not need, or conceal an incomplete result behind a successful tool exit.
note: an agent owns a bounded responsibility with explicit tools, an explicit stop condition and a defined handoff; shared rules stay at their canonical sources under `doc-organization.md` §1.
</critical>

# Defining a specialist agent

## §1 Give the agent a bounded responsibility

The body need not prescribe a persona, voice or opening sentence. Shared project rules remain at their canonical sources under `doc-organization.md` §1.

<rules section="ALWAYS">
- Define the work the agent owns, the conditions under which it should be invoked, and the result the parent needs.
- Inspect existing agents before adding another definition, and resolve overlapping responsibilities so that a request can be assigned for a reason beyond a shared keyword.
- Establish in the body the agent's responsibility, applicable constraints and decision boundaries.
- Pass the relevant sources and task context when the agent cannot be assumed to have loaded them.
</rules>

<rules section="NEVER">
- Inline a substantive shared rule in the body; refer to the guide section that owns it.
- Duplicate content of `CLAUDE.md` in the body.
</rules>

## §2 Declare identity and capabilities

A reviewer may require a shell to execute tests; granting that capability does not authorize it to change the artifact under review. Tool access and task authorization must both be satisfied. The [Claude Code subagent reference](https://code.claude.com/docs/en/sub-agents) describes the platform's metadata and loading behavior.

<rules section="ALWAYS">
- For a genome-managed agent, use a Markdown definition with YAML frontmatter containing `name` and `description`, consistent with the deployed definition and distinct from other agents in the same environment.
- Write a description that identifies when delegation is appropriate and what the agent can accomplish.
- Use an explicit tool list when the assignment requires restricted access, giving the capabilities needed for the work and its verification.
- Set the agent's model and reasoning effort from the capability tier of its work under `.agent-workspace/guide/general/orchestration-policy.md` §3 and the project's mapping of the tiers, using values the installed environment supports.
</rules>

<rules section="NEVER">
- Grant unrelated mutation access, or let a read-only agent inherit every tool by default.
- Copy a model name or a permission setting from an old example without checking its current meaning.
- Put XML tags around the agent body; an agent definition is plain Markdown that the platform reads as prose.
</rules>

<example type="reviewer_tools">
input: an agent that reviews a change and runs its tests
❌ give it edit and write access so it can fix what it finds
✅ give it read access and a shell for the tests; a fix is a separate assignment with its own authorization
</example>

## §3 Specify how the work proceeds

A list of tool names alone does not establish when they should be used. Follow `.agent-workspace/guide/general/orchestration-policy.md` §2 for the choice between local work and delegation.

<rules section="ALWAYS">
- Explain how the agent receives input, finds the required evidence and performs its assigned operations, with dependencies between operations made explicit.
- State when the agent must stop, what it can resolve independently and which unresolved decisions must return to the parent.
- Describe how each granted tool supports the workflow, including any restrictions on side effects.
- Define the information returned at handoff: the result, relevant evidence, changed artifacts, checks performed and unresolved issues.
</rules>

<rules section="NEVER">
- Require a machine-readable schema when no consumer needs it.
- List tools without guidance on when they are used.
- Impose a presentation style on unrelated user-facing outputs from a common agent definition.
</rules>

## §4 Handle uncertainty and failure

Use `.agent-workspace/guide/general/task-planning.md` §3 for acceptance and evidence requirements.

<rules section="ALWAYS">
- Clarify missing information when it prevents safe completion of the assignment, and continue independently with decisions already delegated by the user or parent.
- When a tool fails, distinguish what ran from what was intended, inspect any partial state and choose a retry only when it is safe within the existing authorization.
- Preserve the task's useful state before handing work back.
</rules>

<rules section="NEVER">
- Conceal an incomplete result behind a successful tool exit or an unverified assumption.
</rules>

## §5 Verify the installed definition

Making the description more forceful does not repair a missing dependency.

<rules section="ALWAYS">
- Install the agent in the location owned by the intended project or package.
- Check the active environment for name collisions, effective tool permissions and the loaded revision, and reload the definition using the mechanism that environment supports before testing it.
- Exercise an intended invocation and a request that belongs elsewhere, and check that the agent respects its boundaries and returns enough evidence for its parent to evaluate the work.
- Investigate routing, capability and workflow defects separately.
</rules>
