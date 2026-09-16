---
scope: portable
---

# Ownership and placement of instructions

This rule governs the project's instruction network: its rules, guides, skills, agents, routers and records. Each shared requirement has one authoritative source, and the assistant must be able to reach that source before using it.

## §1 Classify the responsibility

Before adding content, determine what it owns. A substantive rule defines a condition that work must satisfy, such as a data contract or validation requirement. Operational instructions describe how a particular skill or agent performs its work. Routing metadata determines when that capability is selected. A detection catalog identifies symptoms and points to the rule that explains them. An always-loaded guardrail establishes an obligation that must be known before the task can be routed.

Keep a shared substantive rule in its canonical guide or standard. Skills, agents and catalogs refer to that source rather than maintaining their own copies. Keep a capability's own procedure and routing metadata with the capability that uses them. This distinction prevents a change to a shared rule from leaving several incompatible versions in circulation.

The genome owns AI workflow and project governance. Requirements for the voice, wording or presentation of a particular product belong to that product's project-owned instructions and are loaded only for work on that product. They do not become general rules of the genome.

## §2 Refer to stable sections

Use stable section identifiers for references to individual requirements. The reference mechanism and the treatment of retired identifiers are defined in `.agent-workspace/guide/general/doc-system-mechanics.md` §2.

## §4 Copies with distinct operational purposes

The following uses of repeated material are permitted because they have different owners or loading purposes:

- An always-loaded reminder may point to a detailed on-demand rule. The detailed source remains authoritative; the reminder establishes when it must be consulted.
- Routing descriptions belong to their individual skills or agents even when related capabilities use overlapping terminology.
- An example may illustrate different subjects in separate places if neither copy is presented as the shared rule's authoritative definition.
- A distribution bundle contains copies of its deployed portable files. The bundle's comparison and promotion process owns their synchronization.

Outside these cases, resolve repeated requirements by selecting one owner and replacing the other definitions with references. Do not keep conflicting versions merely because they use different words.

## §5 Check the instruction network

Use the authoring, review and automated checks in `.agent-workspace/guide/general/doc-system-mechanics.md` §5 to find duplicate requirements and broken references.

## §6 Apply the classification

Use §1 to identify the content's responsibility and §8.3 to choose its location. `.agent-workspace/guide/general/doc-system-mechanics.md` §6 explains how those decisions interact when a file contains several kinds of information.

## §7 Organize guides by the work they serve

Every guide belongs to an area and is reachable from the guide router. Areas group a shared activity, artifact type or subsystem; `general/` contains guidance that crosses those areas or has not developed a separate grouping. Read `.agent-workspace/guide/general/doc-system-mechanics.md` §7 before creating, moving or renaming a guide.

## §8 Choose where instructions are loaded

### §8.1 Design principles

The network is organized around relevant loading, bounded navigation, growth from actual work, preventive checks and the transfer of proven improvements. These principles are developed in `.agent-workspace/guide/general/doc-system-mechanics.md` §8.1.

### §8.2 Loading mechanisms

A rule without `paths:` in its frontmatter belongs to the always-loaded set. Use that set for obligations needed before a task's file or specialized guide is known. A rule with `paths:` applies to the declared file patterns. Use the guide tree for instructions selected by a task router or trigger.

Choose the loading mechanism from the work's needs, not from a file's length. Keep project identity and routing in `CLAUDE.md` under `claude-md-standards.md` §1. Inspect the installed environment when a change relies on how these mechanisms load; do not infer runtime loading solely from where a file was placed.

### §8.3 Placement decisions

Evaluate the following destinations in order and use the first that matches the content's responsibility.

1. A reusable workflow with a trigger, dependent operations and a verifiable result belongs in a skill under `skill-md-standards.md` §1.
2. A specialist that runs as a separate agent belongs in an agent definition under `subagent-standards.md` §1.
3. An obligation needed in every task belongs in the always-loaded rule set, with a reference to detailed guidance when needed.
4. A standard that applies when working on a particular file type belongs in a path-scoped rule.
5. A record of a failed working method belongs in the relevant lesson store under `.agent-workspace/guide/general/lesson-capture.md` §1. An incident does not become a guide merely because it is useful to read later.
6. Reusable project guidance selected by task belongs in the guide tree. Register it according to §10.
7. A finished project work product belongs in the project's work-product area under §11. Established claims about subject material may belong in the optional wiki under `wiki-tier.md` §1; that tier has its own evidence contract.
8. A navigation entry belongs in the router or project entry point that selects the target. It does not need a second content file.

