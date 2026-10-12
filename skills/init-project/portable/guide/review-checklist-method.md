---
scope: portable
---

<critical>
scope: a free-form audit, review or defect hunt over any artifact — code, document, configuration — that no skill's own method owns; route it to the fitting instrument (§7) and run the method over the layer no instrument reaches.
never: keep a standing accusation with no candidate site, or report a `present` finding without an executed or traced evidence span.
note: pick the instrument before building a checklist; every item is a concrete falsifiable defect hypothesis; the absence sweep runs on fresh attention; findings are reported under `bug-report-format.md`.
</critical>

# Investigating possible defects

This guide provides a review method for work that is not already governed by an owning skill. Use §7 to select the appropriate review instrument before applying the method.

## §1 Investigate concrete failure hypotheses

A sorting defect can be investigated by comparing the query's order with the required order; a general instruction to confirm that sorting is correct does not identify the condition that could fail. The purpose is to challenge the artifact, not to presume it is wrong.

<rules section="ALWAYS">
- Frame each investigation around a possible defect that can be supported or disproved by evidence.
- Identify the candidate location or precondition before spending review effort on it.
</rules>

<rules section="NEVER">
- Keep an accusation in the review when no plausible location or trigger exists.
- Write a positive item that asks to verify that something is correct; whether a creative piece works for its reader is judged by the appeal review in `creative-work.md` §6, not by a checklist item.
</rules>

<example type="hypothesis_shape">
input: a review item about list ordering
❌ verify that the list is sorted correctly
✅ the query orders by creation date while the specification requires order by priority; compare the order clause with the requirement
</example>

## §2 Calibrate conclusions to evidence

Most hypotheses in a competent artifact will be absent. A syntactic match alone does not show that the relevant path behaves as expected. The specification can itself be wrong or ambiguous.

<rules section="ALWAYS">
- Require enough evidence for a positive finding.
- Distinguish a result observed through execution, a semantic trace through the artifact, and an inference, and state the limit when execution is unavailable.
- When code and specification disagree, investigate the discrepancy.
</rules>

<rules section="NEVER">
- Treat the number of findings as a measure of review quality.
- Assign blame to the code automatically when it disagrees with the specification.
</rules>

## §3 Review procedure

1. Inspect the relevant requirements for contradictions or gaps that would make the expected behavior unclear.
2. Look for required behavior that is absent. For each requirement, identify the part of the artifact that establishes it. Give this work fresh attention; use an independent reader for consequential artifacts under `orchestration-policy.md` §7.
3. Build candidate hypotheses from requirements and failure modes appropriate to the artifact. Admit a candidate only when it has a concrete location or precondition. Prioritize by plausible consequence and likelihood, and record any meaningful portion of the requested scope left unexamined.
4. Investigate each candidate by executing or tracing the relevant behavior. Preserve the exact evidence and distinguish `executed`, `traced`, and `inferred` conclusions. A `present` finding needs execution or a semantic trace; inference alone supports only `suspected`.
5. Challenge every proposed finding with the strongest evidence-based explanation of why the artifact might already be correct. Withdraw or qualify findings that do not survive that challenge.
6. Report the surviving conclusions with the information in `bug-report-format.md` §1. Assess severity from demonstrated reachability and consequence, rather than from the alarming form of the original hypothesis.

<rules section="ALWAYS">
- Save the developing candidate list, verdicts, and evidence in the task workspace so the review can resume after context loss.
- When the user supplies a checklist, investigate its items, and explain any required behavior it does not cover when that omission affects the requested conclusion.
</rules>

<rules section="NEVER">
- Silently replace the requested scope with a different checklist.
- Let a supplied checklist lower the requirements for evidence, precision, or honest uncertainty.
- Let an enumerated hunt starve the absence sweep.
</rules>

## §4 Information retained for each candidate

The verdicts `present`, `suspected`, and `absent` distinguish a demonstrated defect, an unresolved possibility, and a hypothesis the inspected evidence does not support. These meanings can be stored in the working format appropriate to the task.

<rules section="ALWAYS">
- Retain the hypothesis, candidate location or precondition, the evidence needed to decide it, and the current conclusion.
- Attach the supporting evidence span to a confirmed finding.
- Reassess an initial severity estimate after the trigger and impact are established.
</rules>

## §5 Examples

<example type="race_condition">
input: a review item about concurrency
❌ investigate a race condition as a standing accusation when no shared mutable state or concurrent access has been located
✅ first establish the candidate path that could race, then investigate that path
</example>

<example type="null_check">
input: a null check exists before one use of an object
❌ conclude that the object is safe to dereference because a check was found
✅ trace the object from its source to every relevant use and determine whether a dereference can occur before the check
</example>

## §6 Related guidance

This guide governs how findings are established. `bug-report-format.md` governs the information needed to communicate those findings. An owning skill decides when review occurs within its workflow; the selected instrument and required evidence determine what the review can establish.

Use `orchestration-policy.md` §4 to preserve task state and §7 when an independent perspective is needed. A clean result is limited to the scope and evidence actually examined.

## §7 Select the review instrument

A code-diff review evaluates changed code. Runtime verification evaluates observed behavior. Security review investigates exposure and access paths. Cleanup changes maintainability and is not a substitute for finding correctness defects. A code-diff instrument and an absence investigation can both be necessary; a clean diff review cannot establish that an unwritten requirement was implemented.

<rules section="ALWAYS">
- Inspect the capabilities available in the current environment and select the one suited to the question before building a checklist.
- Use this guide directly for non-code artifacts, for work outside a diff, for a supplied checklist, or for finding required behavior that was never implemented.
- When a named review command is unavailable, use the applicable method and say that the command did not run.
</rules>

<rules section="NEVER">
- Submit a non-code artifact to a code-only instrument and describe the result as complete coverage.
- Let a skill's review checkpoint decide the depth of the review; it decides the timing, and the instrument decides the depth.
- Treat an instrument's clean verdict on a diff as coverage of the absence layer.
</rules>
