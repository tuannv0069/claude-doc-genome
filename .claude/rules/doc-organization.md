---
scope: portable
---

<critical>
scope: organization + placement of agent doc system — rules tier, on-demand guide tree (`.agent-workspace/guide/`), skills, agents, catalogs/index files, project work-product docs.
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
- topic has no source-of-truth file → create `.agent-workspace/guide/<area>/<topic>.md` with §1 anchor before referencing
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
| substantive rule | canonical code shape, prop list, ❌/✅ snippet, fix template, naming spec, validation criterion | source-of-truth file (guide tree) — **one** file per topic, stable `§ID` |
| operational logic | agent phase order, abort condition, output format, escalation, tool whitelist | local to agent/skill that owns the workflow |
| routing metadata | agent frontmatter `description` / trigger phrases | local to agent (required by harness) |
| detection signal | symptom string, grep pattern, file marker that flags a violation | catalog file — paired with pointer to fix in source-of-truth |
| always-loaded guardrail | 3-5 line reminder + pointer | dedicated rules file loaded every turn |

substantive ≠ operational. Substantive describes **what correct artifact looks like**. Operational describes **how this agent runs**.

---

## §2 Reference mechanism — moved

Reference by stable `§ID`, never by line number or section title. Portable `§ID`s are **append-only**: never renumber, retired sections keep their number. Full forms → `doc-system-mechanics.md` §2; worked ❌/✅ pairs for §1 and §4 → its §3.

---

## §4 When duplication IS allowed

- **Always-loaded guardrail vs full source.** Terse reminder in always-loaded file + full content in the guide tree is intentional caching (loaded into every turn vs on-demand read). Pointer mandatory; content stays terse + non-authoritative.
- **Routing metadata.** Each agent's `description` frontmatter is local and may overlap conceptually with another agent — harness needs distinct strings to route.
- **Identical examples used as illustration in 2 unrelated contexts** — allowed if each is clearly an illustrative example, not the source of the rule.
- **Packaged source vs deployed instance.** A distribution bundle (e.g. an init skill) carries canonical copies of `scope: portable` files; the live tree is deployed instance #1. Intentional duplication — drift detected by the bundle's `check` mode, consolidated via `promote`.

Outside these four: duplication = drift risk.

---

## §5 Enforcement — moved

Five layers catch a duplicated or inlined rule: reviewer, audit script, pointer-rot linter, writer agent, rule author. Detail → `doc-system-mechanics.md` §5.

---

## §6 Content-class flow — moved

The same five classes as §1, walked as a branching flow. §1's table is the operative form and stays here; the flow → `doc-system-mechanics.md` §6. File/tier placement is a different question — §8.3.

---

## §7 On-demand guide tree — moved

Shape of the tree the decision tree (§8.3) places files into: **area = one axis of work** (a stack layer is one shape among several — an artifact type, an activity, or a subsystem count too); every content file lives in exactly one area and is reachable from the router; `general/` holds what cross-cuts, and stays flat when no axis is there.

Full laws — area model §7.1, taxonomy §7.2, router laws §7.3 → `doc-system-mechanics.md` §7. Read it before creating, moving, or renaming any file in the guide tree.

---

## §8 Placement — load tiers, decision tree

### §8.1 Philosophy (network model) — moved

Files are neurons, links are synapses; a file without links is dead content. Five principles — P1 context economy, P2 bounded conduction, P3 growth from evidence, P4 two-layer self-healing, P5 heredity → `doc-system-mechanics.md` §8.1.

### §8.2 Load tiers

Mechanism = harness; this law decides WHICH tier.

| tier | mechanism | entry criterion | constraint |
|---|---|---|---|
| always-loaded | rules file without `paths:` frontmatter | guardrail needed BEFORE the decision point, not predictable by path: safety, scope ownership, placement | terse + pointer; total budget per project data (§10) |
| path-scoped | rules file with `paths:` frontmatter | standard needed only when touching matching file type | full content allowed |
| on-demand | guide tree (`.agent-workspace/guide/`) | task-routed knowledge, reached via router/trigger | §7 |

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
├─ 5. record of a working method that failed — an incident, not yet distilled law?
│     → lesson store `.agent-workspace/lessons/<work-type>.md` per lesson-capture.md
│       (NEVER the guide tree — records are append-only, guides are curated)
├─ 6. project knowledge read per task?
│     → guide tree <area>/ per §7 (stack-layer area | artifact area | general/)
├─ 7. pure project work product (spec/design/research/review/wiki)?
│     → docs/<category>/ per §11
└─ 8. just a pointer/index?
      → project index file (≤ 1 line per rule, per claude-md-standards.md)
