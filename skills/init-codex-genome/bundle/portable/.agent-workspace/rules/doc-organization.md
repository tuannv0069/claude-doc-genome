---
scope: portable
---

# Ownership and placement of Codex guidance

## §1 Identify what the content owns

A shared requirement has one authoritative source within the Codex genome. A guide or standard owns that requirement; a skill or specialist agent owns its own procedure; a router owns the condition and destination used to find it. Detection catalogs may identify symptoms and point to the source that explains the correction. Refer to shared requirements instead of repeating them inside every consumer.

The genome governs work and project responsibilities. It does not define the voice, wording, length or presentation of general responses and deliverables. Requirements for a particular output belong to the project instructions for that output and are reached only for work within that scope.

The Codex and Claude products have independent sources and maintenance. A corresponding requirement in the other product is not a runtime dependency, synchronization target or authority over this product. Shared project work products may still be used by both.

## §2 Maintain stable references

References to individual requirements identify the owning file and stable section. Keep portable section identifiers stable, including a bare retired marker when an identifier must survive. Do not reuse a retired identifier for a different requirement. Project identifiers may change when all current consumers are updated together. See `.agent-workspace/guide/general/doc-system-mechanics.md` §2.

## §3 Distinguish legitimate copies

An entry-point reminder may establish the obligation to read a detailed source. Routing descriptions belong to their capabilities. An example may illustrate separate subjects without becoming a second authority. The initialization skill owns the authored portable sources; project installations and built packages contain deployment copies of those sources. Those copies do not require a second authoring tree. Other duplicated requirements need a single owner and references from their consumers.

## §4 Choose the destination

Place a repeatable workflow with an identifiable trigger, dependent operations and a checkable result in a skill. Place an independently invoked specialist in an agent definition. Put obligations needed before routing and the conditions for reading further guidance in `AGENTS.md`. Put reusable standards under `.agent-workspace/rules/` and task procedures under `.agent-workspace/guide/`.

File-specific standards are reached by explicit action triggers. Markdown files in the rules directory do not load themselves, and nested AGENTS discovery is not equivalent to selecting a rule from the path of a file being edited. Every standard needs a route that operates before the action it governs.

An incident about a failed working method belongs in the lesson store. A reasoned historical choice belongs in the decision journal. Established subject knowledge belongs in the wiki only when that project uses its evidence contract. Finished specifications, research and other deliverables belong in the project's work-product area. Temporary plans and evidence belong under `.agent-workspace/tasks/<task-slug>/`.

## §5 Separate reusable requirements from project data

Rules and guides declare `scope: portable` or `scope: project`. Portable files may refer to the Codex genome's invariant deployed paths but do not contain instance-specific project names, ports, task identifiers, budgets or installed integrations. Project routers and configuration own those values. Skills and agent definitions use the metadata their Codex client supports; the bundle map records their distribution membership.

Do not assume an optional command, model, service or plugin exists in every project. Identify the dependency and verify availability before using it. Portability does not impose a language choice on a project or its deliverables.

## §6 Preserve reachability

Use a subject-based file identity and extend the canonical source when it already owns the subject. Give a new source stable sections before referring to them. Documentation trees use a file named index.md for routing; a README serves human discovery.

Every guide is reached directly from the guide router or through one area hub. Every rule is reached from an entry-point trigger or a registered guide route. A new always-loaded trigger needs an interception reason: without it, what wrong decision could occur before an existing route would be consulted? A message signal, an observed work state, or the assistant's next action and concrete object can provide a decidable condition. An abstract label such as difficult work does not.

Keep the reasoning for consequential routing changes under `.agent-workspace/guide/general/decision-journal.md` §1. Existing task authorization covers routine routing work; a trigger change is not automatically a new permission barrier.

## §7 Keep the network current

When adding, moving, renaming or removing content, update routers, triggers, links and section references in the same change. Search for the old identity and resolve every current operational reference. Historical records may retain historical paths when their role is clear.

Remove a superseded requirement from the active source. The decision journal and Git retain the history; the rule states what applies now. The guide router's §1 records unresolved placement migrations and their destinations, rather than granting permanent exemptions.

## §8 Keep deliverables and guidance separate

Use the project's existing work-product categories. Register a new category in `docs/index.md` when that is the project's work-product router. The router identifies categories; individual categories can provide their own discovery mechanism. Do not introduce output-style requirements through a placement rule.

The wiki and temporary task workspace have their own lifecycles. Their presence under the agent workspace does not make that workspace the destination for finished deliverables.
