---
paths:
  - ".claude/agents/**"
scope: portable
---

# Defining a specialist agent

## §1 Give the agent a bounded responsibility

Define the work the agent owns, the conditions under which it should be invoked, and the result the parent needs. Inspect existing agents before adding another definition. Resolve overlapping responsibilities so that a request can be assigned for a reason beyond a shared keyword.

The body must establish the agent's responsibility, applicable constraints and decision boundaries. It need not prescribe a persona, voice or opening sentence. Shared project rules remain at their canonical sources under `doc-organization.md` §1; pass the relevant sources and task context when the agent cannot be assumed to have loaded them.

## §2 Declare identity and capabilities

For a genome-managed agent, use a Markdown definition with YAML frontmatter containing `name` and `description`. Keep the identity consistent with the deployed definition and distinguish it from other agents available in the same environment. The description identifies when delegation is appropriate and what the agent can accomplish.

Use an explicit tool list when the assignment requires restricted access. Give the agent the capabilities needed for its work and verification, and avoid granting unrelated mutation access. A reviewer may require a shell to execute tests; granting that capability does not authorize it to change the artifact under review. Tool access and task authorization must both be satisfied.

If a model override is needed, choose one supported by the installed environment for the task's requirements. Do not copy a model name or a permission setting from an old example without checking its current meaning. The [Claude Code subagent reference](https://code.claude.com/docs/en/sub-agents) describes the platform's metadata and loading behavior.

## §3 Specify how the work proceeds

Explain how the agent receives input, finds the required evidence and performs its assigned operations. Make dependencies between operations explicit. State when the agent must stop, what it can resolve independently and which unresolved decisions must return to the parent.

Describe how each granted tool supports the workflow, including any restrictions on side effects. A list of tool names alone does not establish when they should be used. Follow `.agent-workspace/guide/general/orchestration-policy.md` §2 for the choice between local work and delegation.

Define the information returned at handoff: the result, relevant evidence, changed artifacts, checks performed and unresolved issues. Require a machine-readable schema only when a consumer actually needs that schema. A common agent definition must not impose a presentation style on unrelated user-facing outputs.

## §4 Handle uncertainty and failure

Clarify missing information when it prevents safe completion of the assignment. Continue independently with decisions already delegated by the user or parent. If a tool fails, distinguish what ran from what was intended, inspect any partial state and choose a retry only when it is safe within the existing authorization.

Preserve the task's useful state before handing work back. Do not conceal an incomplete result behind a successful tool exit or an unverified assumption. Use `.agent-workspace/guide/general/task-planning.md` §3 for acceptance and evidence requirements.

## §5 Verify the installed definition

Install the agent in the location owned by the intended project or package. Check the active environment for name collisions, effective tool permissions and the loaded revision. Reload the definition using the mechanism supported by that environment before testing it.

Exercise an intended invocation and a request that belongs elsewhere. Check that the agent respects its boundaries and returns enough evidence for its parent to evaluate the work. Investigate routing, capability and workflow defects separately; making the description more forceful does not repair a missing dependency.