```

Branch 5 sits before 6 on purpose: a lesson IS read per task, so branch 6 would swallow it and the guide would accumulate incident history. A lesson enters the guide only after it recurs and is distilled into law (`lesson-capture.md` §4).

Branch 6: router entry unconditional; always-loaded trigger decided via interception test + user confirm → §10.

For content classes WITHIN rule docs (substantive vs operational vs routing vs detection) → §6.

## §9 Portability axis

Every file in the rules tier and the on-demand guide tree declares frontmatter `scope:` — 2 values:

| `scope:` | definition | extra law |
|---|---|---|
| `portable` | true for any project; copied verbatim | §ID append-only — never renumber, retired sections keep their number (§2); English regardless of location |
| `project` | meaningful only in this project | free to evolve; renumber allowed if every referrer updates atomically |

- **Portable-pure law:** a `scope: portable` file contains no *per-instance* project value (specific task-id, port number, budget value, project name) — those live on the project side, concretely the root router (`index.md`, always `scope: project`) per §10. **`.agent-workspace/` paths ARE allowed** (`.agent-workspace/guide/`, `.agent-workspace/lessons/`, `.agent-workspace/tasks/`, …): init creates that root in every project it deploys to, so it is an invariant of the genome itself — not a project value. References to genome files (`CLAUDE.md`, `.claude/**` standard files) are likewise not project-specific.
- **Substrate-naming law:** a `scope: portable` file MAY name a command the harness itself ships (`/code-review`, `/verify`) — the genome is a plugin of that harness, so those exist wherever it deploys. It MUST NOT name a bolt-on skill set or external system that may be absent (that is what makes a rule dangle). Bolt-on integrations are named only on the project side: an optional module in the init skill, which writes its trigger when a scan confirms the thing is installed.
- Skills/agents: default `project`; portable exceptions are declared by explicit list in the distribution bundle map — NOT via `scope:` frontmatter in skill/agent files (harness owns that schema).
- Unclassifiable file → tag `project` (safe default — never copied out), note for later audit.

## §10 Placement laws

- **Naming:** kebab-case; topic-based names, no version/date suffixes (`cache.md`, not `cache-v2.md`); the router file of a doc tree is always `index.md` — never `README.md` as router (README = human landing page of repo root only); path already describes — don't repeat folder name in file name.
- **New-file-vs-extend:** topic already has a source-of-truth file → extend it with a new §ID; new topic → new file with §1 anchor from the first commit.
- **Always-loaded budget:** total lines of rules files without `paths:` ≤ budget declared in the project's placement data; project index file excluded (own budget per `claude-md-standards.md`). Over budget → demote least-used file to path-scoped or split terse+pointer.
- **Reachability:** every on-demand content file MUST have a router entry (`doc-system-mechanics.md` §7.3); a behavior-affecting file (per interception test) additionally needs a trigger line at the always-loaded surface (project index file or an always-loaded rule): `cond → MUST Read <file>`. File with neither router entry nor trigger = dead content — audit must flag.
- **Interception test (router-only default):** on-demand file defaults to router entry ONLY. It is *behavior-affecting* (earns an always-loaded trigger) only if WITHOUT the trigger the agent starts the task and acts wrong BEFORE it would consult the router — task self-signals nothing to read a guide, and is not already reached via an existing trigger/hub. Pass → trigger candidate; fail → router-only.
- **Trigger-decision confirm:** on-demand file → router entry written unconditionally (mechanical); always-loaded trigger NEVER self-decided — run interception test, present result + recommendation (add | skip), ask user, write/skip per user. Confirm in BOTH outcomes.
- **Recognizable trigger:** trigger condition = observable signal binary-decidable from user message — user keywords, tool names, code symbols, file patterns, action + concrete object — never abstract task classification (`multi-step task`, `complex task`) or intent interpretation (`when X is needed`). Observable test: can agent decide YES/NO with no classification judgment? A **countable work-state signal** is equally admissible — the Nth file read, an agent dispatched, N files edited: counted, not judged. The ban is on classification (`non-trivial`, `complex`), not on where the signal is read from. Message-scan signals fire at intake; work-state signals fire mid-task, which is the only shape that works for a rule that must act before the work finishes. Wording canon: `claude-md-standards.md <trigger_lines>`.
- **Link integrity:** add/rename/move/delete propagates to every linking node in the same commit — full law in ALWAYS section (top).
- **Project placement data:** the root router (`index.md`) carries the project's placement data in §1: (a) always-loaded budget value, (b) migration ledger — files not yet at their standard location, each with target area; end state = empty ledger; no permanent exemptions.

## §11 Project work-product layer (docs/)

The guide tree (`.agent-workspace/guide/`) answers *"how to do it right"*; `docs/` holds the project's **work product** — spec, design, research, review, wiki. The two never mix: no guide under `docs/`, no work product under `.agent-workspace/`.

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
4. always-loaded only for pre-decision guardrails (budget-capped); everything else = trigger line + on-demand — on-demand trigger to always-loaded surface = interception test + user confirm (both outcomes), router entry stays unconditional
5. every file change maintains its links same-commit; audit hunts orphans + dead links
</critical_recap>
