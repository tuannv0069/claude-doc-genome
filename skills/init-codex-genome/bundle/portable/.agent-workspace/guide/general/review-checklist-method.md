---
scope: portable
---

# Reviewing through concrete failure hypotheses

## §1 Choose an instrument that can answer the question

Inspect available capabilities and select the review method suited to the artifact. A code-diff review evaluates changed code; runtime verification establishes observed behavior; a security investigation examines access paths. An absence check asks whether required behavior exists at all. A clean diff review cannot establish an unwritten requirement.

Use this procedure for non-code artifacts, supplied checklists or work not owned by a review skill. Do not claim an unavailable command ran, and do not pass non-code work through a code-only tool and call that complete coverage.

## §2 Establish scope and possible defects

Read requirements first and identify contradictions that make expected behavior uncertain. Compare required outcomes with the artifact to find omissions. Use an independent reader for consequential absence checks under `orchestration-policy.md` §2.

Form candidate hypotheses only where a concrete location or triggering condition exists. A generic accusation of a race is not useful until shared mutable state and concurrent access have been located. Prioritize by plausible consequence and likelihood; record material requested scope left unexamined.

## §3 Test and challenge each candidate

Execute the relevant behavior or trace its semantics from input to consequence. Distinguish `executed`, `traced` and `inferred` evidence. A confirmed `present` defect requires execution or a semantic trace; inference alone supports `suspected`. Use `absent` when the examined evidence disproves the candidate within the reviewed scope.

Challenge every positive finding with the strongest evidence-based explanation of why the artifact may already be correct. Withdraw or narrow claims that fail this challenge. Neither finding count nor a fixed checklist establishes review quality.

If the user supplied a checklist, investigate its items and explain any material requirement it misses. Do not silently substitute another scope. A specification can itself be wrong, so a discrepancy does not automatically establish which artifact is defective.

## §4 Preserve evidence and communicate limits

Save candidates, locations, required evidence, verdicts and supporting spans in the task workspace while reviewing. Reassess severity after reachability and consequence are established. Use `bug-report-format.md` §1 for the information needed by the recipient.

A clean result is limited to the evidence and scope actually examined. Programs provide a floor of mechanically checked conditions, not a ceiling on reasoning about missing behavior or a guarantee of correctness.
