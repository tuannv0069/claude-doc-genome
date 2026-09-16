# Independent Codex guidance review

Reviewed on 2026-09-16 by the tooling executor, who did not author the guidance. This is a source and semantic review, not a claim that runtime behavior was exercised here.

## Scope and method

Read the complete live Codex AGENTS entry, all eight rule sources, all sixteen general guides, all seven role definitions, the role and guide routers, and the workflow-obligations index. Used the index to locate responsibilities, not as proof that its claims were implemented. Checked the sixteen corresponding Claude guide responsibility headings and inspected the detailed original requirements where the boundary or adaptation could change the mechanism, including planning, orchestration, role selection, review, causal analysis, decisions and rule health. Earlier implementation work had also read the original fix-impact and gate-design sources.

The user requirements used for acceptance were independent product ownership, retained workflow governance, natural readable instructions, and removal of general output-style policies. No paragraph count, keyword score or script result was used as proof of natural language quality. A targeted vocabulary search located potential style clauses, which were then read in context. An initial batched tool output was truncated; its missing guide and skill/wiki text was retrieved before forming this verdict.

## Semantic disposition

The corpus preserves the requested mechanism: AGENTS requires actual router reads before selection, foundational rules are explicitly read, specialized procedures have before-action triggers, references do not pretend to load their targets, evidence precedes factual claims, dependencies precede fixes, and independent verification examines consequential work. Lessons, standing decisions and promotion retain their distinct responsibilities. Existing authorization is preserved, while committing and pushing still require an explicit request.

The source and deployed paths belong to Codex. There are no operational references to `.claude/`, `CLAUDE.md`, or the old unnamespaced guide/lesson/decision/tooling/task/wiki trees in the inspected AGENTS/rule/guide corpus. Mentions of Claude describe the other product's ownership boundary rather than a runtime dependency. Self-hosting AGENTS explicitly distinguishes `codex/` from its enclosing Git repository; configuration, skills, agents and worktrees distinguish source, installed-package and target roots.

No general rule was found requiring compressed sentences, a maximum sentence or paragraph length, a prescribed tone, headings by topic count, tables for comparisons, conclusion-first prose, or a compulsory closing next step. `doc-organization.md` §1 explicitly places output-specific editorial requirements with their project owner. Report information requirements remain scoped to established findings. Markdown/Mermaid requirements concern parser and renderer correctness. Lesson, decision and wiki fields are scoped record contracts. None is presented as a universal response style.

Creative work is not silently routed into software development or runtime QA. Role selection allows an unmatched task to continue, project-specific roles take precedence, and developer/BA/QA roles state their software boundaries. The planning role owns work dependencies without claiming editorial authority.

## Responsibility comparison

| Procedure | Retained responsibility observed in owning Codex source |
|---|---|
| Task planning | Consequence-scaled preparation, explicit sources, preplanned evidence, subtask contracts, independent plan/result review and return paths. |
| Orchestration | Bounded non-overlapping ownership, useful delegation, capability choice, source paths and root propagation, parent integration, research persistence and safe cleanup. |
| Decision journal | Admission by non-reconstructable reasoning, classes, standing/superseded lifecycle, same-turn capture, parent reconciliation and archive limits. |
| Lesson capture | Method failure distinct from facts, action/phase routing, actual lookup, one-hop checks, same-turn learning, recurrence and promotion. |
| Role selection | Specific/project precedence, primary plus checking perspectives, domain boundaries, delegation context and project extension. |
| Instruction mechanics | Canonical ownership, stable references, bounded hubs, reference propagation, prevention plus later repair, independent Codex promotion. |
| Causal analysis | Artifact mechanism plus applicable method/prevention cause, falsifiable evidence and no ceremonial fixed why count. |
| Fix impact | Dependency boundary, consumer expectations, coordinated repair, original defect and downstream compatibility checks. |
| Review method | Instrument selection, absence checks, concrete hypotheses, executed/traced/inferred evidence and adversarial challenge of findings. |
| Finding report | Location, condition, consequence, correction and calibrated severity without a universal layout. |
| Gate design | Compatible units, omissions versus additions, known failure and legitimate fixtures, limits of structural proof. |
| Rule health | Explicit corpus and exit semantics, context versus findings, canonical ownership, meaningful disposition and semantic limits. Claude-specific ledger/CLI mechanics are intentionally not treated as Codex requirements. |
| Capability packaging | Trigger/dependencies/output, existing-owner search, finish current work, scoped authority and remembered rejected proposals. |
| Worktrees | Intended revision, explicit target root, needed configuration, persisted state outside disposable checkout and preservation before cleanup. |
| Markdown | Actual renderer, literal content, working references and separate machine-schema validation. |
| Mermaid | Supported syntax, identifiers, source-true sequences/cardinality/states and final rendering. |