Temporary plans, evidence and intermediate files belong in the task workspace under `.agent-workspace/guide/general/orchestration-policy.md` §4. Move durable deliverables to their project-owned destination when they are ready.

## §9 Separate portable guidance from project data

Rules and guides declare `scope: portable` or `scope: project` in frontmatter. Portable content must remain applicable when copied to another project. Project content may contain that project's identities, source locations, tooling choices and operating values.

Keep instance-specific data in project-owned configuration or routers. Paths that are part of the genome's deployed structure, such as `.agent-workspace/guide/`, are shared conventions and may appear in portable guidance. A dependency on an optional tool or service must be identified as optional and checked before use; do not assume that another project has the author's integrations installed.

A skill or agent uses the metadata its platform supports. Its membership in the portable distribution is recorded by the bundle map rather than by adding unsupported fields to its frontmatter. If portability has not been established, keep the content project-owned until it has been evaluated.

Portable section identifiers remain stable because other projects may reference them. Project section identifiers may change only when every affected reference is updated in the same change. Language choices for a project or deliverable belong to that project; they are not imposed by portability metadata.

## §10 Maintain identity, reachability and links

Use a stable file identity that describes its subject. Extend the existing canonical source when the subject already has one. Give a new source a stable section identifier before other files depend on it. Each documentation tree uses `index.md` as its router; a repository `README.md` remains its human entry point.

Register every on-demand content file in its router, directly or through the permitted hub structure in `.agent-workspace/guide/general/doc-system-mechanics.md` §7.3. Add an always-loaded trigger only when the assistant could otherwise act incorrectly before consulting that router. This interception test asks what decision would be missed, when it occurs and why an existing route does not already reach the guidance.

There are three kinds of observable trigger. Their conditions are evaluated at different points:

| Trigger kind | Information used to decide whether it applies |
|---|---|
| Message-triggered | A keyword, tool name, code symbol, file pattern or other explicit signal in the user's message. |
| Work-state | A count or state the assistant can observe while performing the work. |
| Action-triggered | The operation about to be performed and its concrete object, evaluated before the tool call. |

A trigger must identify a condition the assistant can decide before the required reading. Labels such as a complex task, a multi-step task or work that needs deep analysis do not supply an observable condition by themselves. For an action trigger, name both the action and the class of artifact or resource involved. The trigger's wording may vary; its decision input and target must remain unambiguous.

Record the interception test and the reason for adding or omitting a trigger when that decision requires a journal entry. Act within the user's existing authorization. Ask for a decision only when the proposed change exceeds that authority or requires information the assistant cannot establish; do not require another confirmation for routine routing work already delegated.

When adding, renaming, moving or deleting a content file, update its router entries, triggers, links and section references in the same change. Search for the old identity after a move or deletion. Resolve every operational reference; historical evidence may retain the old path when it is clearly part of the record rather than an instruction to read that file now.

The guide router records project placement data in its §1, including any unresolved migration entries and their intended destinations. A migration entry is tracked work to complete, not a permanent exemption from ownership or reachability.

## §11 Keep work products separate from guidance

The guide tree explains how the assistant performs work. The project's work-product area holds finished specifications, designs, research and reports. Do not turn a work-product directory into another shared rule tree, or store deliverables among operational guides.

Use an existing work-product category when it fits. If a new category is needed, register it in `docs/index.md` in the same change. That router identifies categories rather than maintaining a list of every delivered file; categories may use their own index or discovery convention.

The optional wiki and temporary task workspace serve different purposes and follow their own procedures. Their presence does not make every file under `.agent-workspace/` a finished project deliverable.

## §12 Remove requirements that no longer apply

When a rule is narrowed or retired, remove the superseded instructions from the active source. Keep a retired portable section's identifier with a `(retired)` marker when existing references require the identifier to survive. Do not reuse it for an unrelated requirement.

Record the reason for a qualifying rule change in the decision journal under `.agent-workspace/guide/general/decision-journal.md` §2. Git and the record stores preserve history; the active rule describes the obligations that apply now. A lack of deleted lines may prompt a review, but it is not by itself proof that a rule should be removed.
