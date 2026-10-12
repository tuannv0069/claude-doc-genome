---
scope: portable
---

<critical>
scope: how the documentation system is wired and checked — the stable-identifier reference mechanism, the shape of the on-demand guide tree (areas, folders, routers) and the layers that catch violations.
never: reference by line number or title, place a content file outside an area, or let a hub point to another hub.
note: `doc-organization.md` decides where content goes and is always loaded; this guide describes how the tree is built and is read when building or wiring something. Its §IDs are inherited from that rule (§2, §3, §5, §6, §7, §8.1) and the gaps stay as they are.
</critical>

# Maintaining the instruction network

This guide explains how to connect and check the files whose placement is governed by `.claude/rules/doc-organization.md`. Use it when creating or changing references, guide areas or routers.

## §2 Stable references

A reference such as `.agent-workspace/guide/general/decision-journal.md` §2 identifies both the owning file and the relevant requirement. A line number or section title is unsuitable as a lasting instruction reference because an unrelated edit can change it. References may exist in other projects that cannot be updated with this repository. A visible heading and a parser's identifier are different contracts.

<rules section="ALWAYS">
- Give each independently referenced requirement a stable section identifier.
- Keep portable identifiers unchanged when reorganizing a file, and leave a retired portable identifier as a `(retired)` marker.
- Change a project identifier only when all affected references change with it.
- Before replacing a tagged section that serves as an anchor, find its consumers and update them together.
- Verify both the visible heading and the parser's identifier when a tool reads the structure.
</rules>

<rules section="NEVER">
- Assign a retired identifier to another requirement.
</rules>

## §3 Apply ownership to concrete cases

If several agents need the same validation rule, define it in the guide that owns the validation and have each agent refer to that section. Repeating the complete rule in every agent would give a later editor several places to update and no reliable way to know which one is authoritative.

A procedure used by only one agent can remain in that agent. For example, the order in which it gathers evidence and returns a result belongs to its own workflow. Sharing a procedure is useful when another capability needs the same procedure, not merely because both files contain ordered work.

A detection catalog can store the symptom or search pattern that identifies a potential problem. Its remedy points to the owning rule. The catalog therefore helps find a requirement without becoming another version of it.

<example type="shared_validation">
input: three agents must apply the same validation rule to their output
❌ copy the complete rule into each agent definition
✅ define the rule once in the guide that owns the validation and have each agent refer to its section
</example>

## §5 Check more than one failure mode

The author checks ownership and assigns stable identifiers before introducing references. A reviewer looks for duplicated rules, unresolved conflicts and guidance that a task cannot reach. Automated checks can detect missing paths, missing identifiers and known repeated material. A string-matching tool cannot establish that two differently worded instructions mean the same thing, and a passing tool cannot prove that all required behavior exists.

<rules section="ALWAYS">
- Use the author's check, the reviewer's check and the automated checks together.
- When a check reports a possible defect, inspect the relevant source and its consumers before changing the rule.
- Follow `review-checklist-method.md` §3 for review and `rule-health.md` §2 for interpreting scanner results.
</rules>

<rules section="NEVER">
- Delete active guidance because of a false match in an illustration or a historical record.
</rules>

## §6 Separate mixed responsibilities

Use `.claude/rules/doc-organization.md` §1 to classify information within a file. If it combines a shared requirement, a capability's own procedure and a navigation entry, identify the owner of each part before deciding whether to split it. Keep the references that connect those parts so the resulting workflow remains executable.

The classification of content and the location of a file are separate decisions. A file's folder does not make every statement inside it a rule, and a copied rule does not become routing metadata because it appears in an index. Use `.claude/rules/doc-organization.md` §8.3 for the destination after ownership is clear.

## §7 Organize the guide tree

### §7.1 Areas of work

