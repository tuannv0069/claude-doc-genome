---
scope: portable
---

<critical>
scope: how the doc system is wired and checked — the §ID reference mechanism, the shape of the on-demand guide tree (areas, taxonomy, routers), and the layers that catch violations.
core: reference by stable §ID, never by line or title | every content file lives in exactly one area and is reachable from the router | duplication is caught, not trusted.
pairs with: `doc-organization.md` decides WHERE content goes; this file describes HOW the tree it goes into is built. That file is always-loaded because a placement decision arrives before any path is known; this one is read at the moment you build or wire something, so it stays on-demand.
numbering: §IDs are inherited from `doc-organization.md`, where these sections used to live — §2, §3, §5, §6, §7, §8.1, with the gaps left as-is. `scope: portable` §IDs are append-only (`doc-organization.md` §2), so renumbering here would silently break referrers in projects outside this repo's reach.
</critical>

## §2 Reference mechanism

Every cross-file reference uses **stable §ID anchors**, not line numbers or section titles.

| form | example |
|---|---|
| ✅ pointer | `apply per .agent-workspace/guide/<area>/<topic>.md §4.2` |
| ✅ pointer + intent | `verify file matches canonical shape in <topic>.md §4.2` |
| ✅ pointer into tag-structured file | `<tag-name>` in `file.md` — tag = stable anchor where the file has no §ID scheme |
| ❌ inline copy | embedding the canonical code/template/snippet in the agent body |
| ❌ unstable ref | `see line 314 of <topic>.md` or `see the <topic> section` |

source-of-truth file MUST assign every rule a §ID that survives reordering (heading text may change, ID stays). Renumber sparingly; when renumbered, every referrer updates in the same commit.

Renumbering applies to `scope: project` files only. `scope: portable` files (`doc-organization.md` §9) are §ID **append-only** — never renumber: referrers may live in other projects, outside atomic reach. Obsolete portable sections are marked `(retired)` and keep their number.

---

## §3 Examples (generic)

<example type="canonical_artifact_shape">
input: a recurring artifact pattern that 3 agents need to enforce
❌ output: paste the code template into each agent's checklist + the catalog's fix block + the index summary
✅ output: write canonical artifact once in `.agent-workspace/guide/<area>/<topic>.md §X.Y`; agent checklist = "verify file matches `<topic>.md §X.Y`"; catalog fix = "apply per `<topic>.md §X.Y`"; index = link only
</example>

<example type="agent_local_logic">
input: an agent must run phase A → B → C and abort on first error
❌ output: extract phase order to a shared rule (cross-cuts nothing — over-abstraction)
✅ output: keep workflow inside that agent's body; only extract if a second agent reuses the SAME workflow
</example>

<example type="detection_vs_fix">
input: a bug catalog entry for a recurring violation
❌ output: catalog contains symptom + full fix template (drifts when canonical changes)
✅ output: catalog contains symptom + grep pattern; fix = "apply per <topic>.md §X.Y"
</example>

---

## §5 Enforcement

| layer | check |
|---|---|
| reviewer | when editing any agent/skill/catalog, search for canonical signatures of substantive rules; reject inline copies |
| audit script | grep canonical signature strings outside source-of-truth file → warn |
| pointer-rot linter | grep every `§X.Y` reference → fail if target §ID missing in cited file |
| writer agent (skill/agent author per its meta-standard) | reject body containing inline code/snippets that exist in the source-of-truth tree — must be pointer |
| rule author | every new substantive rule gets a §ID before being referenced elsewhere |

---

## §6 Content-class flow (within a rule doc)

Decides where a piece of content goes once it lives inside the rule/guide system. The operative form is the classification table in `doc-organization.md` §1; this is the same five classes walked as a branching flow. File/tier placement = `doc-organization.md` §8.3.

```
new content to write
  │
  ├── is it a substantive rule (canonical shape / prop list / ❌✅ snippet / fix template / naming / validation criterion)?
  │     → YES: write in source-of-truth file with §ID; others reference
  │     (no source-of-truth exists yet → create .agent-workspace/guide/<area>/<topic>.md first)
  │
  ├── is it operational logic of ONE agent (workflow / abort / output / tool whitelist)?
  │     → YES: keep local in that agent
  │
  ├── is it routing metadata (frontmatter description / trigger phrases)?
  │     → YES: keep local in that agent (harness requirement)
  │
  ├── is it a detection signal for a known bug?
  │     → YES: catalog with grep pattern + pointer to fix in source-of-truth
  │
  └── is it an always-loaded guardrail?
        → YES: terse rules/*.md + pointer to full source
```

---

## §7 On-demand guide tree — areas, taxonomy, routers

### §7.1 Area model

Top level of the on-demand tree = `index.md` (root router) + area folders only — no content file at top level.

Area = one **axis of work**: the thing its files share that a reader would name when reaching for them. A stack layer (`frontend/`, `backend/`) is the most familiar shape, not the required one — an artifact type (`spec/`, `dd/`), a recurring activity (`translation/`, `testing/`, `release/`), or a live subsystem are axes just as valid. A project with no code has areas too; it simply has none that are stack layers. Plus `general/` for what cross-cuts every axis. Infrastructure folders (`templates/`, `scripts/`, `prompts/`) are not areas — taxonomy does not apply to them.

