---
class: scope
subject: .codex/rules/codex-agents-standards.md
anchor: .agent-workspace/tooling/render_codex.py · 202ee4e
---
- decided: `subagent-standards.md` and `claude-md-standards.md` are not mirrored into the Codex set; the Codex set authors `codex-agents-standards.md` and `agents-md-standards.md` instead
- because: both describe a mechanism the other platform does not have — a markdown agent file spawned by that platform's own tool, and a root index of a different name; a path rewrite cannot make a wrong mechanism right
- rejected: mirror them with rewritten paths — it produces prose that reads as authoritative and describes a tool the reader does not have
