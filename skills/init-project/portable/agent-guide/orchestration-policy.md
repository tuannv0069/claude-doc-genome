---
scope: portable
---

<critical>
scope: ad-hoc (free-session) multi-step / multi-agent task where the main high-capability model drives the work directly (no skill owns the flow). Skill-driven flows excluded — each skill follows its own design standard.
core: separate orchestration from execution | externalize durable state | model/effort by task fit, not blanket rule.
note: §ID append-only (portable) — never renumber; retired sections keep their number.
</critical>

# Orchestration policy (free session)

## §1 When this applies

- ad-hoc task requiring **multi-file execution** (Edit/Write across files — review+fix, plan+implement, fan-out) → apply §2–§4.
- single-shot / trivial mechanical task (one file, no delegation benefit) → skip; do it inline.
- research / investigation / RCA task (grep + read + reason, no or few edits) → skip; orchestrator does it inline — subagent re-read cost > benefit.
- task driven by a skill → out of scope (skill's own design governs).

## §2 Orchestrate vs execute (model split)

<rules section="ALWAYS">
- main high-capability model = Orchestrator: scope control, planning, reasoning over artifacts, dispatch, verify-gate, synthesis.
- delegate **execution (Edit/Write across multiple files)** to a cheaper/faster implementer model.
- hard-reasoning execution (subtle business rule, defect-prone pattern) → escalate to the orchestrator model or higher effort, not forced cheap-model + multi-round fixup.
- research / investigation (grep + read + analyze) → orchestrator inline; subagent spawn + re-read duplicates context for no gain.
- ≤3 files to edit + context already warm → inline; delegation overhead (spawn + re-read + verify) costs more than the edit.
</rules>

<rules section="NEVER">
- delegate grep/read/analyze to a subagent when orchestrator already has the context (double-read = wasted tokens).
- block a trivial or medium inline edit behind a subagent when spawn overhead > benefit (re-read cost, latency).
</rules>

Decision: delegate for multi-file execution; inline for research and small edits; escalate for hard reasoning.

<example type="delegation">
input: apply a multi-file change across several modules
✅ dispatch an implementer agent with the plan; orchestrator gates verify
❌ orchestrator edits all files itself
</example>

<example type="inline_edit">
input: fix 3 files already in context (< 50 lines of edits total)
✅ orchestrator edits inline — context already warm, no re-read needed
❌ spawn an implementer agent that must re-read all 3 files + their dependencies
</example>

<example type="inline_research">
input: investigate root cause of a recurring bug (grep + read + analyze)
✅ orchestrator greps, reads relevant sections, reasons over findings inline
❌ spawn 3 subagents to search in parallel → each re-reads overlapping files → 200k tokens for 20k worth of work
</example>

<example type="escape_hatch_escalate">
input: implement one subtle, defect-prone piece of business logic
✅ orchestrator implements (or implementer at high effort with a detailed plan)
❌ hand a thin plan to a cheap model → low-capability re-reasoning → multi-round defects
</example>

## §3 Effort selection

<rules section="ALWAYS">
- pick effort by reasoning difficulty; scope is a signal, not the measure.
- high → multi-file / business logic / structural change / subtle logic in few files.
- mid → local, few files, mechanical (rename, format, single isolated fix).
- split multiple agents by difficulty rather than one effort for a mixed batch.
</rules>

<example type="effort_not_scope">
input: a one-file change touching tricky conditional logic
✅ high effort — difficulty is high though scope is small
❌ mid effort because "only one file"
</example>

## §4 State persistence (anti context-loss)

<rules section="ALWAYS">
- write the plan / fix-plan to a durable file before dispatch; never keep it pure-context.
- store under the gitignored scratch root `.agent/tmp/` in the MAIN repo (survives subagent boundary, worktree cleanup, context compaction).
- free-form/ad-hoc path = `.agent/tmp/<task-slug>/<scope>/...` (e.g. `.agent/tmp/review-fix/<id>/plan.json`); structured skill flows follow the orchestrator `{prefix}/sessions/{JOB_KEY}/{SESSION}/` layout.
- plan file = single source of truth; update it when the plan changes (stale plan worse than none).
- plan must be self-contained for the executor: acceptance criteria + targets + per-task effort — not vague prose.
- subagents + verify rounds read state from the file, not from orchestrator memory.
</rules>

<rules section="NEVER">
- write transient plan/state into long-term doc storage (clutter, gets committed).
- scatter scratch outside `.agent/tmp/` (repo root, ad-hoc dirs) — untracked clutter, no single cleanup root.
- store the plan inside a throwaway worktree (lost on cleanup).
</rules>

<example type="persistence">
input: orchestrate a 2-step review→fix over many findings
✅ write the plan to a gitignored scratch file; agents + verify read it back
❌ keep the finding→agent→effort mapping only in conversation context
</example>

<critical_recap>
1. delegate multi-file execution (Edit/Write); research + small edits = inline; hard-reasoning = escalate.
2. effort by difficulty, not scope.
3. plan → durable file under `.agent/tmp/` (free-form: `<task-slug>/<scope>/`), single source of truth, self-contained; never pure-context, never long-term doc storage, never scattered outside `.agent/tmp/`.
</critical_recap>
