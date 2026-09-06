---
class: choice
subject: .agent-workspace/guide/general/harness-adapter.md
anchor: .agent-workspace/tasks/codex-branch/plan.md · f088ef0
---
- decided: `harness-adapter.md` gets a router entry only — no CLAUDE.md trigger line
- because: the interception test fails, and it fails for a concrete reason — the three NEVER lines added to CLAUDE.md already fire at the decision point, and `render_codex.py --check` in the pre-commit hook catches the miss mechanically
- rejected: an always-loaded trigger — it would spend budget on a guide only a harness-design task reads, and that task self-signals
