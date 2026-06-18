# Skill: skill-designer

Design a Claude Code skill / orchestrator workflow → outputs `design.md` ready for `/skill-writer`.

## Quick Start

```
/skill-designer convert 50 markdown files to PDF in parallel, with a review step
```

**Output:** `.claude/skills/{name}/docs/design.md` (filled from `design-template.md`)

## Requirements

- Dependencies declared in [SKILL.md](SKILL.md) `## dependencies`:
  - `docs/orchestrator-rules.md` — schemas, model decision matrix, anti-patterns
  - `docs/design-template.md` — output document template + field reference
  - `docs/plan-gate-spec.md` — Plan Gate + plan.json + WBS spec
  - `docs/agent-guide/general/markdown.md` — markdown formatting
- Manual invoke only (`disable-model-invocation: true`)

## How It Works

13-step workflow:

1. Read `orchestrator-rules.md` + `design-template.md` + `plan-gate-spec.md`.
2. Gather task description from `$ARGUMENTS` or prompt user.
3. Apply orchestration decision table (`§needs-assessment`).
4. Model A → STOP (point to `/skill-writer`).
5. Apply `§substrate-selection` — dynamic workflow (`.claude/workflows/`, runtime-managed) vs skill orchestration (Model B/C/D).
6. Pick model B/C/D topology (`§model-selection`).
7. Design subagents — 1 sentence per agent objective.
8. Design phases (cohesive XOR distributed) — assign agents per phase.
9. Fill remaining `design-template.md` sections (Planning Gate, State, Staging, QA, Safety, Self-Healing, Token Budget); dynamic-workflow → runtime-managed sections marked n/a.
10. Token budget estimate + 30% headroom check.
11. Ask user for skill name (kebab-case, 4-20 chars) + skill prefix (4-8 chars, unique under `.agent/tmp/`; n/a for dynamic-workflow).
12. Write `.claude/skills/{name}/docs/design.md`.
13. Verify against full `## design-checks` list (22 invariants); PASS = zero violations.

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| `<placeholder>` left in design.md | Re-fill missing sections; step 13 must report zero violations |
| Subagent objective has >1 verb | Split into multiple agents (1 verb each) |
| Parallel agents share write target | Each owns its own staging file; sequential aggregator merges |
| Description+when_to_use >1536 chars | Front-load use case; cut trailing detail |

## Example

**Input:** "I want a skill that lints + tests + summarizes a PR"

**Output (design.md excerpt):**

```markdown
# Workflow Design: pr-review

## Overview
- Model: B (sequential subagents)
- Skill prefix: prrev

## Subagents
| # | Name | Objective | Model | Effort |
|---|------|-----------|-------|--------|
| 1 | prrev-lint | Run lint on changed files | sonnet | medium |
| 2 | prrev-test | Run test suite | sonnet | high |
| 3 | prrev-summary | Summarize lint+test results | sonnet | medium |
...
```

## Self-test

Run shared test script from repo root:

```bash
bash .claude/skills/skill-writer/scripts/test-skill.sh .claude/skills/skill-designer/
```

Checks: frontmatter, description+when_to_use ≤ 1536, dep files exist, design-checks count = 22, no stale `TASK_KEY` / `EX-01..EX-08` / stage prose / Vietnamese leakage. Canonical EX range: `EX-01..EX-09`.
