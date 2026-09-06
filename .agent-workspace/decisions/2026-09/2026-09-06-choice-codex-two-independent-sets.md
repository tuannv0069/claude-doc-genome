---
class: choice
subject: .agent-workspace/guide/general/harness-adapter.md
supersedes: 2026-09-06-choice-codex-one-source-two-renderers
anchor: .agent-workspace/tasks/codex-native-independence/plan.md · 202ee4e
---
- decided: each platform gets a complete set of its own — no file of one names a path of the other; only `.agent-workspace/**` is shared, because it belongs to neither
- because: the superseded design made every Codex deployment depend on a `.claude/` directory it never loads, and turned an auto-load guarantee into a file the agent had to choose to open
- rejected: keep the pointer model and accept the coupling — it is cheaper to maintain and wrong at every deployment that installs one platform, which is the normal case
