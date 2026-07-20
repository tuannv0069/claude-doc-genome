# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.11.0] - 2026-07-20

### Added

- `agent-guide/bug-report-format.md` gains `§7 explanation clarity — Fix and Cause fields` (`scope: portable`, append-only §ID) — every symbol/formula/identifier in a Fix or Cause must be self-evident or glossed inline; framework/domain jargon glossed on first use; a mechanism fix states the chain (current behavior → why wrong → what changes → why the defect is gone); a condition/formula fix gives the literal expression plus its meaning in prose, verified before writing. `<critical_recap>` gains a line 6 pointing to §7.

## [1.10.0] - 2026-06-30

### Added

- New portable guide `agent-guide/task-planning.md` (`scope: portable`) — plan + verify before executing any artifact-changing task. Two independent axes: scale → depth (small/medium/full; the 7-step §4 scales down to inline for small), task type → form (truth source + acceptance-criteria shape; type never raises depth). Invariant principles §3 (plan-before-execute, auditable not-subjective criteria, doer ≠ checker output-audit, genome-rule attached per sub-task), with §3.2/§3.6 pointing to `critical-thinking.md` rather than restating it. §4 seven steps carry two cross-cutting branches — loop-back (later step exposes earlier defect) and off-ramp ("task should not run" → STOP, propose in-scope alternative); §4.5 plan-review is conditional (full + costly-if-wrong only). Registered: posture trigger in `rules/critical-thinking.md` (names this file), router row in `templates/agent-guide/index.md.tpl`, dependencies in `skills/init-project/SKILL.md`.

### Changed

- `rules/critical-thinking.md` ALWAYS gains one posture line: artifact-changing task → scale rigor to scope; plan before execute; design verification into the plan; verify output by an independent check on the truth source, not the doer's own reasoning → points to the new `agent-guide/task-planning.md`. Generic posture (portable-pure, no project path); the named guide is a genome file deployed by every init, so the pointer never dangles.

## [1.9.0] - 2026-06-25

### Changed

- `agent-guide/orchestration-policy.md` §4 now names the concrete scratch root: free-form/ad-hoc plan/state goes under `.agent/tmp/<task-slug>/<scope>/` (was abstract "gitignored scratch location"), structured skill flows keep the orchestrator `{prefix}/sessions/{JOB_KEY}/{SESSION}/` layout. Added a NEVER against scattering scratch outside `.agent/tmp/`. `templates/CLAUDE.md.tpl` orchestration trigger updated to point at `.agent/tmp/<task-slug>/<scope>/` instead of "durable file". New projects standardize on `.agent/tmp/`; existing deployments unaffected.
- `templates/CLAUDE.md.tpl` ALWAYS gains a standalone always-on guardrail (independent of the orchestration-policy scope gate): any agent-created working file (script/dump/log/json/screenshot) with no user- or skill-specified destination → write under `.agent/tmp/<task-slug>/`, never repo root. Closes the gap where single-shot / research tasks creating scratch files were not covered by orchestration-policy §1.

- Decoupled the audit/review trigger from `bug-report-format.md`: the trigger (`templates/CLAUDE.md.tpl`) now points only to `review-checklist-method.md`, which pulls in `bug-report-format.md` itself at its P5 output step. Rationale: the two are used at different times (method = build the checklist; format = report findings at execution), so eager-loading both on any "create checklist" keyword wasted context (context-economy law). P5 strengthened to a "read it now" pointer; §6 notes the timing.
- Split the two triggers by ACTIVITY (run-a-review vs present-findings), not by has-checklist: any review you RUN — from scratch OR against an existing checklist — routes to `review-checklist-method.md` (existing checklist → skip P0–P2, start at P3; pulls in `bug-report-format.md` at P5). `bug-report-format.md` gets its own trigger ONLY for pure presentation — writing/formatting a report for findings already determined, no review to run. Fixes a gap where "review against an existing checklist" had been routed to the format alone, dropping the method's hunt/confirmation/precision discipline. `review-checklist-method.md` §3 gains an "existing checklist → start at P3" note.

### Added

