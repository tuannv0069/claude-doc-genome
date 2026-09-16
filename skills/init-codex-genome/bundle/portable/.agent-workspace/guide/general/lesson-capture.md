---
scope: portable
---

# Learning from a failed working method

## §1 Separate a lesson from other knowledge

A lesson records an incident in how work was performed and a better method supported by its evidence. It is not automatically a binding new rule. Store project facts with their work products or established-knowledge records, and preserve user preferences in the project source that owns them.

Lesson stores live under `.agent-workspace/lessons/` and are organized by the action they protect. Raw incidents remain distinct from curated guides.

## §2 Capture the failure while evidence is available

Record a repeatable method failure when the user corrects the approach or rejects an output, when a check gives a confidently wrong result, when a fix disproves the diagnosis, or when existing guidance repeatedly fails to prevent a defect. Do so during the same turn, without a separate permission request for ordinary lesson recording.

Identify the situation, the failed method, why it seemed plausible, the better method, evidence and recurrence count. The record needs these meanings but need not follow a sentence pattern. If an equivalent lesson exists, preserve its identity and increment its count rather than creating another copy.

## §3 Route stores by work and phase

Register a store in `.agent-workspace/lessons/index.md` §1 when creating it. Its table has `file`, `work type`, `paired guide` and `checks` columns. Record the action protected in a `work_scope` frontmatter field and the prevention phase in a `phase` field. The frontmatter field `scope: project` classifies portability; it does not identify the protected action. The phase is one of `writing`, `reviewing`, `answering`, `building-gate`, `orchestrating`, `investigating` or `operating`. Split stores whose lessons need different phases.

The verifier also accepts these two values as separate `scope:` and `phase:` lines inside a `<critical>` block. In that form, `scope:` describes the protected action and is distinct from the file's frontmatter scope. Use one form consistently within a store. These fields support lesson selection and validation; they do not prescribe the prose used to describe an incident.

In the router table, the `file` cell contains the store's filename, either plain or in backticks. The `checks` cell contains the same kind of filenames separated by commas. These cells are machine keys rather than Markdown links. The `paired guide` cell contains a file path and may include its section identifier. Leave an unused optional cell empty or use a dash.

Choose the phase that could prevent the failure, not merely the phase that discovered it. If production and review both need the lesson, keep one record in the producing phase and let a checking store reach it through `checks`. Keep checking relationships acyclic. A paired guide is optional; a new store does not require an invented guide.

## §4 Read before acting

At the start of each new task, read the lesson router using a file-reading tool. Match the action to the work types, read every matching store and then its named checking stores for one hop only. An empty router or no matching row is valid. Do not infer that no row matches before reading it.

Reuse an unchanged lookup while the work type stays the same. Repeat selection when the action changes. Pass matched paths and checking stores to a delegate. In coordinated work, the delegate returns a lesson candidate and the coordinator writes shared records.

## §5 Promote an established requirement

The first occurrence creates evidence. Recurrence calls for evaluating whether a requirement belongs in the guide for that action. A third occurrence prompts evaluation of a machine check when the condition is reliably decidable; a clear mechanically decidable failure may justify one sooner.

Distill the supported requirement rather than copying incident history into a guide. Test a proposed detector with failing and legitimate cases. Repetition alone does not justify adding an always-loaded obligation; placement still follows `.agent-workspace/rules/doc-organization.md` §6.

## §6 Maintain records and references

Keep a store's declared scope consistent with its records. Split by work responsibility rather than file length. Preserve evidence and recurrence counts when moving records, and update live references. Do not rewrite historical task evidence to make earlier paths appear current. A guide may point to its paired store, while the task-start router remains the normal entry point.
