---
scope: portable
---

<critical>
scope: deploying the genome onto more than one agent harness — which slot binds to which path, and which surface is generated rather than written.
core: the body is harness-agnostic and exists once | only the binding surface differs | the second harness's surface is GENERATED from the first, never hand-kept
note: §ID append-only (portable) — never renumber; retired sections keep their number.
</critical>

# Harness adapter

A harness is the program that loads the genome: Claude Code, Codex. Naming them here does not
break the portable-pure law (`doc-organization.md` §9) — a harness the genome declares as a
deploy target is an invariant of the genome, the same way `.agent-workspace/` is. A harness the
genome does not target is named nowhere.

## §1 The two halves of a deployed genome

| half | what it is | how many copies |
|---|---|---|
| body | the on-demand tree, roles, lessons, decisions, tooling, and the text of every rule | exactly one, byte-identical for every harness |
| binding surface | the files a specific harness looks for by name, at a path it fixes | one rendering per harness |

The body is where the genome's value sits and it never forks. Everything below is about the
binding surface, which is small, mechanical, and the only thing a second harness costs.

## §2 Slot map

A **slot** is a job the genome needs a harness to perform. Six slots, and one non-slot that
exists only to be told apart from a slot.

| slot | Claude Code | Codex |
|---|---|---|
| root index + trigger surface | `CLAUDE.md` | `AGENTS.md` |
| always-loaded rule tier | `.claude/rules/*.md` with no `paths:` — auto-loaded every turn | **no equivalent** — reached only by a `MUST Read` trigger from `AGENTS.md` (§3.1) |
| path-scoped rule | `.claude/rules/*.md` with `paths:` — loads on the file being edited | nested `AGENTS.md` / `AGENTS.override.md` — loads on the working directory (§3.2) |
| skill | `.claude/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` |
| subagent | `.claude/agents/<name>.md` — markdown + frontmatter | `.codex/agents/<name>.toml` — `name`, `description`, `developer_instructions` |
| on-demand tree | `.agent-workspace/**` | `.agent-workspace/**` — identical, nothing to render |
| _(not a slot)_ | — | `.codex/rules/*.rules` — Starlark **shell-command execution policy**. The word collides with the genome's rule tier and the two are unrelated; nothing of the genome is ever written there (§3.3). |

The rule tier keeps its physical home at `.claude/rules/` for both harnesses. One copy of a
law beats a directory name that matches the harness reading it.

## §3 Codex deltas that change behaviour, not just paths

A slot whose only difference is a path is free. These three are not — each one weakens or
moves a guarantee the Claude Code side gives, and a genome deployed to Codex must be written
knowing that.

### §3.1 There is no always-loaded tier — only a size-capped root file

Codex concatenates the `AGENTS.md` chain from the repository root down to the working
directory and stops once the total reaches `project_doc_max_bytes` (32 KiB by default). There
is no second tier that loads on its own.

<rules section="ALWAYS">
- an always-loaded rule reaches Codex as a `MUST Read` trigger line in `AGENTS.md`, never as inlined text
- the rendered `AGENTS.md` stays under the byte cap counted in BYTES, not lines — the cap is on the concatenated chain, and a nested file further down loses its place when the root file is fat
</rules>

<rules section="NEVER">
- inline the always-loaded rule tier into `AGENTS.md` to reproduce the Claude Code load order — the tier is larger than the cap, so the overflow is silently dropped and nobody is told which rule vanished
</rules>

The genome therefore holds one guarantee less on Codex: a rule that Claude Code loads before
the agent can act is, on Codex, a rule the agent must choose to read. That is why the trigger
line's wording law (`doc-organization.md` §10, recognizable trigger) matters more there, not
less — the trigger is the whole mechanism, not a hint on top of one.

### §3.2 A path-scoped rule becomes directory-scoped

`paths:` frontmatter fires on the file being edited. A nested `AGENTS.md` fires on the working
directory. They coincide only when the agent's working directory happens to be the directory
it is editing in, which is not something the genome can require.

<rules section="ALWAYS">
- a path-scoped standard whose correctness matters on Codex gets a `MUST Read` trigger at the root `AGENTS.md`, keyed to the action + concrete object (`doc-organization.md` §10), and not only a nested file
</rules>

### §3.3 `rules/` means something else

`.codex/rules/*.rules` is an allow / prompt / forbidden policy over shell command prefixes,
written in Starlark, loaded only for a trusted project. It is a sandbox control, not a place
where prose law lives. A genome file never lands there, and a reader who maps the genome's
rule tier onto that directory has mapped it onto the wrong thing entirely.

## §4 One source, two renderers

<rules section="ALWAYS">
- a change enters the **live Claude Code tier** first — that tier is the source of truth for every slot in §2
- the Codex surface is produced from it by the renderer, in the same change set
- a slot that gained content on one harness and not the other is drift, and the gate says so before the commit lands
</rules>

<rules section="NEVER">
- hand-edit a generated file listed in §5 — the next render overwrites it and the edit is gone with no diff to show for it
- keep two hand-maintained copies of the same law, one per harness, and rely on remembering to update both
</rules>

The duplication that §5 produces is the fourth case `doc-organization.md` §4 allows: a packaged
form beside its source, with a machine check between them. Without that check it is ordinary
drift, and the second harness is dead within a few releases.

## §5 The generated surface

| generated file | rendered from | carries |
|---|---|---|
| `AGENTS.md` | `CLAUDE.md` | a generated header naming the always-loaded rule files (§3.1), then the source body verbatim |
| `.agents/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` | that skill's `name` + `description`, and a body that sends the reader to the source file |
| `.codex/agents/<name>.toml` | `.claude/agents/<name>.md` | `name`, `description`, and `developer_instructions` that send the reader to the source file |

Every generated file opens with a machine-readable generated-by marker, so a human who opens
one is told where to edit instead.

A stub, not a copy: the Codex-side file carries only what the harness needs in order to *find*
and *route to* the capability — the instructions themselves are read from the single source at
run time. That is what keeps the body count at one.

<rules section="ALWAYS">
- the renderer checks BOTH directions (`verification-gate-design.md` §2): every source has its generated file (nothing dropped) AND every generated file has its source (nothing left behind after a source is deleted)
</rules>

## §6 Adding a harness target

1. read that harness's own configuration documentation and fill a §2 column from it — every slot, path quoted from the doc, not inferred from another harness's shape
2. any slot with no equivalent, or with a weaker guarantee, becomes a `§3.x` delta stating what the genome loses there — a blank cell is a lie, an honest delta is a constraint the writer can work with
3. extend the renderer and its gate; the new surface is generated from the same live tier, never hand-written
4. the body does not change — a harness that would require editing the body is a harness the genome cannot target as written, and that finding is the deliverable

<critical_recap>
1. one body, many binding surfaces — the body never forks
2. Codex has no always-loaded tier: an always-loaded rule arrives as a `MUST Read` trigger inside a 32 KiB-capped `AGENTS.md`
3. `paths:` scoping degrades to directory scoping on Codex — root trigger, not only a nested file
4. `.codex/rules/` is shell-command policy, not the genome's rule tier
5. the second harness's surface is generated and gated in both directions, never hand-kept
</critical_recap>
