---
paths:
  - "**/CLAUDE.md"
scope: portable
---

# Project instructions in CLAUDE.md

## §1 Responsibility of the project entry point

Use `CLAUDE.md` to identify the project, establish its work boundaries and direct the assistant to the guidance it needs. Record the relevant stack, ownership, authorized operations and project conventions where those facts affect decisions. Include the entry points for task-specific guides, lessons and roles.

Treat existing project instructions as project-owned data. When initializing or updating the genome, merge the applicable instructions and resolve conflicts instead of replacing the file with an unfilled template. Do not invent project values that have not been established.

## §2 Place each instruction at its owner

Use `doc-organization.md` §8.3 to decide whether information belongs in the project entry point, a path-scoped rule, a guide, a skill or another project record. The entry point should expose the obligations needed before a task can be routed. Detailed guidance belongs with the work that uses it.

Reference a shared requirement through its canonical source rather than maintaining a second authoritative copy in `CLAUDE.md`. When an instruction is extracted, preserve its reachability under `doc-organization.md` §10. Moving text out of the entry point is incomplete if the assistant can no longer find it before acting.

## §3 Define when guidance is read

For each required reading, identify the condition and the target file. Use the observable trigger kinds in `doc-organization.md` §10. A trigger may depend on the user's message, a countable work state or the action about to be taken; it must be possible to evaluate the condition before the guidance is needed.

Do not assume that a link anywhere in the repository makes a rule available at the right time. Follow the actual route from the project entry point through the relevant router to the guidance, and ensure every target exists.

## §4 Maintain and verify the entry point

When a project changes its tools, directories or ownership, update the affected instructions and their references together. Resolve conflicting instructions according to their authority and applicability; a project entry point does not override higher-priority user or platform instructions.

Verify that the file reflects the current project, that referenced guidance exists, and that a representative task can reach the rules it needs. Check actual loading behavior in the installed Claude Code environment when a change depends on it. A file's location or a successful text search alone is not proof of what a session loaded.
