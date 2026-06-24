---
name: skill-designer
description: Use when the user wants to design a new Claude Code skill or orchestrator workflow before implementation — model A/B/C/D, subagents, contracts, state, substrate (skill-orchestration vs dynamic workflow). Trigger: "design a skill", "thiết kế skill/workflow", "/skill-designer". Outputs design.md ready for /skill-writer. Do NOT use to implement SKILL.md (use /skill-writer) or run an existing workflow.
argument-hint: "[task description]"
allowed-tools: Read Grep Glob Write Edit Bash
---

# skill-designer

## purpose

Guide user from task goal → workflow design document at `.claude/skills/{name}/docs/design.md`, ready for `/skill-writer`.

## dependencies

- `${CLAUDE_SKILL_DIR}/docs/orchestrator-rules.md` — schemas, model decision matrix, anti-patterns
- `${CLAUDE_SKILL_DIR}/docs/design-template.md` — output document template + field reference
- `${CLAUDE_SKILL_DIR}/docs/plan-gate-spec.md` — Plan Gate + Deliverable Checklist consolidated spec
- `docs/agent-guide/general/markdown.md` — markdown formatting
- `.claude/rules/doc-organization.md` — designed skill MUST NOT inline substantive code rule; reference agent-guide §ID instead

## workflow

1. Read `docs/orchestrator-rules.md` + `docs/design-template.md` + `docs/plan-gate-spec.md` before step 2.
2. If `$ARGUMENTS` present → treat as task description, go to step 4. Else ask: "What task to automate? Describe inputs, outputs, task count, dependencies."
3. Gather missing fields: input, output, volume (1/few/many), step dependencies, quality gate.
4. Apply orchestration decision table (§needs-assessment). Present result + reasoning. Confirm with user.
5. If Model A → advise direct SKILL.md write, point to `/skill-writer`, STOP.
6. Apply §substrate-selection. Dynamic-workflow → record `Substrate: dynamic-workflow` in design.md Overview; Planning Gate / State Management / Staging Files sections = "n/a — runtime-managed"; implementation goes to `/skill-writer` §workflow-branch. Skill-orchestration → continue as-is.
7. Present model table (§model-selection). Recommend one model with reason. Confirm.
8. Design subagents — one row per agent in template Subagents table. Reject any agent whose objective is not one sentence; split instead.
9. Design phases (cohesive XOR distributed), planning gate, output contracts, state file, staging files, QA review, batch size, safety controls, self-healing — fill each section of `design-template.md` (dynamic-workflow → skip the n/a sections per step 6).
10. Run token budget estimate: `SKILL.md + (subagent_count × avg_output) + overhead + 30% headroom`. Flag if exceeds limits.
11. Ask user for skill name (kebab-case, 4-20 chars) AND skill prefix (lowercase, 4-8 chars, unique under `.agent/tmp/`). Derive prefix from name: take stem (drop common suffixes `-writer`, `-designer`, `-impl`, etc.), truncate to ≤ 8 chars; if collision, ask user to disambiguate. Warn if `.claude/skills/{name}/` already exists OR `.agent/tmp/{prefix}/` already in use. (dynamic-workflow → no prefix needed; runtime manages state.)
12. Run `mkdir -p .claude/skills/{name}/docs` then Write `design.md` filled from `design-template.md`.
13. Verify against full `## design-checks` list (all 22 items). Report PASS only when zero violations. Output failing checks with file line refs.

## needs-assessment

Orchestration needed when ANY signal true:

| signal | meaning |
|--------|---------|
| multiple distinct phases | analyze → generate → review |
| batch processing | >1 item same treatment |
| state tracking | need resume after interruption |
| QA review cycle | worker + reviewer pattern |
| parallel independent subtasks | yes |
| step output feeds next step | yes |

All false → Model A (single skill, no orchestrator).

## substrate-selection

Orchestration needed → choose who holds the plan (full mapping + caveats: `orchestrator-rules.md <substrate_selection>`):

