# Contributing

## Report a problem

Describe the command or workflow you used, the expected behavior and the result you observed. Include the relevant error or verification output and enough project context to reproduce the problem without exposing private information.

## Work in the correct source

This repository is the source of the genome, not a deployed project. Portable rules, guides, the role template and the verification tools are authored directly under `skills/init-project/portable/`; templates under `skills/init-project/templates/`; the workflow in `skills/init-project/SKILL.md`. Repository scripts and documentation are edited directly as well.

Improvements normally originate in a project that has deployed the genome. Judge each candidate for reusable instructions rather than project-specific values before bringing it into the bundle, and never copy a rendered project index back into a template with its project values still present.

When removing or renaming content, update the routers, triggers, section references and migration behavior in the same change. Historical decisions remain available as records; active guidance should describe the current workflow.

## Verify a change

Enable the local hook after cloning:

```sh
git config core.hooksPath .githooks
```

The hook checks version synchronization and the bundle's documentation network (`node scripts/doc-lint.mjs --bundle`). Run `node scripts/test-bundle-tools.mjs` for the genome tools and `node --test scripts/test-deployment.mjs` for deployment behavior. A clean updater report is useful evidence but does not replace checking routing and project-owned templates.

For changes to deployment behavior, use temporary project fixtures to check additions, updates, retirement, local edits and template handling. Do not use another person's working project as a test fixture. For changes to guidance, read the complete result and verify that its required behavior remains clear and reachable.

Record user-visible changes in the Unreleased section of `CHANGELOG.md`. A pull request should describe the problem, the resulting behavior and the validation actually performed.

## Prepare and publish a release

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
