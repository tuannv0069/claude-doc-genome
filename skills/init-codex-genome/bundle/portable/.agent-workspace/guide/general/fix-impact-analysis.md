---
scope: portable
---

# Checking the consequences of a fix

## §1 Establish the defect and dependency boundary

Before fixing code, guidance, configuration or another artifact, confirm the defect and identify what relies on the part being changed. A requested edit is a starting hypothesis, not proof of the correct remedy. Use `five-why.md` §2 if the cause remains uncertain.

For code, inspect callers, shared state, return values and persistent data. For rules and documents, inspect incoming links, stable sections and statements whose meaning depends on the requirement. For configuration, inspect the reader and the behavior it controls. A valid link may still express the wrong meaning after a rule changes.

## §2 Choose a repair with its consumers in view

Establish the expectation of each affected consumer and whether the target is a shared contract. A narrower change at the faulty caller can sometimes preserve the shared behavior. If the contract itself must change, coordinate its consumers and verification in the same task.

Address the demonstrated cause without unrelated changes. If a temporary symptom remedy is warranted, preserve the reason and remaining limitation under `decision-journal.md` §1. Do not infer low risk from a small diff or high risk from file count alone.

## §3 Verify both correction and compatibility

Confirm that the original defect is resolved and that affected consumers still satisfy their requirements. The initial dependency search is always needed, but an isolated leaf change can use a local check without a separate impact report. Shared or widely referenced behavior needs recorded affected surfaces and verification of those surfaces.

An owning skill may supply the fixing sequence, but it must still account for changed dependencies. Maintain instruction links under `.agent-workspace/rules/doc-organization.md` §7.
