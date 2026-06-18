<critical>
scope: design-phase rules for Claude Code multi-agent orchestration (Skill + subagents).
out-of-scope: single prompts, SDK code, interactive sessions.
core: orchestrator=control | subagent=execution | contract-only routing | state=SSOT
</critical>

<rule_schema>
boundary: who reads what — control vs domain
contract: CONTRACT-V1 fields only between agents
state: atomic rewrite per batch, prefix-isolated
</rule_schema>

<priority>
1. boundary (EX-01..EX-09) — NEVER violate
2. contract format — every subagent
3. state lifecycle — every Model B/C/D
4. safety controls (perm/scope/PII)
5. budgets (batch/model/effort)
</priority>

<substrate_selection>
applies BEFORE Model B/C/D design. Claude Code ships dynamic workflows (code.claude.com/docs/en/workflows): a JS script the runtime executes in background, orchestrating dozens-hundreds of subagents. Everything below `<substrate_selection>` in this file targets the skill-orchestration substrate only.

| signal | substrate |
|--------|-----------|
| scale (dozens-hundreds agents) \| repeatable scripted run \| adversarial cross-check of findings \| no mid-run user input | dynamic workflow |
| mid-run user approval gate \| resume across sessions \| CLI < 2.1.154 / workflows disabled / free plan | skill orchestration (this file) |

dynamic workflow replaces (do NOT design these for workflow substrate):

| Model B/C/D mechanism | workflow equivalent |
|---|---|
| planner agent + plan.json | `meta.phases` + script control flow |
| state.json + `latest` symlink resume | runtime journal; cached per-agent resume (same session only) |
| staging files (EX-03) | script variables — results never enter Claude context |
| CONTRACT-V1 text parse | `schema` structured output (validated) |
| batch_size 3-4 | runtime concurrency cap (≤16 concurrent, 1000 agents/run) |
| `## subagents` allowlist | script `agent()` calls; `agentType` may reference `.claude/agents/*.md` |
| QA reviewer + REJECT cycle | verification phase: refute-prompted agents + vote count (`schema` verdicts) |

caveats: workflow subagents run `acceptEdits` + inherit session tool allowlist regardless of permission mode (§3-style per-agent permission design does not apply); no mid-run user input; save under `.claude/workflows/` (project) or `~/.claude/workflows/` (personal) → `/name`, project wins clash; `args` arrives as structured data. Script shape + checklist: `skill-writer/docs/skill-rules-workflow.md`.
</substrate_selection>

---

<rules section="NEVER">
- orchestrator reads domain content
- subagent-to-subagent direct handoff
- `context: fork` when result feeds routing
- inline handoff > 500 tokens (use staging path)
- parallel agents share write target
- state file append (rewrite atomic)
- cherry-pick items on resume (re-run whole batch)
- delete state file / log / final report on cleanup
- `allowed_prefixes` at parent dir (loses isolation)
- separate `allowed-agents` section/field (duplicates `## subagents` table → drift); the table IS the allowlist
- `bypassPermissions` in CI/CD
- `inherit` model on accuracy-critical task
- agent file missing Avoid section
- log domain content (PII risk, bloat)
- flat layout `.agent/tmp/{prefix}/state-${SESSION}.json` (loses task isolation; collides cross-function)
- timestamp embedded in filename inside session dir (redundant — session dir already timestamped)
- skip `JOB_KEY` segment (concurrent runs for different functions become indistinguishable)
- skip `<plan_v1>` schema on Model B/C/D (planner output must conform)
- plan.json embed domain content (specs, scanned text) — use input_ref
- mix `schema:*` and `domain:*` checks in same acceptance string
- versioned plan files (`plan-v1.json`, `plan-v2.json`) — use `revision` field, overwrite
- spawn `phase.agent` or `task.agent` not in `## subagents` table Name column
- orchestrator parse plan.json with domain heuristic (control-plane only — schema:* checks)
- orchestrator read `scope_ref` file content (path-only — EX-01 extension)
- mix `input_ref` (domain payload) and `scope_ref` (DC) purposes — semantically distinct fields
- set BOTH `phase.agent` AND `task.agent` (mutex — cohesive XOR distributed per phase)
- emit CONTRACT-V1 missing `COVERAGE_DONE`/`COVERAGE_SKIPPED` when task has `scope_ref` set
- `delegated_to` combined with `input` / `input_ref` / `scope_ref` (mutex — task is sub-skill OR inline, not both)
</rules>

