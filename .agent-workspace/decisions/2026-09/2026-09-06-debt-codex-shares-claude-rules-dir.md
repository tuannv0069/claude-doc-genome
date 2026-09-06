---
class: debt
subject: .agent-workspace/guide/general/harness-adapter.md
anchor: .agent-workspace/tasks/codex-branch/plan.md · f088ef0
---
- decided: the rule tier keeps `.claude/rules/` as its physical home on both harnesses; a Codex-only project therefore carries a `.claude/` directory it never loads
- because: the alternative — a neutral `.agents/rules/` — renames a bundle-map path, breaking `update` for every already-deployed project, and buys only a directory name
- unlocks: a MAJOR release that is already renaming bundle paths, or a Codex-only user reporting the directory as confusing
