---
scope: portable
---

# Choosing a working perspective

## §1 Select from the actual action

Read `.agent-workspace/guide/roles/index.md` at the start of a task, including conversational questions and writing requests. Read both project and genome rows before selecting. An explicitly requested role takes precedence; otherwise a project-specific match takes precedence over a genome match, and a specific action takes precedence over a broader one.

Read the selected primary role in full and §6 of each checking role. If two applicable rows differ in specificity, use the more specific primary and add the other primary as a checking perspective. Reuse the lookup while the action and sources are unchanged. An owning skill may define its own selection.

## §2 Respect domain boundaries

When no row matches, proceed without forcing a role. Software requirements, executable scripts and software quality assurance are not the same work as narrative planning, video scripts or editorial review. A project may add its own creative or other domain roles when needed.

A role is a reasoning perspective, not a permission grant or a request to spawn another agent. It cannot override project requirements or user authority. Resolve conflicting portable guidance at its proper source; use a project role for a project-specific requirement rather than adding that exception to a portable role.

## §3 Define and route a role

A role describes its responsibility, questions, decision criteria, level of detail, evidence and completion conditions. Keep §6 for completion criteria because checking-role routing reads that section directly. Other section identities remain stable when referenced. If a handoff names another role, that role must exist and be discoverable.

The router uses `work type`, `primary role` and `checking roles` columns. Primary cells contain one kebab-case role name. Checking cells may be empty or contain comma-separated role names. Each name identifies a Markdown file in the role directory, and every role must be reachable through a row. These fields are routing data rather than a format imposed on deliverables.

## §4 Delegate the right perspective

Choose a delegated task's role from the delegated action. Send its primary and checking paths with the assignment instead of assuming the child sees the parent's selection. State when no role matched. Do not load unrelated roles to imply thoroughness.

## §5 Maintain project extensions

Create project roles with `scope: project` and register them in the project table. Update router entries and handoffs when renaming or removing a role. A role becomes portable only after its cross-project responsibility and evidence requirements have been evaluated through this Codex product's maintenance process.