<rules section="ALWAYS">
- declare model + effort per subagent
- subagent final msg = CONTRACT-V1 block only
- staging/state under `.agent/tmp/{prefix}/sessions/{JOB_KEY}/{SESSION}/`
- `JOB_KEY` derived from input (REPORT_ID | input-hash | slug) — declared in design.md
- update `sessions/{JOB_KEY}/latest` symlink atomic after state.json init
- `cleanup_ready=true` only after phase=completed
- `active_batch` set pre-batch, cleared post-batch
- writer agent reads template before write
- agent ends with self-check before returning
- PII mask before subagent input/staging
- progress notify 2x per batch (pre+post)
- retention: archive session dir at 7d, delete archived at 30d (only when `cleanup_ready=true`)
- plan.json validated against `<plan_v1>` + `<plan_invariants>` before phase 1 spawn
- every phase acceptance includes `schema:pass` (mandatory); `coverage:*` + `domain:*` opt-in
- `phase.agent` / `task.agent` ∈ `name` column of `## subagents` table in SKILL.md (table IS the allowlist; no separate `allowed-agents` field)
- `phase.agent` XOR `task.agent` per phase (cohesive XOR distributed)
- planner output > 500 token → write `<session-root>/staging/plan-input.json`, plan.json refs path
- planner writes plan.json + all scope files atomic in same step (lockstep tmp+mv)
- scope file at `<session-root>/staging/scope/<task-id>.md` when task has `scope_ref`
- agent emits `COVERAGE_DONE` + `COVERAGE_SKIPPED` in CONTRACT-V1 when task has `scope_ref` set
- replan on REJECT → `revision++`, overwrite plan.json + scope files atomic (tmp+mv lockstep)
- state.json `completed/failed/skipped` tasks reference plan.json `(phase_id, task_id)` tuple
</rules>

---

<conditional name="boundary">
| question | who |
|----------|-----|
| who runs next / retry / stop | orchestrator |
| what is content / is it correct | subagent |
| read state file, plan summary | orchestrator (control data) |
| read domain file | subagent only |
</conditional>

<conditional name="model_effort">
| task | model | effort |
|------|-------|--------|
| route/rename/format | haiku | low |
| parse + validate schema | haiku | medium |
| read spec → structured output | sonnet | medium |
| write/transform domain | sonnet | high |
| write code from clear spec | sonnet | high |
| write test cases | sonnet | medium |
| quality review, multi-rule | sonnet | high |
| ambiguous spec, complex design | opus | high |

model field also accepts `fable` + full model IDs; agent default = `inherit` (see NEVER: no `inherit` on accuracy-critical task)
</conditional>

<conditional name="batch_size">
| input | size |
|-------|------|
| default | 3-4 |
| large files/long output | 2 |
| small files, validated | 5-6 |
| compaction observed | reduce first, not resources |
</conditional>

<conditional name="permission_mode">
| mode | when |
|------|------|
| plan | read-only analysis |
| default | new workflow, side effects |
| acceptEdits | edits, no risky bash |
| dontAsk | only after Production Gate |
</conditional>

<conditional name="provider_error">
| error | strategy |
|-------|----------|
| 429/overloaded | backoff 30→60→120s, max 3 |
| 5xx | retry once after 30s, else FAILURE |
| model_not_available | fallback lower model, else halt |
| context_length_exceeded | reduce batch, split, retry |
| timeout no-response | mark NO_RESPONSE = failed |
| >50% batch errors | halt + notify |
</conditional>

<conditional name="final_status">
| items | status | phase |
|-------|--------|-------|
| all SUCCESS/SKIPPED | SUCCESS | completed |
| mix SUCCESS + FAILURE | PARTIAL_SUCCESS | completed |
| all FAILURE | FAILURE | failed |
</conditional>

<conditional name="skipped_reason">
| reason | when |
|--------|------|
| AlreadyProcessed | prior run completed |
| DependencyFailed | upstream item failed |
| UserExcluded | user-excluded scope |
| ValidationFailed | invalid input |
</conditional>

<conditional name="staging_format">
| format | use |
|--------|-----|
| .json | atomic handoff, state snapshot |
| .jsonl | append accumulation, audit |
| .md | text artifacts (specs, reports) |
</conditional>

