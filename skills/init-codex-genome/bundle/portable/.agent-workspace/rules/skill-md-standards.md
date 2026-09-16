---
scope: portable
---

# Codex skills

## §1 Give the workflow a distinct owner

A skill owns a repeatable procedure with recognizable entry conditions, dependencies and a result that can be checked. Inspect available skills before adding one. Extend an existing owner when the workflow is the same; create a separate capability when its responsibility differs.

Describe intended requests and nearby requests outside its scope. Skill discovery depends on metadata before the body is loaded, so a routing description must make the responsibility understandable without the full procedure.

## §2 Use supported metadata and discovery

The entry file is `SKILL.md`, with supported YAML `name` and `description` fields. Project skills use `.agents/skills/<name>/` for the Codex clients verified by this product. Resolve an installed skill's resources relative to its own location, separately from the target project root. Do not assume that a plugin cache, user skill directory and project directory coincide.

Optional metadata and `agents/openai.yaml` are used only when the client supports the required meaning. That YAML file describes a skill's UI or dependencies; it is not a custom subagent definition. Verify invocation and implicit routing against the actual installed client. Metadata appearing in a catalog does not prove that the workflow executed.

## §3 Describe dependencies and completion

State the inputs, ordered dependencies, branch conditions and failure handling that make the procedure executable. Identify external tools or access requirements without embedding credentials. Define the result and compare it with the source of truth before reporting completion. Preserve partial state after a failure so a retry can be assessed safely.

Keep the skill's own orchestration with the skill. Refer to shared guidance by file and stable section. A skill must not become another copy of the project's general requirements or impose its output conventions on unrelated work.

## §4 Package only owned resources

Bundle the scripts, templates and references required by the workflow and link to each dependency before its branch uses it. Check the installed package, not just the development checkout. Write task evidence to the project's task workspace rather than modifying the installed package.

Avoid having both plugin and project copies of the same skill active without a deliberate ownership choice. Similar names are not a merge contract. Installation and updates must retain project modifications and distinguish generated content from project-owned data.

## §5 Test the workflow

Test an intended invocation, a nearby nonmatching request and every materially changed execution branch. Verify the loaded revision after reloading or starting a new session. Investigate discovery, missing dependencies and incorrect procedure separately; making a description more forceful does not fix a broken script.
