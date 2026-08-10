# Plan Gate + plan.json + WBS — Final Spec

> Canonical spec for orchestration skills (Model B/C/D). Consolidates decisions from design discussion. Source of truth — formal schemas in `orchestrator-rules.md` reference this doc.

## §1. Concept

**Plan Gate**: mandatory phase 0 before any execution. Planner agent produces 2 artifacts atomically.

**3-file split**:

| File | Reader | Purpose |
|------|--------|---------|
| `<session-root>/plan.json` | orchestrator | Routing — who does what, in what order, when done |
| `<session-root>/staging/scope/<task-id>.md` | task agent + reviewer | Deliverable Checklist (DC) — what must be covered |
| `.claude/agents/<name>.md` | task agent | Methodology — how to do the work |

EX-01: orchestrator reads plan.json only. Never scope file content, never agent prompt.

## §2. plan.json schema (lean)

```json
{
  "plan_version": "v1",
  "skill_prefix": "<lowercase, 4-8 chars>",
  "model": "B | C | D",
  "job_key": "<REPORT_ID | input-hash | slug>",
  "revision": 1,
  "created_at": "<ISO8601>",
  "requires_user_approval": false,
  "total_tasks": <int>,
  "phases": [
    {
      "id": "<unique>",
      "name": "<human label>",
      "agent": "<phase-level agent | omit for distributed>",
      "mode": "sequential | parallel",
      "depends_on": ["<phase.id>"],
      "batch_size": <int>,
      "tasks": [
        {
          "id": "<unique across plan>",
          "agent": "<task-level agent | omit for cohesive>",
          "input": { "<primitive>": "<value>" },
          "input_ref": "<staging/...path...>",
          "scope_ref": "<staging/scope/<id>.md>",
          "delegated_to": "<sub-skill-name>"
        }
      ],
      "acceptance": ["<prefix>:<check>"]
    }
  ]
}
```

### Naming (full rename)

| Old | New |
|-----|-----|
| `stages[]` | `phases[]` |
| `items[]` | `tasks[]` |
| `TASK_KEY` | `JOB_KEY` |
| `total_items` | `total_tasks` |
| `stage_id` / `item_id` | `phase_id` / `task_id` |

### Cohesive vs distributed phase

- **Cohesive**: `phase.agent` set, `task.agent` omitted (1 agent processes all tasks in phase)
- **Distributed**: `phase.agent` omitted, each `task.agent` set (1 agent per task, parallel possible)
- Mutex: phase.agent AND task.agent cannot both be set

### Task input fields (mutex semantics)

| Field | Purpose | When |
|-------|---------|------|
| `input` | Inline control primitives | Always allowed, ≤ 500 token |
| `input_ref` | Domain payload path | When agent needs read data > 500 token |
| `scope_ref` | Deliverable Checklist path | When phase has `domain:deliverables-complete` OR task produces > 3 distinct deliverable types |
| `delegated_to` | Sub-skill name (Tier 2) | When task exceeds Tier 1 sizing → spawn sub-skill |

`delegated_to` mutex with input/input_ref/scope_ref.

## §3. Scope file (Deliverable Checklist) format

**Path**: `<session-root>/staging/scope/<task-id>.md`
**Format**: markdown nested checklist, leaf-only IDs

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

**Decomposition method**: hierarchical top-down. Stop when leaf is doable in 1 agent pass.

**3 rules** (verifiable):
1. **100%**: parent scope = sum of children
2. **Exclusive**: children don't overlap
3. **Doable**: leaf fits agent budget (≤ Tier 1)

Designer's judgment for how to break (by section / component / element / stage / etc.). No enforced method.

## §4. CONTRACT-V1 extension (when scope_ref present)

```
STATUS: SUCCESS | FAILURE | SKIPPED | REJECT
CHANGES: <number>
MODIFIED_ITEMS: <list or ->
ERROR: <short or ->
DETAIL: <≤5 lines>
COVERAGE_DONE: <comma-separated leaf IDs>
COVERAGE_SKIPPED: <id (reason); id (reason); ...>
REASON: <if SKIPPED>
REJECT_DETAIL: <if REJECT>
```

**Self-check rule**: every scope leaf ID MUST appear in `COVERAGE_DONE` or `COVERAGE_SKIPPED`. Skipped items MUST have specific reason.

## §5. Acceptance prefixes (3-tier)

| Prefix | Verifier | Cost | Example |
|--------|----------|------|---------|
| `schema:*` | orchestrator (parse plan.json) | free | `schema:pass`, `schema:phase-ids-unique` |
| `coverage:*` | orchestrator (deterministic script) | cheap | `coverage:files-exist`, `coverage:symbols-present`, `coverage:json-fields-set`, `coverage:task-count-matches-axis` |
| `domain:*` | reviewer subagent | expensive | `domain:deliverables-complete`, `domain:layout-topology-match` |

`schema:pass` mandatory every phase. Other prefixes opt-in.

`domain:deliverables-complete` protocol (folded into content reviewer, no extra call):
1. Read scope_ref + agent output + COVERAGE_DONE + COVERAGE_SKIPPED
2. missing = scope_leaves \ (DONE ∪ SKIPPED) → REJECT if non-empty
3. Validate semantic content of DONE items
4. Validate SKIPPED reasons plausible

## §6. Lifecycle

