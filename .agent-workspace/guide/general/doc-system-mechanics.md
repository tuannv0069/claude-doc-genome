---
scope: portable
---

# Maintaining the instruction network

This guide explains how to connect and check the files whose placement is governed by `.claude/rules/doc-organization.md`. Use it when creating or changing references, guide areas or routers.

## §2 Stable references

Give each independently referenced requirement a stable section identifier. A reference such as `.agent-workspace/guide/general/decision-journal.md` §2 identifies both the owning file and the relevant requirement. A line number or section title is unsuitable as a lasting instruction reference because an unrelated edit can change it.

Keep portable identifiers unchanged when reorganizing a file. References may exist in other projects that cannot be updated with this repository. A retired portable identifier remains as a `(retired)` marker and is not assigned to another requirement. Project identifiers can change when all affected references change with them.

An existing tagged section may serve as an anchor where a file has no section identifiers. Before replacing such tags, find their consumers and update them together. A visible heading and a parser's identifier are different contracts; verify both when a tool reads the structure.

## §3 Apply ownership to concrete cases

If several agents need the same validation rule, define it in the guide that owns the validation and have each agent refer to that section. Repeating the complete rule in every agent would give a later editor several places to update and no reliable way to know which one is authoritative.

A procedure used by only one agent can remain in that agent. For example, the order in which it gathers evidence and returns a result belongs to its own workflow. Sharing a procedure is useful when another capability needs the same procedure, not merely because both files contain ordered work.

A detection catalog can store the symptom or search pattern that identifies a potential problem. Its remedy points to the owning rule. The catalog therefore helps find a requirement without becoming another version of it.

## §5 Check more than one failure mode

The author checks ownership and assigns stable identifiers before introducing references. A reviewer looks for duplicated rules, unresolved conflicts and guidance that a task cannot reach. Automated checks can detect missing paths, missing identifiers and known repeated material. Use these checks together; a string-matching tool cannot establish that two differently worded instructions mean the same thing.

When a check reports a possible defect, inspect the relevant source and its consumers before changing the rule. A false match in an illustration or historical record does not justify deleting active guidance. Conversely, a passing tool cannot prove that all required behavior exists. Follow `review-checklist-method.md` §3 for review and `rule-health.md` §2 for interpreting scanner results.

## §6 Separate mixed responsibilities

Use `.claude/rules/doc-organization.md` §1 to classify information within a file. If it combines a shared requirement, a capability's own procedure and a navigation entry, identify the owner of each part before deciding whether to split it. Keep the references that connect those parts so the resulting workflow remains executable.

The classification of content and the location of a file are separate decisions. A file's folder does not make every statement inside it a rule, and a copied rule does not become routing metadata because it appears in an index. Use `.claude/rules/doc-organization.md` §8.3 for the destination after ownership is clear.

## §7 Organize the guide tree

### §7.1 Areas of work

Each guide belongs to one area that represents a coherent activity, artifact type or subsystem. Use an existing matching area before creating another. Put cross-cutting guidance and small procedures without a separate grouping in `general/`.

When more than five guides in `general/` share the same work axis, move that group into a named area and update its routes and references together. The common axis must be recognizable from the work those files serve. If no coherent grouping exists, leave `general/` flat instead of inventing divisions to satisfy a count.

Create an area or infrastructure directory when its first real file needs it. Do not create empty folders to suggest a future architecture. Guides do not belong directly at the guide-tree root; record any existing exceptions in the root router's migration ledger until they are moved.

### §7.2 Folders within an area

An area with more than five files uses folders to distinguish its responsibilities. The available default grouping is `concepts/` for explanations of how something works, `patterns/` for reusable approaches, `workflow/` for procedures and navigation, and `enforcement/` for checks and their operation.

Use only folders that match the area's actual content. When those defaults do not fit, declare the area's chosen organization in its hub or router entry. Every content file in a grouped area belongs to one of its declared folders.

Keep conceptual guidance independent of procedural or enforcement details. Checks refer to the concepts and requirements they enforce rather than duplicating them. `general/` remains flat because it contains work without a common area axis; it grows a separate area only under §7.1.

### §7.3 Routers and hubs

Each guide tree has one root router named `index.md`. Every guide is reachable either directly from that router or through one area hub. The navigation path contains at most one hub between the router and the guide. If the organization needs another hub level, divide the guide tree into coherent trees with clear entry points instead of extending an opaque chain.

Route `general/` guides directly. A larger area may use a hub or list its guides directly; whichever arrangement it uses, every leaf file must be reachable. A routing entry supplies the condition and target, not another copy of the target's requirements. The project may use a machine-readable table where a verifier consumes it; the required fields then belong to that verifier's data contract.

Register a new guide or area in the same change that creates it. Update the router, hub and incoming references when it moves or is removed. There is no router inside `.claude/rules/`; Claude Code's rule-loading mechanism handles that tier, while `CLAUDE.md` can point to the rules needed for navigation.

## §8.1 Why the network is organized this way

Relevant loading keeps instructions available at the moment of decision without making every task carry every guide. Bounded navigation gives the assistant a predictable route from a task to its source. Work-product discovery uses the different category model in `.claude/rules/doc-organization.md` §11 because a growing collection of deliverables cannot depend on a hand-maintained global list of files.

Areas and categories grow from actual work. Their organization should preserve a recognizable responsibility as content expands. Updating references during a change prevents immediate breakage, while later audits catch defects that those updates missed. Both are needed because an instruction network can become inconsistent even when each file looks reasonable on its own.

The portable bundle transfers proven guidance between projects. Each project keeps its own data and adaptations; comparison and promotion determine which improvements belong in the shared source. A deployed instance and its bundle copy remain distinct artifacts whose synchronization must be checked.
