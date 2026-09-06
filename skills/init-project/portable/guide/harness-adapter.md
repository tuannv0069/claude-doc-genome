---
scope: portable
---

<critical>
scope: deploying the genome onto more than one agent platform — which slot binds to which path, and which set is generated rather than written.
core: the shared body exists once | each platform set is complete on its own | neither set names a path of the other | the second set is GENERATED and gated, never hand-kept
note: §ID append-only (portable) — never renumber; retired sections keep their number.
</critical>

# Harness adapter

A platform is the program that loads the genome: Claude Code, Codex. Naming them here does not
break the portable-pure law (`doc-organization.md` §9) — a platform the genome declares as a
deploy target is an invariant of the genome, the same way `.agent-workspace/` is. A platform the
genome does not target is named nowhere.

## §1 Three parts, not two

| part | what it is | how many copies |
|---|---|---|
| shared body | the on-demand tree, roles, lessons, decisions, tooling — `.agent-workspace/**` | one, identical, belonging to neither platform |
| platform set | the files one platform loads, at the paths it fixes | one per platform, each complete on its own |
| platform-only rule | a standard describing a mechanism only one platform has | lives in that platform's set alone |

The shared body is where the genome's value sits and it never forks. Both sets may reference it,
because it belongs to neither of them. What neither set may do is reference the other.

## §2 Slot map

A **slot** is a job the genome needs a platform to perform.

| slot | Claude Code | Codex |
|---|---|---|
| root index | `CLAUDE.md` | `AGENTS.md` — the instruction chain, root down to the working directory |
| always-loaded rules | `.claude/rules/*.md` with no `paths:` | carried **inside `AGENTS.md` in full** — Codex has no second auto-load tier (§3.1) |
| path-scoped rules | `.claude/rules/*.md` with `paths:` | `.codex/rules/*.md` + a trigger line in `AGENTS.md` (§3.2) |
| skill | `.claude/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` — the path the platform scans inside a repository |
| subagent | `.claude/agents/<name>.md` | `.codex/agents/<name>.toml` |
| size control | none needed | `.codex/config.toml` → `project_doc_max_bytes`, shipped beside the chain (§3.1) |
| shared body | `.agent-workspace/**` | `.agent-workspace/**` — the same files |
| _(not a slot)_ | — | `.codex/rules/*.rules` — the Starlark command-approval policy. Same directory, different extension, unrelated purpose (§3.3) |

## §3 Codex deltas — where the two platforms genuinely differ

### §3.1 One auto-load surface, and it is size-capped

Codex concatenates the `AGENTS.md` chain from the repository root down to the working directory
and stops once the **combined** size reaches `project_doc_max_bytes`. There is no second tier that
loads on its own. The default is 32 KiB and the overflow is dropped with no warning.

<rules section="ALWAYS">
- an always-loaded rule reaches Codex only by being carried inside the chain, in full text
- the cap ships with the set: a project `config.toml` declaring `project_doc_max_bytes` sized to the rendered chain, with headroom
- the cap is counted in BYTES — a threshold nobody counts is a threshold nobody meets
</rules>

<rules section="NEVER">
- leave an always-loaded rule outside the chain and rely on a trigger to fetch it — that converts a guarantee into a choice, and the platform makes no promise the choice is taken
- let the rendered chain exceed the declared cap — the loss lands on whichever file came next, never on the one whose size caused it, so the symptom never points at the cause
</rules>

The cap is settable from project config: the platform's own list of keys a project may not
override does not include it. That is what makes the tier shippable rather than a per-machine
setup step.

### §3.2 A path-scoped rule becomes directory-scoped

`paths:` frontmatter fires on the file being edited. A nested `AGENTS.md` fires on the working
directory. They coincide only when the agent's working directory happens to be the directory it
is editing in, which is not something the genome can require.

<rules section="ALWAYS">
- a path-scoped standard keeps its file in the platform's rule directory and earns a trigger line in the root index, keyed to the action and its concrete object (`doc-organization.md` §10)
- the trigger names the glob the standard declares, so the reader can decide it without judgment
</rules>

Path-scoped rules are deliberately NOT carried inline: the other platform loads them only when a
matching file is touched, and inlining them would charge every Codex session for what Claude Code
pays only sometimes.

### §3.3 `rules/` holds two unrelated things

`.codex/rules/*.rules` is an allow / prompt / forbidden policy over shell command prefixes,
written in Starlark, loaded for a trusted project. The genome's prose rules live in the same
directory as `*.md`, which that engine does not read.

<rules section="NEVER">
- write prose into a `.rules` file — it is fed to the command-approval engine, and the breakage lands in the user's other work, not in the genome
</rules>

## §4 Independence — neither set reaches into the other

<rules section="ALWAYS">
- a change enters the authored set first; the generated set is produced from it in the same change set
- every generated file is complete where it sits: the instructions themselves, not a pointer to where they really live
- a standard describing a mechanism only one platform has is authored in that platform's set and mirrored nowhere
</rules>

<rules section="NEVER">
- let a file of one platform's set name a path of the other's — it resolves only on a machine that deployed both, and a project deploying one is the normal case
- hand-edit a generated file — the next render overwrites it and the edit leaves no diff behind
- translate a platform-specific standard by rewriting its paths — a path rewrite cannot make a wrong mechanism right; author the other platform's own standard instead
</rules>

An earlier form of this law had the second set point back at the first, so a rule existed once and
the second platform read it across the boundary. That is retired: it makes every deployment of one
platform incomplete, and it turns an auto-load guarantee into a file the agent has to choose to
open.

## §5 The generated set

| generated | composed from | carries |
|---|---|---|
| the root index | the authored root index + every always-loaded rule | the index body, then each rule's full text |
| each rule file | its authored counterpart | the full rule, with every path rewritten to this platform's |
| each skill | its authored counterpart | the full skill body, not a pointer |
| each subagent | its authored counterpart | the full instructions in the definition's own field |
| the size config | the rendered chain | the cap, sized with headroom |

Every generated file opens with a machine-readable marker, so a reader who opens one is told it is
not the editable copy. A file in the generated directory WITHOUT that marker is authored for that
platform alone, and the renderer leaves it alone.

<rules section="ALWAYS">
- the renderer checks three things (`verification-gate-design.md` §2): nothing MISSING (every source has its target, byte for byte), nothing EXTRA (every generated file maps back to a live source), and no file naming the other platform or a rule this set does not carry
</rules>

The third check has no direction, and it is the one that fails silently without a gate: a
cross-reference reads perfectly in review and resolves to nothing on a machine that deployed only
one platform.

## §6 Adding a platform target

1. read that platform's own configuration documentation and fill a §2 column from it — every slot, path taken from the source, not inferred from another platform's shape
2. prefer the running product over its documentation when the two disagree about a path; a doc page can be stale, an installed product cannot
3. any slot with no equivalent, or with a weaker guarantee, becomes a `§3.x` delta stating what the genome loses there — a blank cell is a lie, an honest delta is a constraint the writer can work with
4. any standard describing a mechanism that platform does not have is excluded from the mirror, and its replacement is authored in the new set
5. the shared body does not change — a platform that would require editing it is one the genome cannot target as written, and that finding is the deliverable

<critical_recap>
1. one shared body, one complete set per platform, no reference between sets
2. Codex auto-loads only the instruction chain, so an always-loaded rule is carried inside it in full, under a cap that ships with the set
3. path-scoped rules stay files and earn trigger lines — they are not inlined
4. `.codex/rules/` holds prose `.md` and command policy `.rules`; the two never mix
5. the second set is generated and gated three ways — missing, extra, and reaching across
</critical_recap>