- New portable guide `agent-guide/fix-impact-analysis.md` (`scope: portable`) — determine the impact scope (blast radius) BEFORE applying a fix, for a bug in any artifact (code / docs / rule / config). Artifact-agnostic dependents (code → callers/contract consumers; docs/rule → `§ID` referrers/links; config → readers); generalizes the doc-organization link-integrity law to all artifacts and moves it before the edit. Phased P0–P4 (validate root → reach probe → blast-radius map → smallest root-fix → verify the radius) with a proportionality gate (cheap mandatory reach-probe self-scales depth; trivial-local → fix directly, shared/contract/owner → full map) and silent-change-on-shared/owner forbidden. Closes the defect-lifecycle's fix step (find → report → **fix-with-impact** → RCA). Registered: trigger in `templates/CLAUDE.md.tpl`, router in `templates/agent-guide/index.md.tpl`, dependencies in `skills/init-project/SKILL.md`.
- New portable guide `agent-guide/review-checklist-method.md` (`scope: portable`) — method for GENERATING and running a bug-finding review checklist for free-form audit/review requests, paired with `bug-report-format.md` (generate vs present). Core: every item is a concrete falsifiable bug hypothesis the AI proves EXISTS, admitted only with a real candidate site (no siteless standing accusations); absence-defect sweep runs FIRST on fresh attention; confirmation is honest about execution limits (`executed`/`traced` may be `present` with an evidence span, `inferred` capped at `suspected`); base-rate prior + steelman precision gate before shipping; severity confirmed only after reachability. Phased P0–P5. AI-calibrated via an adversarial self-audit from the AI-executor viewpoint. Registered: trigger in `templates/CLAUDE.md.tpl` (merged with the audit/review trigger, method-first), router in `templates/agent-guide/index.md.tpl`, dependencies in `skills/init-project/SKILL.md`.
- New portable guide `agent-guide/bug-report-format.md` (`scope: portable`) — standard bug report format for free-form audit / review / find-bug requests not owned by a skill's own output contract. Defines a 4-lobe finding schema (Severity · Location · Problem · Fix, Problem/Fix never merged), optional expansion fields (ID/Cause/Impact/Source/Status, default-off), a 5-severity scale, a verdict-led report skeleton self-scaling between inline (≤2) and table (≥3), and §6 output discipline. Registered: trigger line in `templates/CLAUDE.md.tpl` (ALWAYS), router entry in `templates/agent-guide/index.md.tpl` (§2 general), dependencies list in `skills/init-project/SKILL.md`.

## [1.8.0] - 2026-06-24

### Changed

- `skill-designer` and `skill-writer` are now model-invocable — removed `disable-model-invocation: true` from both SKILL.md frontmatter so the agent can self-invoke them, not only the user via slash command (`skills/init-project/portable/skills/skill-designer/SKILL.md`, `skills/init-project/portable/skills/skill-writer/SKILL.md`).
- Rewrote both skills' `description` to the `skill-md-standards` frontmatter spec: open with "Use when…", add concrete trigger phrases, keep the scope boundary. With model-invocation enabled the description is the matcher, so trigger accuracy now matters.

## [1.7.1] - 2026-06-24

### Changed

- Plugin renamed from `init-project` to `claude-doc-genome` so it no longer displays as `init-project:init-project`; the skill keeps its `/init-project` command (now shown as `claude-doc-genome:init-project`). Install command is now `/plugin install claude-doc-genome@claude-doc-genome` (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`).
- Branding unified to `claude-doc-genome` across `README.md`, `CLAUDE.md`, and `CONTRIBUTING.md` for product/plugin references; skill name, `/init-project` commands, and `skills/init-project/` paths unchanged.

## [1.7.0] - 2026-06-23

### Added

- `update` mode now WARNs when a template (`.tpl`) changed in the bundle since deploy. Rendered phenotype files (`CLAUDE.md`, `index.md`) are still never overwritten — slots hold project-specific values — but the user is told to re-render manually instead of the change being silently dropped (`scripts/update.mjs`).
- `init-manifest.json` records a `templates[]` array (`.tpl` path + sha at deploy time); `update` compares it against the current bundle to detect template drift. Manifests predating this field warn conservatively (`cannot prove unchanged`) until the next init (`skills/init-project/SKILL.md` step 6).

## [1.4.0] - 2026-06-19

### Added

- `update` mode — pull newer portable files into an initialized project via a safe 3-way merge (`manifest ↔ live ↔ bundle`) that never overwrites local edits (`scripts/update.mjs`).
- `scripts/sync-version.mjs` — single-source version sync across `VERSION`, the plugin manifests, and the README badge, with a `check` mode (exits non-zero on drift).
- Drift guards: a `version-sync` CI workflow and a `.githooks/pre-commit` hook.
- `Releasing` guide in `CONTRIBUTING.md` with a SemVer-for-the-bundle policy.

### Changed

- `doc-organization.md`: an on-demand file defaults to a router entry only; an always-loaded trigger is earned via an interception test plus user confirmation in both outcomes.

## [1.3.0] - 2026-06-18

### Added

- Initial public release of the `init-project` Claude Code plugin.
- One-shot deploy of the agent documentation standard: `CLAUDE.md` + `.claude/rules/` (7 portable rules) + `docs/agent-guide/` (4 portable guides).
- Skill-authoring toolkit: `skill-designer`, `skill-writer`, `skill-writer-auditor`, `document-writer`.
- Three modes: `init` (seed a new project), `check` (drift report), `promote` (consolidate live changes into the bundle).
- Templates for `CLAUDE.md`, `agent-guide/index.md`, and `docs/index.md`.

[Unreleased]: https://github.com/tuannv0069/claude-doc-genome/compare/v1.11.0...HEAD
[1.11.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.11.0
[1.10.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.10.0
[1.8.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.8.0
[1.7.1]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.7.1
[1.7.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.7.0
[1.4.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.4.0
[1.3.0]: https://github.com/tuannv0069/claude-doc-genome/releases/tag/v1.3.0
