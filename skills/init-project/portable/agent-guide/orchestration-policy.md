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

- ad-hoc task in a free session that is **multi-step OR multi-agent** (review+fix, plan+implement, fan-out) → apply §2–§4.
- single-shot / trivial mechanical task (one file, no delegation benefit) → skip; do it inline.
- task driven by a skill → out of scope (skill's own design governs).

## §2 Orchestrate vs execute (model split)

<rules section="ALWAYS">
- main high-capability model = Orchestrator: scope control, planning, reasoning over artifacts, dispatch, verify-gate, synthesis.
- delegate execution (Edit/Write) to a cheaper/faster implementer model **by default**.
- hard-reasoning execution (subtle business rule, defect-prone pattern) → escalate to the orchestrator model or higher effort, not forced cheap-model + multi-round fixup.
</rules>

<rules section="NEVER">
- block a trivial inline edit behind a subagent when spawn overhead > benefit (re-read cost, latency).
</rules>

Decision: delegate is the default; inline and escalate are the two escape hatches.

<example type="delegation">
input: apply a multi-file change across several modules
✅ dispatch an implementer agent with the plan; orchestrator gates verify
❌ orchestrator edits all files itself
</example>

<example type="escape_hatch_inline">
input: rename one mistyped identifier in a file already in context
✅ orchestrator edits inline — subagent spawn + re-read costs more than the edit
❌ spawn an implementer agent to change one line
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
- store in a gitignored scratch location in the MAIN repo (survives subagent boundary, worktree cleanup, context compaction).
- plan file = single source of truth; update it when the plan changes (stale plan worse than none).
- plan must be self-contained for the executor: acceptance criteria + targets + per-task effort — not vague prose.
- subagents + verify rounds read state from the file, not from orchestrator memory.
</rules>

<rules section="NEVER">
- write transient plan/state into long-term doc storage (clutter, gets committed).
- store the plan inside a throwaway worktree (lost on cleanup).
</rules>

<example type="persistence">
input: orchestrate a 2-step review→fix over many findings
✅ write the plan to a gitignored scratch file; agents + verify read it back
❌ keep the finding→agent→effort mapping only in conversation context
</example>

<critical_recap>
1. orchestrator plans/dispatches; implementer model executes by default — inline trivial, escalate hard-reasoning.
2. effort by difficulty, not scope.
3. plan → durable gitignored file, single source of truth, self-contained; never pure-context, never long-term doc storage.
</critical_recap>
