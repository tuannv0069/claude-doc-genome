# {{PROJECT_NAME}}

{{PROJECT_PURPOSE}}

## stack

{{STACK_RUNTIME}}

{{STACK_FRONTEND}}

{{STACK_OTHER}}

## NEVER

Do not commit or push unless the user has requested that action. Use the authorization already given in the conversation; ask for clarification only when the intended action or its scope remains unresolved.

Do not record a correction, a working preference, a project fact or any other guidance this project must keep in the assistant's harness memory, which exists on one machine only; place it in the repository through `.claude/rules/doc-organization.md` §8.3. Do not link, cite or anchor a committed file to `.agent-workspace/tasks/`, which is gitignored and disposable; move content worth keeping to its work-product destination first, as `.claude/rules/doc-organization.md` §10 requires.

{{NEVER_PROJECT_RULES}}

## ALWAYS

Keep project instructions, reusable workflow guidance and project deliverables in their appropriate locations. Read `.claude/rules/doc-organization.md` §8.3 when adding content, and update its routers and references whenever a file is added, moved, renamed or removed.

### Starting work

Before answering a new task, read `.agent-workspace/lessons/index.md` §1 and `.agent-workspace/guide/roles/index.md` §1 with the file-reading tool. These two lookups are required for conversational questions and writing requests as well as tasks that change files. Do not infer that no row matches before reading the indexes. Read the stores whose work types match, including their one-hop checking stores. Do not repeat an unchanged lookup while the same work continues. State the result of both lookups in the reply before the first substantive step, as `.agent-workspace/guide/general/lesson-capture.md` §7 and `.agent-workspace/guide/general/role-selection.md` §2 require.

Consult `.agent-workspace/guide/roles/index.md` §1 to choose the primary role and its checking roles. Read the primary role and the checking roles' §6 before acting. If no work type matches, continue without forcing a role onto the task.

Use `.agent-workspace/guide/index.md` to find further guidance relevant to the work. The following conditions identify procedures that need to be read before their corresponding action.

### Procedures to read before acting

Before editing a rule, guide, role or lesson store, answering a review comment, or deciding to exclude work, accept debt or reject an option, read `.agent-workspace/guide/general/decision-journal.md`. Search existing decisions about the subject before reversing an earlier choice.

When investigating a defect or its root cause, read `.agent-workspace/guide/general/five-why.md`.

Before running a review or audit that is not owned by a skill, read `.agent-workspace/guide/general/review-checklist-method.md`. Its §7 helps select the review instrument.

Before recording findings already established by a review, read `.agent-workspace/guide/general/bug-report-format.md`.

Before fixing a defect in code, documentation, a rule or configuration, read `.agent-workspace/guide/general/fix-impact-analysis.md` to identify affected dependents.

When a working method fails or the user corrects it, read `.agent-workspace/guide/general/lesson-capture.md` and record the lesson while the evidence is available.

Before recording the measured outcome of a delivered work product, before writing the expectation for a work product about to be released, or before writing a working method into the project's standard on the strength of its results, read `.agent-workspace/guide/general/method-review.md`.

Before writing or editing a Mermaid diagram, read `.agent-workspace/guide/general/mermaid.md`.

Before writing, editing or reviewing source code or an executable script, read `.agent-workspace/guide/general/writing-code.md`.

Before creating an executable script, or creating, changing, moving, renaming or removing a file in a tool group or a product tool folder, read `.agent-workspace/guide/general/tooling.md` and the tool index at `.agent-workspace/tooling/index.md`.

Before writing or editing a machine verification gate, including a `test_*.py` or `verify_*.py` file, read `.agent-workspace/guide/general/verification-gate-design.md`.

Before following a guide procedure with a defined trigger, ordered steps and an output but no owning skill or agent, read `.agent-workspace/guide/general/capability-packaging.md` §2.

Before designing a workflow that will be run again (the body of a skill, a script that coordinates several agents, a guide procedure or a staged production process), or adding, removing, reordering, splitting or merging the steps of one, read `.agent-workspace/guide/general/workflow-measurement.md` and define the per-step record of active time and token cost in the same change.

Before running `scan_rule_health.py` or judging its findings, read `.agent-workspace/guide/general/rule-health.md`.

Before editing more than three files or delegating execution outside a skill-owned workflow, read `.agent-workspace/guide/general/orchestration-policy.md`. Store the execution plan in the task workspace before dispatching work.

When dispatching an agent or writing an agent definition, take the model and the reasoning effort from this mapping of the capability tiers in `.agent-workspace/guide/general/orchestration-policy.md` §3.

{{AGENT_MODEL_TIERS}}

Place working files without a specified destination under `.agent-workspace/tasks/<task-slug>/`. When research passes its third read or search, or involves another agent, persist its findings there according to `.agent-workspace/guide/general/orchestration-policy.md` §6. Keep finished deliverables in the project's work-product area.

Before creating, using or removing an isolated Git worktree, read `.agent-workspace/guide/general/worktree.md`.

{{ALWAYS_PROJECT_RULES}}

{{OPTIONAL_MODULE_TRIGGERS}}

## scope

{{SCOPE_TABLE}}

## language

{{LANGUAGE_ROWS}}

The default language for conversation in this project is {{CONVERSATION_LANGUAGE}}.

## see also

The shared workflow rules are `.claude/rules/file-reading.md`, `.claude/rules/critical-thinking.md`, `.claude/rules/doc-organization.md` and `.claude/rules/natural-language-writing.md`. They govern source reading, evidence, document placement and writing text a native speaker would actually produce.

{{SEE_ALSO_PROJECT}}
