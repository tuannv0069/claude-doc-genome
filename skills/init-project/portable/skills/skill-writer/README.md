# Skill: skill-writer

Take a workflow design (from `/skill-designer`), plain text, or an existing skill → produce a standards-compliant `SKILL.md` + optional supporting files + per-subagent `.claude/agents/<name>.md` + English `README.md`.

## Quick Start

```
/skill-writer .claude/skills/pr-review/docs/design.md
/skill-writer review .claude/skills/foo/SKILL.md
/skill-writer "convert markdown to PDF, manual invoke, single shot"
```

**Output:** `~/.claude/skills/<name>/SKILL.md` (or `.claude/skills/<name>/`) + `docs/`, `scripts/`, `.claude/agents/*.md` (orch only), `README.md`.

## Requirements

- Dependencies declared in [SKILL.md](SKILL.md) `## dependencies`:
  - `docs/skill-rules-spec.md` — platform spec (frontmatter, context loading, substitutions, permissions, writing rules, troubleshooting)
  - `docs/skill-rules-orch.md` — orchestration rules (EX-01..EX-09, CONTRACT-V1, safety controls)
  - `docs/skill-rules-quality.md` — quality gate (audit, self-test, release)
  - `docs/skill-rules-workflow.md` — dynamic workflow branch (script shape, constraints, save locations)
  - `docs/examples.md` — annotated patterns
  - `.claude/rules/skill-md-standards.md` — SKILL.md target body rules
  - `.claude/rules/rule-writing-standards.md` — wording, format, RFC2119 budget
- Manual invoke only (`disable-model-invocation: true`)

## How It Works

13-step workflow:

1. Parse `$ARGUMENTS` → branch (file / design / review / workflow / plain text). Design with `Substrate: dynamic-workflow` → §workflow-branch: script to `.claude/workflows/<name>` instead of SKILL.md + agents.
2. Empty `$ARGUMENTS` → prompt user.
3. Classify simple vs orchestration.
4. Gather requirements per branch.
5. Draft frontmatter via `§frontmatter-decision`.
6. Draft SKILL.md body per `§structure-by-type`.
7. Orchestration → apply EX-01..EX-09 + CONTRACT-V1 + scope_ref protocol.
8. Self-validate.
9. Present + ask: accept / change / write-to-disk.
10. Write skill dir + `docs/` + `scripts/`.
11. Orchestration only → write `.claude/agents/<name>.md` per `## subagents` row (skips existing; warns on conflict).
12. Generate English `README.md` per `§readme-template`.
13. Verify: re-read + run `§self-check` + `skill-rules-quality.md §4` release gate.

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| Skill does not trigger | description does not match intent — add keywords (only if `disable-model-invocation` not set) |
| `.claude/agents/<name>.md` missing | Step 11 skipped — re-run for orch skills |
| description+when_to_use > 1536 chars | Front-load use case; cut trailing detail (per `skill-rules-spec.md §2.1`) |
| Permission prompts | Missing `allowed-tools` for safe tools (Read/Grep/Glob) |
| `disable-model-invocation: true` + `user-invocable: false` | Skill unreachable — never set both |
| `TASK_KEY` in generated skill | Stale — rename to `JOB_KEY` (canonical per `plan-gate-spec.md §2`) |

## Example

**Input:** `/skill-writer "deploy current branch to staging, manual invoke"`

**Output (SKILL.md excerpt):**

```yaml
---
name: deploy-staging
description: Deploy current branch to staging environment...
argument-hint: "[branch-name]"
disable-model-invocation: true
allowed-tools: Bash Read
---

# deploy-staging

## purpose
Deploy current branch to staging...

## workflow
1. ...
N. Verify: deploy ID returned + smoke test passes
```

## Self-test

Run shared test script from repo root:

```bash
bash .claude/skills/skill-writer/scripts/test-skill.sh .claude/skills/skill-writer/
```

Checks: frontmatter, description+when_to_use ≤ 1536, dep files exist, no stale `TASK_KEY` / `EX-01..EX-08` / stage prose / Vietnamese leakage; examples use `phases` naming. Canonical EX range: `EX-01..EX-09`.