---

<defaults>
- model: sonnet
- effort: medium
- batch_size: 3-4
- max_retries: 1 per item
- max_review_rounds: 2 → then FAILURE
- skill prefix: lowercase, 4-8 chars, unique
- JOB_KEY: REPORT_ID (preferred) | input-hash (8 hex) | kebab slug (≤ 24 chars)
- SESSION: `${CLAUDE_SESSION_ID}` or `YYYYMMDD-HHMMSS-<6-hex>`
- session root: `.agent/tmp/{prefix}/sessions/{JOB_KEY}/{SESSION}/`
- state path: `<session-root>/state.json`
- plan path: `<session-root>/plan.json`
- staging dir: `<session-root>/staging/` (inter-agent handoff, `.json`/`.jsonl`)
- scope dir: `<session-root>/staging/scope/` (DC files per task, `.md` markdown checklist)
- artifacts dir: `<session-root>/artifacts/` (user-facing: summary.md, gaps.json, mr-body.md)
- visual/binary dir: `<session-root>/artifacts/visual/` (.png/.yml/.pdf)
- logs dir: `<session-root>/logs/`
- latest pointer: `.agent/tmp/{prefix}/sessions/{JOB_KEY}/latest` (symlink → SESSION)
- locks dir: `.agent/tmp/{prefix}/locks/` (cross-session)
- archive dir: `.agent/tmp/{prefix}/archive/{JOB_KEY}/{SESSION}/`
- retention: archive at 7d idle, delete archived at 30d (only when `cleanup_ready=true`)
- SKILL.md target: ≤ 800 lines
- DETAIL field: ≤ 5 lines, no file echo
- plan schema: `<plan_v1>` (this file)
- plan acceptance default: `["schema:pass"]` per phase
- plan inline threshold: 500 token per `input` object (else input_ref)
- plan replan rounds: max 2 → then FAILURE
- plan user-approval: default false (automatic on schema:pass)
- scope file format: markdown nested checklist, dotted-path leaf IDs
- scope file conditional: required if phase has `domain:deliverables-complete` OR task produces > 3 deliverable types
</defaults>

---

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
- missing STATUS → NO_RESPONSE (fail)
- parse only this block, ignore surrounding text
- `COVERAGE_DONE` + `COVERAGE_SKIPPED` are OPTIONAL fields:
  - present when task has `scope_ref` set
  - omitted when task has no `scope_ref` (no DC to cover)
- when present: every scope leaf ID MUST appear in DONE ∪ SKIPPED (else reviewer REJECT)
- SKIPPED entries MUST have specific reason (not bare "N/A")
</contract_v1>

<plan_v1>
```json
{
  "plan_version": "v1",
  "skill_prefix": "<lowercase, 4-8 chars>",
  "model": "B | C | D",
  "job_key": "<must equal SESSION_ROOT JOB_KEY segment>",
  "revision": 1,
  "created_at": "<ISO8601>",
  "requires_user_approval": false,
  "total_tasks": 0,
  "phases": [
    {
      "id": "<unique-within-plan>",
      "name": "<human label>",
      "agent": "<phase-level agent | omit for distributed>",
      "mode": "sequential | parallel",
      "depends_on": ["<phase.id>"],
      "batch_size": 1,
      "tasks": [
        { "id": "<unique-across-plan>", "input": { "key": "primitive" } },
        { "id": "<unique-across-plan>", "input_ref": "<session-root>/staging/<name>.json" },
        { "id": "<unique-across-plan>", "input": {...}, "scope_ref": "<session-root>/staging/scope/<task-id>.md" },
        { "id": "<unique-across-plan>", "agent": "<task-level agent>", "input": {...} },
        { "id": "<unique-across-plan>", "delegated_to": "<sub-skill-name>" }
      ],
      "acceptance": ["schema:pass", "coverage:<check>", "domain:<check_id>"]
    }
  ]
}
```

shape unification:
- Model B → typically 1 phase = 1 task (sequential chain across phases)
- Model C → 1 phase with N tasks (parallel)
- Model D → multi-phase, each with 1..N tasks

cohesive vs distributed phase:
- **cohesive**: `phase.agent` set, `task.agent` omitted → 1 agent processes all tasks in phase
- **distributed**: `phase.agent` omitted, each `task.agent` set → 1 agent per task, parallel possible
- mutex: `phase.agent` AND `task.agent` cannot both be set on same task

