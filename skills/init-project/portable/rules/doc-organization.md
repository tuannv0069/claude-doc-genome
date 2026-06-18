---
scope: portable
---

<critical>
scope: organization + placement of agent doc system — rules tier, on-demand guide tree (`docs/agent-guide/`), skills, agents, catalogs/index files, project work-product docs.
core: substantive rule lives in ONE source-of-truth file — agents/skills/catalogs reference via §ID, never inline | new content placed via decision tree §8.3 | every file reachable via trigger/router (§10).
forbidden: copy-paste canonical code | duplicated ❌/✅ snippets | embedded fix templates | duplicated prop lists across files | content file outside an area | dead links.
</critical>

---

<rules section="NEVER">
- inline substantive rule (canonical code shape, prop list, ❌/✅ snippet, fix template, naming spec) in agent/skill/catalog/index
- restate a rule's content when a pointer suffices
- create rule content without a stable `§ID` anchor (downstream references break on re-numbering)
- reference a rule by file-path only (no §ID) — section ordering changes silently
- duplicate the same rule across multiple source-of-truth files — pick one canonical home, leave pointer-only stub in the other (exceptions: §4)
- commit a link whose target does not exist (dead pointer — file path or §ID)
</rules>

<rules section="ALWAYS">
- substantive rule → one source-of-truth file with stable `§ID`
- agent/skill/catalog/index → pointer-only (`see <file> §X.Y`)
- always-loaded guardrail file → terse reminder + pointer to full source
- operational logic (agent workflow, abort, output format, tool whitelist) → local to that agent (NOT cross-cut)
- routing description (frontmatter) → local to that agent (NOT cross-cut)
- topic has no source-of-truth file → create `docs/agent-guide/<area>/<topic>.md` with §1 anchor before referencing
- renumber `§ID` → update every referrer atomically in the same commit
- add/rename/move/delete a content file → update every linking node (router/index, hub, trigger line, §ID pointer) in the same commit
- rename/move → grep old path repo-wide after fixing referrers: 0 hits
- delete → remove its router/hub/trigger entries + resolve each remaining referrer (fix or delete per context)
</rules>

---

## §1 Content classification

Classify each piece of doc content BEFORE choosing where to put it.

| class | examples | location |
|---|---|---|
| substantive rule | canonical code shape, prop list, ❌/✅ snippet, fix template, naming spec, validation criterion | source-of-truth file (agent-guide tree) — **one** file per topic, stable `§ID` |
| operational logic | agent phase order, abort condition, output format, escalation, tool whitelist | local to agent/skill that owns the workflow |
| routing metadata | agent frontmatter `description` / trigger phrases | local to agent (required by harness) |
| detection signal | symptom string, grep pattern, file marker that flags a violation | catalog file — paired with pointer to fix in source-of-truth |
| always-loaded guardrail | 3-5 line reminder + pointer | dedicated rules file loaded every turn |

substantive ≠ operational. Substantive describes **what correct artifact looks like**. Operational describes **how this agent runs**.

---

## §2 Reference mechanism

Every cross-file reference uses **stable §ID anchors**, not line numbers or section titles.

| form | example |
|---|---|
| ✅ pointer | `apply per docs/agent-guide/<area>/<topic>.md §4.2` |
| ✅ pointer + intent | `verify file matches canonical shape in <topic>.md §4.2` |
| ✅ pointer into tag-structured file | `<tag-name>` in `file.md` — tag = stable anchor where the file has no §ID scheme |
| ❌ inline copy | embedding the canonical code/template/snippet in the agent body |
| ❌ unstable ref | `see line 314 of <topic>.md` or `see the <topic> section` |

source-of-truth file MUST assign every rule a §ID that survives reordering (heading text may change, ID stays). Renumber sparingly; when renumbered, every referrer updates in the same commit.

Renumbering applies to `scope: project` files only. `scope: portable` files (§9) are §ID **append-only** — never renumber: referrers may live in other projects, outside atomic reach. Obsolete portable sections are marked `(retired)` and keep their number.

---

## §3 Examples (generic)

<example type="canonical_artifact_shape">
input: a recurring artifact pattern that 3 agents need to enforce
❌ output: paste the code template into each agent's checklist + the catalog's fix block + the index summary
✅ output: write canonical artifact once in `docs/agent-guide/<area>/<topic>.md §X.Y`; agent checklist = "verify file matches `<topic>.md §X.Y`"; catalog fix = "apply per `<topic>.md §X.Y`"; index = link only
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

## §4 When duplication IS allowed

