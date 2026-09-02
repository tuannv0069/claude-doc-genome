---
name: init-project
description: Use this skill ONCE per new project to deploy the agent documentation standard — the trio CLAUDE.md + .claude/rules/ + .agent-workspace/guide/ — plus the skill-authoring set (skill-designer, skill-writer, skill-writer-auditor) and the document-writer documentation skill. Trigger phrases — "init project docs", "khởi tạo bộ tài liệu agent", "deploy doc standard", "/init-project". Two maintenance modes run ONLY at this master repo — "/init-project check" (drift report) and "/init-project promote" (consolidate live → bundle). Do NOT use to author a single new skill (use skill-designer/skill-writer), and do NOT re-run init on an already-initialized project.
---

# init-project

## purpose
Bootstrap a new project's agent documentation system from a portable bundle in one shot. After init the project self-maintains using the deployed standard (`doc-organization.md §8.3` decision tree + portable meta-standards). `init` runs once per project; `update` may be re-run later at that project to pull newer portable files from the bundle (3-way safe merge — never clobbers un-promoted local edits). `check`/`promote` maintain the bundle itself and run only at this master repo.

## dependencies
- `./portable/rules/` — 9 portable rules (always-loaded + path-scoped)
- `./portable/guide/` — bug-report-format.md, doc-system-mechanics.md, five-why.md, fix-impact-analysis.md, lesson-capture.md, markdown.md, mermaid.md, decision-journal.md, orchestration-policy.md, review-checklist-method.md, role-selection.md, task-planning.md, verification-gate-design.md, worktree.md (deploy to `.agent-workspace/guide/general/`)
- `./portable/roles/` — business-analyst.md, tech-lead.md, developer.md, qa.md, project-manager.md, security.md, comtor.md (deploy to `.agent-workspace/guide/roles/`) — the genome role set, seven sections each, capped at 90 lines (`role-selection.md` §3)
- `./portable/tooling/` — verify_lesson_router.py, verify_role_files.py, verify_decision_log.py, verify_wiki.py (each with its test_*.py) and archive_decisions.py (deploy to `.agent-workspace/tooling/`) — the gates over the genome's own artifacts, Python 3 stdlib only; a project's own tools never enter this group
- `./portable/skills/` — skill-designer/, skill-writer/, document-writer/ (whole trees)
- `./portable/agents/` — skill-writer-auditor.md
- `./templates/` — CLAUDE.md.tpl, guide/index.md.tpl, docs/index.md.tpl, lessons/index.md.tpl, roles/index.md.tpl, decisions/index.md.tpl, wiki/index.md.tpl
- `./VERSION` — bundle version, bumped on every promote
- `scripts/update.mjs` (repo root) — engine for the `update` mode (3-way bundle→live merge); `scripts/init-manifest.mjs` — computes the step-6 manifest; `scripts/sync-version.mjs` — version single-source sync

## modes

