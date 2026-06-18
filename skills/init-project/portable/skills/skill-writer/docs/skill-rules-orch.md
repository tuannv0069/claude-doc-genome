<critical>
target: skill-writer agent reference — orchestration rules
purpose: rules for skills that orchestrate multiple subagents (Model B/C/D)
scope: size limits, EX-01..EX-09 mandatory rules, safety controls, CONTRACT-V1, model+effort, agent file rules
</critical>

<rule_schema>
ex_rule: id | rule (≤ 1 line, control/exec plane separation)
control_table: control | spec
</rule_schema>

<dependencies>
- ${CLAUDE_SKILL_DIR}/docs/skill-rules-spec.md — platform spec
- ${CLAUDE_SKILL_DIR}/docs/skill-rules-quality.md — quality gate
- ${CLAUDE_SKILL_DIR}/docs/examples.md — §6 sequential, §7 parallel patterns
- `.claude/skills/skill-designer/docs/orchestrator-rules.md` — formal schemas (<plan_v1>, <plan_invariants>, <plan_acceptance>, <state_invariants>, <contract_v1>)
- `.claude/skills/skill-designer/docs/plan-gate-spec.md` — Plan Gate + DC consolidated spec
</dependencies>

---

## §1 size + split

| content | location |
|---|---|
| orchestrator flow | SKILL.md (≤ 800 lines) |
| agent prompts | `.claude/agents/*.md` |
| schemas, error tables | `${CLAUDE_SKILL_DIR}/docs/*.md` |

---

## §2 mandatory orchestrator rules

| id | rule |
|---|---|
| EX-01 | orchestrator = control-plane; reads STATUS, counts, progress; never domain content; never `input_ref` or `scope_ref` file content |
| EX-02 | subagent = execution-plane; all domain read/review/transform/generate |
| EX-03 | data > 500 tokens → staging file; pass path, not content |
| EX-04 | state file = SSOT; atomic rewrite per batch |
| EX-05 | flow decisions from CONTRACT-V1, not domain content |
| EX-06 | no subagent-to-subagent; route via orchestrator or shared artifact |
| EX-07 | planning gate mandatory (Model B/C/D); planner (named agent OR `orchestrator-direct` for uniform-task Model C — orchestrator emits plan.json deterministically from `$ARGUMENTS`, no semantic synthesis, no Reviewer needed) → plan.json (`<plan_v1>` schema) + scope files (atomic lockstep) → three-tier acceptance: `schema:*` orchestrator-parse, `coverage:*` orchestrator-script, `domain:*` Reviewer subagent → approve / replan(max 2) / fail |
| EX-08 | no `context: fork` if orchestrator needs subagent output |
| EX-09 | `scope_ref` field (when set) → DC file at `<session-root>/staging/scope/<task-id>.md`; agent reads to know coverage scope, emits `COVERAGE_DONE`/`COVERAGE_SKIPPED` in CONTRACT-V1; orchestrator only validates path (never reads content) |

---

## §3 safety controls

