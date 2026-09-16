---
class: choice
subject: docs/genome/ke-hoach-ho-tro-codex.md
anchor: User clarification on 2026-09-16 that Claude Code and Codex must work through the same project `.agent-workspace/`.
supersedes: 2026-09-16-choice-independent-codex-genome-plan
---

decided: Maintain independent Claude Code and Codex source distributions, but deploy both adapters against one project genome under `.agent-workspace/`. Keep harness-specific instructions, configuration and deployment bookkeeping separate. A second adapter reuses a complete existing core genome instead of creating a harness namespace or taking ownership of shared files; it may seed an optional shared router that is absent and then owns only that added file.

because: The genome represents the project's working behavior and accumulated knowledge. Splitting guide, lesson, decision, wiki and task state by agent would allow the agents to learn different lessons and follow different processes, which defeats the intended mechanism.

rejected: A `.agent-workspace/claude/` and `.agent-workspace/codex/` split; generating one harness distribution from the other; or treating independent source maintenance as a requirement for separate deployed records.