| invocation | runs where | action |
|---|---|---|
| `/init-project` | new project | deploy bundle (workflow below) |
| `/init-project check` | master repo (init'd) | sha256 compare bundle ↔ live per §map → report drift |
| `/init-project promote` | master repo (init'd) | copy live → bundle for every mapped file, bump VERSION |
| `/init-project update` | initialized project | pull newer portable files bundle → live, 3-way safe (manifest ↔ live ↔ bundle); skip conflicts (workflow below) |

## workflow (init — new project)
0. Create the agent workspace `.agent-workspace/` at the project root — everything the agent owns lives here, nothing of it under `docs/` (`doc-organization.md §11`). Subfolders are created by the step that fills them: `guide/` (step 3), `lessons/` (step 4), `tasks/` and `worktrees/` (first use at runtime). Add `.agent-workspace/tasks/` and `.agent-workspace/worktrees/` to `.gitignore` — task state and throwaway checkouts are never committed (`orchestration-policy.md §5`). `tooling/` is filled by step 3 — the genome ships its own gates there (`.agent-workspace/tooling/`); a project keeps its own scripts beside them, grouped one subfolder per purpose, and those never enter the bundle.
1. Scan project: detect stack + optional modules per `## module matrix` signal column. Output: proposed module set + discovered slot values.
2. Interview: confirm proposed module set; ask slots not scannable (dev ports in use, scope ownership, doc language, the decision-journal per-shard cap, always-loaded budget — offer 600 lines as the default; the genome's own floor is the figure recorded in the placement-data row of the router this init renders). Unanswerable slot → leave TODO marker, never invent a value; module uncertain → skip it.
3. Copy `portable/` verbatim: `portable/rules/*` → `.claude/rules/`; `portable/guide/*` → `.agent-workspace/guide/general/`; `portable/roles/*` → `.agent-workspace/guide/roles/`; `portable/tooling/*` → `.agent-workspace/tooling/`; `portable/skills/*` → `.claude/skills/`; `portable/agents/*` → `.claude/agents/`.
4. Render templates: fill `{{slots}}` from interview into `CLAUDE.md`, `.agent-workspace/guide/index.md`, `docs/index.md`; missing slot → keep TODO marker. `lessons/index.md.tpl` carries no slot — copy it verbatim to `.agent-workspace/lessons/index.md`, seeding the lesson store empty (`lesson-capture.md` §5); its §1 is the only router a lesson store is ever registered in, and `CLAUDE.md.tpl` already carries the one line that reaches it — never add a per-store trigger. `roles/index.md.tpl` carries no slot either — copy it verbatim to `.agent-workspace/guide/roles/index.md`; its §1 holds the genome roles and its §1a is the empty table a project adds its own roles to (`role-selection.md` §5). `decisions/index.md.tpl` renders to `.agent-workspace/decisions/index.md`, seeding the journal with a router and no entry (`decision-journal.md` §5: an entry is written when a decision is made, never upfront); its only slot, the per-shard entry ceiling the gate reads — unanswerable → TODO marker. `wiki/index.md.tpl` renders to `.agent-workspace/wiki/index.md` ONLY when the wiki module is confirmed (see `## module matrix`), seeding the tier with a router and no cluster (`wiki-tier.md` §2: a cluster is created when an investigation first touches its lookup topic, never upfront). Its slots are the extension points `wiki-tier.md` §7 requires the project to declare — the locator root and the claim-class table are the two the interview must reach; unanswerable → TODO marker, never an invented value. Module not confirmed → the template is not rendered and no wiki trigger is written; the rule still deploys.
   - **A rendered target that already exists is MERGED, never overwritten.** A project with its own `CLAUDE.md` is carrying rules nothing else records — release steps, ownership, domain guardrails — and rendering over them deletes the only copy. Carry every existing rule into the project-rule slots, then add the template's; the deployed standard is additive to that project, not a replacement for it. A category the project has no work products for (`docs/`) is not rendered at all — an empty router is scaffolding, not content; record the `.tpl` sha in the manifest anyway so `update` warns only on a real template change.
5. Generate optional rules: for each confirmed optional module, write a project-fitted rule into `.agent-workspace/guide/general/` per `rule-writing-standards`, and append its trigger line to `CLAUDE.md` in the same step — no hardcoded template.
6. Write manifest `.claude/init-manifest.json`: `{ version, deployedAt, files:[{path,sha256}], templates:[{path,sha256}], modules:[...] }` (provenance; `files[]` read by `update` for 3-way drift detection — keep sha256 accurate; `templates[]` records the `.tpl` sha each rendered file was built from — `path` = template path relative to `templates/` e.g. `CLAUDE.md.tpl`, used by `update` to WARN when a template changed since deploy). Generate it — `node <plugin>/scripts/init-manifest.mjs --project <project-root> --modules <list>` — never hand-write the hashes: a wrong sha256 does not fail here, it surfaces later as a phantom CONFLICT or a silent overwrite of a local edit.
7. Verify: every deployed file is at the correct tier; every rule/guide file carries `scope:` frontmatter; CLAUDE.md within token budget; every behavior-affecting on-demand file has a trigger line or router entry (reachability, file→trigger); every `MUST Read` trigger in CLAUDE.md resolves to a deployed file (reachability, trigger→file — no dead trigger); `.agent-workspace/lessons/index.md` exists and CLAUDE.md carries the lookup line pointing at it (without it every future lesson store is born dead); `.agent-workspace/guide/roles/index.md` exists, CLAUDE.md carries the role lookup line pointing at it, and every role name in that index (primary and checking cells alike) resolves to a `.md` file of the same name under `.agent-workspace/guide/roles/` — the router is rendered by step 4 and the role files are copied by step 3, independently, so a router existing alone does not prove the role files landed; the deployed gates run green from the project root — `python .agent-workspace/tooling/verify_lesson_router.py`, `python .agent-workspace/tooling/verify_role_files.py`, `python .agent-workspace/tooling/verify_decision_log.py`, `python .agent-workspace/tooling/verify_wiki.py` and each paired `test_*.py`, all exit 0 (`verify_wiki.py` on a project without the wiki module reports `clusters: 0` and passes; it fails only if the router is missing while clusters exist, or `source_root` is undeclared) (running them is the only proof the copied gate matches the copied artifacts; a gate present but red means the deploy is incomplete, not that the gate is wrong); no unrendered `{{slot}}` remains except intentional TODO markers. Done = checklist passes + manifest written.

## bundle ↔ live map (check / promote — master repo; update — initialized project)
| bundle path | live path |
|---|---|
| `portable/rules/*` | `.claude/rules/*` |
| `portable/guide/*` | `.agent-workspace/guide/general/*` |
| `portable/roles/*` | `.agent-workspace/guide/roles/*` — `index.md` excluded: it is rendered from `templates/roles/index.md.tpl` and is `scope: project` |
| `portable/tooling/*` | `.agent-workspace/tooling/*` |
| `portable/skills/*` | `.claude/skills/*` |
| `portable/agents/*` | `.claude/agents/*` |

- **Precondition:** the master repo must itself be init'd — it is *deployed instance #1* (`doc-organization.md §4`), and without a live tier `check` has nothing to compare and `promote` has nothing to copy from. A master repo with no `.claude/rules/` runs `/init-project` on itself first (step 4's merge rule applies to its existing `CLAUDE.md`). Until then the bundle is edited directly and no mechanism can detect that it drifted.
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
6. Verify reachability of every ADD — mandatory, and the reason step 4's WARN is not enough. `update` writes the portable file but never the trigger line or router entry that reaches it, so a newly-added guide lands as dead content: present in the project, read by nobody. For each ADD, confirm the live `CLAUDE.md` carries its trigger (when the file is behavior-affecting per `doc-organization.md` §10 interception test) AND the live `.agent-workspace/guide/index.md` carries its router entry; write whichever is missing, and create any directory the new file's guidance assumes (e.g. a store folder seeded from `templates/`). Done = every ADD reachable by trigger or router, both directions resolving.

## module matrix
| module | includes | deploy when | scan signal (examples, not exhaustive) |
|---|---|---|---|
| core | `portable/*` (all 4 groups) + 4 templates | always | — |
| runtime | `.agent-workspace/guide/general/local-runtime.md` + CLAUDE.md trigger (skill writes per scan, step 5) | project self-runs a dev server | `package.json` dev/start scripts, `launchSettings.json`, vite/next/dotnet/django/cargo config |
| e2e | `.agent-workspace/guide/general/<tool>.md` (named after detected tool) + CLAUDE.md trigger (step 5) | project has E2E browser tests | playwright/cypress/selenium dep, `e2e/` folder, E2E config |
| wiki | `.agent-workspace/wiki/index.md` rendered from `wiki/index.md.tpl` + CLAUDE.md trigger (step 5) | the project investigates SUBJECT MATERIAL it does not own — a legacy codebase, a customer's system, a body of source documents — and needs established claims written back. The rule `wiki-tier.md` ships in core either way: it is `paths:`-scoped to `.agent-workspace/wiki/**`, so it costs nothing while the tier is absent | a large read-only source tree the project analyses but does not build; an existing investigation/analysis workflow; the user confirms there is external material to establish facts about |

- Optional module deploys only when scan confirms OR user confirms at interview — uncertain → skip.
- Git: minimal guardrail (commit only on request, never push) ships in `CLAUDE.md.tpl`; detailed policy is `scope: project` — project writes `.agent-workspace/guide/general/git.md` on demand, adding its trigger line in the same commit (reachability — never a trigger pointing at a missing file).
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