task input fields (4 forms, mutex semantics):
| Field | Purpose | When |
|-------|---------|------|
| `input` | Inline control primitives (id, REPORT_ID, path, enum, flag) | Always allowed, ≤ 500 token |
| `input_ref` | Domain payload path (staging file) | When agent needs read data > 500 token, or domain content |
| `scope_ref` | Deliverable Checklist path (`staging/scope/<id>.md`) | When phase has `domain:deliverables-complete` OR task produces > 3 distinct deliverable types |
| `delegated_to` | Sub-skill name (Tier 2 delegation) | When task exceeds Tier 1 sizing — spawns sub-skill with own session |

`delegated_to` mutex with input/input_ref/scope_ref.

inline-vs-ref decision:
- inline `input` IF control-plane primitive AND size ≤ 500 token
- `input_ref` otherwise — ALWAYS for domain payload, regardless of size
- hard cap: any `input` object > 500 token → `input_ref` required

orchestrator parse rules:
- read only schema fields (id, agent, mode, depends_on, acceptance, tasks[].id, tasks[].input_ref, tasks[].scope_ref, tasks[].delegated_to)
- never parse `input` payload as content (EX-01 — control plane only)
- never read `input_ref` or `scope_ref` file content (paths only)
- domain quality judgment → spawn Reviewer subagent, not orchestrator self-read
</plan_v1>

<state_invariants>
- `len(completed) + len(failed) + len(skipped)` ≤ `total_tasks`
- `total_tasks` === plan.json `total_tasks`
- `completed/failed/skipped[].ref` = `(phase_id, task_id)` from plan.json
- timestamps ISO8601, monotonically increasing
- `active_batch != null` ⇒ batch NOT in execution_log
- `max_retries` ≤ 3
- `cleanup_ready=true` only when phase=completed
- write via tmp+mv (atomic)
</state_invariants>

<plan_invariants>
- `plan_version`, `skill_prefix`, `model`, `job_key`, `created_at` present
- `job_key` === SESSION_ROOT JOB_KEY segment
- `total_tasks` === sum(phases[].tasks.length)
- `phases[].id` unique within plan
- `phases[].tasks[].id` unique across entire plan (cross-phase)
- `depends_on` references existing `phase.id`; no cycle
- `phase.agent` (when set) ∈ `name` column of `## subagents` table in SKILL.md
- `task.agent` (when set) ∈ `name` column of `## subagents` table in SKILL.md
- `phase.agent` AND `task.agent` MUTEX (cohesive XOR distributed per phase)
- `mode='parallel'` ⇒ `phase.tasks.length` > 1
- `batch_size` ≤ `phase.tasks.length`
- every phase `acceptance` non-empty AND includes `schema:pass`
- inline `input` ≤ 500 token; larger → `input_ref` required
- domain payload (specs, scanned data, generated text) → `input_ref` always, regardless of size
- `scope_ref` required if phase acceptance has `domain:deliverables-complete` OR task produces > 3 distinct deliverable types; else optional
- `scope_ref` path under `<session-root>/staging/scope/`; `.md` extension
- `scope_ref` file MUST exist before phase dispatch (orchestrator schema:pass check)
- `scope_ref` file content MUST match checklist regex `^(\s*- \[ \] [\w.-]+( — .+)?\n?)+$` (markdown nested checklist with dotted IDs)
- `delegated_to` mutex with `input` / `input_ref` / `scope_ref`
- `delegated_to` references existing skill at `.claude/skills/<name>/SKILL.md`
- `revision` monotonically increasing on replan; plan.json + scope files overwritten atomic (tmp+mv lockstep)
- no `plan-v{N}.json` files (use `revision` field, single path)
</plan_invariants>

<plan_acceptance>
three layers, declared per phase in `acceptance: [...]`:

| prefix | who verifies | cost | how |
|--------|--------------|------|-----|
| `schema:*` | orchestrator (control-plane) | free | parse plan.json, run schema/invariant checks |
| `coverage:*` | orchestrator (deterministic script) | cheap | run grep / stat / jq / AST check; mechanical pass/fail |
| `domain:*` | Reviewer subagent (execution-plane) | expensive | orchestrator spawns Reviewer with (plan_path, check_id) → CONTRACT-V1 |

