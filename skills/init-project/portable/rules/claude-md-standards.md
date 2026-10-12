---
paths:
  - "**/CLAUDE.md"
scope: portable
---

<critical>
scope: creating or editing a project's `CLAUDE.md`, the entry point loaded on every turn.
never: keep a second authoritative copy of a shared requirement in `CLAUDE.md`, or replace an existing entry point with an unfilled template.
note: a purpose paragraph under the title states the work and the assistant's role, and the file keeps the fixed section set `stack`, `NEVER`, `ALWAYS`, `scope`, `language`, `see also` (§1); it is written in English regardless of the conversation language.
</critical>

# Project instructions in CLAUDE.md

## §1 Responsibility of the project entry point

`CLAUDE.md` identifies the project, establishes its work boundaries and directs the assistant to the guidance it needs. The repository's contents do not reveal the kind of work by themselves — a project full of code may exist to publish videos — so the purpose paragraph states it before the assistant reads anything else. The section names are deliberately short and constant so the assistant recognizes each section's purpose before reading it, and the constraints sit at the top of the file where attention is highest. Rewording the prose inside a section does not change its heading.

<rules section="ALWAYS">
- Open the file with a purpose paragraph under the title, before `stack`: what the project exists to produce, the kind of work that produces it, the role the assistant takes, and which technical parts of the repository are tools serving that work rather than the work itself.
- Keep the fixed section set in this order: `stack`, `NEVER`, `ALWAYS`, `scope`, `language` and `see also`.
- Put a hard limit under `NEVER`; put a required action, or a reading that must precede an action, under `ALWAYS`, where subsections may group the entries.
- Record ownership under `scope`, language choices under `language` and references under `see also`.
- Record the relevant stack, ownership, authorized operations and project conventions where those facts affect decisions, and include the entry points for task-specific guides, lessons and roles.
- Name in `stack` each language the project's code is written in, the style standard it follows and the commands that format, lint and test it, or state that the project has none; `.agent-workspace/guide/general/writing-code.md` §2 reads them from there.
- Treat existing project instructions as project-owned data: when initializing or updating the genome, merge the applicable instructions and resolve conflicts.
- Write the file in English.
</rules>

<rules section="NEVER">
- Replace the file with an unfilled template.
- Invent project values that have not been established.
- Wrap the file in XML; the entry point is plain Markdown.
</rules>

## §2 Place each instruction at its owner

The entry point exposes the obligations needed before a task can be routed. Detailed guidance belongs with the work that uses it. Moving text out of the entry point is incomplete if the assistant can no longer find it before acting.

<rules section="ALWAYS">
- Use `doc-organization.md` §8.3 to decide whether information belongs in the project entry point, a path-scoped rule, a guide, a skill or another project record.
- Reference a shared requirement through its canonical source.
- When an instruction is extracted, preserve its reachability under `doc-organization.md` §10.
</rules>

<rules section="NEVER">
- Maintain a second authoritative copy of a shared requirement in `CLAUDE.md`.
</rules>

## §3 Define when guidance is read

A link anywhere in the repository does not make a rule available at the right time.

<rules section="ALWAYS">
- For each required reading, identify the condition and the target file, using the observable trigger kinds in `doc-organization.md` §10.
- Give a trigger a condition that can be evaluated before the guidance is needed: the user's message, a countable work state or the action about to be taken.
- Follow the actual route from the project entry point through the relevant router to the guidance, and ensure every target exists.
</rules>

<example type="trigger_line">
input: a guide that must be read before rendering a composition
❌ Read the local runtime guide when working on video.
✅ Before starting Remotion Studio or rendering a composition, read `.agent-workspace/guide/general/local-runtime.md`.
</example>

## §4 Maintain and verify the entry point

A project entry point does not override higher-priority user or platform instructions. A file's location or a successful text search alone is not proof of what a session loaded.

<rules section="ALWAYS">
- When a project changes its tools, directories or ownership, update the affected instructions and their references together.
- Resolve conflicting instructions according to their authority and applicability.
- Verify that the file reflects the current project, that referenced guidance exists, and that a representative task can reach the rules it needs.
- Check actual loading behavior in the installed Claude Code environment when a change depends on it.
</rules>
