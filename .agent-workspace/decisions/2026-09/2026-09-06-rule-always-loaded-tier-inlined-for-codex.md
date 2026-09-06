---
class: rule
subject: .agent-workspace/guide/general/harness-adapter.md §3.1
anchor: codex-manual.md:12146,22756 · 202ee4e
---
- decided: the always-loaded tier is carried INSIDE the Codex instruction chain in full, and the size cap ships beside it in a project config
- because: the platform's own list of keys a project config may not override does not contain `project_doc_max_bytes`, so a repo can raise the cap; the earlier NEVER rested on treating the 32 KiB default as fixed
- rejected: deliver the tier through a `SessionStart` hook — it works and stays the fallback, but it needs the project trusted and a limit override to avoid spilling to a temp file
