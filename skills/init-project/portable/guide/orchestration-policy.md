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
- research / investigation / RCA task (grep + read + reason, no or few edits) → skip §2–§3; orchestrator does it inline — subagent re-read cost > benefit. **§6 still applies** — the findings get persisted even though nothing was delegated.
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
- store in the task workspace `.agent-workspace/tasks/<task-slug>/` (durable across subagent boundary, worktree cleanup, context compaction).
- free-form/ad-hoc path = `.agent-workspace/tasks/<task-slug>/<scope>/...` (e.g. `.agent-workspace/tasks/review-fix/<id>/plan.json`); structured skill flows follow the orchestrator `{prefix}/sessions/{JOB_KEY}/{SESSION}/` layout.
- skill writes its working files to its own default path → redirect them to `.agent-workspace/tasks/<task-slug>/`; only the finished deliverable goes to `docs/` (`doc-organization.md §11`).
- plan file = single source of truth; update it when the plan changes (stale plan worse than none).
- plan must be self-contained for the executor: acceptance criteria + targets + per-task effort — not vague prose.
- subagents + verify rounds read state from the file, not from orchestrator memory.
</rules>

<rules section="NEVER">
- write transient plan/state into long-term doc storage (clutter, gets committed).
- scatter working files outside `.agent-workspace/tasks/` (repo root, `docs/`, ad-hoc dirs) — no single home.
- store the plan inside a throwaway worktree (lost on cleanup).
</rules>

<example type="persistence">
input: orchestrate a 2-step review→fix over many findings
✅ write the plan to a file in the task workspace; agents + verify read it back
❌ keep the finding→agent→effort mapping only in conversation context
</example>

## §5 Task-workspace lifecycle

`tasks/` is durable, not permanent: it outlives a subagent, a worktree, and a compaction — not the task. The folder name says what the state is FOR, never how long it lives, so the lifetime is stated here instead of implied by the name.

<rules section="ALWAYS">
- one folder per task, named by task slug — never by date, never shared between tasks.
- project adds `.agent-workspace/tasks/` and `.agent-workspace/worktrees/` to `.gitignore` at init — task state and throwaway checkouts are never committed; `guide/` and `lessons/` are.
- task closes (shipped or abandoned) → delete its folder.
- something in it outlives the task → promote it BEFORE deleting: working technique → `lessons/` (`lesson-capture.md`); fact about the project → `docs/` (`doc-organization.md §11`); law → a guide `§ID`.
</rules>

<rules section="NEVER">
- read a task folder whose task already closed — stale plan presented as current state is worse than no plan.
- keep a folder "in case it is useful later" — that is a promotion decision dodged, not state preserved.
</rules>

<example type="lifecycle">
input: the review→fix task just merged; its folder holds plan.json + a probe script that finally worked
❌ leave the folder — the next agent finds plan.json and works from a plan that already shipped
✅ promote the probe technique into `lessons/`, then delete the folder
</example>

## §6 Research output persistence

Research changes no file, so §1 sends it past §2–§5 — and its product ends up in the reply alone. That is the one place compaction can erase mid-task, and the one place a later session cannot reach at all. The cost is asymmetric: the reading was expensive, retyping it is not possible, re-doing it is.

<rules section="ALWAYS">
- research past its 3rd file read / search, or that dispatched an agent → write the findings to `.agent-workspace/tasks/<task-slug>/` **while working**, not at the end.
- file carries the full artifact; reply carries the conclusion + the path — never the same content twice.
- a finding that outlives the task → promote per §5 before the folder is deleted.
</rules>

<rules section="NEVER">
- defer the write to the end of a long investigation — compaction lands mid-task, and then there is nothing left to write down. That case IS the rule.
- open a file for a single-fact lookup or an answer already complete in one sentence.
</rules>

<example type="research_persistence">
input: compare two subsystems' guides against each other, 6 files read
❌ full comparison in the reply only → the next session starts from zero and pays the 6 reads again
✅ table written to `.agent-workspace/tasks/<task-slug>/findings.md` as it is built; reply gives the verdict and the path
</example>

## §7 Delegating for fresh attention

§2 forbids handing grep/read/analyze to a subagent — that rule is about **throughput**, where the orchestrator already holds the context and a second reader only pays for it twice. This section is the opposite case: the value is precisely that the agent has **not** seen the artifact, the earlier reasoning, or the conclusion someone already reached. Unprimed attention is the deliverable, not extra hands.

<rules section="ALWAYS">
- delegate when the work needs a reader who has not been primed: an absence sweep (what SHOULD be here and is not), an output-audit of a finished product (`task-planning.md` §3.6, doer ≠ checker), adversarial verification of a claim.
- hand it a brief, not a transcript — the prior reasoning is the contamination being avoided.
- the orchestrator having read the artifact is what makes this delegation necessary, not what makes it redundant.
</rules>

<rules section="NEVER">
- cite this section for a search the orchestrator could run itself — that is §2's double-read, and it stays forbidden.
- spawn parallel readers over the same files for speed and call it fresh attention.
</rules>

<example type="fresh_attention">
input: the orchestrator has just written a rule file and needs to know what is missing from it
❌ the author lists the gaps — it cannot see what it never thought of; that blind spot is the defect
✅ a subagent that has read only the requirement set and the file reports what the requirements demand and the file lacks
</example>

<critical_recap>
1. delegate multi-file execution (Edit/Write); research + small edits = inline; hard-reasoning = escalate.
2. effort by difficulty, not scope.
3. plan → durable file under `.agent-workspace/tasks/` (free-form: `<task-slug>/<scope>/`), single source of truth, self-contained; never pure-context, never long-term doc storage, never scattered outside `.agent-workspace/tasks/`.
4. `tasks/` is durable, not permanent — one folder per task, deleted when the task closes (§5).
5. research past its 3rd read persists findings to a file WHILE working (§6) — a reply-only analysis dies at the next compaction.
</critical_recap>
