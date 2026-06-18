<critical>
scope: output template for skill-designer — fill and save to `.claude/skills/{name}/docs/design.md`.
core: every section filled | no `<placeholder>` left | feeds `/skill-writer`
</critical>

<rule_schema>
template: code block below = verbatim copy target
fields: each row = atomic, ≤ 1 line
</rule_schema>

---

<rules section="ALWAYS">
- copy template block verbatim → fill all placeholders
- declare Substrate in Overview (skill-orchestration | dynamic-workflow); dynamic-workflow → Planning Gate / State Management / Staging Files sections = "n/a — runtime-managed" (see orchestrator-rules `<substrate_selection>`)
- every subagent: 1 objective sentence | else split
- every phase: explicit transition condition
- self-check per agent: ≥ 5 items, mix format + domain
- handoff > 500 tokens → staging file, pass path
- skill prefix: lowercase, 4-8 chars, unique
- declare `JOB_KEY` source (REPORT_ID | input-hash | slug) in State Management
- declare retention (archive Nd | delete Md) in State Management
- plan.json conforms to `<plan_v1>` (orchestrator-rules.md) — phases/tasks naming
- every phase chooses cohesive (`phase.agent`) XOR distributed (`task.agent`)
- every phase acceptance lists `schema:pass` (mandatory); `coverage:*` for mechanical; `domain:<check_id>` opt-in
- `domain:*` check declared → name Reviewer agent in Planning Gate
- `## Subagents` table doubles as allowlist (no separate `allowed_agents` field)
- inline `input` for control primitives ≤ 500 token; else `input_ref`
- `scope_ref` set when phase has `domain:deliverables-complete` OR task produces > 3 deliverable types
- scope file at `<session-root>/staging/scope/<task-id>.md`, markdown nested checklist
- fill `## Decomposition Rationale` section (shape, axes, fold, ordering source)
</rules>

<rules section="NEVER">
- leave `<placeholder>` unfilled
- parallel agents share write target
- `inherit` model on accuracy-critical task
- empty self-check or format-only check
- staging without skill prefix
- staging without JOB_KEY segment (flat `.agent/tmp/{prefix}/state-*` layout)
- timestamp embedded in filename inside session dir (redundant)
- free-text `Acceptance checks` (use `schema:*` / `coverage:*` / `domain:*` prefix array)
- mix `schema:*`, `coverage:*`, `domain:*` in single check string
- domain payload inline in plan.json (`input_ref` always)
- versioned plan files (use `revision` field, single plan.json)
- `phase.agent` or `task.agent` not in `## Subagents` table Name column
- set BOTH `phase.agent` AND `task.agent` (mutex per phase — cohesive XOR distributed)
- mix `input_ref` (domain payload) and `scope_ref` (DC) purposes
- duplicate allowlist in separate section/field (table is the only source)
</rules>

---

## template

```markdown
# Workflow Design: <WORKFLOW_NAME>

## Overview
- Model: A | B | C | D
- Substrate: skill-orchestration | dynamic-workflow
- Description: <1-2 sentences>
- Input: <what it processes>
- Output: <what it produces>
- Skill prefix: <prefix | n/a for dynamic-workflow>

## Decomposition Rationale
- shape: atomic | sequential | parallel | tree
- model: A | B | C | D
- review_cycle: on | off
- outer_axes: [<axes with dependency arrows>]
- inner_axes: [<axes without arrows>]
- fold_axes: [<low-cardinality OR no-split axes → task.input metadata>]
- ordering_source: <where arrow rules come from (CLAUDE.md, project convention, data-flow)>
- scope_ref strategy: <which phases/tasks use scope_ref + which omit>
- delegation: <none | tasks delegated to sub-skill X (Tier 2)>

## Subagents
This table is **also the allowlist** — plan.json `phase.agent` AND `task.agent` MUST appear in `Name` column. skill-writer copies this table to SKILL.md as `## subagents`.

| # | Name | Objective | Model | Effort | Input | Output |
|---|------|-----------|-------|--------|-------|--------|
| 1 | ... | ... | ... | ... | ... | CONTRACT-V1 + ... |

## Phases
| Phase | Name | Agent kind | Mode | Task count | Depends On | Transition |
|-------|------|-----------|------|-----------|------------|------------|
| 0 | Planning | cohesive (planner) | sequential | 1 | - | approve → phase 1 |
| 1 | ... | cohesive | parallel | N | phase 0 | SUCCESS → phase 2 |
| 2 | ... | distributed | sequential | N | phase 1 | SUCCESS → done |

