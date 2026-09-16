---
scope: portable
---

# Investigating a root cause

## §1 Establish what needs explanation

Use causal investigation when requested, when a defect recurs or when a proposed local fix leaves the cause uncertain. An isolated correction with an established cause does not need a ceremonial chain of questions. Start with the observed symptom and the conditions that make it occur.

## §2 Investigate the artifact and the working method

First establish the mechanism that produces the artifact defect, the location responsible and the correction that would remove its cause. Reproduce it when execution is relevant and available; otherwise trace evidence in the artifact and its sources.

For an AI-produced artifact or genome defect, also ask whether an instruction, missing check or working method contributed. Cite the governing source and section when present; identify an appropriate owner when the problem exposes a gap. If the artifact explanation already resolves the method question, do not repeat it. An external failure does not require an invented genome cause.

A proposed change to production needs consideration of how verification would detect the same mistake. A detector alone does not repair a faulty production method, and a better method does not prove the result was checked.

## §3 Follow evidence rather than a fixed count

Continue causal questioning while another answer could change diagnosis or remedy. Follow independent causes separately. Stop when further questions add no useful distinction, not when a predetermined question count has been reached. Keep unsupported hypotheses unresolved.

Each explanation must connect to evidence that could disprove it. Saying the assistant misunderstood does not identify a mechanism. Establishing that a schema field was inferred from a neighboring example instead of read from its definition does identify a testable method failure.

## §4 Preserve and verify the conclusion

Retain the symptom, evidence, causal trace, proposed correction and verification. Identify any workflow prevention change and whether existing authority covers it. Use `fix-impact-analysis.md` §2 before applying a remedy and `lesson-capture.md` §2 for a repeatable method failure. Do not expand an authorized local fix into an unrelated policy change without establishing its scope.