mandatory: every phase MUST include `schema:pass`.
opt-in: `coverage:<check>` for mechanical verification (file-exists, symbol-present, json-field-set).
opt-in: `domain:<check_id>` for semantic quality gate requiring judgment.

common `coverage:*` checks:
- `coverage:files-exist` → orchestrator runs `stat` on declared output paths
- `coverage:symbols-present` → orchestrator runs `grep -E <pattern>` on agent output
- `coverage:json-fields-set` → orchestrator runs `jq` to verify required fields
- `coverage:task-count-matches-axis` → orchestrator counts plan.tasks vs declared axis cardinality

`domain:deliverables-complete` protocol (folded into content reviewer, no extra reviewer call):
1. Reviewer reads `scope_ref` (DC) + agent output + `COVERAGE_DONE` + `COVERAGE_SKIPPED` from CONTRACT-V1
2. compute `missing = scope_leaves \ (COVERAGE_DONE ∪ COVERAGE_SKIPPED)` → REJECT if non-empty
3. validate semantic content of COVERAGE_DONE items (existing content review)
4. validate COVERAGE_SKIPPED reasons plausible (e.g., "N/A for read-only endpoint" → OK; bare "N/A" → REJECT)

reject path:
- `schema:*` fail → halt with `REJECT_DETAIL: <fail reason>`, no replan
- `coverage:*` fail → halt with `REJECT_DETAIL: <script output>`, no replan (deterministic; re-run same → same fail)
- `domain:*` fail → replan: spawn planner with reject context, `revision++`, overwrite plan.json + scope files atomic
- max replan rounds = 2 → then FAILURE with `MAX_REVIEW_ROUNDS_EXCEEDED`

never:
- mix `schema:*`, `coverage:*`, `domain:*` in single check string (use array entries)
- orchestrator self-evaluates `domain:*` (must delegate to Reviewer)
- orchestrator read `scope_ref` content (EX-01 extension; only path validation OK)
</plan_acceptance>

<resume_logic>
- `active_batch != null` + recent ts → re-run entire batch
- `active_batch != null` + ts > 1h → stale, resume from next unprocessed
- failed item, retry_count < max → retry
- failed item, retry_count ≥ max → UNRECOVERABLE skip
- corrupt state JSON → abort, manual fix
</resume_logic>

---

<examples>

<example type="boundary">
input: orchestrator step "evaluate plan correctness"
❌ output: orchestrator reads plan.json, judges quality
✅ output: spawn Reviewer subagent → contract STATUS → route
</example>

<example type="handoff">
input: phase 1 produces 2000-token analysis for phase 2
❌ output: pass analysis inline in subagent prompt
✅ output: phase 1 writes `<session-root>/staging/phase1-analysis.json` → pass path to phase 2
</example>

<example type="parallel_write">
input: 4 parallel agents produce report sections
❌ output: each writes to `report.md`
✅ output: each writes own `staging/section-N.json` → sequential aggregator merges into `artifacts/report.md`
</example>

<example type="cohesive_vs_distributed">
input: report writing phase has 3 tasks (intro/body/summary)
❌ output: `{"phase.agent":"report-writer","tasks":[{"id":"intro","agent":"intro-writer"},...]}` (both phase.agent + task.agent set — mutex violation)
✅ cohesive: `{"phase.agent":"report-writer","tasks":[{"id":"intro"},{"id":"body"},{"id":"summary"}]}` (1 agent processes all tasks)
✅ distributed: `{"tasks":[{"id":"intro","agent":"intro-writer"},{"id":"body","agent":"body-writer"},...]}` (1 agent per task)
</example>

<example type="scope_ref_dc_format">
input: task `write-intro` produces a report section with 5 parts
✅ scope file at `staging/scope/write-intro.md`:
```markdown
- [ ] out-param
  - [ ] field-list — list of response fields with name + type
  - [ ] nullability — mark nullable per field
- [ ] in-param
  - [ ] query-params
  - [ ] body-schema
- [ ] business-logic
- [ ] error-handling
```
agent CONTRACT-V1:
```
COVERAGE_DONE: out-param.field-list, out-param.nullability, in-param.body-schema, business-logic
COVERAGE_SKIPPED: in-param.query-params (this endpoint has no query params); error-handling (read-only, no error path)
```
reviewer accepts SKIPPED with specific reason; REJECT only if any leaf absent from both sets.
</example>