## Actionable contract mismatches

### G1 — Lesson protected-scope storage is underspecified

Evidence: `codex/.agent-workspace/codex/guide/general/lesson-capture.md` §3 requires action scope and phase in metadata but does not identify how the action scope differs from the required portability field `scope: project`. The installed verifier requires either `work_scope` in frontmatter or `scope` inside a critical metadata block. A new store that follows the visible guide using `scope: project`, a valid `phase`, and an ordinary prose description of the protected action is rejected.

Consequence: an agent cannot infer the complete machine data contract from its owning guide. This is a bounded integration blocker for claiming the lesson-creation workflow is documented and verified. State the accepted metadata fields in this lesson-specific source; this is not a general writing-style policy.

Resolution: reread the coordinator's revised §3 and the parser together. The guide now declares `work_scope` and `phase` frontmatter, distinguishes portability `scope: project`, and documents the accepted `<critical>` scope/phase alternative. These meanings and phase values match the parser. The paragraph explicitly limits the fields to lesson selection and validation, leaving incident prose unconstrained. G1 is closed.

### G2 — Role gate exceeds the documented section contract

Evidence: `guide/general/role-selection.md` §3 gives semantic responsibilities and mandates §6 for the checking-role entry point. The current verifier additionally rejects a role without each numbered section §1 through §5. The original role guide explicitly separated required meanings from a fixed section count.

Consequence: a legitimate project role with all required meanings and §6 completion criteria can fail an undocumented layout requirement. Align the verifier with the actual §6 routing contract and check semantic completeness by review. Alternatively, an intentional additional machine schema needs an explicit scoped requirement, but no runtime consumer for §1–§5 was established in this review.

Resolution: at the coordinator's explicit request, the tooling owner removed the undocumented §1–§5 gate. A new fixture accepts a project role expressed in ordinary prose with its required §6 and rejects the same role when §6 is missing. The 33-test tooling suite passes with one privileged symlink skip, and the live guidance passes verification for 37 Markdown files. G2 is closed. This repair changes the gate to match the reviewed guidance; it does not add a layout rule.

## Acceptance boundary

The independent source and absence-of-global-style review is clean within the inspected corpus. G1 and G2 concerned agreement between guidance and the record gates, not a discovered global prose policy; both are now resolved. No remaining blocker was found in this bounded guidance review. This review does not prove future prose quality, task compliance, native custom-agent support, or fresh desktop loading; those require their corresponding behavioral evidence.

## Final record-contract addendum

Independently reread the later lesson-router paragraph in lesson-capture §3 against `table_rows` and `typed_records`. The documented plain or backtick-wrapped filename keys match the parser, which does not parse Markdown links as store keys. Comma-separated checking filenames, empty or dash optional values, and paired-guide paths with an optional section identifier match the implemented handling. This clarification supplies the machine contract without imposing a form on the prose in a lesson.

Independently reread the later decision paragraph in decision-journal §3 against the common `verify` frontmatter check and decision-specific parser. Requiring `scope: project` first matches the current anchored frontmatter check, while `class`, `subject`, `anchor` and optional `supersedes` remain separate decision fields. This resolves the documented-creation-path ambiguity that could omit the portability declaration.

No new inconsistency was found in these two additions. The coordinator reports a separate actual CLI record workflow with 41 files passing verification; this review confirms source/parser agreement and does not relabel that coordinator-run runtime test as independently executed here.
