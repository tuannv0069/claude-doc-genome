---
class: choice
subject: CLAUDE.md
supersedes: 2026-09-16-choice-independent-codex-genome-plan
anchor: User instruction in the genome repository conversation on 2026-10-12.
---
- decided: The repository again contains only the Claude Code genome, `skills/init-project/`. The Codex distribution (`skills/init-codex-genome/`, `tests/codex/`, `scripts/codex/`, `docs/codex/`, its design and evidence documents and its CI workflow) and the Claude tooling changes that served a shared-workspace Codex deployment were removed by reversing commit ba018cb outside `.agent-workspace/`. This also retires the other 2026-09-16 Codex choices (`choice-codex-skill-source`, `choice-shared-project-genome`, `debt-codex-client-verification`).
- because: The user asked to return the repository to a state with only the Claude Code initialization skill. The lesson-router gate fix of 9fb7a66 stays because it accepts two documented store forms regardless of which adapter wrote them.
- rejected: Keeping the Codex files inactive in the tree would leave a second product to maintain and keep its checks in CI. Rewriting history was not requested; the removed files remain recoverable from commit ba018cb.
