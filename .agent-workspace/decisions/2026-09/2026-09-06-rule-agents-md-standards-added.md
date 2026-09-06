---
class: rule
subject: .claude/rules/agents-md-standards.md
anchor: learn.chatgpt.com/docs/agent-configuration/agents-md · f088ef0
---
- decided: `AGENTS.md` gets its own path-scoped standard holding ONLY the Codex deltas — generated-not-written, the 32 KiB byte budget, no always-loaded tier, `.codex/rules/` is not a rule tier
- because: the wording, density and trigger laws are identical to CLAUDE.md's, and restating them would put the same law in two source-of-truth files
- rejected: widen `claude-md-standards.md` to cover both targets — its `paths:` is `**/CLAUDE.md`, and renaming a `scope: portable` file is a MAJOR break for a delta this small
