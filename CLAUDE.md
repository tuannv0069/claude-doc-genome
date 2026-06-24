# claude-doc-genome

Claude Code documentation genome — portable rules, guides, skills, agents, and templates for the `claude-doc-genome` plugin.

## stack
- Node.js (scripts: sync-version.mjs, update.mjs)
- Claude Code plugin (.claude-plugin/)
- SemVer versioning via `skills/init-project/VERSION` (canonical)

## NEVER
- add project-specific names, paths, or values to `skills/init-project/portable/` (portable-pure law)
- renumber `§ID` in `scope: portable` files (append-only; retired sections keep their number)
- push without completing the full release workflow (version bump + tag + GitHub Release)
- edit VERSION or version mirrors manually — use `node scripts/sync-version.mjs set X.Y.Z`
- commit with version drift (pre-commit hook enforces `sync-version.mjs check`)

## ALWAYS
- enable hooks after clone: `git config core.hooksPath .githooks`
- release workflow (ALL 5 steps mandatory, in order):
  1. `node scripts/sync-version.mjs set <X.Y.Z>` — bumps VERSION + mirrors (plugin.json, marketplace.json, README badge)
  2. commit: `release: vX.Y.Z` — list changed files in body
  3. `git tag vX.Y.Z`
  4. `git push origin main --tags`
  5. `gh release create vX.Y.Z --title "vX.Y.Z" --notes "<changelog>"` — GitHub Release mandatory, not optional

## conventions
| domain | rule |
|--------|------|
| commit | conventional commits (`release:`, `feat:`, `fix:`, `chore:`, `docs:`) |
| version bump | MAJOR = breaking (rename/remove portable file), MINOR = additive (new rule/guide/§ID), PATCH = wording/typo |
| changelog | update `## [Unreleased]` in CHANGELOG.md; maintainer cuts version sections at release |
| portable files | `scope: portable` frontmatter, English only, §ID append-only |
