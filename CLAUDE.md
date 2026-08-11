# claude-doc-genome

Claude Code documentation genome — portable rules, guides, skills, agents, and templates for the `claude-doc-genome` plugin. This repo is also **deployed instance #1** of its own standard (`doc-organization.md §4`).

## stack
- Node.js (scripts: `sync-version.mjs`, `update.mjs`, `doc-lint.mjs`, `init-manifest.mjs`)
- Claude Code plugin (`.claude-plugin/`)
- SemVer versioning via `skills/init-project/VERSION` (canonical)

## NEVER
- commit or push without explicit user request (`commit`, `push`, `/commit`)
- edit `skills/init-project/portable/**` directly — edit the live tier, then `/init-project promote` (see scope table)
- add project-specific names, paths, or values to `skills/init-project/portable/` (portable-pure law)
- renumber `§ID` in `scope: portable` files (append-only; retired sections keep their number)
- push without completing the full release workflow (version bump + tag + GitHub Release)
- edit VERSION or version mirrors manually — use `node scripts/sync-version.mjs set X.Y.Z`
- commit with version drift (pre-commit hook enforces `sync-version.mjs check`)
- commit with a broken doc network — dead trigger, orphan guide, dead `§ID` (pre-commit hook enforces `doc-lint.mjs`)
- inline substantive rule in agent/skill/catalog — reference source-of-truth §ID; see `.claude/rules/doc-organization.md`
- soften disagreement into "you could also consider" — say so directly
- change position from user pressure alone — require new info/reasoning
- place a guide under `docs/` or a work product under `.agent-workspace/` — see `.claude/rules/doc-organization.md §11`

## ALWAYS
- enable hooks after clone: `git config core.hooksPath .githooks`
- change a portable rule/guide/skill/agent → edit the **live** copy, run `/init-project check` to see the drift, then `/init-project promote` (live → bundle + version bump) in the same change set
- release workflow (ALL 5 steps mandatory, in order):
  1. `node scripts/sync-version.mjs set <X.Y.Z>` — bumps VERSION + mirrors (plugin.json, marketplace.json, README badge)
  2. commit: `release: vX.Y.Z` — list changed files in body
  3. `git tag vX.Y.Z`
  4. `git push origin main --tags`
  5. `gh release create vX.Y.Z --title "vX.Y.Z" --notes "<changelog>"` — GitHub Release mandatory, not optional
- start any artifact task (write / edit / review / investigate) → MUST Read `.agent-workspace/lessons/index.md` §1 first → row matches the work about to be done → read that store; no row matches → skip, lookup done
- new doc content → place via `.claude/rules/doc-organization.md §8.3` decision tree
- add/rename/move/delete a content file → update every linking node (router, trigger, §ID pointer) in the same commit
- debug / root cause / RCA / "why" / "root cause" → MUST Read `.agent-workspace/guide/general/five-why.md` first
- run a review (audit / review / code review / inspect / vet / find bug(s) / build a checklist, incl. running against an existing checklist) (free-form, not a skill-owned flow) → MUST Read `.agent-workspace/guide/general/review-checklist-method.md` first — its §7 picks the instrument (a dedicated review skill usually wins); §1–§6 is the fallback for a non-code artifact, a non-diff scope, or an absence hunt
- write or format a bug report for findings already determined, no review to run (free-form, not a skill-owned flow) → MUST Read `.agent-workspace/guide/general/bug-report-format.md`
- fix a bug / apply a fix / patch a defect in any artifact — code, docs, rule, config (free-form, not a skill-owned flow) → MUST Read `.agent-workspace/guide/general/fix-impact-analysis.md` first (scope the blast radius before editing)
- user corrects the method / rejects the output / "why did you" · "that's not right" · "it should be" → MUST Read `.agent-workspace/guide/general/lesson-capture.md` (record it in that same turn, into `.agent-workspace/lessons/<work-type>.md` — not harness memory, not a guide file)
- write/edit mermaid block in .md → MUST Read `.agent-workspace/guide/general/mermaid.md` before emit
- fan-out Edit/Write across >3 files / dispatch subagent for execution (no skill owns flow) → MUST Read `.agent-workspace/guide/general/orchestration-policy.md` first (delegate Edit/Write to implementer model, inline ≤3 files or warm context, escalate hard-reasoning; persist plan under `.agent-workspace/tasks/<task-slug>/<scope>/`); research/grep/read/analyze = orchestrator inline; skill-driven flow excluded
- agent creates a working file (script/dump/log/json/screenshot) with no user- or skill-specified destination → write under `.agent-workspace/tasks/<task-slug>/`; never repo root (layout: `.agent-workspace/guide/general/orchestration-policy.md` §4)
- research / investigation passes its 3rd file read or search, or dispatches an agent, with no file to change → MUST Read `.agent-workspace/guide/general/orchestration-policy.md` §6 — persist findings to `.agent-workspace/tasks/<task-slug>/` while working, never only in the reply
- create / use / clean up isolated git worktree → MUST Read `.agent-workspace/guide/general/worktree.md` first (path convention, symlink non-tracked config, pass realpath to child agents, cleanup only after verified push)
- skill writes its working files (plan, research notes, run state) to its own default path → redirect them to `.agent-workspace/tasks/<task-slug>/`; only the finished deliverable goes to `docs/` (full rule: `.agent-workspace/guide/general/orchestration-policy.md` §4; boundary: `doc-organization.md §11`)
- design / plan a non-trivial task → run the superpowers brainstorming → writing-plans flow; it supersedes `task-planning.md` §6–§8 per that file's §1 precedence (its §2/§3/§4 governance still applies)
- implement task-by-task under superpowers → superpowers sets WHEN the review checkpoints fire; the instrument still comes from `.agent-workspace/guide/general/review-checklist-method.md` §7, which superpowers does not override. Working files of either flow → `.agent-workspace/tasks/<task-slug>/`

