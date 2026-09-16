---
paths:
  - ".claude/skills/**"
scope: portable
---

# Skills that own a workflow

## §1 Establish the purpose and entry conditions

A skill owns a repeatable workflow with a recognizable trigger, an ordered set of dependencies and a result that can be checked. Before creating one, inspect existing skills and decide whether the requested workflow already has an owner. Extend that owner when the work is the same; create a separate skill when its responsibility is distinct.

Describe the task the skill handles, the information it needs and the circumstances in which another workflow should be used. Test the routing description against both an intended request and a nearby request outside its scope. Similar terminology is acceptable when the responsibilities remain distinguishable.

## §2 Keep metadata separate from instructions

Store the skill entry point in `SKILL.md`. For genome-managed skills, declare `name` and `description` in YAML frontmatter so that the package has an explicit identity and routing description. Use a name accepted by the installed Claude Code version and keep it consistent with the packaged skill. These fields are a packaging contract, not a prose template.

Only add optional metadata when the workflow needs it and the installed platform supports it. Check its actual meaning before relying on it, especially invocation controls or tool permissions. Do not infer a capability from a field that happens to parse as YAML. The [Claude Code skill reference](https://code.claude.com/docs/en/skills) describes the platform fields; verify local loading when the workflow depends on a particular behavior.

## §3 Describe an executable workflow

State what inputs and dependencies each operation requires, how it uses earlier results, and which conditions select another branch or stop the work. Identify required tools, libraries, credentials or external resources without embedding secrets in the instructions. Resolve environment-specific paths from the project or runtime instead of assuming that every installation uses the author's machine layout.

Define the information or artifact handed back at completion and the evidence needed to accept it. Include a verification step that checks the requested result against its source of truth. If execution fails, retain enough state to explain the failure and resume safely; do not report the intended result as completed.

Keep the skill's own orchestration in its body. Shared rules belong at the source identified by `doc-organization.md` §1 and are referenced by stable section identifiers. A skill must not become a second authoritative copy of project conventions or shared domain rules.

## §4 Package dependencies with the skill

Place scripts, templates and reference material with the skill when they are part of its implementation, and provide explicit references from the entry point. A resource needed by a branch must be reachable before that branch executes. Verify that the installed package contains the files the workflow names.

Separate resources by purpose or independent branch when that makes loading selective. Do not split a file merely to meet an arbitrary line count, and do not require an assistant to discover a chain of undocumented dependencies. Use the project placement rules for work records and deliverables rather than writing task output into the installed skill package.

## §5 Validate routing and maintenance changes

After editing a skill, confirm that the installed environment loads the intended revision. Exercise its relevant branches with representative input and inspect the resulting artifacts. When routing fails, examine the task boundaries and description; when execution fails, examine the dependency and operation that failed.

Update references, dependency declarations and verification steps in the same change as the behavior they describe. Requirements for the style of a user-facing product belong to that product's project-owned instructions, not to this shared skill standard.
