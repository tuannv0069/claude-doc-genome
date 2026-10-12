---
scope: portable
---

<critical>
scope: running `scan_rule_health.py` and judging its findings — deciding whether a reported duplicate, broken reference, drift or growth signal is a real defect, and resolving it.
never: create a ledger entry for a context line, or delete text the report does not prove is duplicated.
note: every finding ends `fixed` or `exempt`, and an `exempt` names the section that allows it (§6); the scanner locates candidates and proves nothing about quality (§7).
</critical>

# Interpreting rule-health findings

The scanner supplies evidence about the document network. It cannot decide every semantic question or replace reading the source.

## §1 Scanner input and result

Run `python .agent-workspace/tooling/genome/scan_rule_health.py` from the project root to scan the full declared corpus. With `--paths <files>`, the scanner selects those files and also includes up to three of the least recently scanned files by default. Set `--rotate N` together with `--paths` to change that additional count; use `--rotate 0` for a touched-file-only selection. `--rotate` has no effect without `--paths`.

Exit code `0` means the scan completed, including when it reported open findings. Exit code `1` means the ledger is invalid. Exit code `2` means the input scope could not be resolved. The report identifies the examined corpus, contextual measurements, and actionable findings.

<rules section="NEVER">
- Interpret an unresolved scope as a clean review.
- Treat a single unmatched glob within an otherwise valid scope as proof that the whole scope was absent.
</rules>

## §2 Distinguish findings from context

A finding is a specific condition that can be resolved by a concrete change or justified exception. Context describes a wider property of the corpus and does not necessarily have one corrective action. Legitimate bundle copies, collapsed instances, shared template structures, filename-only citation resolution, and comparative growth measurements can help interpret the scan without being defects in themselves. Bundle drift belongs to the bundle/live comparison.

<rules section="NEVER">
- Create a ledger entry for a line labeled as context.
- Treat every packaged bundle copy as an unauthorized second source.
</rules>

## §3 Evaluate duplication

Similar wording alone does not establish identical meaning.

<rules section="ALWAYS">
- When the scanner identifies the same requirement in several locations, establish the canonical source and replace unnecessary copies with references under `.claude/rules/doc-organization.md` §4 and §10.
- For a repeated passage within one file, determine whether both occurrences state the same obligation before removing one.
- For divergent copies, establish which requirement is current and reconcile the others.
- Cite the section that permits the duplication in every exception.
</rules>

<rules section="NEVER">
- Merge incompatible versions merely to preserve their words.
</rules>

## §4 Evaluate broken references

An unmatched `paths:` declaration can identify a stale rule or an optional tier that is not present in this project. Deliberately hypothetical filenames and section numbers used as examples are not live dependencies. A live lesson is not exempt merely because it records an earlier incident.

<rules section="ALWAYS">
- For a missing section or path, inspect both the reference and its intended target, then repoint the reference when the target moved or remove the dependency when it no longer exists.
- When the target contains no governing content, determine whether the reference is unnecessary or the source is incomplete.
- Determine which case an unmatched `paths:` declaration is before changing it.
- Confirm by hand that the scanner selected the intended file when a result was resolved only by filename.
- Justify from context the interpretation of a hypothetical filename or section number as an example.
</rules>

## §5 Evaluate drift and growth

A drift signal asks whether a referring statement still agrees with a changed source section. A growth signal asks whether superseded requirements have accumulated; a file can legitimately grow when its new content remains useful.

<rules section="ALWAYS">
- For a drift signal, read both the referring statement and the changed section, and correct the referring statement when its meaning is stale.
- For a growth signal, identify the requirement that should have been removed before deleting anything.
</rules>

<rules section="NEVER">
- Change the canonical source solely to satisfy an old reference.
- Treat a file's size alone as proof of a defect.
</rules>

## §6 Record a resolution

Exceptions are tied to the normalized content fingerprint, so changed content must be judged again. An unresolved finding remains visible on later scans.

<rules section="ALWAYS">
- Record actionable findings in `.agent-workspace/rule-health/ledger.json`.
- Use `fixed` only when the correction is present in the working tree.
- Use `exempt` with a reason and an `allowed_by` reference to the requirement that permits the condition.
</rules>

## §7 Limits of the scanner

The scanner may miss equivalent requirements written differently, contradictions without shared vocabulary, and a correct requirement placed in the wrong area. Review those questions by reading. Treat the report as a way to locate candidates. Neither a large finding count nor a clean scan establishes the quality of every instruction.
