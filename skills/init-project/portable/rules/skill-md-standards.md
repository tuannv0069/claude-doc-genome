---
paths:
  - ".claude/skills/**"
scope: portable
---

<critical>
scope: creating or editing a skill under `.claude/skills/`, whose `SKILL.md` is loaded when its description matches the task.
never: inline a substantive shared rule in a skill, or report a skill's intended result as completed after a failed execution.
note: a skill owns one workflow with a trigger, ordered dependencies and a checkable result; shared rules are referenced by stable section identifier under `doc-organization.md` §1.
</critical>

# Skills that own a workflow

## §1 Establish the purpose and entry conditions

A skill owns a repeatable workflow with a recognizable trigger, an ordered set of dependencies and a result that can be checked. Similar terminology between skills is acceptable when the responsibilities remain distinguishable.

<rules section="ALWAYS">
- Before creating a skill, inspect existing skills and decide whether the requested workflow already has an owner; extend that owner when the work is the same and create a separate skill when its responsibility is distinct.
- Describe the task the skill handles, the information it needs and the circumstances in which another workflow should be used.
- Test the routing description against both an intended request and a nearby request outside its scope.
</rules>

<rules section="NEVER">
- Write a description so vague or so overlapping with another skill that the matcher cannot choose.
</rules>

## §2 Keep metadata separate from instructions

The `name` and `description` fields are a packaging contract, not a prose template. The [Claude Code skill reference](https://code.claude.com/docs/en/skills) describes the platform fields.

<rules section="ALWAYS">
- Store the skill entry point in `SKILL.md`.
- For a genome-managed skill, declare `name` and `description` in YAML frontmatter, using a name accepted by the installed Claude Code version and consistent with the packaged skill.
- Add optional metadata only when the workflow needs it and the installed platform supports it, and check its actual meaning before relying on it.
- Verify local loading when the workflow depends on a particular platform behavior.
</rules>

<rules section="NEVER">
- Infer a capability from a field that happens to parse as YAML.
- Wrap the body of `SKILL.md` in XML; the target file is plain Markdown.
</rules>

## §3 Describe an executable workflow

Shared rules belong at the source identified by `doc-organization.md` §1 and are referenced by stable section identifiers.

<rules section="ALWAYS">
- State what inputs and dependencies each operation requires, how it uses earlier results, and which conditions select another branch or stop the work.
- Identify required tools, libraries, credentials or external resources, and resolve environment-specific paths from the project or runtime.
- Define the information or artifact handed back at completion and the evidence needed to accept it.
- Include a verification step that checks the requested result against its source of truth.
- Define the per-step record of active time and token cost in the same change that designs or redesigns the workflow's steps, as `.agent-workspace/guide/general/workflow-measurement.md` §1 requires.
- When execution fails, retain enough state to explain the failure and resume safely.
- Keep the skill's own orchestration in its body.
</rules>

<rules section="NEVER">
- Embed a secret in the instructions.
- Hardcode a path that varies by environment.
- Report the intended result as completed after a failure.
- Restate a workflow step for emphasis.
- Turn the skill into a second authoritative copy of project conventions or shared domain rules.
</rules>

<example type="shared_rule_reference">
input: a skill step must apply the project's naming convention
❌ copy the naming rules into the skill body
✅ refer to the guide section that owns the naming convention and apply it from there
</example>

## §4 Package dependencies with the skill

Separate resources by purpose or independent branch when that makes loading selective.

<rules section="ALWAYS">
- Place scripts, templates and reference material with the skill when they are part of its implementation, and reference them explicitly from the entry point.
- Make a resource needed by a branch reachable before that branch executes.
- Verify that the installed package contains the files the workflow names.
- Use the project placement rules for work records and deliverables.
</rules>

<rules section="NEVER">
- Split a file merely to meet an arbitrary line count.
- Require an assistant to discover a chain of undocumented dependencies.
- Write task output into the installed skill package.
</rules>

## §5 Validate routing and maintenance changes

When routing fails, examine the task boundaries and description; when execution fails, examine the dependency and operation that failed. Requirements for the style of a user-facing product belong to that product's project-owned instructions, not to this shared skill standard.

<rules section="ALWAYS">
- After editing a skill, confirm that the installed environment loads the intended revision.
- Exercise the relevant branches with representative input and inspect the resulting artifacts.
- Update references, dependency declarations and verification steps in the same change as the behavior they describe.
</rules>
