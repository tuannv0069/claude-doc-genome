---
scope: portable
---

# Maintaining the instruction network

## §1 Assign authority before splitting files

Use `.agent-workspace/rules/doc-organization.md` §1 to identify the owner of a shared requirement, a local procedure and a routing condition. A file can contain several responsibilities, but moving a copied rule into a router does not make it routing metadata. Split responsibilities when they have distinct owners and preserve the references that connect the workflow.

## §2 Keep references stable

Refer to a requirement by its owning file and stable section. Line numbers and heading wording may change without a semantic change. Preserve portable identifiers across reorganizations and retain retired identifiers where external consumers depend on them. A historical identifier is not available for an unrelated new rule.

When a parser depends on a tagged field or table, treat that shape as a data contract in addition to the visible headings. Coordinate parser, fixtures and records before changing it. Human-readable prose alone does not prove the parser sees the intended data.

## §3 Organize areas around real work

Each guide belongs to one work area and is reachable from the root guide router, directly or through one area hub. Keep `general/` for cross-cutting procedures without a coherent separate axis. When a group develops a recognizable responsibility, create an area and describe its organization in its hub. Do not create empty folders or force unrelated procedures into a category just to balance file counts.

Keep concepts, procedures and enforcement connected without duplicating their requirements. Route general guides directly. A reader should not need a chain of nested hubs to find the governing leaf. Use a separate clearly entered tree when the scope truly requires one.

The rules directory has no host-provided discovery guarantee. Its files need explicit entry-point triggers or guide routes. The project's router records placement data and any unresolved migration with its intended destination.

## §4 Check the network from several directions

An author establishes ownership and stable references. A reviewer examines duplicate meanings, contradictions and guidance reached too late. A program can find missing paths, missing sections and selected structural conditions. None of these checks substitutes for the others.

For a reported broken reference, inspect its target and consumer before editing. An example or historical path may be valid evidence rather than a live dependency. A successful path check does not show that the referring sentence still has the correct meaning after the target changes.

## §5 Maintain both prevention and repair

Update references during the change that adds, moves or removes content. Later audits detect mistakes those updates missed. Keep each scan's scope and unresolved findings so a passing check is not interpreted as coverage of unexamined material.

Selective loading, bounded routes and growth from actual work make the network usable. Evaluate useful improvements from deployed Codex instances and edit the owning source inside the initialization skill. Its bundle is the authored source; no separate live tree needs synchronization. This process is independent of other genome products; differences between products are not drift to repair.

## §6 Separate content responsibilities

Classify shared requirements, local workflow, routing metadata, detection signals and always-loaded guardrails before choosing a file. A substantive requirement has one source of truth. Skills and routers point to that source instead of restating it, while a harness adapter keeps only the operational detail needed by that harness.

## §7 Organize the guide tree

Use one directory for each coherent area of work and keep cross-cutting procedures in `general/`. A guide belongs to one area even when several kinds of work use it. Add another area only when the project has a real routing axis for it.

### §7.3 Keep every guide reachable

Register each guide in the root router or in one area hub. A behavior-changing guide also needs a trigger that reaches it before the governed action. When a file moves or disappears, update its router, triggers and incoming stable references in the same change.

## §8.1 Treat the genome as a connected network

The usefulness of a guide depends on both its content and the paths that reach it. Keep common entry points small, load detailed procedures when their condition appears, and grow the network from observed work. A file with no route or trigger cannot reliably affect agent behavior.
