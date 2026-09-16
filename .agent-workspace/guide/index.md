---
scope: project
---

# Guide index

Use this index to find the guidance relevant to the task. The procedures live in the linked files; this index provides their routing information.

## §1 Placement data

This project records pending moves below. Resolve each entry by moving the file and updating its references according to `.claude/rules/doc-organization.md` §10.

| file | target area | move at |
|---|---|---|
| _(none)_ | | |

## §2 Router

### General guidance

The paths in this table are relative to `.agent-workspace/guide/`.

| file | read when |
|---|---|
| `general/five-why.md` | Read this when investigating a defect or its root cause. |
| `general/review-checklist-method.md` | Read this before a review or audit to select an instrument and determine how to inspect the evidence. |
| `general/doc-system-mechanics.md` | Read this when creating or reorganizing the guide tree, maintaining a router, or adding a section reference. |
| `general/capability-packaging.md` | Read this when a repeatable guide procedure has no owning skill or agent, or when assessing packaging candidates. |
| `general/bug-report-format.md` | Read this when recording findings whose evidence has already been established. |
| `general/fix-impact-analysis.md` | Read this before fixing a defect so that affected dependents are included in the work. |
| `general/lesson-capture.md` | Read this when a working method fails, when the user corrects it, or when maintaining lesson stores. |
| `general/markdown.md` | Read this when editing Markdown and checking its syntax or links. |
| `general/mermaid.md` | Read this before creating or changing a Mermaid diagram. |
| `general/orchestration-policy.md` | Read this before delegating execution or editing more than three files outside a skill-owned workflow. Its §6 also covers research persistence. |
| `general/decision-journal.md` | Read this when a decision needs to be recorded, when interpreting an earlier decision, or before reversing a rule. |
| `general/worktree.md` | Read this before creating, using or removing an isolated Git worktree. |
| `general/task-planning.md` | Read this when planning work that changes an artifact and deciding how to verify its outcome. |
| `general/verification-gate-design.md` | Read this before writing a machine verification gate or evaluating whether its checks prove the intended requirement. |
| `general/rule-health.md` | Read this before running the rule-health scanner or judging its findings. |
| `general/role-selection.md` | Read this when selecting roles, adding a role, or maintaining the role router. |


### Roles

| file | read when |
|---|---|
| `roles/index.md` | Consult this at the start of a task to select the primary role and the checking roles. |

Lesson stores have their own router at `.agent-workspace/lessons/index.md` §1. Register them there, following `general/lesson-capture.md` §7. When the guide tree gains a new area, register its content according to `general/doc-system-mechanics.md` §7.
