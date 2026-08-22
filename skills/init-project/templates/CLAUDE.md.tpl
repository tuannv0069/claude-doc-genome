# {{PROJECT_NAME}}

{{ONE_LINE_DESCRIPTION}}

## stack
- {{STACK_RUNTIME}}
- {{STACK_FRONTEND}}
- {{STACK_OTHER}}

## NEVER
- commit or push without explicit user request (`commit`, `push`, `/commit`)
- inline substantive rule in agent/skill/catalog — reference source-of-truth §ID; see `.claude/rules/doc-organization.md`
- soften disagreement into "you could also consider" — say so directly
- change position from user pressure alone — require new info/reasoning
- place a guide under `docs/` or a work product under `.agent-workspace/` — see `.claude/rules/doc-organization.md §11`
{{NEVER_PROJECT_RULES}}

## ALWAYS
- start any artifact task (write / edit / review / investigate) → MUST Read `.agent-workspace/lessons/index.md` §1 first → row matches the work about to be done → read that store; no row matches → skip, lookup done
- new doc content → place via `.claude/rules/doc-organization.md §8.3` decision tree
- add/rename/move/delete a content file → update every linking node (router, trigger, §ID pointer) in the same commit
- debug / root cause / RCA / "why" / "root cause" → MUST Read `.agent-workspace/guide/general/five-why.md` first
- run a review (audit / review / code review / inspect / vet / find bug(s) / build a checklist, incl. running against an existing checklist) (free-form, not a skill-owned flow) → MUST Read `.agent-workspace/guide/general/review-checklist-method.md` first — its §7 picks the instrument (a dedicated review skill usually wins); §1–§6 is the fallback for a non-code artifact, a non-diff scope, or an absence hunt
- write or format a bug report for findings already determined, no review to run (free-form, not a skill-owned flow) → MUST Read `.agent-workspace/guide/general/bug-report-format.md`
- fix a bug / apply a fix / patch a defect in any artifact — code, docs, rule, config (free-form, not a skill-owned flow) → MUST Read `.agent-workspace/guide/general/fix-impact-analysis.md` first (scope the blast radius before editing)
- user corrects the method / rejects the output / "why did you" · "that's not right" · "it should be" → MUST Read `.agent-workspace/guide/general/lesson-capture.md` (record it in that same turn, into `.agent-workspace/lessons/<work-type>.md` — not harness memory, not a guide file)
- write/edit mermaid block in .md → MUST Read `.agent-workspace/guide/general/mermaid.md` before emit
- fan-out Edit/Write across >3 files / dispatch subagent for execution (no skill owns flow) → MUST Read `.agent-workspace/guide/general/orchestration-policy.md` first (delegate Edit/Write to implementer model, inline ≤3 files or warm context, escalate hard-reasoning; persist plan under `.agent-workspace/tasks/<task-slug>/<scope>/`); research/grep/read/analyze = orchestrator inline; skill-driven flow excluded
- agent creates a working file (script/dump/log/json/screenshot) with no user- or skill-specified destination → write under `.agent-workspace/tasks/<task-slug>/`; never repo root (layout: `.agent-workspace/guide/general/orchestration-policy.md` §4)
- research / investigation passes its 3rd file read or search, or dispatches an agent, with no file to change → MUST Read `.agent-workspace/guide/general/orchestration-policy.md` §6 — persist findings to `.agent-workspace/tasks/<task-slug>/` while working, never only in the reply
- create / use / clean up isolated git worktree → MUST Read `.agent-workspace/guide/general/worktree.md` first (path convention, symlink non-tracked config, pass realpath to child agents, cleanup only after verified push)
- skill writes its working files (plan, research notes, run state) to its own default path → redirect them to `.agent-workspace/tasks/<task-slug>/`; only the finished deliverable goes to `docs/` (full rule: `.agent-workspace/guide/general/orchestration-policy.md` §4; boundary: `doc-organization.md §11`)
{{ALWAYS_PROJECT_RULES}}
{{OPTIONAL_MODULE_TRIGGERS}}

<!-- git: minimal guardrail above (NEVER block); detailed policy is scope: project — when the project writes .agent-workspace/guide/general/git.md, add its trigger line here in the same commit (reachability — never a trigger pointing at a missing file) -->

## scope
{{SCOPE_TABLE}}

## language

| target | language |
|--------|----------|
| frontmatter `scope: portable` | English, any location (overrides rows below) |
| `CLAUDE.md` | English regardless of conversation language (`claude-md-standards.md`) |
| `.claude/**` | English |
| `.agent-workspace/guide/**` | English (portable doc standard) |
| `.agent-workspace/lessons/**` | English — same language as the paired guide, so a promotion is a copy, not a translation (`lesson-capture.md` §3) |
{{LANGUAGE_ROWS}}
| conversation default | {{CONVERSATION_LANGUAGE}} |

## see also

always-loaded (`.claude/rules/`):
- `file-reading.md` — grep vs Read, parallel, subagent
- `critical-thinking.md` — agent decision posture
- `doc-organization.md` — placement decision tree §8.3 + one-source-of-truth §ID + link integrity
- `conversational-output.md` — structure/tone of chat replies: conclusion-first, one idea per paragraph, fact vs recommendation labeled
{{SEE_ALSO_PROJECT}}

on-demand: read `.agent-workspace/guide/index.md` → task → which file.