<example type="acceptance_three_tier">
input: phase needs schema + mechanical + semantic checks
✅ output:
```json
"acceptance": [
  "schema:pass",
  "coverage:files-exist",
  "coverage:symbols-present",
  "domain:deliverables-complete"
]
```
orchestrator runs schema:pass + coverage:* mechanically; spawns Reviewer for domain:*
</example>

<example type="task_isolation">
input: skill `my-skill` runs concurrently for REPORT-A and REPORT-B
❌ output: `.agent/tmp/my-skill/state-${SESSION}.json` (flat; both runs collide visually, hard to debug)
✅ output: `.agent/tmp/my-skill/sessions/REPORT-A/{SESSION}/state.json` + `.agent/tmp/my-skill/sessions/REPORT-B/{SESSION}/state.json`
</example>

<example type="latest_pointer">
input: resume command needs to find current run for REPORT_ID=REPORT-A
❌ output: scan `sessions/REPORT-A/` for newest mtime each time
✅ output: read `sessions/REPORT-A/latest` symlink → resolves to active SESSION dir
</example>

<example type="contract_output">
input: subagent finishes domain task
❌ output: "I analyzed X, found Y, then did Z. STATUS: SUCCESS ..."
✅ output: CONTRACT-V1 block only, no reasoning
</example>

<example type="prefix_isolation">
input: skill `report-writer` cleanup hook
❌ output: `allowed_prefixes: ['.agent/tmp/']`
✅ output: `allowed_prefixes: ['.agent/tmp/rptw/']`
</example>

<example type="plan_inline_vs_ref">
input: planner builds plan task for my-skill RED phase of REPORT_ID=REPORT-A
❌ output: `{"id":"red-1","input":{"report_id":"REPORT-A","spec_input":"<full markdown 3000 lines>"}}`
✅ output: `{"id":"red-1","input":{"report_id":"REPORT-A"},"input_ref":"staging/red-input-report-a.json"}`
reason: report_id is control primitive (inline OK); spec content is domain payload (input_ref always)
</example>

<example type="plan_acceptance_split">
input: report-writer plan phase 1 needs schema + report-quality check
❌ output: `acceptance: ["schema and report quality good"]`
❌ output: `acceptance: ["schema:pass, domain:report-complete"]` (mixed in one string)
✅ output: `acceptance: ["schema:pass", "domain:report-complete"]`
reason: array entries; orchestrator self-verifies `schema:*`, spawns Reviewer for `domain:*`
</example>

<example type="session_layout">
input: design layout for one run of skill `my-skill` on REPORT_ID=REPORT-A
✅ output:
```
.agent/tmp/my-skill/
├── sessions/REPORT-A/
│   ├── latest → 20260515-143012-7a3f9c
│   └── 20260515-143012-7a3f9c/
│       ├── state.json
│       ├── plan.json
│       ├── staging/
│       │   ├── red-output.json
│       │   ├── prepare-output.json
│       │   ├── green-output.json
│       │   └── scope/
│       │       ├── write-red.md
│       │       ├── write-prepare.md
│       │       └── write-green.md
│       ├── artifacts/
│       │   └── summary.md
│       └── logs/orchestrator.log
├── locks/
└── archive/
```
</example>

</examples>

---

<anti_patterns>
- cherry-pick items on resume — re-run whole batch
- `context: fork` when orchestrator needs result back
- inline prompts/schemas/hooks in SKILL.md → extract
- subagent returns reasoning + contract → contract only
- agent file Do without Avoid → behavior drift
- staging without prefix → cross-skill collision
- per-skill Stop hook → use shared dispatcher
- log domain content → log contract fields only
- delete staging in Stop without `cleanup_ready` check
</anti_patterns>

---

<edge_cases>
QA reject cycle: max 2 rounds. Round 3 → mark FAILURE with `MAX_REVIEW_ROUNDS_EXCEEDED`. Orchestrator reads only STATUS + REJECT_DETAIL, never the artifact.

Conditional branching: route on STATUS + control data only. Domain-dependent branch → spawn Evaluator subagent that returns control signal. Declare every branch in plan; untaken branches → SKIPPED in state file.

