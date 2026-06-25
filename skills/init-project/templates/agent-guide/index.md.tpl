---
scope: project
---

<critical>
scope: map task → which `docs/agent-guide/` file to read on-demand.
never: auto-load any agent-guide file | duplicate content from sub-files
always: read explicitly when task in column matches
</critical>

## §1 placement data (per `doc-organization.md §10`)

| key | value |
|---|---|
| always-loaded budget | {{ALWAYS_LOADED_BUDGET}} lines (total of `.claude/rules/*.md` without `paths:`) |

Migration ledger — top-level files not yet at standard location (target = empty ledger, no permanent exemption):

| file | target area | move at |
|---|---|---|
| _(none — fresh init)_ | | |

## §2 router

### general (`docs/agent-guide/general/`)

| file (`docs/agent-guide/`) | read when |
|---|---|
| `general/five-why.md` | RCA / "5 why" / "root cause" request; debug bug in AI-produced artifact (code/doc) |
| `general/review-checklist-method.md` | build a review checklist / run a free-form bug-finding review not owned by a skill — bug-hypothesis method (absence-first, gated hunt, honest confirmation) |
| `general/bug-report-format.md` | audit / review / find-bug request not owned by a skill — standard bug report format (finding schema, severity, skeleton) |
| `general/fix-impact-analysis.md` | fix a bug in any artifact (code/docs/rule/config) not owned by a skill — determine impact scope/blast radius before editing (probe dependents, map regression surfaces, verify the radius) |
| `general/markdown.md` | edit any `*.md` (GFM rules) |
| `general/mermaid.md` | create/edit Mermaid diagram |
| `general/orchestration-policy.md` | fan-out Edit/Write across >3 files / dispatch subagent for execution (no skill owns flow) — delegate Edit/Write, inline ≤3 files or warm context, escalate hard-reasoning, plan persistence; research/grep/read = orchestrator inline |
| `general/worktree.md` | create / use / clean up an isolated git worktree — path convention, symlink non-tracked config, pass realpath to child agents, cleanup only after verified push |
{{GENERAL_OPTIONAL_ROWS}}

<!-- areas (frontend/, backend/, bd/, dd/, ...) grow per doc-organization.md §7 as the project accumulates content; register each new file here in the same commit -->
