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
{{NEVER_PROJECT_RULES}}

## ALWAYS
- new doc content → place via `.claude/rules/doc-organization.md §8.3` decision tree
- add/rename/move/delete a content file → update every linking node (router, trigger, §ID pointer) in the same commit
- debug / root cause / RCA / "why" / "root cause" → MUST Read `docs/agent-guide/general/five-why.md` first
- write/edit mermaid block in .md → MUST Read `docs/agent-guide/general/mermaid.md` before emit
- fan-out Edit/Write across >3 files / dispatch subagent for execution (no skill owns flow) → MUST Read `docs/agent-guide/general/orchestration-policy.md` first (delegate Edit/Write to implementer model, inline ≤3 files or warm context, escalate hard-reasoning; persist plan to durable file); research/grep/read/analyze = orchestrator inline; skill-driven flow excluded
- create / use / clean up isolated git worktree → MUST Read `docs/agent-guide/general/worktree.md` first (path convention, symlink non-tracked config, pass realpath to child agents, cleanup only after verified push)
{{ALWAYS_PROJECT_RULES}}
{{OPTIONAL_MODULE_TRIGGERS}}

<!-- git: minimal guardrail above (NEVER block); detailed policy is scope: project — when the project writes docs/agent-guide/general/git.md, add its trigger line here in the same commit (reachability — never a trigger pointing at a missing file) -->

## scope
{{SCOPE_TABLE}}

## language

| target | language |
|--------|----------|
| frontmatter `scope: portable` | English, any location (overrides rows below) |
| `.claude/**` | English |
{{LANGUAGE_ROWS}}
| conversation default | {{CONVERSATION_LANGUAGE}} |

## see also

always-loaded (`.claude/rules/`):
- `file-reading.md` — grep vs Read, parallel, subagent
- `critical-thinking.md` — agent decision posture
- `doc-organization.md` — placement decision tree §8.3 + one-source-of-truth §ID + link integrity
{{SEE_ALSO_PROJECT}}

on-demand: read `docs/agent-guide/index.md` → task → which file.
