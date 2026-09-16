## Codex adapter: authority and evidence

These instructions connect Codex to this project's shared genome. Resolve every path from the project root. Claude Code and Codex use the same guidance, roles, lessons, decisions, wiki and task state under `.agent-workspace/`; harness-specific configuration and deployment records retain their own ownership.

Do not commit or push without the user's explicit request. Carry forward authority already granted for the task instead of asking for the same permission again. A tool's capabilities do not expand the user's authorization.

Before answering a new task, use a file-reading tool to read `.agent-workspace/lessons/index.md` §1 and `.agent-workspace/guide/roles/index.md` §1. This applies to questions and writing requests as well as edits. Read matched lesson stores and their one-hop checking stores; read the selected primary role and §6 of its checking roles. Do not infer that there is no match before reading the routers. When no row matches, continue without inventing a role or lesson requirement. Reuse unchanged lookups while the same action continues.

At task start, also read `.agent-workspace/rules/critical-thinking.md`, `.agent-workspace/rules/file-reading.md` and `.agent-workspace/rules/doc-organization.md` in full unless those unchanged sources are already available in the current context. They establish evidence, source-reading and ownership obligations across all their sections. The detailed procedures are reached through `.agent-workspace/guide/index.md` and the following conditions. A reference does not mean the target's contents have already been loaded.

When a condition below matches, read the named guide or standard in full before the governed action, unless the unchanged file is already available in the current context. The section reference identifies the entry to that requirement; it does not limit the reading to that section when the procedure continues elsewhere in the file. Role-router selection retains its separate primary-role and checking-section procedure.

## Procedures to read before the action they govern

Before changing an artifact or producing a deliverable, read `.agent-workspace/guide/general/task-planning.md` §1. Scale preparation and verification to the consequence and reversibility of the work. An accepted implementation request does not require another approval of ordinary steps.

Before editing a rule, guide, role or lesson requirement, responding to a review comment, or deciding to exclude work, accept debt or reject an alternative, read `.agent-workspace/guide/general/decision-journal.md` §1. Search standing decisions about the subject before reversing one.

Before investigating a defect or its root cause, read `.agent-workspace/guide/general/five-why.md` §1. Before applying a defect fix, read `.agent-workspace/guide/general/fix-impact-analysis.md` §1 and examine affected consumers.

Before performing a review or audit that has no owning skill, read `.agent-workspace/guide/general/review-checklist-method.md` §1. Before recording established review findings, read `.agent-workspace/guide/general/bug-report-format.md` §1.

When a working method fails or the user corrects it, read `.agent-workspace/guide/general/lesson-capture.md` §2 and capture the supported lesson during the same turn.

Before writing or editing a machine verification gate, including a `test_*.py` or `verify_*.py` file, read `.agent-workspace/guide/general/verification-gate-design.md` §1. Before running or judging genome validation or rule-health checks, read `.agent-workspace/guide/general/rule-health.md` §1.

Before editing more than three files or delegating execution, read `.agent-workspace/guide/general/orchestration-policy.md` §1 and save the execution plan. Place unspecified working files under `.agent-workspace/tasks/<task-slug>/`. When research passes its third read or search, or is delegated, persist its sources and developing findings there under the guide's §4.

Before following an unpackaged guide procedure that has a trigger, dependent steps and a defined output, read `.agent-workspace/guide/general/capability-packaging.md` §2. Finish the current task before raising any optional packaging proposal.

Before creating, using or removing an isolated Git worktree, read `.agent-workspace/guide/general/worktree.md` §1. Preserve useful work and verify the exact target before cleanup.

## Standards selected by the intended operation

Before creating, editing or renaming an `AGENTS.md` or `AGENTS.override.md` file, read `.agent-workspace/rules/agents-md-standards.md` §1. Do not assume a child instruction file is selected merely because a file in that directory is being edited.

Before creating, editing or renaming a file under `.agents/skills/`, or another installed Codex skill's owned files, read `.agent-workspace/rules/skill-md-standards.md` §1. Before changing a custom agent definition under `.codex/agents/`, read `.agent-workspace/rules/codex-agents-standards.md` §1. A working role is not a request to spawn a separate agent.

Before editing Codex configuration, execution policies, hooks or MCP declarations, read `.agent-workspace/rules/codex-config-standards.md` §1. Do not alter personal permissions, trust or model choices merely to install the genome.

Before adding, moving, renaming or removing a rule, guide, router or other instruction-network file, read `.agent-workspace/rules/doc-organization.md` §4 and `.agent-workspace/guide/general/doc-system-mechanics.md` §2. Update affected routes, triggers and stable references together. Before changing a role or its routing, also read `.agent-workspace/guide/general/role-selection.md` §1.

Before editing Markdown whose rendering or parser behavior matters, read `.agent-workspace/guide/general/markdown.md` §1. Before creating or changing a Mermaid diagram, read `.agent-workspace/guide/general/mermaid.md` §2.

Before investigating project subject material for which established knowledge may already exist, read `.agent-workspace/wiki/index.md` §1. When its registered subjects match, or before editing wiki claims, read `.agent-workspace/rules/wiki-tier.md` §1. An inactive or unmatched wiki adds no claim-writing obligation.
