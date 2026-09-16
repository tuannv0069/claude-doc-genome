# Maintaining the Codex genome in this skill

This skill is the only authored source of the Codex distribution. Its `VERSION` identifies the bundle version. Edit portable bootstrap instructions and the deployment tool directly under `bundle/portable/`, project seeds under `bundle/templates/`, and the workflow in `SKILL.md` and `references/`. There is no second live authoring tree to synchronize. The Claude distribution is maintained separately even though both adapters use one deployed `.agent-workspace/` inside a project.

## Check and refresh source metadata

Use the wrapper from this skill's actual directory:

```text
python <skill>/scripts/genome.py check
python <skill>/scripts/genome.py refresh
```

`check` validates the bundle inventory, recorded hashes and version, then checks the instruction network in a temporary deployment. `refresh` describes the inventory and hash changes caused by direct source edits. Review the added, changed and removed entries, then run `refresh --apply` to update the map. This writes metadata; it does not copy guidance from another project. An incomplete or invalid bundle must be fixed before refreshing its metadata. Run `check` again after applying the refresh.

The wrapper supplies its own package root. Use `--package-root <absolute-skill-directory>` only when deliberately checking another skill copy. Never treat an installed project's local modifications as automatic changes to this source. Bring back a useful improvement by reviewing it and editing its owning source in this skill.

## Verify deployment behavior

Copy the whole skill into an unrelated temporary project when checking portability. Run `init --project <absolute-project-path>`, review and apply the returned plan, then run the installed tool with `verify --project <absolute-project-path>`. Test `update` against an earlier deployment when changing installation behavior. Also test initialization against a project whose shared workspace was created by the Claude distribution. Check preservation of local edits, shared records, project routers and content outside the managed AGENTS region.

Structural validation does not establish the quality of every instruction or the assistant's behavior. Read changed guidance and its consumers. Test affected loading obligations in a fresh Codex session when the change can alter them. Keep project-specific records out of installation seeds.

## Repository development support

The source repository also contains development tests under `tests/codex/`, version and packaging tools under `scripts/codex/`, and human documentation under `docs/codex/`. Those files are not needed to copy this skill to another project or run its deployment commands. In that repository, follow `docs/codex/contributing.md` for the test and packaging commands. Packaging is an optional distribution form; it does not create another authored genome or authorize publication.

A skill copied into a project belongs to that project's workflow. Source edits, version changes and deployment to another project still require the authority supplied by the current task. The Claude genome has independent sources and versioning.
