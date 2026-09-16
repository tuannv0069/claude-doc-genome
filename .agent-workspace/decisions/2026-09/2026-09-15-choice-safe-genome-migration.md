---
class: choice
subject: scripts/update.mjs
anchor: docs/genome/thiet-ke-goc.md §5 and deployment fixture evidence from this rewrite.
---
- decided: Manage all six Claude portable groups and all seven template sources through one mapping. Retire only unchanged manifest-owned portable files, preserve conflicts, and require acknowledgement of completed manual template migration before recording a completed new version.
- because: The old mapping omitted roles and tooling, left retired policies installed and could record an upgraded version despite unresolved changes. File ownership and hashes provide an auditable basis for safe automated changes.
- rejected: Rebuilding the manifest from arbitrary local content or blindly deleting files absent from the new bundle would erase provenance and could discard project work.
