---
scope: portable
---

# Interpreting rule-health findings

The scanner supplies evidence about the document network. It cannot decide every semantic question or replace reading the source.

## §1 Scanner input and result

Run `python .agent-workspace/tooling/scan_rule_health.py` from the project root to scan the full declared corpus. With `--paths <files>`, the scanner selects those files and also includes up to three of the least recently scanned files by default. Set `--rotate N` together with `--paths` to change that additional count; use `--rotate 0` for a touched-file-only selection. `--rotate` has no effect without `--paths`.

Exit code `0` means the scan completed, including when it reported open findings. Exit code `1` means the ledger is invalid. Exit code `2` means the input scope could not be resolved. Do not interpret an unresolved scope as a clean review.

The report identifies the examined corpus, contextual measurements, and actionable findings. A single unmatched glob within an otherwise valid scope is a candidate finding rather than proof that the whole scope was absent.

## §2 Distinguish findings from context

A finding is a specific condition that can be resolved by a concrete change or justified exception. Context describes a wider property of the corpus and does not necessarily have one corrective action.

Do not create ledger entries for lines labeled as context. Legitimate bundle copies, collapsed instances, shared template structures, filename-only citation resolution, and comparative growth measurements can help interpret the scan without being defects in themselves.

Bundle drift belongs to the bundle/live comparison. A duplicate detector should not treat every packaged copy as an unauthorized second source.

## §3 Evaluate duplication

When the scanner identifies the same requirement in several locations, establish the canonical source and replace unnecessary copies with references under `.claude/rules/doc-organization.md` §4 and §10.

For a repeated passage within one file, determine whether both occurrences state the same obligation before removing one. For divergent copies, establish which requirement is current and reconcile the others. Do not merge incompatible versions merely to preserve their words.

An exception must cite the section that permits the duplication. Similar wording alone does not establish identical meaning.

## §4 Evaluate broken references

For a missing section or path, inspect both the reference and its intended target. Repoint the reference when the target moved, or remove the dependency when it no longer exists. If the target contains no governing content, determine whether the reference is unnecessary or the source is incomplete.

An unmatched `paths:` declaration can identify a stale rule or an optional tier that is not present in this project. Determine which case applies before changing it.

A result resolved only by filename requires manual confirmation that the scanner selected the intended file. Deliberately hypothetical filenames and section numbers used as examples are not live dependencies; justify that interpretation from their context. A live lesson is not exempt merely because it records an earlier incident.

## §5 Evaluate drift and growth

A drift signal asks whether a referring statement still agrees with a changed source section. Read both. Correct the referring statement when its meaning is stale; do not change the canonical source solely to satisfy an old reference.

A growth signal asks whether superseded requirements have accumulated. Identify the requirement that should have been removed before deleting anything. A file can legitimately grow when its new content remains useful; its size alone does not prove a defect.

## §6 Record a resolution

Record actionable findings in `.agent-workspace/rule-health/ledger.json`. Use `fixed` only when the correction is present in the working tree. Use `exempt` with a reason and an `allowed_by` reference when an applicable requirement permits the condition.

Exceptions are tied to the normalized content fingerprint. Changed content must be judged again. An unresolved finding remains visible on later scans.

## §7 Limits of the scanner

The scanner may miss equivalent requirements written differently, contradictions without shared vocabulary, and a correct requirement placed in the wrong area. Review those questions by reading.

Treat the report as a way to locate candidates. Neither a large finding count nor a clean scan establishes the quality of every instruction.
