---
scope: portable
---

<critical>
scope: ownership and placement in the project's instruction network — rules, guides, skills, agents, routers and records, and the project's work-product area.
never: keep a second authoritative copy of a shared requirement, reference a rule by file path alone, or leave a link whose target does not exist.
note: a substantive rule lives in one canonical source with a stable §ID; new content is placed through §8.3; every on-demand file is reachable through its router (§10).
</critical>

# Ownership and placement of instructions

This rule governs the project's instruction network: its rules, guides, skills, agents, routers and records. Each shared requirement has one authoritative source, and the assistant must be able to reach that source before using it.

## §1 Classify the responsibility

Before adding content, determine what it owns. A substantive rule defines a condition that work must satisfy, such as a data contract or validation requirement. Operational instructions describe how a particular skill or agent performs its work. Routing metadata determines when that capability is selected. A detection catalog identifies symptoms and points to the rule that explains them. An always-loaded guardrail establishes an obligation that must be known before the task can be routed.

This distinction prevents a change to a shared rule from leaving several incompatible versions in circulation. The genome owns AI workflow and project governance. Requirements for the voice, wording or presentation of a particular product belong to that product's project-owned instructions and are loaded only for work on that product; they do not become general rules of the genome.

<rules section="ALWAYS">
- Keep a shared substantive rule in its canonical guide or standard, and let skills, agents and catalogs refer to that source.
- Keep a capability's own procedure and routing metadata with the capability that uses them.
- When a topic has no canonical source yet, create one with a stable identifier before referring to it.
</rules>

<rules section="NEVER">
- Inline a substantive rule, such as a canonical code shape, a property list, a ❌/✅ snippet or a fix template, in an agent, skill, catalog or index.
- Restate a rule's content where a reference suffices.
</rules>

## §2 Refer to stable sections

The reference mechanism and the treatment of retired identifiers are defined in `.agent-workspace/guide/general/doc-system-mechanics.md` §2.

<rules section="ALWAYS">
- Use a stable section identifier for a reference to an individual requirement.
- When a project identifier is renumbered, update every referrer in the same change.
</rules>

<rules section="NEVER">
- Reference a rule by file path alone; section order changes silently.
</rules>

## §4 Copies with distinct operational purposes

The following uses of repeated material are permitted because they have different owners or loading purposes:

- An always-loaded reminder may point to a detailed on-demand rule. The detailed source remains authoritative; the reminder establishes when it must be consulted.
- Routing descriptions belong to their individual skills or agents even when related capabilities use overlapping terminology.
- An example may illustrate different subjects in separate places if neither copy is presented as the shared rule's authoritative definition.
- A distribution bundle contains copies of its deployed portable files. The bundle's comparison and promotion process owns their synchronization.

<rules section="ALWAYS">
- Outside these cases, resolve a repeated requirement by selecting one owner and replacing the other definitions with references.
</rules>

<rules section="NEVER">
- Keep conflicting versions of a requirement merely because they use different words.
</rules>

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

A rule without `paths:` in its frontmatter belongs to the always-loaded set. A rule with `paths:` applies to the declared file patterns. The guide tree holds instructions selected by a task router or trigger. Project identity and routing stay in `CLAUDE.md` under `claude-md-standards.md` §1.

<rules section="ALWAYS">
- Use the always-loaded set only for obligations needed before a task's file or specialized guide is known.
- Choose the loading mechanism from the work's needs, not from a file's length.
- Inspect the installed environment when a change relies on how these mechanisms load.
</rules>

<rules section="NEVER">
- Infer runtime loading solely from where a file was placed.
</rules>

### §8.3 Placement decisions

Evaluate the following destinations in order and use the first that matches the content's responsibility.

1. A reusable workflow with a trigger, dependent operations and a verifiable result belongs in a skill under `skill-md-standards.md` §1.
2. A specialist that runs as a separate agent belongs in an agent definition under `subagent-standards.md` §1.
3. An obligation needed in every task belongs in the always-loaded rule set, with a reference to detailed guidance when needed.
4. A standard that applies when working on a particular file type belongs in a path-scoped rule.
5. A record of a failed working method belongs in the relevant lesson store under `.agent-workspace/guide/general/lesson-capture.md` §1. An incident does not become a guide merely because it is useful to read later.
6. Reusable project guidance selected by task belongs in the guide tree. Register it according to §10.
7. A finished project work product belongs in the project's work-product area under §11, and so do the taste notes and annotated references of creative work (`.agent-workspace/guide/general/creative-work.md` §5). Established claims about subject material may belong in the optional wiki under `wiki-tier.md` §1; that tier has its own evidence contract.
8. A navigation entry belongs in the router or project entry point that selects the target. It does not need a second content file.

An executable script or tool is not instruction content and is placed under `.agent-workspace/guide/general/tooling.md` §1: in the task workspace, in the package of the skill that owns it, or in a tool group.

Temporary plans, evidence and intermediate files belong in the task workspace under `.agent-workspace/guide/general/orchestration-policy.md` §4. Move durable deliverables to their project-owned destination when they are ready.

Every destination above is inside the repository. An assistant's harness memory (for Claude Code, the per-project directory under the user's home) exists on one machine only, is not versioned and is not read by another agent, so a correction, working preference or project fact stored there is lost to everyone else who works on the project.

<rules section="NEVER">
- Record a correction, a working preference, a project fact or any other guidance the project must keep in the assistant's harness memory or in any other store outside the repository; place it through the list above, even when the harness prompt invites a memory entry.
</rules>


## §9 Separate portable guidance from project data

Rules and guides declare `scope: portable` or `scope: project` in frontmatter. Portable content must remain applicable when copied to another project. Project content may contain that project's identities, source locations, tooling choices and operating values. Paths that are part of the genome's deployed structure, such as `.agent-workspace/guide/`, are shared conventions and may appear in portable guidance.