| control | spec |
|---|---|
| permission modes | `plan` (read-only), `default` (new), `acceptEdits` (file edits), `dontAsk` (post-gate only) |
| minimal privilege | research → Read/Glob/Grep; edit → add Edit/Write |
| batch size | default 3-4; scale only after validation |
| output trimming | subagent final = CONTRACT-V1 only |
| JOB_KEY | REPORT_ID (preferred) \| input-hash (8 hex) \| slug ≤ 24 chars |
| session root | `.agent/tmp/{prefix}/sessions/{JOB_KEY}/{SESSION}/` |
| state file | `<session-root>/state.json` (no timestamp suffix) |
| plan file | `<session-root>/plan.json` (schema = `<plan_v1>` in skill-designer/orchestrator-rules.md) |
| plan schema field renames | `stages`→`phases`, `items`→`tasks`, `TASK_KEY`→`JOB_KEY`, `total_items`→`total_tasks`, `stage_id`/`item_id`→`phase_id`/`task_id` |
| cohesive vs distributed | `phase.agent` set ⇒ cohesive (1 agent for all phase tasks); `task.agent` set ⇒ distributed (1 agent per task); MUTEX per phase |
| plan acceptance | per-phase array; **three layers**: `schema:*` orchestrator-parse, `coverage:*` orchestrator-script (grep/stat/jq), `domain:*` Reviewer subagent (mandatory `schema:pass`) |
| plan replan | overwrite plan.json + all scope files atomic lockstep with `revision++`; max 2 rounds → FAILURE |
| allowed agents | `## subagents` table in SKILL.md body IS the allowlist; `phase.agent` AND `task.agent` MUST appear in `name` column |
| plan inline-vs-ref | inline control primitive ≤ 500 token; domain payload → `input_ref` always |
| scope file | `<session-root>/staging/scope/<task-id>.md`; markdown nested checklist with dotted-path leaf IDs |
| scope conditional | required if phase has `domain:deliverables-complete` OR task produces > 3 deliverable types |
| delegated_to | sub-skill name; mutex with input/input_ref/scope_ref; references existing `.claude/skills/<name>/SKILL.md` |
| staging dir | `<session-root>/staging/` (inter-agent handoff) |
| scope dir | `<session-root>/staging/scope/` (DC files) |
| artifacts dir | `<session-root>/artifacts/` (user-facing: summary/gaps/mr-body); `artifacts/visual/` for binary |
| logs dir | `<session-root>/logs/` |
| latest pointer | `.agent/tmp/{prefix}/sessions/{JOB_KEY}/latest` symlink → SESSION |
| retention | archive 7d idle → `archive/{JOB_KEY}/{SESSION}/`; delete archived 30d (cleanup_ready only) |
| .gitignore | `.agent/` required |
| parallel write safety | each agent owns file; sequential aggregator |

---

## §4 CONTRACT-V1

```text
STATUS: SUCCESS | FAILURE | SKIPPED | REJECT
CHANGES: <number>
MODIFIED_ITEMS: <comma-separated or ->
ERROR: <short or ->
DETAIL: <max 5 lines, no full file echo>
COVERAGE_DONE: <comma-separated scope leaf IDs | omit if no scope_ref>
COVERAGE_SKIPPED: <id (reason); id (reason); ... | omit if no scope_ref>
REASON: <required when STATUS=SKIPPED>
REJECT_DETAIL: <required when STATUS=REJECT>
```

`COVERAGE_DONE` + `COVERAGE_SKIPPED` rules:
- present ONLY when task has `scope_ref` set (DC checklist exists)
- every scope leaf ID MUST appear in `COVERAGE_DONE` ∪ `COVERAGE_SKIPPED` (reviewer REJECT if missing)
- `COVERAGE_SKIPPED` entries MUST have specific reason (not bare "N/A")

include in every agent prompt: *"Final message contains ONLY the CONTRACT-V1 block. Discard all reasoning. When `scope_ref` is set, every leaf ID in the scope file must appear in COVERAGE_DONE or COVERAGE_SKIPPED with reason."*

---

## §5 model + effort per task

| task type | model | effort |
|---|---|---|
| routing, rename, format | haiku | low |
| parse + validate fixed schema | haiku | medium |
| read spec, generate structured output | sonnet | medium |
| write/transform domain | sonnet | high |
| code from clear spec | sonnet | high |
| execute UT (run, fix) | sonnet | high |
| test case / UT spec | sonnet | medium |
| quality review, multi-rule synthesis | sonnet | high |
| complex design, ambiguous spec | opus | high |

---

## §6 agent file rules

