---
scope: portable
---

<critical>
scope: reporting findings from a free-form audit, review or defect hunt that no skill's own output contract owns.
never: present an inferred conclusion as confirmed, or split one cause into several findings to inflate the count.
note: a skill that defines its own report schema wins; the final report is written in the conversation language.
</critical>

# Reporting review findings

This guide defines the evidence needed to make a review finding actionable. It applies when a skill or project does not already define the reporting contract. It does not prescribe a document layout or writing style.

## §1 Information a finding needs

The problem identifies the defect; the correction identifies the change that would address it. A location that lets the recipient inspect the evidence is a file and line, a stable section, or a reproducible screen state.

<rules section="ALWAYS">
- Give every finding a severity, a location, a description of the problem, and a proposed correction, with the problem and the correction kept identifiable.
- When one cause appears at several locations, describe that cause once and identify the affected locations.
- Make every finding actionable without a follow-up question: precise location, concrete correction.
</rules>

<rules section="NEVER">
- Merge the problem and the correction into one statement that hides which is which.
- Paste a code block to describe a defect that a file and line already pinpoint.
</rules>

### §1.1 Additional information

Include the cause when the defect alone does not explain how it arose, and the impact when it is needed to justify severity. Identify the governing requirement or other source when the reader needs it to evaluate the conclusion. Give findings stable identifiers when later work needs to refer to them.

<rules section="ALWAYS">
- Distinguish a confirmed finding from an unverified possibility.
</rules>

<rules section="NEVER">
- Present a conclusion based only on inference as confirmed because a reporting template has no uncertainty field.
</rules>

## §2 Severity

Assess severity from the demonstrated effect and the reachable conditions that trigger it.

| Severity | Meaning |
|---|---|
| Blocker | The defect prevents a build, deployment, or core workflow, or causes data loss or corruption. |
| Critical | The system remains usable, but the defect produces a wrong business result or exposes a security vulnerability. |
| High | The defect affects a real path without a safe workaround, or violates a requirement with a demonstrated substantial consequence. |
| Medium | The defect is localized, has a workable alternative, or introduces a contained maintenance risk. |
| Low | The issue has no demonstrated behavioral impact, such as unused code or a cosmetic defect. |

For a non-software artifact, assess the consequence within the project's domain. A broken factual claim can affect the artifact's purpose even when there is no executable behavior.

## §3 Reporting the review outcome

The project's reporting requirements determine how the information is presented. A count of findings describes the report; it does not establish the depth or completeness of the review.

<rules section="ALWAYS">
- State what was examined, what evidence was available, and what conclusion that evidence supports.
- Lead with the verdict and the counts per severity, then the findings sorted by severity.
</rules>

<rules section="NEVER">
- Open with preamble or close with a paragraph that restates the verdict.
</rules>

### §3.1 (retired)

### §3.2 (retired)

## §4 Scaling the report

The information required by §1 is the same for a small review and a broad audit. An absence of demonstrated findings is not a guarantee that the artifact has no defects.

<rules section="ALWAYS">
- Expand the evidence when a recipient would otherwise have to guess why a finding is valid or how to act on it.
- When no findings survive verification, identify the inspected scope and any limits of the review.
</rules>

## §5 Example

Suppose saving an item succeeds but the visible list still shows its old value. A useful finding identifies the mutation handler, explains that the list query is not refreshed after the save, and proposes refreshing the query when the mutation succeeds. If the stale list can cause a user to submit the same operation twice, that consequence helps justify severity.

A statement that the cache might be wrong lacks a concrete condition and demonstrated consequence. It belongs in the investigation until the evidence supports a finding.

## §6 Review integrity

Reporting a possible fix does not prove that it has been implemented or verified.

<rules section="ALWAYS">
- Before declaring a finding confirmed, check that its evidence supports both the triggering condition and the claimed consequence.
- Propose a correction that addresses the demonstrated defect.
- When a correction changes a shared contract, identify the affected consumers and use `fix-impact-analysis.md` §3 before applying it.
</rules>

<rules section="NEVER">
- Split one cause into several findings.
- Report a correction as applied or verified when it has only been proposed.
</rules>

## §7 Explaining a proposed correction

For example, a formula that allows negative values based on a configured minimum needs a correct comparison and a defined meaning for an absent minimum. Exposing those assumptions lets the recipient judge the logic. This does not require a fixed wording pattern: a value swap needs one sentence, while a change of mechanism needs the chain from current behavior to why the defect is gone.

<rules section="ALWAYS">
- Explain the meaning of a condition, formula or unfamiliar identifier when that meaning is necessary to judge the correction.
- Check the expression itself, including boundary and missing-value cases, before proposing it.
- Gloss framework or domain jargon on first use when the reader may not build this layer.
</rules>

<rules section="NEVER">
- Emit a bare expression with no statement of what it decides.
- Assume the reader codes this component.
</rules>

<example type="bare_expression">
input: a correction to a range check
❌ change it to `min >= 0`
✅ change the check to `min >= 0`, so that a configured minimum of zero is accepted and only a negative minimum is rejected; an absent minimum is treated as zero
</example>
