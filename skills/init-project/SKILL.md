---
name: init-project
description: Use this skill ONCE per new project to deploy the agent documentation standard — the trio CLAUDE.md + .claude/rules/ + docs/agent-guide/ — plus the skill-authoring set (skill-designer, skill-writer, skill-writer-auditor) and the document-writer documentation skill. Trigger phrases — "init project docs", "khởi tạo bộ tài liệu agent", "deploy doc standard", "/init-project". Two maintenance modes run ONLY at this master repo — "/init-project check" (drift report) and "/init-project promote" (consolidate live → bundle). Do NOT use to author a single new skill (use skill-designer/skill-writer), and do NOT re-run init on an already-initialized project.
---

# init-project

## purpose
Bootstrap a new project's agent documentation system from a portable bundle in one shot. After init the project self-maintains using the deployed standard (`doc-organization.md §8.3` decision tree + portable meta-standards) — this skill is never run again in that project. `check`/`promote` modes maintain the bundle itself and run only at this master repo.

## dependencies
- `./portable/rules/` — 7 portable rules (always-loaded + path-scoped)
- `./portable/agent-guide/` — five-why.md, markdown.md, mermaid.md, orchestration-policy.md (deploy to `docs/agent-guide/general/`)
- `./portable/skills/` — skill-designer/, skill-writer/, document-writer/ (whole trees)
- `./portable/agents/` — skill-writer-auditor.md
- `./templates/` — CLAUDE.md.tpl, agent-guide/index.md.tpl, docs/index.md.tpl
- `./VERSION` — bundle version, bumped on every promote

## modes

| invocation | runs where | action |
|---|---|---|
| `/init-project` | new project | deploy bundle (workflow below) |
| `/init-project check` | master repo | sha256 compare bundle ↔ live per §map → report drift |
| `/init-project promote` | master repo | copy live → bundle for every mapped file, bump VERSION |

## workflow (init — new project)
1. Scan project: detect stack + optional modules per `## module matrix` signal column. Output: proposed module set + discovered slot values.
2. Interview: confirm proposed module set; ask slots not scannable (dev ports in use, scope ownership, doc language). Unanswerable slot → leave TODO marker, never invent a value; module uncertain → skip it.
3. Copy `portable/` verbatim: `portable/rules/*` → `.claude/rules/`; `portable/agent-guide/*` → `docs/agent-guide/general/`; `portable/skills/*` → `.claude/skills/`; `portable/agents/*` → `.claude/agents/`.
4. Render templates: fill `{{slots}}` from interview into `CLAUDE.md`, `docs/agent-guide/index.md`, `docs/index.md`; missing slot → keep TODO marker.
5. Generate optional rules: for each confirmed optional module, write a project-fitted rule into `docs/agent-guide/general/` per `rule-writing-standards`, and append its trigger line to `CLAUDE.md` in the same step — no hardcoded template.
6. Write manifest `.claude/init-manifest.json`: `{ version, deployedAt, files:[{path,sha256}], modules:[...] }` (provenance only, not read at runtime).
7. Verify: every deployed file is at the correct tier; every rule/agent-guide file carries `scope:` frontmatter; CLAUDE.md within token budget; every behavior-affecting on-demand file has a trigger line or router entry (reachability, file→trigger); every `MUST Read` trigger in CLAUDE.md resolves to a deployed file (reachability, trigger→file — no dead trigger); no unrendered `{{slot}}` remains except intentional TODO markers. Done = checklist passes + manifest written.

## bundle ↔ live map (check / promote — master repo)
| bundle path | live path |
|---|---|
| `portable/rules/*` | `.claude/rules/*` |
| `portable/agent-guide/*` | `docs/agent-guide/general/*` |
| `portable/skills/*` | `.claude/skills/*` |
| `portable/agents/*` | `.claude/agents/*` |

- `check`: sha256 each pair → list mismatches. Default update direction is live → bundle (promote); fix live first, then promote.
- `promote`: copy live → bundle for every mapped file, bump `VERSION`.

## module matrix
| module | includes | deploy when | scan signal (examples, not exhaustive) |
|---|---|---|---|
| core | `portable/*` (all 4 groups) + 3 templates | always | — |
| runtime | `agent-guide/general/local-runtime.md` + CLAUDE.md trigger (skill writes per scan, step 5) | project self-runs a dev server | `package.json` dev/start scripts, `launchSettings.json`, vite/next/dotnet/django/cargo config |
| e2e | `agent-guide/general/<tool>.md` (named after detected tool) + CLAUDE.md trigger (step 5) | project has E2E browser tests | playwright/cypress/selenium dep, `e2e/` folder, E2E config |

- Optional module deploys only when scan confirms OR user confirms at interview — uncertain → skip.
- Git: minimal guardrail (commit only on request, never push) ships in `CLAUDE.md.tpl`; detailed policy is `scope: project` — project writes `docs/agent-guide/general/git.md` on demand, adding its trigger line in the same commit (reachability — never a trigger pointing at a missing file).
- A skipped module needed later → project writes the rule itself per the deployed standard. New module enters the bundle only via `promote` after a real project battle-tests the pattern.

## independence rules
- Skill runs once per project; deployed files reference no file of this master repo; project rules never name this skill.
- Self-contained except the bundle↔live map above, which executes only at the master repo for check/promote.

## examples
```
✅ scan finds package.json with "dev" script → propose runtime module → step 5 writes
   general/local-runtime.md + appends "self-run dev server → MUST Read ..." to CLAUDE.md
❌ deploy runtime module with no scan signal and no interview confirm (guessed module)

✅ /init-project check → "MISMATCH: portable/rules/doc-organization.md != .claude/rules/doc-organization.md"
   → fix live first → /init-project promote
❌ edit portable/* directly then init a new project (bundle diverges silently from live)
```

## reference files
- bundle: `./portable/**`
- templates: `./templates/**`
- version: `./VERSION`