A skill or agent uses the metadata its platform supports. Its membership in the portable distribution is recorded by the bundle map rather than by adding unsupported fields to its frontmatter. Language choices for a project or deliverable belong to that project; they are not imposed by portability metadata.

<rules section="ALWAYS">
- Keep instance-specific data in project-owned configuration or routers.
- Identify a dependency on an optional tool or service as optional and check it before use.
- Keep the content project-owned until its portability has been evaluated.
- When a project section identifier changes, update every affected reference in the same change.
</rules>

<rules section="NEVER">
- Assume that another project has the author's integrations installed.
- Change a portable section identifier; other projects may reference it.
</rules>

## §10 Maintain identity, reachability and links

Each documentation tree uses `index.md` as its router; a repository `README.md` remains its human entry point. An always-loaded trigger is justified only by the interception test: what decision would be missed, when it occurs and why an existing route does not already reach the guidance.

There are three kinds of observable trigger. Their conditions are evaluated at different points:

| Trigger kind | Information used to decide whether it applies |
|---|---|
| Message-triggered | A keyword, tool name, code symbol, file pattern or other explicit signal in the user's message. |
| Work-state | A count or state the assistant can observe while performing the work. |
| Action-triggered | The operation about to be performed and its concrete object, evaluated before the tool call. |

The guide router records project placement data in its §1, including any unresolved migration entries and their intended destinations. A migration entry is tracked work to complete, not a permanent exemption from ownership or reachability.

<rules section="ALWAYS">
- Use a stable file identity that describes its subject, and extend the existing canonical source when the subject already has one.
- Give a new source a stable section identifier before other files depend on it.
- Register every on-demand content file in its router, directly or through the permitted hub structure in `.agent-workspace/guide/general/doc-system-mechanics.md` §7.3.
- Add an always-loaded trigger only when the assistant could otherwise act incorrectly before consulting that router, and record the interception test when the decision requires a journal entry.
- Give a trigger a condition the assistant can decide before the required reading; for an action trigger, name both the action and the class of artifact or resource involved.
- When adding, renaming, moving or deleting a content file, update its router entries, triggers, links and section references in the same change, and search for the old identity after a move or deletion.
- Act within the user's existing authorization, and ask for a decision only when the proposed change exceeds it or requires information the assistant cannot establish.
</rules>

<rules section="NEVER">
- Word a trigger as a task class such as a complex task, a multi-step task or work that needs deep analysis; those supply no observable condition.
- Commit a link whose target does not exist.
- Link, cite or anchor a committed file to a path under `.agent-workspace/tasks/`; that workspace is uncommitted and may be deleted at any time, so content worth keeping is moved to its work-product destination first and the link points there.
- Leave an operational reference unresolved after a move or deletion; only historical evidence may retain the old path when it is clearly part of the record.
</rules>

<example type="trigger_condition">
input: a guide that must be read before the assistant edits a machine verification gate
❌ before a complex verification task, read the guide; the assistant must classify the task first
✅ before writing or editing a `test_*.py` or `verify_*.py` file, read the guide; the action and its object are observable before the call
</example>

## §11 Keep work products separate from guidance

The guide tree explains how the assistant performs work. The project's work-product area holds finished specifications, designs, research and reports. The optional wiki and temporary task workspace serve different purposes and follow their own procedures; their presence does not make every file under `.agent-workspace/` a finished project deliverable.

<rules section="ALWAYS">
- Use an existing work-product category when it fits.
- When a new category is needed, register it in `docs/index.md` in the same change.
- Keep the router at category level; categories may use their own index or discovery convention.
</rules>

<rules section="NEVER">
- Turn a work-product directory into another shared rule tree, or store deliverables among operational guides.
- Maintain a list of every delivered file in the category router.
</rules>

### §11.1 A category may hold rule-bearing content

A work-product category can include a small amount of content that states the law for the shape of that category's own deliverables — a required structure, a section a review cites, a criterion a gate checks — rather than a finished deliverable itself. This differs from a guide-tree rule: rule-bearing content applies only within its own category and has no meaning apart from that category's deliverables, while a guide-tree rule states a method usable independently of any one deliverable.

Mark rule-bearing content with a `_` prefix on its file or folder name; deliverable content carries no prefix. The prefix is the only registration this distinction needs.

Rule-bearing content still follows §1 to establish what it owns and §2 for a stable section identifier, and a review or gate that depends on it must cite that identifier rather than restate the requirement. To load it automatically when a matching deliverable is touched, bind it from a project-scoped rule whose `paths:` frontmatter (§8.2) points to the deliverable's location; that rule stays a thin pointer to the identifier, not a restatement. Reach a single project's paths through that project-scoped rule, never by widening a portable rule's own `paths:`. The category list itself remains `scope: project`; the rule that a category may hold its own law this way is portable.

## §12 Remove requirements that no longer apply

Git and the record stores preserve history; the active rule describes the obligations that apply now. A lack of deleted lines may prompt a review, but it is not by itself proof that a rule should be removed.

<rules section="ALWAYS">
- When a rule is narrowed or retired, remove the superseded instructions from the active source in the same change.
- Keep a retired portable section's identifier with a `(retired)` marker when existing references require the identifier to survive.
- Record the reason for a qualifying rule change in the decision journal under `.agent-workspace/guide/general/decision-journal.md` §2.
</rules>

<rules section="NEVER">
- Leave the superseded sentence beside the new one; the next reader cannot tell which binds.
- Reuse a retired identifier for an unrelated requirement.
- Write change history into the body of a rule, guide or standard; the record stores own that job.
</rules>
