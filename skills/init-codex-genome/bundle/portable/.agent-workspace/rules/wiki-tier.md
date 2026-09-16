---
scope: portable
---

# Established knowledge about project subjects

## §1 Activate knowledge storage deliberately

The wiki is an optional record of claims established about material a project investigates. It is separate from working-method lessons, governing instructions and finished deliverables. Use it when a later task would otherwise repeat the same lookup, not to store every incidental observation.

Before activating claims, the project declares the subjects, allowed source material and claim classes in `.agent-workspace/wiki/index.md`. Each class states what evidence it requires. An empty inactive router is valid and does not authorize invented domain values.

The router's class declaration table uses the columns `class` and `required evidence`. It may be empty while the wiki is inactive. Each claim's class must refer to a declared row; the row's evidence obligations remain applicable even when the installed verifier checks only declaration and record structure.

## §2 Look up the question before investigating

Read the wiki router before investigating its registered subjects. Select a cluster by the question it answers, inspect applicable claims and decide whether their evidence remains sufficient for the present work. End the investigation by recording established knowledge when it belongs here. An investigation that establishes nothing creates no sourced claim.

A cluster groups a lookup topic under `.agent-workspace/wiki/<subject>/`. Register a real Markdown link to each cluster in the router in the same change that creates it. Search by subject and evidence locator before adding a claim; different questions can uncover the same fact.

## §3 Preserve a claim's identity and data

Each cluster has one claim table with columns `id`, `claim`, `class`, `confidence` and `evidence`. These columns are a storage contract for wiki records, not a format for unrelated outputs. Give each claim an identifier unique across this wiki, retain it when wording changes and resolve collisions explicitly during merges.

Use `hypothesis` until every evidence obligation of the declared class is satisfied. Use `sourced` only when that evidence has been obtained and checked. A hypothesis can guide research but cannot answer the lookup as established fact.

## §4 Record evidence that can be revisited

For source-text evidence, retain the source path, location and exact anchor needed to find it again. Resolve paths from the project-defined source root in the wiki router. For absence evidence, retain the exact query, searched scope and expected counterexample. For stored data, retain the dataset, object, field and query. For a running system, retain the relevant account or session context, entry point and observation without disclosing secrets.

Keep distinct evidence items distinguishable and retain every cited source location. Compare recorded and observed anchor locations within the cited file, including missing and extra positions. A match in another file does not verify that locator. Decode source text with the project's declared encodings when required.

Transient counts, sizes or measurements belong in dated task evidence rather than durable claim text when the observation can become stale without a structural source change. A locator check can show text still exists; it cannot prove its interpretation or that a query was rerun.

## §5 Resolve contradictions before reuse

Before a claim supports a deliverable, compare it with the relevant current evidence. Stop the dependent conclusion and resolve a contradiction when found, correcting the wiki in the same turn. An old confidence label does not defeat new evidence.

Update an existing fact in place instead of adding duplicate claims. Remove an obsolete claim after resolving internal references. Git retains prior content. References from outside the wiki point to clusters, while references to individual claim identifiers remain within the wiki so internal corrections do not strand external artifacts.

## §6 Preserve knowledge during merges

Compare claim identifiers in each merge parent with the result. Resolve collisions with a new identifier for the later record and update its internal references. An intentional removal needs an explicit resolution; silent loss is not successful conservation. Ordinary deletion on one branch and preserving both parents' knowledge are different operations.

Do not move or overwrite another genome's wiki during Codex adoption. Import selected knowledge only with provenance, identifier mapping and reference checks. The original store remains under its existing ownership.

## §7 Distinguish checks from truth

Validate the router links, record structure, identifier uniqueness, declared class and evidence required by that class. Check which parts an installed verifier actually performs; perform the remaining obligations explicitly. Do not invent a command or assume the availability of an ID allocator.

No structural success establishes that a cited source is authoritative, that an absence query was rerun or that a runtime observation is current. Retain those limits when reporting verification. Configure automation only when its scope and effective behavior have been tested.
