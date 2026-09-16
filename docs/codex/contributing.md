# Contributing to the Codex genome

The source is `skills/init-codex-genome/` at the repository root. Edit that skill directly. Development support lives in `tests/codex/`, `scripts/codex/` and `docs/codex/`. There is no separate product directory or live instruction tree at the repository root.

## Source ownership

Within the skill, `bundle/portable/` owns reusable instructions and the deployment tool. `bundle/templates/` owns the initial AGENTS body and project router seeds. `SKILL.md`, `references/` and the small `scripts/genome.py` wrapper own the initialization workflow. The deployment map records destinations and hashes; it does not point to another authored tree.

Review source changes and run the wrapper's `refresh` command to inspect metadata changes. `refresh --apply` updates inventory and hashes, and `check` validates the skill plus a temporary deployment. Neither operation imports improvements from a live project. Bring a useful project improvement back through a reviewed source edit.

Keep the Claude and Codex source distributions independent. A change useful to both needs a separate implementation and verification in each; no generator, shared authoring source or text-equality gate connects them. Their deployed adapters still use one `.agent-workspace/` in a project, so compatibility tests must verify that either agent can read the same guides and records without the second installer overwriting them.

## Guidance and verification

Write understandable instructions with complete grammatical explanations. That is an authoring criterion for the genome, not a runtime style policy for project outputs. Preserve workflow obligations, routes and stable references when changing sources. Use the obligation map to inspect missing responsibilities; a parser test does not prove the assistant reads a guide before acting.

From the repository root:

```text
python skills/init-codex-genome/scripts/genome.py check
python -m unittest discover -s tests/codex
python scripts/codex/sync-version.py check --skill-root skills/init-codex-genome
```

Use temporary projects for deployment tests. Copy only the skill for its standalone portability test. The isolated development suite copies those support directories, the repository license and that one skill without the Claude product. The shared-workspace integration test invokes both products' real tools as external processes and checks that Codex reuses a Claude-created `.agent-workspace/`; production tools never import each other. Windows and Linux results must be reported separately.

## Versions and packaging

`skills/init-codex-genome/VERSION` is canonical. To prepare an authorized version change, run:

```text
python scripts/codex/sync-version.py set X.Y.Z --skill-root skills/init-codex-genome
```

The command updates the Codex map and plugin metadata only. Record changes in this product's changelog. The present 1.0.0 work is unreleased. The shared-workspace correction changes deployed destinations and places Codex bookkeeping under `.codex/`; no earlier Codex release contract needs migration.

Build with `python scripts/codex/package.py --skill-root skills/init-codex-genome --output <new-directory>`. The package copies this skill into the plugin and adds its distribution metadata. Test it outside the source checkout. Publication, commits, pushes and account installation still require the relevant user authorization.
