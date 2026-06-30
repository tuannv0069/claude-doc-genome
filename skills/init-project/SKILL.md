---
name: init-project
description: Use this skill ONCE per new project to deploy the agent documentation standard — the trio CLAUDE.md + .claude/rules/ + docs/agent-guide/ — plus the skill-authoring set (skill-designer, skill-writer, skill-writer-auditor) and the document-writer documentation skill. Trigger phrases — "init project docs", "khởi tạo bộ tài liệu agent", "deploy doc standard", "/init-project". Two maintenance modes run ONLY at this master repo — "/init-project check" (drift report) and "/init-project promote" (consolidate live → bundle). Do NOT use to author a single new skill (use skill-designer/skill-writer), and do NOT re-run init on an already-initialized project.
---

# init-project

## purpose
Bootstrap a new project's agent documentation system from a portable bundle in one shot. After init the project self-maintains using the deployed standard (`doc-organization.md §8.3` decision tree + portable meta-standards). `init` runs once per project; `update` may be re-run later at that project to pull newer portable files from the bundle (3-way safe merge — never clobbers un-promoted local edits). `check`/`promote` maintain the bundle itself and run only at this master repo.

## dependencies
- `./portable/rules/` — 7 portable rules (always-loaded + path-scoped)
- `./portable/agent-guide/` — five-why.md, bug-report-format.md, review-checklist-method.md, fix-impact-analysis.md, markdown.md, mermaid.md, orchestration-policy.md, worktree.md, task-planning.md (deploy to `docs/agent-guide/general/`)
- `./portable/skills/` — skill-designer/, skill-writer/, document-writer/ (whole trees)
- `./portable/agents/` — skill-writer-auditor.md
- `./templates/` — CLAUDE.md.tpl, agent-guide/index.md.tpl, docs/index.md.tpl
- `./VERSION` — bundle version, bumped on every promote
- `scripts/update.mjs` (repo root) — engine for the `update` mode (3-way bundle→live merge); `scripts/sync-version.mjs` — version single-source sync

## modes

| invocation | runs where | action |
|---|---|---|
| `/init-project` | new project | deploy bundle (workflow below) |
| `/init-project check` | master repo | sha256 compare bundle ↔ live per §map → report drift |
| `/init-project promote` | master repo | copy live → bundle for every mapped file, bump VERSION |
| `/init-project update` | initialized project | pull newer portable files bundle → live, 3-way safe (manifest ↔ live ↔ bundle); skip conflicts (workflow below) |

## workflow (init — new project)
1. Scan project: detect stack + optional modules per `## module matrix` signal column. Output: proposed module set + discovered slot values.
2. Interview: confirm proposed module set; ask slots not scannable (dev ports in use, scope ownership, doc language). Unanswerable slot → leave TODO marker, never invent a value; module uncertain → skip it.
3. Copy `portable/` verbatim: `portable/rules/*` → `.claude/rules/`; `portable/agent-guide/*` → `docs/agent-guide/general/`; `portable/skills/*` → `.claude/skills/`; `portable/agents/*` → `.claude/agents/`.
4. Render templates: fill `{{slots}}` from interview into `CLAUDE.md`, `docs/agent-guide/index.md`, `docs/index.md`; missing slot → keep TODO marker.
5. Generate optional rules: for each confirmed optional module, write a project-fitted rule into `docs/agent-guide/general/` per `rule-writing-standards`, and append its trigger line to `CLAUDE.md` in the same step — no hardcoded template.
6. Write manifest `.claude/init-manifest.json`: `{ version, deployedAt, files:[{path,sha256}], templates:[{path,sha256}], modules:[...] }` (provenance; `files[]` read by `update` for 3-way drift detection — keep sha256 accurate; `templates[]` records the `.tpl` sha each rendered file was built from — `path` = template path relative to `templates/` e.g. `CLAUDE.md.tpl`, used by `update` to WARN when a template changed since deploy).
7. Verify: every deployed file is at the correct tier; every rule/agent-guide file carries `scope:` frontmatter; CLAUDE.md within token budget; every behavior-affecting on-demand file has a trigger line or router entry (reachability, file→trigger); every `MUST Read` trigger in CLAUDE.md resolves to a deployed file (reachability, trigger→file — no dead trigger); no unrendered `{{slot}}` remains except intentional TODO markers. Done = checklist passes + manifest written.

## bundle ↔ live map (check / promote — master repo; update — initialized project)
| bundle path | live path |
|---|---|
| `portable/rules/*` | `.claude/rules/*` |
| `portable/agent-guide/*` | `docs/agent-guide/general/*` |
| `portable/skills/*` | `.claude/skills/*` |
| `portable/agents/*` | `.claude/agents/*` |

- `check`: sha256 each pair → list mismatches. Default update direction is live → bundle (promote); fix live first, then promote.
- `promote`: copy live → bundle for every mapped file, then bump the version via `node scripts/sync-version.mjs set <x.y.z>` (writes canonical `VERSION` + mirrors it into `.claude-plugin/*` and the README badge).

## workflow (update — initialized project)
Direction bundle → live (reverse of promote). Touches only the verbatim portable set; rendered phenotype (`CLAUDE.md`, `index.md`, project-authored guides) is out of scope. Invoke `update.mjs` by its path **inside the installed plugin** (it self-locates the bundle from its own location); `--project` is the initialized project root and defaults to the current directory.
1. Dry-run: `node <plugin>/scripts/update.mjs --project <project-root>` → review the ADD / UPDATE / CONFLICT plan and the version delta.
2. Resolve every CONFLICT first — a conflict = a portable file edited locally since deploy. Promote it upstream (so the improvement enters the bundle) or overwrite manually after review. Never blind-overwrite.
3. Apply: `node <plugin>/scripts/update.mjs --apply --project <project-root>` → writes ADD + UPDATE, skips conflicts, refreshes manifest `version` + `files[].sha256`.
4. Additive + in-place only — `update` never deletes: a file removed from the bundle stays in the project, and a file deleted locally is re-added. Prune those manually if needed.
   - `templates/*` (CLAUDE.md, index.md — rendered phenotype) are never overwritten: their slots hold project-specific values. `update` only emits a WARN when a `.tpl` changed since deploy (sha vs `manifest.templates[]`); re-render manually (diff `.tpl` vs live, re-apply structural changes, keep slot values) or re-run `/init-project`. The WARN persists until the next init re-records the template sha.
5. Exit code: 0 = up-to-date or applied cleanly; 1 = conflicts remain; 2 = setup error (no manifest → project was not init'd by this plugin).

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
