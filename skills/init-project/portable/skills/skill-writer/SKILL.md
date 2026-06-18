---
name: skill-writer
description: >
  Write, create, or review a SKILL.md (slash-command skill definition). Handles
  simple skills + orchestration (Model B/C/D) + dynamic workflow scripts, incl.
  per-subagent agent files. Do NOT use for project rules
  (rule-writing-standards) or non-skill markdown.
argument-hint: "<description | path-to-design | review path>"
disable-model-invocation: true
allowed-tools: Read Grep Glob Write Edit Bash
---

# skill-writer

## purpose

Take a workflow design (from `/skill-designer`), a plain-text requirement, or an
existing skill, and produce a complete, standards-compliant SKILL.md with
optional supporting files, per-subagent `.claude/agents/<name>.md` (orch only),
and an English README.md (per project `.claude/**` rule).

## dependencies

- `${CLAUDE_SKILL_DIR}/docs/skill-rules-spec.md` — platform spec (frontmatter, context loading, substitutions, permissions, writing rules, troubleshooting)
- `${CLAUDE_SKILL_DIR}/docs/skill-rules-orch.md` — orchestration rules (EX-01..EX-09, CONTRACT-V1, scope_ref protocol, safety controls)
- `${CLAUDE_SKILL_DIR}/docs/skill-rules-quality.md` — quality gate (audit, self-test, release)
- `${CLAUDE_SKILL_DIR}/docs/skill-rules-workflow.md` — dynamic workflow branch (script shape, constraints, save locations)
- `${CLAUDE_SKILL_DIR}/docs/examples.md` — annotated patterns
- `.claude/rules/skill-md-standards.md` — SKILL.md target body rules
- `.claude/rules/rule-writing-standards.md` — wording, format, RFC2119 budget
- `.claude/rules/doc-organization.md` — generated SKILL.md MUST NOT inline substantive code rule; reference agent-guide §ID instead

## workflow

