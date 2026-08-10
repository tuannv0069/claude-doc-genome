# Contributing

Thanks for your interest in improving `claude-doc-genome`.

## Report an issue

Open a GitHub issue with:

- what you ran (`/init-project`, `check`, or `promote`) and on what kind of project;
- what you expected vs. what happened;
- relevant output (the manifest, the verify step, or any error).

## Local setup

Enable the pre-commit hook once per clone (CI enforces the same checks on every PR):

```sh
git config core.hooksPath .githooks
```

It blocks two things: version fields out of sync (`scripts/sync-version.mjs check`) and a broken
documentation network — dead trigger, orphan guide, dead `§ID` (`scripts/doc-lint.mjs`). Run either
by hand at any time.

## Propose a change

1. Fork the repository and create a branch from `main`.
2. Make your change in the right copy. This repo is **deployed instance #1** of its own standard, so a portable rule, guide, skill, or agent exists twice on purpose (`doc-organization.md` §4): the live copy under `.claude/` and `.agent-workspace/guide/`, and the packaged copy under `skills/init-project/portable/`. Edit the **live** copy — that is the one the agent actually reads — then mirror it into the bundle with `/init-project promote`. If you cannot run the skill, copy the file across by hand and say so in the PR. Either way `node scripts/update.mjs --project .` must end with `conflict: 0` before you open it. Keep the bundle generic — no project-specific names, paths, or values.
   Everything else (`SKILL.md`, `templates/`, `scripts/`, the repo's own docs) has one copy and is edited directly.
3. Log your change under `## [Unreleased]` in `CHANGELOG.md`. Do **not** bump the version — the maintainer cuts versions at release time (see [Releasing](#releasing)).
4. Open a pull request describing the change and the reasoning.

## Releasing

The version means something to anyone who runs `/init-project update`, so it follows SemVer **for the bundle**:

| bump | meaning | effect on `update` |
|---|---|---|
| MAJOR | breaks an initialized project: a portable file referrers depend on is removed/renamed, or a template slot contract changes | may need manual migration |
| MINOR | additive: a new portable rule/guide/skill, a new `§ID` (append-only), or a new mode | safe to update |
| PATCH | wording/typo/clarification inside an existing portable file; no `§ID` or structure change | safe to update |

Commits follow [Conventional Commits](https://www.conventionalcommits.org/) so the changelog stays derivable.

Cut a release (maintainer, on `main` after merge):

1. `node scripts/sync-version.mjs set X.Y.Z`
2. Add a `## [X.Y.Z] - YYYY-MM-DD` section to `CHANGELOG.md`, plus a `[X.Y.Z]: …/releases/tag/vX.Y.Z` link line.
3. Commit: `release: vX.Y.Z`.
4. Tag and push: `git tag -a vX.Y.Z -m "vX.Y.Z" && git push origin main --tags`.
5. (Optional) Publish a GitHub Release from the tag, pasting the changelog section.

Every released version MUST have a matching `vX.Y.Z` git tag — the `CHANGELOG.md` links resolve to `releases/tag/vX.Y.Z`.

## Design principles

This plugin treats the documentation set as a living network (see the README "Philosophy" section). Two rules matter most for contributions:

- **One source of truth.** A substantive rule lives in exactly one file with a stable `§ID`; everything else references it. Never inline a copy.
- **Portable-pure bundle.** Files under `portable/` are copied verbatim into every project, so they must contain no project-specific name, path, or value.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