`Agent kind`: **cohesive** = `phase.agent` set (1 agent for all tasks). **distributed** = `task.agent` per task (1 agent per task).

## Planning Gate
- Planner: <name | "orchestrator-direct" for uniform Model C>
- Planner model/effort: <model>/<effort>
- Plan file: .agent/tmp/<prefix>/sessions/<JOB_KEY>/<SESSION>/plan.json
- Plan schema: `<plan_v1>` (orchestrator-rules.md)
- requires_user_approval: <true | false>  (default false)
- Allowed agents: derived from `## Subagents` table (no separate list)
- Reviewer agent (required if any `domain:*` acceptance): <name | n/a>
- Replan policy: revision++ on domain:* REJECT, max 2 rounds → FAILURE; plan.json + scope files overwritten atomic
- Acceptance per phase:

| phase.id | acceptance checks |
|----------|-------------------|
| <id-1>   | schema:pass, coverage:<check>, domain:<check_id> |
| <id-2>   | schema:pass |

## State Management
- JOB_KEY source: <REPORT_ID | input-hash | slug from $ARGUMENTS>
- SESSION format: <${CLAUDE_SESSION_ID} | YYYYMMDD-HHMMSS-<6-hex>>
- Session root: .agent/tmp/<prefix>/sessions/<JOB_KEY>/<SESSION>/
- State file: <session-root>/state.json
- Latest pointer: .agent/tmp/<prefix>/sessions/<JOB_KEY>/latest (symlink → SESSION)
- Resume: read `latest` symlink → re-run active_batch from state.json
- Retention: archive 7d idle → archive/<JOB_KEY>/<SESSION>/; delete archived 30d (only when cleanup_ready=true)
- Cleanup: cleanup_ready + shared dispatcher

## Staging Files
location: `<session-root>/staging/` (inter-agent) | `<session-root>/staging/scope/` (DC files) | `<session-root>/artifacts/` (user-facing)

| File (no timestamp in name) | Purpose | Format | Writer | Reader |
|---|---|---|---|---|
| staging/<phase>-output.json | handoff phase→phase | .json | <agent> | <next agent> |
| staging/scope/<task-id>.md | Deliverable Checklist (DC) per task | .md (nested checklist) | planner | task agent + reviewer |
| artifacts/summary.md | end-user summary | .md | aggregator | user |
| artifacts/visual/<name>.png | screenshots | .png | visual agent | user/reviewer |

## QA Review
- Needed: yes | no
- Worker: <agent>
- Reviewer: <agent (or "folded into content reviewer")>
- Max rounds: 2

## Safety
- Permission mode: <mode>
- Tool allowlist per subagent: <list>
- Write scope: <allowed_prefixes>
- Worktree: yes | no
- PII handling: <if applicable>

## Self-Healing
- Rules file: <path | "embedded">
- Output template: embedded
- Self-check per agent: ≥5 (count each)
- Coverage protocol: COVERAGE_DONE + COVERAGE_SKIPPED in CONTRACT-V1 when scope_ref set
- Escalation: <criteria>

## Token Budget
- SKILL.md: ~X
- Per subagent output: ~Y
- Total + 30% headroom: ~Z
- Batch size: N

