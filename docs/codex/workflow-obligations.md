# Codex workflow obligations and acceptance evidence

## §1 Purpose and source independence

This map identifies the workflow responsibilities carried by the Codex distribution and where its implementation owns them. It is a review aid, not another authoritative copy of the requirements. Read each owning source before judging a change to that responsibility.

The initial design was reviewed against the workflow topics in the accepted genome design and the implementation plan dated 2026-09-16. The resulting Codex files are maintained independently. They do not import another product's instructions, require text equality with another product or use another product's version as their release contract.

The initialization skill at `skills/init-codex-genome/` is the only authored Codex genome. Its portable sources and templates are edited directly. Project routers are installation seeds that remain project-owned after creation. The deployment map owns exact destinations and file kinds; it does not refer to another live source tree.

## §2 Responsibility map

Paths in this table describe deployed files relative to `.agent-workspace/` unless the cell identifies `AGENTS.md`. Their authored sources live under the skill's `bundle/portable/`; the AGENTS body and initial routers live under `bundle/templates/`. The evidence column describes the required check; it does not claim every check has already run.

| ID | Responsibility retained | Authoritative Codex source | Entry condition | Acceptance evidence |
|---|---|---|---|---|
| W01 | Reuse existing authorization while identifying unresolved scope | `rules/critical-thinking.md` §1 | Task-start reading through AGENTS | An authorized edit proceeds without asking for the same approval; an unrequested commit is not performed. |
| W02 | Open definitions and inspect producers and consumers | `rules/critical-thinking.md` §2 | Task-start reading through AGENTS | A boundary explanation identifies both sources and separates source claims from runtime observations. |
| W03 | Revise conclusions from evidence and retain method failures | `rules/critical-thinking.md` §3 | New evidence or a failed method | A correction changes the supported conclusion and reaches the lesson procedure. |
| W04 | Read relevant, current source material without hidden truncation | `rules/file-reading.md` §1 | Task-start reading through AGENTS | The agent retrieves missing ranges and rereads changed material before relying on it. |
| W05 | Keep canonical ownership, project data and work products distinct | `rules/doc-organization.md` §1 | Task start and before changing the instruction network | A requirement has one Codex owner; project values remain in project sources. |
| W06 | Maintain stable references and reachable guidance | `guide/general/doc-system-mechanics.md` §2 | Add, move, rename or remove instruction-network content | Routers, triggers and incoming references remain valid after the operation. |
| W07 | Preserve effective AGENTS ownership and instruction discovery | `rules/agents-md-standards.md` §1 | Before creating, editing or renaming AGENTS files | Fresh root and child-directory cases distinguish loaded instructions from action-routed rules. |
| W08 | Package executable skills with selective loading and verified dependencies | `rules/skill-md-standards.md` §1 | Before modifying a skill or its owned resource | Installed skill discovery and an actual invocation use the intended package revision. |
| W09 | Distinguish working roles from independent agents | `rules/codex-agents-standards.md` §1 | Before creating or changing a custom agent | A role can operate in the main context; unsupported delegation is reported rather than fabricated. |
| W10 | Preserve existing Codex configuration and verify effective capabilities | `rules/codex-config-standards.md` §1 | Before changing config, hooks, execution policies or MCP | A fixture retains unrelated values and separates syntax, trust and execution evidence. |
| W11 | Plan in proportion to consequences and define verification first | `guide/general/task-planning.md` §1 | Before changing an artifact or producing a deliverable | The plan maps requirements to outcomes and checks; small isolated work is not burdened with unrelated ceremony. |
| W12 | Coordinate bounded assignments and independently verify consequential results | `guide/general/orchestration-policy.md` §1 | Before multi-file execution or delegation | Assignment roots and ownership are explicit; final integration examines the returned artifact. |
| W13 | Persist developing research and protect disposable state | `guide/general/orchestration-policy.md` §4 | Third research read/search exceeded or work delegated | Resumable evidence exists under the shared project task namespace before handoff; useful work survives cleanup. |
| W14 | Record decisions that version history cannot explain | `guide/general/decision-journal.md` §1 | Before law changes, review responses, scope exclusions, accepted debt or rejection | A qualifying choice records its source and rejected alternative; superseded history remains intact. |
| W15 | Look up and capture lessons in the phase they protect | `guide/general/lesson-capture.md` §2 | Task start, user correction or failed method | Matched stores and one-hop checks are read; a supported method failure is recorded during the turn. |
| W16 | Select task-specific roles without imposing software criteria on creative work | `guide/general/role-selection.md` §1 | Required role-router lookup at task start | A software task receives the relevant role; an unregistered creative task receives no forced software role. |
| W17 | Explain artifact causes and investigate prevention where applicable | `guide/general/five-why.md` §1 | Defect or root-cause investigation | The explanation is falsifiable, stops when the causal distinction is established and does not invent a genome cause for an external failure. |
| W18 | Examine affected consumers before fixing a defect | `guide/general/fix-impact-analysis.md` §1 | Before a fix in code, guidance, config or another artifact | The original defect and affected contracts are checked after the repair. |
| W19 | Review omissions and concrete failure hypotheses with calibrated evidence | `guide/general/review-checklist-method.md` §1 | Review or audit without an owning skill | Candidate findings have a location or condition and retain executed, traced or inferred status. |
| W20 | Report actionable findings without inventing a global report style | `guide/general/bug-report-format.md` §1 | Before reporting established findings | Findings retain location, condition, consequence, severity and correction; uncertainty remains visible. |
| W21 | Build gates that compare compatible units and detect loss as well as invention | `guide/general/verification-gate-design.md` §1 | Before creating or editing a machine gate | Known failing and legitimate fixtures test the invariant and expose misleading count comparisons. |
| W22 | Distinguish scanner findings from context and semantic judgment | `guide/general/rule-health.md` §1 | Before running or judging genome checks | The report identifies its corpus and unverified meaning; duplicate package copies do not become defects by default. |
| W23 | Recognize packageable workflows without interrupting authorized work | `guide/general/capability-packaging.md` §1 | Before following an unpackaged procedure | The current task finishes; an optional candidate has a trigger, dependencies, output and no existing owner. |
| W24 | Preserve working state across isolated checkouts and cleanup | `guide/general/worktree.md` §1 | Before creating, using or removing a worktree | Setup uses the intended revision, tools receive its absolute root and cleanup preserves tracked and untracked results. |
| W25 | Validate Markdown against its real renderer and parser | `guide/general/markdown.md` §1 | Before editing Markdown whose syntax or parsing matters | Literal content, links and any machine data contract survive rendering and parsing. |
| W26 | Check diagram syntax separately from represented meaning | `guide/general/mermaid.md` §1 | Before creating or changing a Mermaid diagram | The destination renders it and the actors, relationships or transitions match source evidence. |
| W27 | Reuse established subject knowledge with confidence, provenance and contradiction handling | `rules/wiki-tier.md` §1 | Matching wiki subject investigation or claim edit | Claims have required evidence; a structural check is not reported as renewed factual verification. |
| W28 | Preserve knowledge identity during updates, imports and merges | `rules/wiki-tier.md` §3 | Claim creation, migration or merge | Identifiers remain unique, intentional removals are resolved and imported records do not overwrite another store. |
| W29 | Maintain independent source distributions over one deployed project genome | `rules/doc-organization.md` §1 and deployment map | Genome maintenance or adoption | The package can bootstrap a new project alone, reuses an existing complete `.agent-workspace/`, keeps Codex bookkeeping under `.codex/`, and preserves shared histories during updates. |
| W30 | Keep output-specific editorial requirements outside the general genome | `rules/doc-organization.md` §1 | Rule authoring and final semantic review | No general sentence, length, heading, table, tone or voice policy enters the portable instructions. |

