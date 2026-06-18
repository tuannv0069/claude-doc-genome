# Contributing

Thanks for your interest in improving `init-project`.

## Report an issue

Open a GitHub issue with:

- what you ran (`/init-project`, `check`, or `promote`) and on what kind of project;
- what you expected vs. what happened;
- relevant output (the manifest, the verify step, or any error).

## Propose a change

1. Fork the repository and create a branch from `main`.
2. Make your change inside `skills/init-project/` (the plugin) — keep the `portable/` bundle generic (no project-specific names, paths, or values).
3. Bump the version in `skills/init-project/VERSION`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json` together, and add a `CHANGELOG.md` entry.
4. Open a pull request describing the change and the reasoning.

## Design principles

This plugin treats the documentation set as a living network (see the README "Philosophy" section). Two rules matter most for contributions:

- **One source of truth.** A substantive rule lives in exactly one file with a stable `§ID`; everything else references it. Never inline a copy.
- **Portable-pure bundle.** Files under `portable/` are copied verbatim into every project, so they must contain no project-specific name, path, or value.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
