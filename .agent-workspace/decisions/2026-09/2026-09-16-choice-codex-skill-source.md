---
class: choice
subject: skills/init-codex-genome/SKILL.md
anchor: The user approved moving init-codex-genome into skills/ after identifying the duplicated Codex live and bundle trees.
---

decided: Author the complete Codex genome directly inside skills/init-codex-genome. Keep its version, portable sources, templates and deployment implementation there. Remove the root codex/ directory entirely, as the user clarified during implementation. Development tests, packaging tools and human documentation belong under tests/codex/, scripts/codex/ and docs/codex/. Validate temporary deployments instead of maintaining a second live authoring tree.

because: Copying the skill already supplies everything needed to initialize another project. The second tree existed for self-use and live-to-bundle promotion, not because Codex deployment required it. Maintaining that tree made source ownership harder to understand and added a synchronization workflow the user did not want. Direct authorship preserves deployment behavior while removing that maintenance cost.

rejected: Keeping the old live tree after moving the skill would change its address without resolving the duplication. Removing tests and packaging support would discard useful checks that do not duplicate the genome. Sharing sources with Claude would contradict the independent-product decision.

The Claude product keeps its own authoring and release mechanism. Existing Codex project destinations and deployment manifests remain compatible; the retired source-root and promotion interfaces were part of the unreleased development layout. No user project, account configuration or publication is changed by this reorganization.
