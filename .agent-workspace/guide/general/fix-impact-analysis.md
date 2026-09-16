---
scope: portable
---

# Assessing the impact of a fix

This guide applies to a defect fix when no skill already owns the fixing workflow. It covers code, documentation, rules, configuration, and other artifacts with dependents.

## §1 Establish the scope before editing

Before applying a fix, determine what relies on the part being changed and what could stop working after the change. The defect description is a starting point for investigation, not proof that the requested edit is the correct remedy.

A local change can remove a visible symptom while breaking another consumer. Examine the dependency boundary before deciding that the change is local.

## §2 Finding dependents

For code, inspect callers, importers, shared state, return values, side effects, and persisted data that consumers rely on. For documentation and rules, inspect incoming links, stable-section references, and statements whose meaning depends on the changed requirement. For configuration, inspect the readers of the value and the behavior it controls.

This is the same dependency question across artifact types. The evidence used to answer it changes with the artifact.

## §3 Procedure

1. Confirm the defect and its cause. Reproduce the behavior when execution is available, or trace the relevant evidence for a non-executable artifact. If the cause remains unclear, use `five-why.md` §2.
2. Find the dependents of the proposed change. Determine whether the target is shared, widely referenced, or part of a contract. This search sets the depth of the remaining work.
3. Identify the behavior that each affected consumer expects. Include references whose meaning could change even when their links still resolve.
4. Choose a change that addresses the cause while avoiding unnecessary effects. If a temporary symptom fix is appropriate, record why it was chosen and what limitation remains. Identify any change to an owned component or shared contract before applying it.
5. Verify that the defect is resolved and that affected consumers still meet their requirements. The disappearance of the original symptom is only part of this verification.

## §4 Scale the work to the dependency findings

Every fix needs the initial dependency search. A leaf change with no affected consumers can proceed with a local check; it does not need a separate impact report. A change to shared behavior or a widely referenced requirement needs a record of the affected surfaces and verification of those surfaces.

Do not infer low risk from a small diff. Conversely, do not require an extensive impact analysis after the search has established that the change is isolated.

## §5 Examples

If a shared helper returns a shape used by several callers, changing that shape to satisfy one caller can break the others. Read the callers first. A correction at the faulty caller may preserve the shared contract; if the contract itself needs to change, update and verify affected consumers.

If a rule's meaning changes, a link to its section can remain valid while the referring sentence becomes false. Read the referring statements and reconcile them in the same change.

## §6 Related requirements

The documentation instance follows `.claude/rules/doc-organization.md` §10, which governs link integrity. `five-why.md` addresses why the defect arose; this guide addresses the consequences of its repair. An owning skill can supply its own fixing workflow, but it still needs to account for the dependencies it changes.
