---
scope: portable
---

# Selecting a working role

A role provides a task-specific perspective, evidence standard, and completion check. It does not set the project's output style.

## §1 When this applies

Consult the role router when starting a task. When a skill owns the running workflow, use the role selection that workflow defines.

## §2 Choose the role from the action

Identify the action about to be performed, then read both tables in `.agent-workspace/guide/roles/index.md` before choosing a match. A project-specific row takes precedence over a genome row for the same work. Within one table, a row identifying a specific task or artifact takes precedence over a general row.

Read the primary role in full. For each checking role, read only its §6 completion criteria. When two applicable rows differ in specificity, use the more specific primary role and add the other primary role as a checking perspective.

If no row matches, continue without forcing a role onto the task. Do not repeat the lookup while the work type is unchanged. A role explicitly selected by the user takes precedence over the router.

## §3 Define a role by its responsibility

A role should explain what it examines, which questions guide its decisions, how it resolves competing criteria, what level of detail it covers, what evidence it accepts, and where its responsibility ends. Those meanings matter; they do not require a fixed number of sections or a prescribed sentence pattern.

Every role keeps §6 for completion criteria because checking-role selection reads that section directly. Existing stable section identifiers remain valid under `.claude/rules/doc-organization.md` §2. Additional sections can be added when they serve the role.

Completion criteria identify conditions that would leave the assigned work unresolved. They can be explained without a fixed negative-state formula. A role's criteria govern its task, not every task in the project.

When §7 identifies handoffs, mark receiving role names with backticks so the role verifier can resolve them. Those names identify existing roles in the router. The marker is a data convention for the handoff, not a rule for surrounding prose.

## §4 Delegate the subtask's role

Resolve the role for the delegated action, not the coordinating agent's own action. Pass the primary role's file path with the subtask so its executor can read the governing perspective.

Assign one primary role per subtask. Do not load additional full role files merely to imply thoroughness. If no role applies, state that the lookup found no match so the executor does not infer a missing assignment.

## §5 Add a domain role when the project needs one

A project can create a `scope: project` role for work the portable roles do not cover. Register it in the project table of `.agent-workspace/guide/roles/index.md` and use §3 to define its responsibility.

When a project needs a different policy from a portable role, create a project-specific role and route to it rather than changing the portable copy to contain a project exception. A role can enter the portable set through promotion after its usefulness across projects has been established.

If a role is deleted or renamed, update its router entries and every handoff that refers to it.

## §6 Router data contract

The role router uses the columns `work type`, `primary role`, and `checking roles`. The primary cell contains one role name. The checking cell can be empty or contain comma-separated role names.

Use kebab-case role names without backticks in these cells. Each name must identify an existing role file. Every role file other than the index must be reachable through at least one router row. The verifier reads this table as data; changes to its shape require a corresponding parser and test change.

## §7 Relationship to project requirements

A role describes how to reason about a class of work. It does not override a governing project requirement or expand the user's authorization.

When a role conflicts with a project rule or guide, apply the governing requirement and identify the conflicting role clause and source section. Correct the portable role only when the defect is portable; otherwise create a project role under §5. Do not turn a software-specific criterion into an obligation for creative work merely because both products are files.
