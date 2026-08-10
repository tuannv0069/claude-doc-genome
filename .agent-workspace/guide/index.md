---
scope: project
---

<critical>
scope: map task → which `.agent-workspace/guide/` file to read on-demand.
never: auto-load any guide file | duplicate content from sub-files
always: read explicitly when task in column matches
</critical>

## §1 placement data (per `doc-organization.md §10`)

| key | value |
|---|---|
| always-loaded budget | 600 lines — total of `.claude/rules/*.md` without `paths:`. The three rules the genome deploys are the floor (330 lines at v2.0.0); everything above that is this project's headroom for its own always-loaded rules. Over budget → demote the least-used file to path-scoped, or split it into terse + pointer (`doc-organization.md §10`). |

Migration ledger — top-level files not yet at standard location (target = empty ledger, no permanent exemption):

| file | target area | move at |
|---|---|---|
| _(none — fresh init)_ | | |

## §2 router

### general (`.agent-workspace/guide/general/`)

| file (`.agent-workspace/guide/`) | read when |
|---|---|
| `general/five-why.md` | RCA / "5 why" / "root cause" request; debug bug in AI-produced artifact (code/doc) |
| `general/review-checklist-method.md` | run a free-form review / build a review checklist — §7 picks the instrument first (dedicated review skill usually wins); §1–§6 = the method for a non-code artifact, a non-diff scope, or an absence hunt |
| `general/doc-system-mechanics.md` | create / move / rename a file in this guide tree, or write a `§ID` pointer — area model + folder taxonomy + router laws (§7), reference mechanism (§2), enforcement layers (§5), design principles (§8.1). `doc-organization.md` decides WHERE content goes; this describes HOW the tree is built |
| `general/bug-report-format.md` | audit / review / find-bug request not owned by a skill — standard bug report format (finding schema, severity, skeleton) |
| `general/fix-impact-analysis.md` | fix a bug in any artifact (code/docs/rule/config) not owned by a skill — determine impact scope/blast radius before editing (probe dependents, map regression surfaces, verify the radius) |
| `general/lesson-capture.md` | agent was just corrected on method / same failure class recurred — record the working-technique lesson into the store `.agent-workspace/lessons/` (own router: `lessons/index.md`); §1 the three-store boundary, §4 escalation record → rule → machine check, §5 read-back routing |
| `general/markdown.md` | edit any `*.md` (GFM rules) |
| `general/mermaid.md` | create/edit Mermaid diagram |
| `general/orchestration-policy.md` | fan-out Edit/Write across >3 files / dispatch subagent for execution (no skill owns flow) — delegate Edit/Write, inline ≤3 files or warm context, escalate hard-reasoning, plan persistence; research/grep/read = orchestrator inline, but §6 persists its findings to a file past the 3rd read |
| `general/worktree.md` | create / use / clean up an isolated git worktree — path convention, symlink non-tracked config, pass realpath to child agents, cleanup only after verified push |
| `general/task-planning.md` | plan/execute any artifact-changing task (not a pure question) — scale rigor by size §2.1, task-type→form §2.2, plan-before-execute, design verification, genome-rule per sub-task, loop-back/off-ramp; small task → §2.1 inline exit |

<!-- areas (frontend/, backend/, bd/, dd/, ...) grow per doc-system-mechanics.md §7 as the project accumulates content; register each new file here in the same commit -->