Tool feasibility: before design, test each external tool (API/MCP/bash) with worst-case input (largest item, max parallel). Fails worst-case → split workflow, fallback path, or rescope. Document timeout/rate-limit/max-output in SKILL.md `## Tool Constraints`.
</edge_cases>

---

<pre_design_checklist>
- [ ] classify Model A/B/C/D
- [ ] orchestrator vs subagent boundary defined
- [ ] B/C/D: planner agent (or "orchestrator-direct" for uniform Model C) + plan.json
- [ ] plan.json conforms to `<plan_v1>` schema (phases / tasks naming)
- [ ] every phase chooses cohesive (`phase.agent`) XOR distributed (`task.agent`) — not both
- [ ] every phase.acceptance includes `schema:pass`; `coverage:*` for mechanical; `domain:*` declares Reviewer agent
- [ ] inline-vs-input_ref rule applied per task (kind + 500 token cap)
- [ ] `scope_ref` set when phase has `domain:deliverables-complete` OR task produces > 3 deliverable types
- [ ] scope files written at `<session-root>/staging/scope/<task-id>.md` in markdown checklist format
- [ ] agent emits `COVERAGE_DONE` + `COVERAGE_SKIPPED` in CONTRACT-V1 when `scope_ref` set
- [ ] SKILL.md has `## subagents` table; every plan `phase.agent` / `task.agent` ∈ table `name` column
- [ ] each subagent: 1 objective, model+effort declared, output contract
- [ ] inter-agent > 500 tokens → staging file designed
- [ ] side effects → idempotency + state file
- [ ] QA needed → REJECT cycle defined
- [ ] PII → masking + sanitization
- [ ] cleanup_ready + Stop dispatcher
- [ ] external tools tested worst-case
- [ ] every agent has Do + Avoid + ≥5 self-check items
</pre_design_checklist>

<production_gate>
Two-layer gate. Both required for production.

**Layer 1 — runtime maturity** (this file):
- L1 (subagent isolation): contract match, valid→SUCCESS, invalid→FAILURE
- L2 (smoke 1-2 items): parse, progress, final summary correct
- L3 (full run): all batches, failures accumulate, token within budget
- gate to `dontAsk`: L3 pass ≥3 on ≥2 input sets, fail rate ≤2%, allowlist 100%, audit log, rollback verified, human sign-off

**Layer 2 — artifact quality** (skill-writer/docs/skill-rules-quality.md §4 release gate):
- writer called audit explicitly | audit ran syntax + runtime | skill has self-test | token budget estimated | no orphans | matches project conventions

orchestrator-rules `<production_gate>` = runtime behavior; quality-rules §4 = file-level artifact compliance. Both must PASS.
</production_gate>

---

<critical_recap>
1. orchestrator NEVER reads domain content — delegate to subagent
2. handoff > 500 tokens → staging file path, never inline
3. subagent final message = CONTRACT-V1 block only
4. state file atomic rewrite per batch, prefix-isolated AND job-isolated
5. parallel agents write own file → sequential aggregator merges
6. resume: re-run entire batch, never cherry-pick; resume path via `sessions/{JOB_KEY}/latest`
7. cleanup_ready true only after phase=completed; retention 7d archive / 30d delete
8. layout: `.agent/tmp/{prefix}/sessions/{JOB_KEY}/{SESSION}/{state.json,plan.json,staging/{scope/}/,artifacts/,logs/}`
9. plan.json conforms to `<plan_v1>` (phases/tasks naming); planner output respects inline (control primitive ≤ 500 tok) vs `input_ref` (domain payload always)
10. acceptance THREE-tier: `schema:*` orchestrator-parse, `coverage:*` orchestrator-script, `domain:*` Reviewer subagent; `schema:pass` mandatory per phase
11. cohesive phase = `phase.agent` set; distributed phase = `task.agent` per task; MUTEX per phase
12. `scope_ref` (conditional) → DC checklist at `staging/scope/<task-id>.md`; agent emits `COVERAGE_DONE`/`COVERAGE_SKIPPED` in CONTRACT-V1
13. replan via `revision++` + overwrite plan.json + scope files atomic lockstep; max 2 rounds → FAILURE
14. `phase.agent` / `task.agent` ∈ `name` column of SKILL.md `## subagents` table (table IS the allowlist; no separate field)
</critical_recap>