<rules section="ALWAYS">
- agent file has Do + Avoid sections
- Avoid lists specific known errors (not generic)
- writer agents read template before writing
- workflow ends with self-check before CONTRACT-V1
- when scope_ref is set in task input, agent prompt MUST include instruction to read scope_ref and emit COVERAGE_DONE/SKIPPED
- agent prompt MUST reference scope_ref by path (not enumerate deliverables inline) — DC file is SSOT
</rules>

---

## §6.1 subagents table (Model B/C/D only)

orchestration skills MUST include `## subagents` section in SKILL.md body — this table is the allowlist for `phase.agent` AND `task.agent` in plan.json.

format:
```markdown
## subagents

| name | role | model | effort | file |
|------|------|-------|--------|------|
| <agent-name> | <1-line role> | haiku\|sonnet\|opus | low\|medium\|high\|max | .claude/agents/<file>.md |

Allowlist: plan.json `phase.agent` AND `task.agent` MUST appear in `name` column above.
```

rules:
- derive from design.md `## Subagents` (full spec: # | Name | Objective | Model | Effort | Input | Output) by column mapping → SKILL.md `## subagents` (compact allowlist: name | role | model | effort | file)
- column mapping: `Name → name`, `Objective → role` (one-line summary), `Model → model`, `Effort → effort`, `file = .claude/agents/<name>.md`; `#`, `Input`, `Output` columns drop (already specified in the .claude/agents/<name>.md file produced by skill-writer §agent-file-template)
- every agent skill spawns (including helpers, reviewers) MUST appear → no hidden agents
- skill-writer Self-check: every `## subagents` row points to a real `.claude/agents/*.md` file
- audit script: `grep '^| ' SKILL.md` extracts allowlist mechanically

---

## §6.2 acceptance prefix usage

| prefix | when to use | example |
|--------|------------|---------|
| `schema:pass` | mandatory per phase | plan parses against `<plan_v1>` |
| `schema:<check>` | other schema invariants | `schema:phase-ids-unique` |
| `coverage:files-exist` | mechanical file presence check | output files at declared paths |
| `coverage:symbols-present` | grep-based symbol presence | callbacks/exports in agent output |
| `coverage:json-fields-set` | jq-based JSON field check | structured output validation |
| `domain:deliverables-complete` | DC coverage via Reviewer | reviewer reads scope_ref + output + COVERAGE_*; folds into content reviewer (no extra call) |
| `domain:<other>` | semantic quality gate needing judgment | layout-topology-match, cross-layer-consistent |

`coverage:*` runs deterministic scripts (cheap). `domain:*` spawns Reviewer (expensive, fold when possible).

---

<critical_recap>
1. EX-01: orchestrator = control-plane only; never reads domain content; never `scope_ref` content
2. EX-03: data > 500 tokens → staging file (pass by reference)
3. CONTRACT-V1 = sole subagent return format; discard all reasoning; `COVERAGE_DONE`/`COVERAGE_SKIPPED` when scope_ref set
4. batch size default 3-4; scale only after validation
5. EX-07: planning gate mandatory; plan.json (`<plan_v1>`, phases/tasks naming) + scope files atomic; three-tier acceptance (schema/coverage/domain)
6. layout: `.agent/tmp/{prefix}/sessions/{JOB_KEY}/{SESSION}/{state.json,plan.json,staging/{scope/}/,artifacts/,logs/}`
7. resume via `sessions/{JOB_KEY}/latest` symlink; retention 7d archive / 30d delete
8. plan: inline only control primitives (≤ 500 token); domain payload → `input_ref` always; DC checklist → `scope_ref` (conditional)
9. plan `phase.agent`/`task.agent` ∈ `## subagents` table Name column (allowlist); cohesive XOR distributed per phase
10. EX-09: scope_ref → `staging/scope/<task-id>.md` markdown nested checklist; agent reads as SSOT; reviewer verifies coverage
11. replan via `revision++` + overwrite plan.json + scope files atomic lockstep; max 2 rounds → FAILURE
</critical_recap>