An area represents one axis of work: the thing its files share that a reader would name when reaching for them. A stack layer is the most familiar shape, not the required one; an artifact type, a recurring activity or a live subsystem are axes just as valid, and a project with no code has areas too. `general/` holds cross-cutting guidance and small procedures without a separate grouping. Infrastructure directories such as `templates/` or `scripts/` are not areas.

<rules section="ALWAYS">
- Place each guide in exactly one area, using an existing matching area before creating another.
- Put a guide with no matching area in `general/`.
- When more than five guides in `general/` share the same work axis, move that group into a named area and update its routes and references together.
- Create an area or infrastructure directory when its first real file needs it.
- Record any guide that still sits at the guide-tree root in the root router's migration ledger until it is moved.
</rules>

<rules section="NEVER">
- Add a new guide directly at the guide-tree root.
- Design the area shape upfront; areas grow from real work under §8.1.
- Invent divisions in `general/` to satisfy a count when no coherent axis exists.
- Create empty folders to suggest a future architecture.
</rules>

<example type="no_axis">
input: a documentation-only project's `general/` holds eight small guides: release notes, a glossary, a translation checklist, a meeting-notes format and four one-off procedures
❌ split them into two arbitrary folders to get under five; the folder names describe nothing, so nobody can predict where the ninth file goes
✅ leave it flat; when the third translation guide arrives, `translation/` has a real axis and earns the promotion
</example>

### §7.2 Folders within an area

An area with more than five files uses folders to distinguish its responsibilities. The default grouping is `concepts/` for explanations of how something works, `patterns/` for reusable approaches, `workflow/` for procedures and navigation, and `enforcement/` for checks and their operation. `general/` remains flat because it contains work without a common area axis; it grows a separate area only under §7.1.

<rules section="ALWAYS">
- Use only folders that match the area's actual content.
- When the defaults do not fit, declare the area's chosen organization in its hub or router entry.
- Put every content file in a grouped area into one of its declared folders.
- Keep conceptual guidance independent of procedural or enforcement details.
</rules>

<rules section="NEVER">
- Keep an empty default folder for symmetry.
- Duplicate a concept or pattern inside an enforcement file; a check refers to the requirement it enforces.
</rules>

### §7.3 Routers and hubs

Each guide tree has one root router named `index.md`. The navigation path contains at most one hub between the router and the guide. A routing entry supplies the condition and target, not another copy of the target's requirements. The project may use a machine-readable table where a verifier consumes it; the required fields then belong to that verifier's data contract. There is no router inside `.claude/rules/`; Claude Code's rule-loading mechanism handles that tier, while `CLAUDE.md` can point to the rules needed for navigation.

<rules section="ALWAYS">
- Make every guide reachable either directly from the root router or through one area hub.
- Route `general/` guides directly.
- Give a larger area either a hub or a direct list of its guides, so that every leaf file stays reachable.
- Register a new guide or area in the same change that creates it, and update the router, hub and incoming references when it moves or is removed.
- Divide a tree that would need a second hub level into coherent trees with clear entry points.
</rules>

<rules section="NEVER">
- Let a hub point to another hub.
- Put substantive content in a router or hub entry.
- Create a router or index file inside `.claude/rules/`.
</rules>

## §8.1 Why the network is organized this way

Relevant loading keeps instructions available at the moment of decision without making every task carry every guide. Bounded navigation gives the assistant a predictable route from a task to its source. Work-product discovery uses the different category model in `.claude/rules/doc-organization.md` §11 because a growing collection of deliverables cannot depend on a hand-maintained global list of files.

Areas and categories grow from actual work. Their organization should preserve a recognizable responsibility as content expands. Updating references during a change prevents immediate breakage, while later audits catch defects that those updates missed. Both are needed because an instruction network can become inconsistent even when each file looks reasonable on its own.

The portable bundle transfers proven guidance between projects. Each project keeps its own data and adaptations; comparison and promotion determine which improvements belong in the shared source. A deployed instance and its bundle copy remain distinct artifacts whose synchronization must be checked.
