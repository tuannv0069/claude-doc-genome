---
scope: project
---

# Lessons from planning products for different agent hosts

<critical>
scope: Planning ownership and maintenance when adapting the genome to another agent host.
phase: orchestrating
</critical>

## Distinguish shared intent from shared source ownership

- signal: A second agent host needs the same overall working principles but has different configuration mechanisms.
- ❌ The initial plan treated a shared source of rules as the preferred architecture before establishing the user's maintenance preference. Reducing duplicate work appeared useful, but it imposed coupling the user did not want.
- ✅ Treat independent products and a common source as separate ownership choices. When the user chooses independence, preserve the common intent through separately authored and tested instructions; do not reintroduce a generator or automatic synchronization under another name.
- evidence: On 2026-09-16 the user explicitly requested two independent genomes and accepted updating two places. The revised design is in `docs/genome/ke-hoach-ho-tro-codex.md`.
- seen: 1

## Do not inherit a second authoring tree merely because the previous product has one

When implementing the independent Codex product, I retained a live instruction tree outside the self-contained initialization skill, copied the same portable instructions and tool into its bundle, and added check/promote machinery between them. This appeared useful because the source project could use the genome while developing it, following the established Claude maintenance model.

The user then questioned why copying the skill was sufficient for deployment while the source repository retained another complete tree. Inspection of `codex/CONTRIBUTING.md` and the tool's `maintenance` function confirmed that the extra tree is an authoring and self-use choice, not a dependency required by target projects. My earlier deployment explanation did not distinguish that choice from the skill's self-contained payload.

For a product centered on a portable initialization skill, evaluate keeping its payload as the single authored source. Test deployed instances in temporary projects, and justify any persistent self-use copy separately. Tests, maintenance tools and development documentation may still be necessary without duplicating the genome's substantive instructions. This is a proposed simplification for the current product, not a claim that the existing paths have already changed. This failure has been observed once.

During implementation, the user further clarified that even the development support should use the repository's ordinary tests, scripts and docs areas rather than preserve a separate product directory at the root. The resulting layout puts those responsibilities in tests/codex/, scripts/codex/ and docs/codex/, while the genome itself remains entirely in the skill. This clarification resolves repository organization without introducing shared rule ownership between products.

## Separate source ownership from deployed collaboration state

- signal: Two agent harnesses need independently maintained configuration while the user expects them to learn from the same project history and follow the same working process.
- ❌ I interpreted “two independent genomes” as both independent source distributions and separate deployed namespaces. That created a second guide, lesson, decision, wiki and task tree, so switching agents could change behavior and lose accumulated context.
- ✅ Decide source ownership and deployed collaboration topology separately. Keep harness packages and manifests independent, but place project-level guidance and records in the shared `.agent-workspace/`. A later adapter reuses the complete workspace and owns only the adapter files it installs.
- evidence: On 2026-09-16 the user explicitly defined `.agent-workspace/` as the common genome for Claude Code and Codex and rejected `.agent-workspace/codex/`.
- seen: 1
