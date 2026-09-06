---
class: scope
subject: scripts/doc-lint.mjs
anchor: .agent-workspace/tasks/codex-branch/plan.md · f088ef0
---
- decided: doc-lint gets no AGENTS.md checks — not the trigger-resolution corpus, not the byte cap
- because: AGENTS.md is regenerated from the live rule directory, so its trigger paths cannot go dead, and the byte cap already has an owner in `render_codex.py --check`
- rejected: add them anyway for symmetry — both checks would be unfailable, and doc-lint's own scope note says a linter reporting non-defects gets ignored
