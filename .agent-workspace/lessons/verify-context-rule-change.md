---
scope: project
---

# Lessons — verifying a change to always-loaded context

Store for: about to check whether a change to `CLAUDE.md` or `.claude/rules/*` actually changes agent behaviour.

### Verify an always-loaded rule change in a fresh session — a subagent of the current session reads a frozen copy

- signal — just edited `CLAUDE.md` / a `.claude/rules/*.md`, and the next move is "spawn an agent and see whether it obeys"
- ❌ spawned a subagent in the same session as the edit; it inherits the context snapshot taken at session start, so it saw the pre-edit file and skipped the new rule. The negative result looked like an adherence failure of the rule
- ✅ edit an always-loaded file → verify statically this session (lint, wiring, wording); test behaviour only in a session started after the edit
- evidence — probe agent reported 18 bullets under `## ALWAYS` and `enable hooks after clone` as the first; `awk` over `CLAUDE.md` on disk counted 19 with the new trigger first in its block
- seen — 1

### Ask a probe agent what is IN its context before reading anything into what it did

- signal — using a subagent's behaviour as evidence about a rule, prompt, or file the agent was supposed to act on
- ❌ inferred from the tool-call log alone that the rule failed to fire — the log cannot distinguish "rule ignored" from "rule absent"
- ✅ probe agent → ask it to quote the governing text from its context first; only then read its actions as evidence
- evidence — the second audit question ("does your `## ALWAYS` contain this line?") is what turned a false negative into a measurement
- seen — 1
