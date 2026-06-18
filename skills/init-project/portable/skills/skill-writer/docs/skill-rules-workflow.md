<critical>
target: skill-writer agent reference — dynamic workflow branch
purpose: produce a dynamic workflow script (substrate decided by skill-designer §substrate-selection) instead of SKILL.md + agents
source: code.claude.com/docs/en/workflows + Workflow tool runtime
scope: §1 save locations, §2 script shape, §3 checklist, §4 constraints, §5 mapping from design.md
</critical>

<dependencies>
- `.claude/skills/skill-designer/docs/orchestrator-rules.md` `<substrate_selection>` — when workflow substrate applies + mechanism mapping
</dependencies>

---

## §1 save locations

| location | scope | invoke |
|---|---|---|
| `.claude/workflows/<name>` | project (commit to git) | `/<name>` |
| `~/.claude/workflows/<name>` | personal, every project | `/<name>` |

name clash → project wins. `args` reaches the script as a structured global (arrays/objects usable directly). The `/workflows` view `s` key saves a finished run's script to either location.

## §2 script shape

Plain JavaScript (NOT TypeScript). Must begin with a pure-literal meta block:

```javascript
export const meta = {
  name: 'audit-endpoints',
  description: 'Audit API endpoints for missing auth checks',  // one line, shown in permission dialog
  whenToUse: 'run on demand before release',                   // optional, shown in workflow list
  phases: [
    { title: 'Find', detail: 'one finder agent per route group' },
    { title: 'Verify', detail: 'adversarial check per finding' },
  ],
}
// body runs in async context — await directly
phase('Find')
const findings = await parallel(groups.map(g => () =>
  agent(`Scan ${g} for missing auth checks.`, { phase: 'Find', schema: FINDINGS })))
```

body hooks: `agent(prompt, {label, phase, schema, model, agentType, isolation})`, `parallel(thunks)` (barrier), `pipeline(items, ...stages)` (default for multi-stage), `phase(title)`, `log(msg)`, `args`, `budget`.

| rule | detail |
|---|---|
| `meta` pure literal | no variables, calls, spreads, interpolation |
| `meta.phases` titles | match `phase()` calls exactly |
| structured returns | pass `schema` (JSON Schema) → validated object; no text parsing |
| reuse project agents | `agentType: '<name>'` resolves `.claude/agents/<name>.md` |
| parallel file edits | `isolation: 'worktree'` per agent (expensive — only on real conflicts) |
| default `pipeline()` | barrier (`parallel` between stages) only when stage N needs ALL of stage N-1 |
| no `Date.now()` / `Math.random()` / argless `new Date()` | breaks resume — pass timestamps via `args` |
| no filesystem / Node API in script | agents do I/O; script only coordinates |

## §3 checklist (verify before save)

- [ ] `export const meta = {...}` first statement; pure literal; `name` + `description` present
- [ ] every `phase()` title appears in `meta.phases`
- [ ] plain JS — no type annotations / interfaces / generics
- [ ] structured data via `schema`, not free-text parsing
- [ ] `pipeline()` unless a genuine cross-item barrier is needed
- [ ] `.filter(Boolean)` after `parallel()` (skipped/dead agents resolve to null)
- [ ] no `Date.now()` / `Math.random()` / argless `new Date()`
- [ ] unbounded loops guarded (`budget.total` check or fixed rounds)
- [ ] silent caps logged (`log()` what was dropped)
- [ ] saved under `.claude/workflows/` or `~/.claude/workflows/`

## §4 runtime constraints

| constraint | consequence for design |
|---|---|
| no mid-run user input | user sign-off between stages → split into separate workflows (or keep skill-orchestration substrate) |
| subagents run `acceptEdits` + inherit session tool allowlist | per-agent permission modes (skill-rules-orch §3) do not apply |
| ≤ 16 concurrent agents; 1000 agents/run; 4096 items/call | runtime queues excess — do not design batch_size |
| resume same-session only | cross-session resume requirement → skill-orchestration substrate |
| requires CLI ≥ 2.1.154, paid plan, workflows not disabled | env not guaranteed → skill-orchestration substrate |

## §5 mapping from design.md (Model B/C/D → workflow)

canonical mapping table lives in `.claude/skills/skill-designer/docs/orchestrator-rules.md` `<substrate_selection>` — read it before mapping; do not duplicate here.

---

<critical_recap>
1. workflow = script artifact under `.claude/workflows/` → `/<name>`; NOT a SKILL.md
2. meta pure literal; phases titles match phase() calls
3. schema replaces CONTRACT-V1; pipeline() is the default shape
4. no mid-run user input; subagents run acceptEdits — gate-heavy designs stay skill-orchestration
5. no Date.now()/Math.random() in script (breaks resume)
</critical_recap>
