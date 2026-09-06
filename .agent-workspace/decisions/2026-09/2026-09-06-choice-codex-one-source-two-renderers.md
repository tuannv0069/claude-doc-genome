---
class: choice
subject: .agent-workspace/guide/general/harness-adapter.md
anchor: .agent-workspace/tasks/codex-branch/plan.md · f088ef0
---
- decided: one genome body with a generated binding surface per harness — the live Claude Code tier is the source, the Codex surface is rendered from it by `render_codex.py`
- because: the body is 90% of the genome and forking it makes every future rule edit a two-file edit whose only sync mechanism is memory; `doc-organization.md` §4 admits packaged-beside-source duplication only when a machine check separates them
- rejected: two full parallel bundles (`portable-claude/` + `portable-codex/`) with a parity gate — the user's literal ask; it buys per-harness fidelity the slot map showed nothing needs, at a permanent 2x edit cost and a MAJOR bundle-layout break
