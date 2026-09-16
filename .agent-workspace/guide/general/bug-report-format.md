---
scope: portable
---

# Reporting review findings

This guide defines the evidence needed to make a review finding actionable. It applies when a skill or project does not already define the reporting contract. It does not prescribe a document layout or writing style.

## §1 Information a finding needs

A finding needs a severity, a location, a description of the problem, and a proposed correction. The problem identifies the defect; the correction identifies the change that would address it. Keep both meanings identifiable in the report.

Use a location that lets the recipient inspect the evidence, such as a file and line, a stable section, or a reproducible screen state. When one cause appears at several locations, describe that cause once and identify the affected locations.

### §1.1 Additional information

Include the cause when the defect alone does not explain how it arose, and the impact when it is needed to justify severity. Identify the governing requirement or other source when the reader needs it to evaluate the conclusion. Give findings stable identifiers when later work needs to refer to them.

Distinguish a confirmed finding from an unverified possibility. A conclusion based only on inference remains suspected; do not present it as confirmed because a reporting template has no uncertainty field.

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

State what was examined, what evidence was available, and what conclusion that evidence supports. The project's reporting requirements determine how this information is presented. A count of findings describes the report; it does not establish the depth or completeness of the review.

### §3.1 (retired)

### §3.2 (retired)

## §4 Scaling the report

The information required by §1 is the same for a small review and a broad audit. Expand the evidence when a recipient would otherwise have to guess why a finding is valid or how to act on it.

If no findings survive verification, identify the inspected scope and any limits of the review. An absence of demonstrated findings is not a guarantee that the artifact has no defects.

## §5 Example

Suppose saving an item succeeds but the visible list still shows its old value. A useful finding identifies the mutation handler, explains that the list query is not refreshed after the save, and proposes refreshing the query when the mutation succeeds. If the stale list can cause a user to submit the same operation twice, that consequence helps justify severity.

A statement that the cache might be wrong lacks a concrete condition and demonstrated consequence. It belongs in the investigation until the evidence supports a finding.

## §6 Review integrity

Report distinct defects rather than inflating the count by splitting one cause into several entries. Before declaring a finding confirmed, check that its evidence supports both the triggering condition and the claimed consequence.

A proposed correction should address the demonstrated defect. When it changes a shared contract, identify the affected consumers and use `fix-impact-analysis.md` §3 before applying it. Reporting a possible fix does not prove that it has been implemented or verified.

## §7 Explaining a proposed correction

Explain the meaning of a condition, formula, or unfamiliar identifier when that meaning is necessary to judge the correction. Check the expression itself, including boundary and missing-value cases, before proposing it.

For example, a formula that allows negative values based on a configured minimum needs a correct comparison and a defined meaning for an absent minimum. Expose those assumptions so the recipient can judge the logic. This does not require a fixed wording pattern.