1. Parse `$ARGUMENTS` per `## conditional` "input type" → choose branch (file, design, review, workflow, plain text).
2. `$ARGUMENTS` empty → ask user for description / design path / `review <path>`.
3. Classify skill type → simple or orchestration (`## conditional` "skill type"). Design declares `Substrate: dynamic-workflow` → go to §workflow-branch (steps 4-13 do not apply). Ambiguous → ask one question; default simple.
4. Gather requirements per branch — simple: §req-simple; orchestration: §req-orch.
5. Read `skill-rules-spec.md` §2 → draft frontmatter using §frontmatter-decision matrix.
6. Draft SKILL.md body using `## conditional` "structure by type".
7. Orchestration → read `skill-rules-orch.md` → apply EX-01..EX-09 + CONTRACT-V1; when any task uses `scope_ref`, agent prompts MUST emit `COVERAGE_DONE`/`COVERAGE_SKIPPED` (EX-09).
8. Self-validate against §self-check.
9. Present complete SKILL.md + supporting files; ask: accept / change / write-to-disk.
10. User confirms → write to `~/.claude/skills/<name>/` or `.claude/skills/<name>/`; create `docs/`, `scripts/` only if needed.
11. Orchestration only → derive `## subagents` allowlist table (5 cols: name | role | model | effort | file) from design.md `## Subagents` (7 cols) by column mapping (Name→name, Objective→role, Model→model, Effort→effort, file=`.claude/agents/<name>.md`; drop #/Input/Output). Then for every row, create `.claude/agents/<name>.md` per §agent-file-template (skip if file already exists; warn on conflict).
12. Generate `README.md` (English, per `.claude/**` project rule) using §readme-template; ask user which optional sections.
13. Spawn `skill-writer-auditor` with `SKILL_DIR=.claude/skills/{name}/` and `IS_ORCH=<true|false>`:
    - STATUS: SUCCESS → report PRODUCTION READY, done.
    - STATUS: FAILURE → fix every item in MODIFIED_ITEMS → re-spawn (round 2 max).
    - Round 2 FAILURE → escalate to user with full DETAIL; do not attempt round 3.

## subagents

| name | role | model | effort | file |
|------|------|-------|--------|------|
| skill-writer-auditor | Audit output skill for production readiness | sonnet | low | .claude/agents/skill-writer-auditor.md |

## conditional

### input type

| detection | branch |
|---|---|
| starts with `/`, `./`, `~`, ends with `.md` | file path → Read, extract requirements |
| contains `Substrate: dynamic-workflow` or "dynamic workflow" | dynamic workflow → §workflow-branch |
| contains "Model B/C/D", "subagent", "orchestrat" | workflow design → orchestration input |
| first word is "review" | review mode → audit (§review) |
| else | plain text → simple skill requirement |

### skill type

| indicator | type |
|---|---|
| reference content, single task, no subagents, no state | simple |
| multiple phases, subagent spawning, state file, parallel exec, retry | orchestration |

### structure by type

| section | simple | orchestration |
|---|---|---|
| frontmatter | required | required |
| role / purpose | 1-3 lines | 1-3 lines |
| input validation | if args | if args |
| workflow | numbered, ≤ 500 lines / < 1500 tokens | numbered, ≤ 800 lines / < 3000 tokens |
| verification step | mandatory at end of workflow | mandatory at end of workflow |
| subagent prompts | n/a | extract to `.claude/agents/*.md` |
| `## subagents` table | n/a | required — IS the allowlist for plan.json `phase.agent` AND `task.agent` |
| schemas / large refs (>20 lines) | extract to `${CLAUDE_SKILL_DIR}/docs/*.md` | extract to `${CLAUDE_SKILL_DIR}/docs/*.md` |

### format density (target SKILL.md body — pick most-compressed that fits)

| content | format |
|---|---|
| 3+ parallel rules same schema | table |
| simple if-then | `cond → action` arrow |
| ordered workflow | numbered list |
| independent rules | bullet |
| nuance required | prose (≤ 3 sentences) |

---

## §req-simple

determine through conversation or input:

1. purpose — what does this skill do (1-2 sentences)
2. trigger — manual only or auto-invoked, what signals
3. arguments — accepts arguments, format
4. tools needed — Read, Grep, Glob, Edit, Write, Bash
5. side effects — deploy, commit, send messages, modify external state
6. output location — `~/.claude/skills/` or `.claude/skills/`

## §req-orch

beyond §req-simple, also determine:

1. orchestration model — B (sequential), C (parallel), D (hybrid)
2. subagent inventory — how many, what each does
3. state management — what state needs tracking
4. handoff data — what passes between phases
5. failure handling — retry, partial success

## §frontmatter-decision

field reference: `skill-rules-spec.md` §2.1
field interactions: `skill-rules-spec.md` §2.2

decision matrix (writer-specific):

| field | rule |
|---|---|
| `name` | match dir name; lowercase kebab-case (display label — command comes from dir name) |
| `description` | start "Use when..."; front-load use case + triggers + scope; combined with `when_to_use` ≤ 1536 chars |
| `when_to_use` | extra trigger phrases / example requests when description alone under-matches |
| `argument-hint` | `[brackets]` optional, `<angles>` required |
| `arguments` | ≥ 2 positional args with distinct meanings → declare names for `$name` substitution |
| `disable-model-invocation` | side effects OR manual-only → `true` |
| `allowed-tools` | declare safe tools to skip permission prompts |
| `disallowed-tools` | autonomous/background skill → remove unsafe tools (e.g. `AskUserQuestion`) |
| `context: fork` | only if self-contained AND orchestrator does not need output |

## §content-rules

target body of generated SKILL.md must follow these (per `skill-md-standards.md`):

ALWAYS:
- SKILL.md ≤ 500 lines / < 1500 tokens (simple) | ≤ 800 lines / < 3000 tokens (orchestration)
- side effects → `disable-model-invocation: true`
- supporting files via `${CLAUDE_SKILL_DIR}/...`, never relative
- large schemas/scripts (>20 lines) → `docs/` or `scripts/`, not inline
- declare `allowed-tools` for safe tools
- task skill: workflow ends with explicit verification step
- abstract rule → paired ✅/❌ example
- one step = one line, imperative verb start
- semantic headings (= "when read this?")

NEVER:
- XML wrap target SKILL.md body (`<rules section="...">`, `<critical>`, etc. — those belong in `.claude/rules/*.md`, not SKILL.md targets)
- hedge words: `generally | typically | usually | try | consider | might | perhaps | ideally`
- decorative md: emoji, `!!!`, CAPS-for-emphasis
- nest bullets > 2 levels
- MUST/NEVER on rules with exceptions (budget ≤ 10% of rules)
- restate workflow steps for emphasis
- duplicate rule across sections

## §review

input starts with "review" → audit existing skill against §self-check, output:

```text
SKILL: <skill-name>
TYPE: simple | orchestration
LINE COUNT: <N> / <limit>
STATUS: PASS | ISSUES_FOUND

ISSUES:
- [severity] [rule]: [description]

SUGGESTIONS:
- [description]
```

severity: `MUST` (mandatory rule), `SHOULD` (recommended), `INFO` (optional)

## §self-check

structure + frontmatter:
- [ ] SKILL.md exists as entrypoint
- [ ] frontmatter valid per `skill-rules-spec.md` §2
- [ ] `description` starts "Use when..." / "Use this skill when...", front-loads use case + triggers + scope; combined with `when_to_use` ≤ 1536 chars
- [ ] line count under limit (500 simple / 800 orchestration) AND token budget (< 1500 simple / < 3000 orchestration)
- [ ] side-effect skills set `disable-model-invocation: true`
- [ ] never combine `disable-model-invocation: true` + `user-invocable: false` (unreachable)
- [ ] supporting files via `${CLAUDE_SKILL_DIR}/...`, never relative
- [ ] no large schemas / scripts inline (>20 lines → companion file)
- [ ] `allowed-tools` declared for safe tools
- [ ] skill name does not duplicate bundled (`/batch`, `/claude-api`, `/code-review`, `/debug`, `/deep-research`, `/loop`, `/run`, `/run-skill-generator`, `/simplify`, `/verify`) or Skill-tool built-ins (`/init`, `/review`, `/security-review`)

target body content rules (per `skill-md-standards.md`):
- [ ] NO XML wrap in target body (`<rules>`, `<critical>`, etc. — plain markdown only)
- [ ] zero hedges (`generally|typically|usually|try|consider|might|perhaps|ideally`)
- [ ] MUST/NEVER ≤ 10% of rules
- [ ] no decorative md (emoji, `!!!`, CAPS-for-emphasis)
- [ ] no nested bullets > 2 levels
- [ ] semantic headings (`## when to refuse`, not `## 🔥 important`)
- [ ] one step = one line, imperative verb start
- [ ] workflow ends with explicit verification step
- [ ] abstract rule → paired ✅/❌ example
- [ ] no duplicate rule across sections
- [ ] format chosen by density (table > arrow > numbered > bullet > prose)
- [ ] string substitutions correct per `skill-rules-spec.md` §5

orchestration only:
- [ ] orchestrator does not read domain content (EX-01)
- [ ] subagents use CONTRACT-V1
- [ ] state / staging paths use layout `.agent/tmp/{prefix}/sessions/{JOB_KEY}/{SESSION}/...`
- [ ] JOB_KEY source declared (REPORT_ID | input-hash | slug); no flat `state-${SESSION}.json` at prefix root
- [ ] `latest` symlink per JOB_KEY for resume
- [ ] retention declared (archive 7d, delete 30d, cleanup_ready gated)
- [ ] no timestamp suffix in filenames inside session dir (dir already timestamped)
- [ ] batch size starts 3-4
- [ ] plan.json schema = `<plan_v1>` (skill-designer/orchestrator-rules.md)
- [ ] every phase `acceptance` is array including `schema:pass`
- [ ] `domain:*` acceptance → Reviewer agent named
- [ ] `## subagents` table present in SKILL.md body (Model B/C/D); every plan `phase.agent` AND `task.agent` ∈ table `name` column
- [ ] every `## subagents` row points to existing `.claude/agents/*.md` file
- [ ] no separate `allowed-agents` field/section (table is sole allowlist)
- [ ] inline `input` ≤ 500 token AND control primitive only; else `input_ref`
- [ ] replan via `revision++` overwrite (no `plan-v{N}.json` files)

## §workflow-branch

design.md declares `Substrate: dynamic-workflow` (or user asks for one) → produce a workflow script, NOT a SKILL.md.

1. Read `${CLAUDE_SKILL_DIR}/docs/skill-rules-workflow.md` (script shape, constraints, save locations).
2. Map design.md → script: Phases table → `meta.phases` + `phase()` calls; Subagents table → `agent()` prompts (reference an existing `.claude/agents/<name>.md` via `agentType` when one fits); handoffs → script variables; QA review → verification phase with `schema` structured output.
3. Present script; user confirms → save under `.claude/workflows/<name>` (project, shared) or `~/.claude/workflows/<name>` (personal) — runs as `/<name>`; project wins name clash.
4. Verify against `skill-rules-workflow.md` §3 checklist.
5. Do NOT generate: `## subagents` table, CONTRACT-V1 prompts, state/staging files, README per §readme-template — runtime manages orchestration state; document usage in the script's `meta.description` + `whenToUse`.

## §readme-template

always generate `.claude/skills/<name>/README.md` (English — project rule: `.claude/**` = English)

required sections:

```markdown
# Skill: <skill-name>

<1-2 sentence description>

## Quick Start

/skill-name <example>

**Output:** where results are stored, what gets created

## Requirements

- Dependencies
- Input format (if any)

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| Issue 1 | Check step |

## Example

**Input:** [input description]

[code/format example]

**Output:** [expected result]
```

optional sections by skill type:

| skill type | add section | position |
|---|---|---|
| data transformation | Data Mapping | after Requirements |
| file processing | File Structure | after Requirements |
| complex workflow | How It Works | after Requirements |
| file generation | Output Naming | after Requirements |

language rule: English (per project CLAUDE.md `.claude/**` rule)

before writing, prompt user:

```text
README.md sections:
  - Quick Start
  - Requirements
  - Troubleshooting
  - Example

Add any of these optional sections?
  - Data Mapping (if transforms/maps data)
  - File Structure (if works with dirs/files)
  - How It Works (if workflow is multi-step)
  - Output Naming (if generates named outputs)

Write to .claude/skills/<name>/README.md?
```

## §agent-file-template

orchestration only — write one `.claude/agents/<name>.md` per row in target SKILL.md `## subagents` table.

required structure:

```markdown
---
name: <agent-name>
description: <one-line role from ## subagents table>
model: <haiku | sonnet | opus | fable | inherit>
effort: <low | medium | high | xhigh | max>
tools: <Read, Grep, Glob, Edit, Write, Bash — least-privilege subset>
---

# <agent-name>

## Objective
<single sentence — what this agent produces>

## Input
- <field>: <type> — <purpose>
- scope_ref: <path | omit if no DC> — markdown checklist of deliverables

## Workflow
1. Read input + scope_ref (if set)
2. Read template / reference files
3. <execute task>
4. Self-check against ## Self-check
5. Emit CONTRACT-V1 block ONLY (discard reasoning)

## Self-check (≥5 items, mix format + domain)
- [ ] <format check>
- [ ] <format check>
- [ ] <domain check>
- [ ] <domain check>
- [ ] when scope_ref set: every leaf in COVERAGE_DONE ∪ COVERAGE_SKIPPED

## Do
- <known-good behavior 1>
- <known-good behavior 2>

## Avoid
- <specific known error 1>
- <specific known error 2>

## Output (CONTRACT-V1)
```
STATUS: SUCCESS | FAILURE | SKIPPED | REJECT
CHANGES: <number>
MODIFIED_ITEMS: <list or ->
ERROR: <short or ->
DETAIL: <≤5 lines>
COVERAGE_DONE: <leaf IDs | omit if no scope_ref>
COVERAGE_SKIPPED: <id (reason); ... | omit if no scope_ref>
REASON: <if SKIPPED>
REJECT_DETAIL: <if REJECT>
```
```

rules:
- agent frontmatter uses `tools` (comma-separated) — NEVER `allowed-tools` (skill-only field; ignored on agents → agent silently inherits ALL tools)
- optional agent fields when the design needs them: `disallowedTools`, `skills` (preload full skill content at startup), `memory`, `maxTurns`, `permissionMode`, `isolation: worktree`, `background`, `color`
- one agent file per `## subagents` row; no hidden agents
- file path: `.claude/agents/<name>.md` (project) or `~/.claude/agents/<name>.md` (user)
- on conflict (file exists): warn user, ask: keep existing | overwrite | skip
- when `scope_ref` is set in any task input, agent prompt MUST include "read scope_ref + emit COVERAGE_DONE/SKIPPED" instruction (EX-09)
- Do + Avoid sections mandatory (EX-09 + agent file rules §6)

## examples

### description

✅ Good:
```yaml
description: >
  Use when user asks to clean, normalize, deduplicate, or validate CSV/TSV
  files. Trigger keywords: CSV, TSV, clean data, remove duplicates. Do NOT
  use for Excel files (use xlsx skill).
```

❌ Bad: `description: Helps with data stuff` — vague, no triggers, no scope

❌ Bad: `description: Use this skill for any document work` — overlaps docx/pdf/xlsx

### frontmatter for side-effect skill

✅ Good:
```yaml
---
name: deploy-staging
description: Use when user asks to deploy current branch to staging environment...
disable-model-invocation: true
allowed-tools: Bash Read
---
```

❌ Bad: missing `disable-model-invocation: true` on a deploy skill → auto-trigger risk

### orchestrator vs subagent split

✅ Good: orchestrator reads `state.json` (counts, STATUS), routes to next agent based on CONTRACT-V1

❌ Bad: orchestrator reads source `.md` content to decide next step → violates EX-01

---

troubleshooting → `skill-rules-spec.md` §13