<!-- git: minimal guardrail above (NEVER block) + release workflow (ALWAYS block); detailed policy is scope: project — when the project writes .agent-workspace/guide/general/git.md, add its trigger line here in the same commit (reachability — never a trigger pointing at a missing file) -->

## scope

| area | path | status |
|------|------|--------|
| bundle (genome) | `skills/init-project/portable/` | **promote-only** — never hand-edit; written by `/init-project promote` from the live tier |
| live tier (deployed instance #1) | `.claude/rules/`, `.claude/skills/`, `.claude/agents/`, `.agent-workspace/guide/general/` | implement — this is where a portable rule/guide/skill/agent is edited |
| templates (phenotype) | `skills/init-project/templates/` | implement — `{{slot}}` rendering; not covered by check/promote |
| skill body | `skills/init-project/SKILL.md`, `VERSION` | implement |
| scripts | `scripts/` | implement |
| plugin manifest | `.claude-plugin/**`, README version badge | generated — `sync-version.mjs` owns every version field |
| repo docs | `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE` | implement |
| this project's own phenotype | `CLAUDE.md`, `.agent-workspace/guide/index.md`, `.agent-workspace/lessons/` | implement — rendered once at init, then hand-maintained |

`/init-project check` is the drift gate between the first two rows: a mismatch means live moved and the bundle has not caught up.

## language

| target | language |
|--------|----------|
| frontmatter `scope: portable` | English, any location (overrides rows below) |
| `.claude/**` | English |
| `.agent-workspace/guide/**` | English (portable doc standard) |
| `.agent-workspace/lessons/**` | English — same language as the paired guide, so a promotion is a copy, not a translation (`lesson-capture.md` §3) |
| `skills/**`, `scripts/**` | English |
| `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md` | English (public-facing) |
| conversation default | Vietnamese; switch to English if user does |

## conventions

| domain | rule |
|--------|------|
| commit | conventional commits (`release:`, `feat:`, `fix:`, `chore:`, `docs:`) |
| version bump | MAJOR = breaking (rename/remove portable file), MINOR = additive (new rule/guide/§ID), PATCH = wording/typo |
| changelog | update `## [Unreleased]` in CHANGELOG.md; maintainer cuts version sections at release |
| portable files | `scope: portable` frontmatter, English only, §ID append-only |

## see also

always-loaded (`.claude/rules/`):
- `file-reading.md` — grep vs Read, parallel, subagent
- `critical-thinking.md` — agent decision posture
- `doc-organization.md` — placement decision tree §8.3 + one-source-of-truth §ID + link integrity

on-demand: read `.agent-workspace/guide/index.md` → task → which file.
