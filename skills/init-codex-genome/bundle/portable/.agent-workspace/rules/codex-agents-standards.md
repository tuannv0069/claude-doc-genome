---
scope: portable
---

# Specialist agents and working roles

## §1 Separate perspective from delegation

A role is a reasoning perspective selected through `.agent-workspace/guide/roles/index.md`. The current assistant can apply it. A subagent is a separate execution context with an assigned result. Do not create an agent for every role or assume role selection authorizes delegation.

Use a specialist when its bounded work benefits from independent context and the current task permits delegation. Follow `.agent-workspace/guide/general/orchestration-policy.md` §2. When the client lacks the required agent capability, perform the applicable workflow in the main context and disclose any independence requirement that remains unmet.

## §2 Verify the installed definition format

For clients supporting the documented custom-agent interface, project definitions use `.codex/agents/*.toml` with `name`, `description` and `developer_instructions`. Confirm the installed schema and successful invocation before shipping a definition that depends on it. Parsing TOML alone does not establish discovery or tool behavior.

Choose a distinct name and inspect conflicts with built-in, user and project agents. Do not set a universal model, reasoning effort or permission policy. A required override must be supported by the actual client and justified by the assigned work.

## §3 Bound instructions and permissions

The definition identifies the agent's responsibility, inputs, evidence, decision boundaries and return contract. It points to project guidance instead of copying all project rules into `developer_instructions`. Pass the project root and relevant source paths with each assignment; do not assume the parent's context or working directory is inherited.

Tool availability and task authorization are separate constraints. A reviewer who can run a shell is not thereby authorized to alter the reviewed artifact. Grant only the capabilities needed for the task and verify effective restrictions, including inherited settings, in the deployed client.

## §4 Return assessable results

Return the established result, source evidence, changed artifacts, checks and unresolved conditions. Preserve enough partial state to resume after failure. Use a machine-readable return schema only when a real consumer needs it. The parent remains responsible for integration and must evaluate the evidence rather than treating a subagent's completion message as proof.

Test a matching task, an out-of-scope request and a capability boundary. Do not claim that schema validation demonstrates runtime isolation or actual permission enforcement.
