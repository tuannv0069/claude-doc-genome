---
scope: portable
---

# Investigating possible defects

This guide provides a review method for work that is not already governed by an owning skill. Use §7 to select the appropriate review instrument before applying the method.

## §1 Investigate concrete failure hypotheses

Frame each investigation around a possible defect that can be supported or disproved by evidence. Identify the candidate location or precondition before spending review effort on it.

For example, a sorting defect can be investigated by comparing the query's order with the required order. A general instruction to confirm that sorting is correct does not identify the condition that could fail.

The purpose is to challenge the artifact, not to presume it is wrong. Do not keep an accusation in the review when no plausible location or trigger exists.

## §2 Calibrate conclusions to evidence

Most hypotheses in a competent artifact will be absent. Require enough evidence for a positive finding rather than treating the number of findings as a measure of review quality.

Distinguish a result observed through execution, a semantic trace through the artifact, and an inference. If execution is unavailable, state the limit. A syntactic match alone does not show that the relevant path behaves as expected.

The specification can itself be wrong or ambiguous. When code and specification disagree, investigate the discrepancy rather than automatically assigning blame to the code.

## §3 Review procedure

1. Inspect the relevant requirements for contradictions or gaps that would make the expected behavior unclear.
2. Look for required behavior that is absent. For each requirement, identify the part of the artifact that establishes it. Give this work fresh attention; use an independent reader for consequential artifacts under `orchestration-policy.md` §7.
3. Build candidate hypotheses from requirements and failure modes appropriate to the artifact. Admit a candidate only when it has a concrete location or precondition. Prioritize by plausible consequence and likelihood, and record any meaningful portion of the requested scope left unexamined.
4. Investigate each candidate by executing or tracing the relevant behavior. Preserve the exact evidence and distinguish `executed`, `traced`, and `inferred` conclusions. A `present` finding needs execution or a semantic trace; inference alone supports only `suspected`.
5. Challenge every proposed finding with the strongest evidence-based explanation of why the artifact might already be correct. Withdraw or qualify findings that do not survive that challenge.
6. Report the surviving conclusions with the information in `bug-report-format.md` §1. Assess severity from demonstrated reachability and consequence, rather than from the alarming form of the original hypothesis.

Save the developing candidate list, verdicts, and evidence in the task workspace so the review can resume after context loss.

If the user supplies a checklist, investigate its items rather than silently replacing the requested scope. The checklist does not remove the requirements for evidence, precision, or honest uncertainty. Explain any required behavior it does not cover when that omission affects the requested conclusion.

## §4 Information retained for each candidate

Retain the hypothesis, candidate location or precondition, the evidence needed to decide it, and the current conclusion. A confirmed finding also needs the evidence span that supports it. An initial severity estimate is for prioritization and must be reassessed after the trigger and impact are established.

The verdicts `present`, `suspected`, and `absent` distinguish a demonstrated defect, an unresolved possibility, and a hypothesis the inspected evidence does not support. These meanings can be stored in the working format appropriate to the task.

## §5 Examples

Do not investigate a race condition as a standing accusation when no shared mutable state or concurrent access has been located. First establish the candidate path that could race.

Finding a null check does not prove that an object is safe to dereference. Trace the object from its source to every relevant use and determine whether a dereference can occur before the check.

## §6 Related guidance

This guide governs how findings are established. `bug-report-format.md` governs the information needed to communicate those findings. An owning skill decides when review occurs within its workflow; the selected instrument and required evidence determine what the review can establish.

Use `orchestration-policy.md` §4 to preserve task state and §7 when an independent perspective is needed. A clean result is limited to the scope and evidence actually examined.

## §7 Select the review instrument

Inspect the capabilities available in the current environment and select the one suited to the question. A code-diff review evaluates changed code. Runtime verification evaluates observed behavior. Security review investigates exposure and access paths. Cleanup changes maintainability and is not a substitute for finding correctness defects.

Use this guide directly for non-code artifacts, for work outside a diff, for a supplied checklist, or for finding required behavior that was never implemented. A code-diff instrument and an absence investigation can both be necessary; a clean diff review cannot establish that an unwritten requirement was implemented.

If a named review command is unavailable, use the applicable method without pretending the command ran. Do not submit a non-code artifact to a code-only instrument and describe the result as complete coverage.
