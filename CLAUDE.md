# claude-doc-genome

This repository is the source of the Claude Code documentation genome, distributed as the `init-project` skill. It holds the bundle, its deployment scripts and the documents that explain them. It is not a deployed project: it has no instance of the genome of its own. Real projects deploy the bundle and later feed their working experience back into it.

The default language for conversation in this project is Vietnamese, unless the user requests another language. The bundle and public repository documentation are authored in English; the design, rewrite plan and implementation report under `docs/genome/` are in Vietnamese.

## Authorization

Do not commit or push unless the user has requested that action. Use the authorization already given in the conversation; ask for clarification only when the intended action or its scope remains unresolved.

## Sources

The bundle under `skills/init-project/` is the only authored source. Edit it directly; there is no live copy to edit first or to synchronize from.

| Area | Location |
|---|---|
| Portable rules, guides, roles template and genome tools | `skills/init-project/portable/` |
| Project index templates | `skills/init-project/templates/` |
| Initialization, update and promotion workflow | `skills/init-project/SKILL.md` |
| Deployment, version and check scripts | `scripts/`, `.githooks/`, `.github/workflows/` |
| Repository documentation | `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `docs/` |

Keep project-specific values out of the portable content. When a file is added, moved, renamed or removed, update `SKILL.md`, the templates and every reference to it in the same change.

The canonical bundle version is `skills/init-project/VERSION`. Use `node scripts/sync-version.mjs set X.Y.Z` to change it; the script updates all version mirrors. Follow `CONTRIBUTING.md` for release work only when a release has been authorized.

## Verification

Enable the repository hooks after cloning with `git config core.hooksPath .githooks`. Before handing off a change, run:

- `node scripts/sync-version.mjs check`
- `node scripts/doc-lint.mjs --bundle`
- `node --test scripts/test-deployment.mjs`
- `node scripts/test-bundle-tools.mjs`

Node.js runs the repository scripts; the genome tools use Python and its standard library. Record changes under Unreleased in `CHANGELOG.md`. Place working files without a specified destination under `.agent-workspace/tasks/<task-slug>/`, which Git ignores.