<rules section="ALWAYS">
- every content file lives in exactly one area
- new content file → existing matching area; no matching area → `general/` (create folder with the first file)
- `general/` = cross-cutting + small-operational-guide zone; never split on the 2nd shared-axis file — forcing area shape upfront violates §8.1 P3
- promote a `general/` cluster to a named area when files sharing one axis exceed 5 (matches §7.2 threshold); axis test = their router "read when" names the same task type, artifact type, activity, or live subsystem; fix referrers same commit
- no axis emerges → `general/` stays flat at any count; the promotion rule above waits, it does not force
- single-axis area > 5 files → apply a folder taxonomy (§7.2 supplies the default set); ≤ 5 files → flat allowed
- `general/` is axis-less by definition → never applies taxonomy; it sheds size by splitting when an axis appears (rule above)
- taxonomy folder is created with its first file — no empty folders
</rules>

<rules section="NEVER">
- add a NEW content file at top-level of the on-demand tree (existing violations = migration debt recorded in the router's ledger — `doc-organization.md` §10)
- design area shape upfront — areas grow from real stimulus (§8.1 P3)
- invent an area to satisfy the promotion rule when no axis is there — a wrong axis misroutes every file placed after it, which costs more than a long flat `general/`
</rules>

<example type="no_axis">
input: a doc-only project's `general/` holds 8 small guides — release notes, a glossary, a translation checklist, a meeting-notes format, four one-offs
❌ split into `docs-a/` and `docs-b/` to get under 5 — the folder names describe nothing, so nobody can predict where the 9th file goes
✅ leave it flat; when the 3rd translation guide arrives, `translation/` has a real axis and earns the promotion
</example>

### §7.2 Folder taxonomy inside an area (area > 5 files)

The four below are the **default set** — they fit most areas, and an area that fits them should use them rather than invent names.

| folder | content | signal |
|---|---|---|
| `concepts/` | describes "how X works" | read at onboarding, rarely edited |
| `patterns/` | "for X, do as follows" | read when hitting a new pattern |
| `workflow/` | task order / checklist / hub | read per task |
| `enforcement/` | rule registry, fix hints, automation guide, lint script | machine-read (verifier agent) |

<rules section="ALWAYS">
- new file in a taxonomy area → must live in a folder; use the default set where it fits
- default set does not fit the area's real content → the area defines its own folders and records them in its hub (or the router entry when it has no hub); an empty `enforcement/` kept for symmetry is a smell, not compliance
- abstract rule in `patterns/*.md` → ✅/❌ pair mandatory
</rules>

<rules section="NEVER">
- top-level orphan inside a taxonomy area — every file must live in a folder
- `concepts/*.md` referencing `workflow/` or `enforcement/` (concepts are stable, not process-bound)
- `enforcement/*.md` duplicating a rule from `concepts/` or `patterns/` — reference via §ID
</rules>

### §7.3 Router laws

<rules section="ALWAYS">
- each on-demand tree has exactly ONE root router `index.md`; entry form: `task/condition → file` — agent reads router, jumps straight, never searches repeatedly
- every content file appears in the router, reachable by EITHER a direct entry OR a hub entry whose hub lists it; `general/` always direct; a single-axis area > 5 files MAY route via its hub (a `workflow/` file) or list leaves directly — either way every leaf is reachable
- navigation chain: always-loaded trigger/see-also → router [→ hub] → file; max ONE hub layer
- entry = 1 line; condition per recognizable-trigger law (`doc-organization.md` §10); table format, most-used area first
- new file / new area → register in router (and hub) in the same commit (link-integrity law)
</rules>

<rules section="NEVER">
- hub pointing to another hub — tree grown to need a 2nd hub layer → split the doc tree, never widen the cap
- substantive content in router/hub — pointer-only (condition + read target)
- router/index file INSIDE the rules tier — harness auto-loads rules (always-loaded | path-scoped), so no in-tree index; the project index file (CLAUDE.md) may still point to rules in its see-also
</rules>

Canonical shapes:

```
index.md (root router)                 hub (area > 5 files, hub optional)
  frontmatter: scope                     frontmatter: scope
  §1 placement data (§10)                §1 task → leaf-file table
  §2 router table, grouped by area         (leaf files only — never another hub)
```

---

## §8.1 Philosophy (network model)

The agent doc system is a neural network: content files = neurons; links (trigger lines, router/hub entries, §ID pointers) = synapses. Value lives in the network — a file without links is dead content.

P1. **Context economy** — always-loaded only for what must be present BEFORE the decision point; everything else pays 1 recognizable trigger line to buy a whole on-demand file.
P2. **Bounded conduction, two modes** — guidance knowledge routes via `router [→ hub] → file` (§7.3); mass work products route via naming convention, router stops at category (`doc-organization.md` §11). Neither layer borrows the other's mode.
P3. **Growth from evidence** — areas/categories grow on real stimulus; the standard fixes growth laws, never final shape.
P4. **Two-layer self-healing** — prevention (link-integrity law, same commit) + immunity (periodic audit for orphan files and dead links). Compliance is probabilistic; both layers required.
P5. **Heredity** — the portable set is the genome: seeded once at init, each project grows its own phenotype; battle-tested experience consolidates back into the genome via promote.

<critical_recap>
1. reference by stable §ID; portable §IDs are append-only, retired sections keep their number (§2).
2. every content file lives in exactly one area, and `general/` stays flat when no axis is there (§7.1).
3. the four taxonomy folders are a default set, not a closed vocabulary — an empty one kept for symmetry is a smell (§7.2).
4. every leaf reachable from the router; max ONE hub layer; register in the same commit (§7.3).
5. duplication is caught by a layer, not trusted to discipline (§5).
</critical_recap>