## Next Steps
1. Hand to `/skill-writer` to implement SKILL.md
2. Create `.claude/agents/*.md` per subagent
3. Create scope file template generator (planner agent emits per-task scope files at run time)
4. Test L1 (isolation) → L2 (smoke) → L3 (full)
```

---

<field_reference>

<conditional name="subagent_fields">
| field | rule |
|-------|------|
| Name | kebab-case |
| Objective | 1 sentence, 1 job (else split) |
| Model | haiku | sonnet | opus |
| Effort | low | medium | high | max |
</conditional>

<contract_v1>
```
STATUS: SUCCESS | FAILURE | SKIPPED | REJECT
CHANGES: <number>
MODIFIED_ITEMS: <list or ->
ERROR: <short or ->
DETAIL: <≤5 lines>
COVERAGE_DONE: <comma-separated scope leaf IDs | omit if no scope_ref>
COVERAGE_SKIPPED: <id (reason); id (reason); ... | omit if no scope_ref>
REASON: <if SKIPPED>
REJECT_DETAIL: <if REJECT>
```
</contract_v1>

<conditional name="phase_mode">
| mode | when |
|------|------|
| sequential | tasks ordered within phase (chain or shared write target) |
| parallel | tasks independent within phase (each owns its writes) |
</conditional>

<conditional name="agent_kind">
| kind | when |
|------|------|
| cohesive | `phase.agent` set; 1 agent processes all tasks; tasks/subtasks = WBS scope spec |
| distributed | `task.agent` per task; 1 agent per task; mode=parallel for independent work |
</conditional>

<conditional name="scope_ref_required">
| condition | scope_ref |
|-----------|-----------|
| phase acceptance has `domain:deliverables-complete` | required |
| task produces > 3 distinct deliverable types | required |
| cohesive phase with multiple work units | required |
| atomic task (1 deliverable) | omit |
| verification-only task | omit |
</conditional>

<conditional name="batch">
| field | default |
|-------|---------|
| size | 3-4 tasks |
| notify | 2 per batch (pre, post) |
| failure | log + continue (no fail-fast) |
</conditional>

</field_reference>

---

<examples>

<example type="objective_split">
input: "agent reads spec, parses sections, validates rules, writes report"
❌ output: single agent with 4 verbs
✅ output: parser-agent + validator-agent + writer-agent (1 verb each)
</example>

<example type="self_check">
input: writer agent self-check list
❌ output: ["output not empty", "JSON valid"]  (format-only, 2 items)
✅ output: 5+ items mixing format + domain: ["all sections present", "no `<placeholder>`", "every subagent has model+effort", "no parallel write to shared file", "self-check count ≥5 per agent"]
</example>

<example type="planning_gate_fill">
input: report-writer Planning Gate
❌ output:
```
Acceptance checks: plan is good, has 3 layers
```
✅ output:
```
Planner: report-planner | model: sonnet | effort: medium
Allowed agents: derived from `## Subagents` table (no separate list)
Reviewer agent: report-reviewer
Replan policy: revision++ on domain:* REJECT, max 2 rounds
Acceptance per phase:
| phase.id   | acceptance checks                                                  |
| analyze    | schema:pass                                                        |
| produce    | schema:pass, coverage:task-count-matches-axis, domain:deliverables-complete |
| cross-verify | schema:pass, domain:report-cross-consistent                      |
```
reason: structured, prefix-tagged, reviewer named, allowlist inherited from Subagents table
</example>

<example type="decomposition_rationale_fill">
input: REPORT-A report-building task
✅ output:
```
## Decomposition Rationale
- shape: tree
- model: D
- review_cycle: off
- outer_axes: [phase] — arrow source: data flow (setup → produce → verify-static → verify-ui)
- inner_axes: [section] — mode resolved per phase by file-conflict analysis
- fold_axes: [endpoint, field, url_state]
- ordering_source: universal data flow + project file-write-conflict analysis
- scope_ref strategy: omit for atomic phases (setup, verify-static); set for produce + verify-ui (>3 deliverables per task)
- delegation: none — all tasks within Tier 1 sizing
```
</example>

<example type="agent_kind_choice">
input: produce phase with 3 tasks (intro/body/summary report writing)
❌ output: phase.agent="report-writer" AND each task has agent="section-writer" (mutex violation)
✅ cohesive: phase.agent="report-writer", tasks=[{id:"intro"},{id:"body"},{id:"summary"}] (1 agent reads scope per task, processes all 3)
✅ distributed: tasks=[{id:"intro",agent:"intro-writer"},{id:"body",agent:"body-writer"},{id:"summary",agent:"summary-writer"}] (3 agents, parallel if no dependency)
choice depends on cohesiveness — the report often cohesive (shared context); per-section often distributed (independent files)
</example>

</examples>

---

<critical_recap>
1. fill every placeholder before save
2. 1 objective sentence per subagent — else split
3. every phase has explicit transition + agent kind (cohesive XOR distributed)
4. self-check ≥ 5 items, mix format + domain
5. handoff > 500 tokens → staging path
6. plan.json schema = `<plan_v1>` (phases/tasks); acceptance per phase uses `schema:*` / `coverage:*` / `domain:*` array
7. every phase has `schema:pass`; `domain:*` requires Reviewer agent; `coverage:*` requires deterministic script
8. `## Subagents` table IS the allowlist; plan `phase.agent`/`task.agent` ∈ Name column (no separate `allowed-agents` field)
9. fill `## Decomposition Rationale` — shape + axes (outer/inner/fold) + ordering source + scope_ref strategy
10. scope file at `<session-root>/staging/scope/<task-id>.md` when `scope_ref` set; agent emits `COVERAGE_DONE`/`COVERAGE_SKIPPED`
</critical_recap>
