---
scope: project
---

# Lessons — verifying a change to always-loaded context

<critical>
scope: about to check whether a change to `CLAUDE.md` or `.claude/rules/*` actually changes agent behaviour — how to build a probe that measures the rule instead of the session.
phase: building-gate
</critical>

### Verify an always-loaded rule change in a fresh session — a subagent of the current session reads a frozen copy

- signal — just edited `CLAUDE.md` / a `.claude/rules/*.md`, and the next move is "spawn an agent and see whether it obeys"
- ❌ spawned a subagent in the same session as the edit; it inherits the context snapshot taken at session start, so it saw the pre-edit file and skipped the new rule. The negative result looked like an adherence failure of the rule
- ✅ edit an always-loaded file → verify statically this session (lint, wiring, wording); test behaviour only in a session started after the edit
- evidence — probe agent reported 18 bullets under `## ALWAYS` and `enable hooks after clone` as the first; `awk` over `CLAUDE.md` on disk counted 19 with the new trigger first in its block
- seen — 1

### Check retained workflow obligations while evaluating a prose rewrite

- signal — A rewrite preserves the apparent meaning of a workflow instruction, and static checks pass.
- ❌ Treating source equivalence and passing structural gates as sufficient evidence that the rewritten instruction remains effective leaves a behavioral gap.
- ✅ In fresh sessions, inspect the required actions as well as the prose produced. If an action is skipped, test an explicit description of the operation and its scope before changing unrelated instructions. Keep pre-fix samples and report the repair separately.
- evidence — The September 2026 genome comparison found no router reads in six sessions with the initial rewritten template. The original read both routers in six sessions. Two subsequent conversation probes read both after the template explicitly named file reading and included conversational and writing tasks. See `docs/genome/so-sanh-dau-ra-claude.md` for the full results and their limits.
- seen — 1

### Ask a probe agent what is IN its context before reading anything into what it did

- signal — using a subagent's behaviour as evidence about a rule, prompt, or file the agent was supposed to act on
- ❌ inferred from the tool-call log alone that the rule failed to fire — the log cannot distinguish "rule ignored" from "rule absent"
- ✅ probe agent → ask it to quote the governing text from its context first; only then read its actions as evidence
- evidence — the second audit question ("does your `## ALWAYS` contain this line?") is what turned a false negative into a measurement
- seen — 1