- **Always-loaded guardrail vs full source.** Terse reminder in always-loaded file + full content in agent-guide is intentional caching (loaded into every turn vs on-demand read). Pointer mandatory; content stays terse + non-authoritative.
- **Routing metadata.** Each agent's `description` frontmatter is local and may overlap conceptually with another agent — harness needs distinct strings to route.
- **Identical examples used as illustration in 2 unrelated contexts** — allowed if each is clearly an illustrative example, not the source of the rule.
- **Packaged source vs deployed instance.** A distribution bundle (e.g. an init skill) carries canonical copies of `scope: portable` files; the live tree is deployed instance #1. Intentional duplication — drift detected by the bundle's `check` mode, consolidated via `promote`.

Outside these four: duplication = drift risk.

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

Decides where a piece of content goes once it lives inside the rule/guide system. File/tier placement = §8.3.

```
new content to write
  │
  ├── is it a substantive rule (canonical shape / prop list / ❌✅ snippet / fix template / naming / validation criterion)?
  │     → YES: write in source-of-truth file with §ID; others reference
  │     (no source-of-truth exists yet → create docs/agent-guide/<area>/<topic>.md first)
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

Top level of the on-demand tree = `index.md` (root router) + area folders only — no content file at top level. Area = one axis of work: stack layer (`frontend/`, `backend/`), artifact type (e.g. `bd/`, `dd/`), or cross-cutting (`general/`). Infrastructure folders (`templates/`, `scripts/`, `prompts/`) are not areas — taxonomy does not apply to them.

<rules section="ALWAYS">
- every content file lives in exactly one area
- new content file → existing matching area; no matching area → `general/` (create folder with the first file)
- `general/` = cross-cutting + small-operational-guide zone; never split on the 2nd shared-axis file — forcing area shape upfront violates §8.1 P3
- promote a `general/` cluster to a named area when files sharing one axis exceed 5 (matches §7.2 threshold); axis test = their router "read when" names the same task type or live subsystem; fix referrers same commit
- single-axis area > 5 files → apply the 4-folder taxonomy (§7.2); ≤ 5 files → flat allowed
- `general/` is axis-less by definition → never applies taxonomy; it sheds size by splitting (rule above)
- taxonomy folder is created with its first file — no empty folders
</rules>

<rules section="NEVER">
- add a NEW content file at top-level of the on-demand tree (existing violations = migration debt recorded in the router's ledger — §10)
- design area shape upfront — areas grow from real stimulus (§8.1 P3)
</rules>

### §7.2 4-folder taxonomy (area > 5 files)

| folder | content | signal |
|---|---|---|
| `concepts/` | describes "how X works in the stack" | read at onboarding, rarely edited |
| `patterns/` | "for X, do as follows" | read when hitting a new pattern |
| `workflow/` | task order / checklist / hub | read per task |
| `enforcement/` | rule registry, fix hints, automation guide, lint script | machine-read (verifier agent) |

<rules section="ALWAYS">
- new file in a taxonomy area → must live in 1 of the 4 folders
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
- entry = 1 line; condition per recognizable-trigger law (§10); table format, most-used area first
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

## §8 Placement — philosophy, load tiers, decision tree

### §8.1 Philosophy (network model)

The agent doc system is a neural network: content files = neurons; links (trigger lines, router/hub entries, §ID pointers) = synapses. Value lives in the network — a file without links is dead content.

P1. **Context economy** — always-loaded only for what must be present BEFORE the decision point; everything else pays 1 recognizable trigger line to buy a whole on-demand file.
P2. **Bounded conduction, two modes** — guidance knowledge routes via `router [→ hub] → file` (§7.3); mass work products route via naming convention, router stops at category (§11). Neither layer borrows the other's mode.
P3. **Growth from evidence** — areas/categories grow on real stimulus; the standard fixes growth laws, never final shape.
P4. **Two-layer self-healing** — prevention (link-integrity law, same commit) + immunity (periodic audit for orphan files and dead links). Compliance is probabilistic; both layers required.
P5. **Heredity** — the portable set is the genome: seeded once at init, each project grows its own phenotype; battle-tested experience consolidates back into the genome via promote.

### §8.2 Load tiers

Mechanism = harness; this law decides WHICH tier.

| tier | mechanism | entry criterion | constraint |
|---|---|---|---|
| always-loaded | rules file without `paths:` frontmatter | guardrail needed BEFORE the decision point, not predictable by path: safety, scope ownership, placement | terse + pointer; total budget per project data (§10) |
| path-scoped | rules file with `paths:` frontmatter | standard needed only when touching matching file type | full content allowed |
| on-demand | guide tree (`docs/agent-guide/` equivalent) | task-routed knowledge, reached via router/trigger | §7 |

The project index file (CLAUDE.md equivalent) is NOT a tier — it is an index + minimal guardrail surface: pointers and ≤ 1-line rules only (per `claude-md-standards.md`).

### §8.3 Placement decision tree

New content goes through this tree; first matching branch wins.

```
new content
├─ 1. workflow with trigger + steps + defined output?
│     → skill (per skill-md-standards.md)
├─ 2. persona running standalone in a subagent?
│     → agent definition (per subagent-standards.md)
├─ 3. guardrail that must hold EVERY turn?
│     → rules, always-loaded: terse + pointer to source-of-truth
├─ 4. meta-standard needed only when touching a specific file type?
│     → rules, path-scoped (paths: matching that file type)
├─ 5. project knowledge read per task?
│     → guide tree <area>/ per §7 (stack-layer area | artifact area | general/)
├─ 6. pure project work product (spec/design/research/review/wiki)?
│     → docs/<category>/ per §11
└─ 7. just a pointer/index?
      → project index file (≤ 1 line per rule, per claude-md-standards.md)
