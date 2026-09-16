# Contributing

## Report a problem

Describe the command or workflow you used, the expected behavior and the result you observed. Include the relevant error or verification output and enough project context to reproduce the problem without exposing private information.

## Work in the correct source

For the Claude genome, portable rules are authored in `.claude/rules/`, guides and roles in `.agent-workspace/guide/`, and verification tools in `.agent-workspace/tooling/`. Edit the live file first, verify it, then synchronize it into the corresponding group under `skills/init-project/portable/`.

The Claude bundle and live copy are intentionally separate deployment copies. Project-owned additions are not automatically portable. Check that a candidate contains reusable instructions rather than project-specific values before promoting it.

For the Codex distribution, edit `skills/init-codex-genome/` directly. That self-contained skill is its only authored source. Development tests, packaging support and documentation live in `tests/codex/`, `scripts/codex/` and `docs/codex/`. Follow [the Codex contribution guide](docs/codex/contributing.md) for its commands and independent version lifecycle. Independence applies to the source distribution; deployed Claude Code and Codex adapters use the same project `.agent-workspace/`.

Edit `skills/init-project/SKILL.md`, the templates, repository scripts and repository documentation directly. A rendered project index must not be copied back into a template with its project values still present.

When removing or renaming content, update the routers, triggers, section references and migration behavior in the same change. Historical decisions remain available as records; active guidance should describe the current workflow.

## Verify a change

Enable the local hook after cloning:

```sh
git config core.hooksPath .githooks
```

The hook checks Claude version synchronization and the documentation network. Run the tests for any changed tool as well. Before handing off a Claude portable change, compare every affected live file with its bundle copy; a clean updater report is useful evidence but does not replace checking routing and project-owned templates. Run the separate Codex checks when its skill or support files change.

For changes to deployment behavior, use temporary project fixtures to check additions, updates, retirement, local edits and template handling. Do not use another person's working project as a test fixture. For changes to guidance, read the complete result and verify that its required behavior remains clear and reachable.

Record user-visible changes in the Unreleased section of `CHANGELOG.md`. A pull request should describe the problem, the resulting behavior and the validation actually performed.

## Prepare and publish a release

The release procedure below is for Claude. Codex has its own version and packaging commands in its contribution guide.

Version changes follow the compatibility of the bundle. Removing or renaming a portable contract, or changing a template slot contract, requires a major version. Compatible additions require a minor version. Wording corrections that preserve those contracts require a patch version.

The canonical version is `skills/init-project/VERSION`. Use the synchronizer when preparing a release:

```sh
node scripts/sync-version.mjs set X.Y.Z
node scripts/sync-version.mjs check
```

The synchronizer updates the plugin metadata, marketplace metadata and README badge. Do not edit the version mirrors independently. Version preparation does not publish the change.

After the maintainer authorizes a release and the checks pass, move the relevant Unreleased notes into a dated version section, commit the release, create its `vX.Y.Z` tag, push the authorized branch and tag, and publish the corresponding GitHub Release. Ensure the changelog's release link uses that tag. Do not commit, push or publish merely because a wording or maintenance task was requested.

## Design responsibilities

Keep one source for each substantive workflow requirement and maintain stable references to it. Keep project data out of portable content. The project or the workflow that owns a deliverable also owns any requirements specific to that deliverable.

Contributions are licensed under the repository's [MIT License](LICENSE).
