---
scope: portable
---

# Interpreting checks of the instruction network

## §1 Establish the tool's actual scope

Before running or interpreting a rule-health scan, inspect the command's supported options and input corpus. Resolve the product root explicitly. A check of the Codex product does not cover its enclosing repository or another genome, and a selected-file check does not establish a clean full tree.

Record the scanned paths, the checks performed and unresolved inputs. Interpret exit status according to the running tool's documented contract. A process that completed while reporting findings is not necessarily a clean result; an unresolved scope cannot count as an absence of defects.

The distributed tool is `.agent-workspace/tooling/genome.py`. Its `verify` and `health` commands require an explicit `--project` path and return JSON with status, examined files, errors and observations. Exit code 0 means the implemented checks passed, 1 means findings remain and 2 means a command error. Source maintenance uses the initialization skill's `check` command, which validates its payload in a temporary deployment. Inspect the available command help when working with another installed revision rather than assuming the same contract.

## §2 Separate findings from measurements

A finding identifies a condition that can be corrected or supported by a documented exception. Context measurements such as growth, repeated template structure or amount of content are not defects by themselves. Do not turn those measurements into global writing limits.

Bundle copies are intentional distribution artifacts. Drift belongs to comparison between the live Codex source and its own bundle, not equality with another product. Do not report legitimate package copies as independent canonical rules.

## §3 Investigate reported duplication and broken references

Read the matching passages before deciding they state the same requirement. Choose the current authoritative source, replace unnecessary copies with references and retain allowed routing reminders under `.agent-workspace/rules/doc-organization.md` §3. A wording match alone cannot establish a semantic duplicate.

Inspect both ends of a broken path or section reference. Correct the target, the consumer or the obsolete dependency as appropriate. Examples and historical paths need their actual context considered; filename-only resolution needs confirmation that the intended file was selected.

## §4 Keep dispositions supported

For a consequential accepted finding or exception, record the evidence, owning requirement and remaining limitation. Do not close a finding merely because its string vanished from the scanner. Recheck the corrected relationship and affected consumers. Use `decision-journal.md` §1 for reasons that a diff cannot preserve.

A scanner supplements semantic review under `review-checklist-method.md` §2. A clean structural result does not certify natural-language meaning, proper routing in execution or completeness of the underlying workflow.