| signal | substrate |
|--------|-----------|
| dozens-hundreds of agents; repeatable scripted run; adversarial cross-check of findings; no mid-run user gate | dynamic workflow (`.claude/workflows/` → `/name`; implement via `/skill-writer` §workflow-branch) |
| mid-run user approval gate; resume across sessions; env lacks workflows (CLI < 2.1.154, disabled, free plan) | skill orchestration (Model B/C/D, this skill's default) |

## model-selection

Model = topology (B/C/D applies to both substrates); substrate per §substrate-selection decides the runtime machinery.

| Model | Name | Use When |
|-------|------|----------|
| A | Single Skill | linear, 1 agent, no orchestrator |
| B | Sequential Subagents | output N feeds step N+1 |
| C | Parallel Subagents | independent subtasks, same phase |
| D | Hybrid (B+C) | sequential phases, each with parallel subtasks |

Selection:

| condition | model |
|-----------|-------|
| all subtasks independent, one phase | C |
| independent within phases, phases depend | D |
| clear dependency chain | B |
| short linear chain | B |

## design-checks

Apply during step 9. Substrate dynamic-workflow → rows on CONTRACT-V1 / staging / state / JOB_KEY / latest / retention / plan.json / acceptance / subagents-allowlist / input_ref / replan apply only to skill-orchestration; verify remaining rows + the substrate row.

- Orchestrator reads only CONTRACT-V1 fields, never domain content
- Subagent final message = CONTRACT-V1 block only
- Handoff > 500 tokens → staging file, pass path
- Parallel agents write to individual files only
- State file atomic rewrite per batch (not append)
- `active_batch` set pre-batch, cleared post-batch
- Layout `.agent/tmp/{prefix}/sessions/{JOB_KEY}/{SESSION}/` — prefix + job + session isolation
- `JOB_KEY` source declared in design.md (REPORT_ID | input-hash | slug)
- `latest` symlink per JOB_KEY for predictable resume
- Retention spec declared (archive 7d, delete 30d, cleanup_ready gated)
- Plan.json conforms to `<plan_v1>` (orchestrator-rules.md)
- Every phase `acceptance` is array; includes `schema:pass`; `domain:*` opt-in
- `domain:*` check → Reviewer agent named in Planning Gate
- `## Subagents` table in design.md doubles as allowlist; skill-writer copies it to SKILL.md `## subagents` (5-col mapping per §agent-file-template); plan `phase.agent` AND `task.agent` MUST ∈ Name column
- Inline `input` only for control primitives ≤ 500 token; domain payload → `input_ref`
- Replan via `revision++` overwrite (no `plan-v{N}.json` files)
- SKILL.md target stays < 800 lines
- Rules separated from agent flow (domain rules → `docs/`, agent → flow only)
- Output template embedded in agent definition (no runtime external read)
- Each agent has self-check ≥5 items, mix format + domain checks
- REJECT cycle max 2 rounds → then FAILURE
- Substrate declared in Overview (skill-orchestration XOR dynamic-workflow); dynamic-workflow → Planning Gate / State / Staging marked "n/a — runtime-managed"

## anti-patterns

- Cherry-picking items on resume — re-run entire batch
- `context: fork` when orchestrator needs result
- Subagent returns reasoning instead of CONTRACT-V1
- Parallel agents share write target
- Missing Avoid section in agent file
- State/staging files without skill prefix
- Flat layout `.agent/tmp/{prefix}/state-${SESSION}.json` (missing JOB_KEY → cross-function clutter)
- Timestamp in filename inside session dir (dir already timestamped — redundant)
- Rules hardcoded in agent definition (1 rule change = N file edits)
- Agent reads external file at runtime not passed via input
- Empty self-check or format-only checks
- No retention spec (stale sessions accumulate forever)
- Free-text `Acceptance checks` (must be array with `schema:*`/`domain:*` prefix)
- Mixing `schema:*` and `domain:*` in one check string
- Orchestrator self-evaluates `domain:*` (must delegate to Reviewer subagent)
- Domain payload inline in plan.json (use `input_ref`)
- Versioned plan files `plan-v1.json`, `plan-v2.json` (use `revision` field)
- Separate `allowed-agents` field/section (duplicates `## Subagents` table → drift)
- Skill spawns agent NOT in `## Subagents` table (hidden agent → audit failure)

## escalation

| error scope | handler |
|-------------|---------|
| add/edit rule in methodology file | agent self-fixes |
| change agent flow (step/input/output) | escalate |
| change orchestrator pipeline | escalate |

## examples

input: user says "I want to convert 50 markdown files to PDF in parallel, with a review step"
✅ output: Model D (parallel convert phase + sequential review phase), planner → convert batch → reviewer.

input: user says "audit all 300 API endpoints, cross-check every finding, fully unattended"
❌ output: Model C skill orchestrator with state.json + batches of 3-4
✅ output: Model C topology on dynamic-workflow substrate — scale + adversarial verify + no user gate → `.claude/workflows/`, implement via /skill-writer §workflow-branch.

input: user says "Fix this one bug in foo.ts"
❌ output: design Model B workflow
✅ output: Model A — no orchestration. Point to /skill-writer or direct edit.

input: subagent objective = "analyze input, then generate output, then format result"
❌ output: accept as single agent
✅ output: split into 3 agents (one sentence each)