| Event | Action |
|-------|--------|
| Plan synthesis | Planner writes plan.json + all scope files atomic (tmp+mv lockstep) |
| Schema validation | Orchestrator validates plan.json against `<plan_v1>` + verifies scope file paths exist + format regex |
| Phase dispatch | Orchestrator spawns agent per task; passes input/input_ref/scope_ref paths |
| Task execution | Agent reads scope_ref → completes leaves → emits CONTRACT-V1 with COVERAGE_DONE/SKIPPED |
| Acceptance | Orchestrator runs schema:* + coverage:* mechanically; spawns reviewer for domain:* |
| REJECT (round ≤ 2) | Orchestrator replans: `revision++`, overwrite plan.json + scope files atomic |
| REJECT (round > 2) | Final STATUS=FAILURE with MAX_REVIEW_ROUNDS_EXCEEDED |
| Completion | Set `cleanup_ready=true` |
| Cleanup | Bundled retention: archive 7d, delete archived 30d |

## §7. Subagents table (allowlist)

Heading-case convention: design.md uses `## Subagents` (capital), generated SKILL.md uses `## subagents` (lowercase). Same data, different document. Allowlist invariant checks the `name` column entries, NOT heading case.

Skill SKILL.md MUST have `## subagents` table:

```markdown
## subagents

| name | role | model | effort | file |
|------|------|-------|--------|------|
| <agent-name> | <1-line role> | sonnet/haiku/opus | low/med/high | .claude/agents/<file>.md |
```

Invariant: every `phase.agent` and `task.agent` in plan.json MUST appear in `name` column. Single source of truth — no separate `allowed-agents` field.

## §8. Plan invariants (mechanical checks)

```
- plan_version, skill_prefix, model, job_key, created_at present
- job_key === SESSION_ROOT JOB_KEY segment
- total_tasks === sum(phases[].tasks.length)
- phase.id unique within plan
- task.id unique across entire plan
- depends_on references existing phase.id; no cycle
- phase.agent ∈ SKILL.md `## subagents` Name column
- task.agent (when set) ∈ subagents Name column
- phase.agent + task.agent mutex (exactly one, not both)
- mode='parallel' ⇒ tasks.length > 1
- batch_size ≤ tasks.length
- input ≤ 500 token; else input_ref required
- domain payload → input_ref (always, regardless of size)
- scope_ref required if phase has 'domain:deliverables-complete' OR task produces >3 deliverable types
- scope_ref path under <session-root>/staging/scope/; .md extension
- scope_ref file exists + matches checklist regex
- delegated_to mutex with input/input_ref/scope_ref
- delegated_to references existing skill
- acceptance includes 'schema:pass'
- revision monotonic; overwrite plan.json atomic
```

## §9. Decomposition rationale (mandatory in design.md)

Designer writes in `design.md`:

```markdown
## Decomposition Rationale
- shape: atomic | sequential | parallel | tree
- model: A | B | C | D
- review_cycle: on | off
- outer_axes: [<axes with arrows>]
- inner_axes: [<axes without arrows>]
- fold_axes: [<low-cardinality or no-split axes>]
- ordering_source: <where arrow rules come from>
- scope_ref strategy: <when used, when omitted>
- delegation: <none | tasks delegated to sub-skill X>
```

3 universal rules for decomposition:
1. Phase has dependency arrow → outer
2. No arrow → inner (mode by file-conflict analysis)
3. Low cardinality OR no-split → fold into task.input metadata

## §10. Patch order for adoption

1. `orchestrator-rules.md`:
   - rename stages→phases / items→tasks / TASK_KEY→JOB_KEY in all blocks
   - add `scope_ref` to `<plan_v1>` items
   - add `coverage:*` row to `<plan_acceptance>`
   - extend `<contract_v1>` with COVERAGE_DONE / COVERAGE_SKIPPED
   - add 6 invariants to `<plan_invariants>` for scope_ref + naming
   - update `<critical_recap>`
2. `design-template.md`:
   - rename Stages section → Phases
   - add staging files row for scope/
   - add `## Decomposition Rationale` block as mandatory template section
3. `skill-writer/docs/skill-rules-orch.md`:
   - update EX-07 + §3 safety table rename
   - add scope_ref + coverage:* rows
4. Examples — deferred; create on-demand when applying TDM v2 to a real new skill (avoid pre-curated stale examples).

## §11. Conditional requirements summary

| Condition | scope_ref | Reviewer | coverage:* |
|-----------|-----------|----------|------------|
| Simple atomic task (1 deliverable) | omit | not needed | not needed |
| Multi-deliverable task (>3) | required | required (`domain:deliverables-complete`) | optional |
| Cohesive phase (1 agent, many work units) | required | required | recommend |
| Verification-only task | omit | not needed | use `coverage:*` mechanical |
| Sub-skill delegation | use delegated_to instead | n/a | n/a |

## §12. Open items deferred (acknowledged, not in spec)

- DC sourcing method declaration (spec-derived / template / discovery / curated) — kept implicit, designer judgment
- Cross-task scope sharing (5 endpoints same DC structure) — default to per-task file, planner may template
- Reviewer escalation when 2-round REJECT — current: hard FAILURE, future: human gate
- Existing skill retrofit — opt-in / new-skill-only mandatory
- Risk/value-increment PM layer — rejected per user (avoid added complexity)