## §3 Role coverage

The portable role set retains seven distinct responsibilities: software requirements (`business-analyst`), software contracts (`tech-lead`), executable implementation (`developer`), runtime verification (`qa`), work-item dependencies (`project-manager`), permission paths (`security`) and technical translation fidelity (`comtor`). Each source has §6 completion criteria so the router can load checking perspectives without treating every role as another full instruction layer.

The project role table starts empty. Creative and other non-software domains use their own project requirements and may add roles when needed. The planning role can apply across domains because it owns scope and dependencies, but its presence does not turn the artifact into software work.

## §4 Codex-specific adaptations

The root entry point explicitly requests task-start router reads and foundational-rule reads. Specialized rules are read before their actions. This replaces any assumption that a Markdown rules directory or a path-scoped frontmatter field will automatically place the rule into Codex's context.

Guide, lesson, decision, wiki and task paths use the shared `.agent-workspace/` namespace. Installation seeds are created only when no complete project genome exists; an existing genome is consumed in place. Custom agents, hooks, execution policies and MCP remain optional mechanisms whose installed support must be established before use. The core workflow can operate in the main agent without a custom-agent definition.

The AGENTS template contains the managed region's body. The installer adds its boundary markers and records the resulting region hash. Each target project retains its own context outside those markers. Source verification materializes a temporary project rather than keeping a second authored AGENTS in the repository.

## §5 Verification boundaries

Structural checks can establish required files, references, stable sections, router data and package drift. They cannot establish the semantic completeness of every procedure or whether the assistant actually reads the guide during work. Behavioral verification must inspect fresh task executions, including a root-to-child edit, a creative request, a method correction and a task resumed from persisted state.

The wiki guide preserves knowledge responsibilities without promising an unavailable ID allocator or renewed source observations. Its empty seed is inactive. Before a project activates it, that project must declare subject and evidence classes and perform the checks the installed tooling does not automate. Structural claim validation does not establish that class-specific evidence is sufficient or that its source is current. Likewise, no custom-agent definition is considered verified merely because its TOML parses.

Use the product's implementation and acceptance report for actual test results. This map records what must be checked and where the governing requirements live; it is not a passing-test certificate.
