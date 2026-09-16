# {{PROJECT_NAME}}

{{ONE_LINE_DESCRIPTION}}

## Project environment

{{STACK_RUNTIME}}

{{STACK_FRONTEND}}

{{STACK_OTHER}}

## Authorization and project boundaries

Do not commit or push unless the user has requested that action. Use the authorization already given in the conversation; ask for clarification only when the intended action or its scope remains unresolved.

Keep project instructions, reusable workflow guidance and project deliverables in their appropriate locations. Read `.claude/rules/doc-organization.md` §8.3 when adding content, and update its routers and references whenever a file is added, moved, renamed or removed.

{{NEVER_PROJECT_RULES}}

## Starting work

Before answering a new task, read `.agent-workspace/lessons/index.md` §1 and `.agent-workspace/guide/roles/index.md` §1 with the file-reading tool. These two lookups are required for conversational questions and writing requests as well as tasks that change files. Do not infer that no row matches before reading the indexes. Read the stores whose work types match, including their one-hop checking stores. Do not repeat an unchanged lookup while the same work continues.

Consult `.agent-workspace/guide/roles/index.md` §1 to choose the primary role and its checking roles. Read the primary role and the checking roles' §6 before acting. If no work type matches, continue without forcing a role onto the task.

Use `.agent-workspace/guide/index.md` to find further guidance relevant to the work. The following conditions identify procedures that need to be read before their corresponding action.

## Procedures to read before acting

Before editing a rule, guide, role or lesson store, answering a review comment, or deciding to exclude work, accept debt or reject an option, read `.agent-workspace/guide/general/decision-journal.md`. Search existing decisions about the subject before reversing an earlier choice.

When investigating a defect or its root cause, read `.agent-workspace/guide/general/five-why.md`.

Before running a review or audit that is not owned by a skill, read `.agent-workspace/guide/general/review-checklist-method.md`. Its §7 helps select the review instrument.

Before recording findings already established by a review, read `.agent-workspace/guide/general/bug-report-format.md`.

Before fixing a defect in code, documentation, a rule or configuration, read `.agent-workspace/guide/general/fix-impact-analysis.md` to identify affected dependents.

When a working method fails or the user corrects it, read `.agent-workspace/guide/general/lesson-capture.md` and record the lesson while the evidence is available.

Before writing or editing a Mermaid diagram, read `.agent-workspace/guide/general/mermaid.md`.

Before writing or editing a machine verification gate, including a `test_*.py` or `verify_*.py` file, read `.agent-workspace/guide/general/verification-gate-design.md`.

Before following a guide procedure with a defined trigger, ordered steps and an output but no owning skill or agent, read `.agent-workspace/guide/general/capability-packaging.md` §2.

Before running `scan_rule_health.py` or judging its findings, read `.agent-workspace/guide/general/rule-health.md`.

Before editing more than three files or delegating execution outside a skill-owned workflow, read `.agent-workspace/guide/general/orchestration-policy.md`. Store the execution plan in the task workspace before dispatching work.

Place working files without a specified destination under `.agent-workspace/tasks/<task-slug>/`. When research passes its third read or search, or involves another agent, persist its findings there according to `.agent-workspace/guide/general/orchestration-policy.md` §6. Keep finished deliverables in the project's work-product area.

Before creating, using or removing an isolated Git worktree, read `.agent-workspace/guide/general/worktree.md`.

{{ALWAYS_PROJECT_RULES}}

{{OPTIONAL_MODULE_TRIGGERS}}

## Ownership

{{SCOPE_TABLE}}

## Project language choices

{{LANGUAGE_ROWS}}

The default language for conversation in this project is {{CONVERSATION_LANGUAGE}}.

## Reference points

The shared workflow rules are `.claude/rules/file-reading.md`, `.claude/rules/critical-thinking.md` and `.claude/rules/doc-organization.md`. They govern source reading, evidence and document placement.

{{SEE_ALSO_PROJECT}}