```

For content classes WITHIN rule docs (substantive vs operational vs routing vs detection) → §6.

## §9 Portability axis

Every file in the rules tier and the on-demand guide tree declares frontmatter `scope:` — 2 values:

| `scope:` | definition | extra law |
|---|---|---|
| `portable` | true for any project; copied verbatim | §ID append-only — never renumber, retired sections keep their number (§2); English regardless of location |
| `project` | meaningful only in this project | free to evolve; renumber allowed if every referrer updates atomically |

- **Portable-pure law:** a `scope: portable` file contains no project-specific file name, path, or value — project data (budget, ledger, port tables, area lists) lives on the project side, concretely the root router (`index.md`, always `scope: project`) per §10. References to genome files (`CLAUDE.md`, `.claude/**` standard files) are not project-specific.
- Skills/agents: default `project`; portable exceptions are declared by explicit list in the distribution bundle map — NOT via `scope:` frontmatter in skill/agent files (harness owns that schema).
- Unclassifiable file → tag `project` (safe default — never copied out), note for later audit.

## §10 Placement laws

- **Naming:** kebab-case; topic-based names, no version/date suffixes (`cache.md`, not `cache-v2.md`); the router file of a doc tree is always `index.md` — never `README.md` as router (README = human landing page of repo root only); path already describes — don't repeat folder name in file name.
- **New-file-vs-extend:** topic already has a source-of-truth file → extend it with a new §ID; new topic → new file with §1 anchor from the first commit.
- **Always-loaded budget:** total lines of rules files without `paths:` ≤ budget declared in the project's placement data; project index file excluded (own budget per `claude-md-standards.md`). Over budget → demote least-used file to path-scoped or split terse+pointer.
- **Reachability:** every on-demand content file MUST have a router entry (§7.3); a behavior-affecting file additionally needs a trigger line at the always-loaded surface (project index file or an always-loaded rule): `cond → MUST Read <file>`. File with neither router entry nor trigger = dead content — audit must flag.
- **Recognizable trigger:** trigger condition = observable signal at decision time — user keywords, task type, file type touched — never an abstract description. Wording canon: `claude-md-standards.md <trigger_lines>`.
- **Link integrity:** add/rename/move/delete propagates to every linking node in the same commit — full law in ALWAYS section (top).
- **Project placement data:** the root router (`index.md`) carries the project's placement data in §1: (a) always-loaded budget value, (b) migration ledger — files not yet at their standard location, each with target area; end state = empty ledger; no permanent exemptions.

## §11 Project work-product layer (docs/)

The guide tree answers *"how to do it right"*; the rest of `docs/` is the project's **work product** — spec, design, research, review, wiki.

<rules section="ALWAYS">
- new work product → existing category; no matching category → new category + register in the docs router (`docs/index.md`) in the same commit
- docs router stops at CATEGORY level — 1 line per category; file-level discovery = naming convention (e.g. functionId) + optional per-category `index.md`
</rules>

<rules section="NEVER">
- list individual files in the docs router (work-product volume outgrows any hand-kept list)
- place a work product in the guide tree or a guide in a work-product category
</rules>

Category list = `scope: project`; the laws of this layer = portable. Content-writing rules for work products are owned by the project's documentation standard — out of placement scope.

---

<critical_recap>
1. substantive rule → ONE source-of-truth file, stable §ID; portable files = append-only §ID
2. agent/skill/catalog → pointer-only, NEVER inline canonical content
3. new content → decision tree §8.3; on-demand tree: area + router laws §7
4. always-loaded only for pre-decision guardrails (budget-capped); everything else = trigger line + on-demand
5. every file change maintains its links same-commit; audit hunts orphans + dead links
</critical_recap>
