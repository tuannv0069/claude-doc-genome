# claude-doc-genome

This repository develops independent documentation genomes for Claude Code and Codex. Its own working instructions use the Claude genome.

## Project environment

The maintenance scripts use Node.js. The portable verification tools use Python and its standard library.

The Claude Code plugin metadata lives in `.claude-plugin/`.

The canonical bundle version is `skills/init-project/VERSION`. Use `node scripts/sync-version.mjs set X.Y.Z` when preparing a version change; the script updates all version mirrors.

## Authorization and project boundaries

Do not commit or push unless the user has requested that action. Use the authorization already given in the conversation; ask for clarification only when the intended action or its scope remains unresolved.

Keep project instructions, reusable workflow guidance and project deliverables in their appropriate locations. Read `.claude/rules/doc-organization.md` §8.3 when adding content, and update its routers and references whenever a file is added, moved, renamed or removed.

For the Claude genome, edit the live file, verify it, and then synchronize it into the bundle. The Codex genome is authored directly in `skills/init-codex-genome/`; it has no separate live authoring tree. Keep project-specific values out of portable content in both products.

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

Enable the repository hooks after cloning with `git config core.hooksPath .githooks`. Before handing off a change, run the relevant checks. For Claude portable changes, confirm that live files match their bundle copies. For Codex changes, follow `docs/codex/contributing.md` to check the skill directly. Record changes under Unreleased in `CHANGELOG.md`. Follow `CONTRIBUTING.md` for release work only when a release has been authorized.



## Ownership

| Area | Source and responsibility |
|---|---|
| Portable rules | Edit `.claude/rules/`, then synchronize into `skills/init-project/portable/rules/`. |
| Portable guides and roles | Edit `.agent-workspace/guide/general/` and `.agent-workspace/guide/roles/`, then synchronize their portable files. Routers belong to this project. |
| Portable tooling | Edit `.agent-workspace/tooling/`, then synchronize the genome tools into `skills/init-project/portable/tooling/`. |
| Optional skills and agents | Edit the live source under `.claude/skills/` or `.claude/agents/`. Promote only components intentionally owned by the genome. |
| Templates and init workflow | Edit `skills/init-project/templates/` and `skills/init-project/SKILL.md` directly. |
| Codex genome | Edit `skills/init-codex-genome/` directly. Support belongs in `tests/codex/`, `scripts/codex/` and `docs/codex/`; none is another genome source. |
| Repository tooling | Edit `scripts/`, hooks and CI directly. |
| Project records | Maintain this file, routers, lessons, decisions and repository documentation as project-owned content. |

## Project language choices

Author the distributed genome and public repository documentation in English. The design, rewrite plan and implementation report under `docs/genome/` are in Vietnamese for this work. These are this repository's language choices.

The default language for conversation in this project is Vietnamese, unless the user requests another language.

## Reference points

The shared workflow rules are `.claude/rules/file-reading.md`, `.claude/rules/critical-thinking.md` and `.claude/rules/doc-organization.md`. They govern source reading, evidence and document placement.

The human-facing overview is `README.md`; contribution and release procedures are in `CONTRIBUTING.md`. The current rewrite design and plan are under `docs/genome/`.
