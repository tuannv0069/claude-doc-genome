---
scope: portable
---

<critical>
scope: judging a rule-health finding — deciding whether a reported duplicate, dead pointer, drift or growth flag is a real defect, and resolving it.
never: close a finding without writing its state to the ledger | delete text the report does not prove is duplicated | treat a CONTEXT line as a finding
always: every finding ends `fixed` or `exempt`; `exempt` names the §ID that allows it
note: §ID append-only (portable) — never renumber; retired sections keep their number.
</critical>

# Rule health — judging findings

## §1 Input

Run `python .agent-workspace/tooling/scan_rule_health.py [--paths <touched files>] [--rotate N]`.

Exit codes: `0` clean · `1` the `budget` hard gate fired, or the ledger is malformed · `2` the scan scope could not be resolved at all. A `2` is never "nothing found" — it means the tool could not find its input. One glob among several matching nothing is NOT a `2`; it is a `paths_no_match` finding (§4).

The report prints its denominator first, then context lines, then one line per open finding.

## §2 Findings versus context — read this before judging anything

| kind | test | where it goes |
|---|---|---|
| **finding** | one concrete action closes it, and it then disappears | the ledger, as `fixed` or `exempt` |
| **context** | true and worth knowing, but no single action closes it | printed only, never in the ledger |

Context lines are labelled `(context, NOT a finding)`. Do not open ledger entries for them. They exist so a corpus-wide habit stays visible without becoming thousands of items nobody can close.

The context counts and what each means:

| count | meaning |
|---|---|
| `packaging (§4 legitimate)` | a file and its bundle copy — legitimate per `doc-organization.md` §4; `/init-project check` owns their drift |
| `instances collapsed` | paths collapsed to one representative because they are instances of one logical file |
| `bundle drift` | instance pairs that no longer match — again `/init-project check`'s job |
| `template skeleton (§7.1 legitimate)` | lines shared by a majority of one directory's files: that is the template, not a repeated rule |
| `citations resolvable only BY FILE NAME` | citations missing the path segment that would pick between same-named files |
| `growth — the least-deleting files` | the least-deleting eligible files, ranked |

## §3 Judging a `dup` finding

| report says | judgement |
|---|---|
| `verbatim duplicate` across files | one file is the source of truth; the others become `§ID` pointers (`doc-organization.md` §2) |
| `verbatim duplicate` inside one file | delete the later occurrence (`rule-writing-standards.md` NEVER duplicate rule across sections) |
| `divergent copy` | two texts state one rule differently — decide which is current and delete the other; never merge both |

`exempt` is correct only for the cases `doc-organization.md` §4 allows. Name which one in `allowed_by`.

## §4 Judging a `dead` finding

| `detail` prefix | fix |
|---|---|
| `sid_missing` | the cited section was renumbered or removed — repoint, or delete the citing sentence |
| `path_missing` | the file moved or was deleted — repoint, or delete the citing sentence |
| `target_empty` | the target holds no law — remove the citation, or fill the target |
| `paths_no_match` | a declared `paths:` glob matches no file — either the declaration is stale (repoint or delete it) or the rule ships ahead of an optional tier, which is `exempt`, `allowed_by` the §ID that makes the tier optional |
| `naming_prefix` | a declared rule-bearing folder lacks the `_` prefix (§10) — rename the folder and every reference; never `exempt` |

`(fallback-by-name)` means the target was matched by filename, not by path. Verify the match by hand before acting.

A pointer that is illustrative BY CONSTRUCTION — a deliberately impossible section number, a hypothetical filename inside the prose — is `exempt`, `allowed_by` the record's own §ID. A pointer that merely sits inside a lesson store is NOT exempt: `lesson-capture.md` §8 says a file still read as live guidance keeps its pointers current, and that includes the lessons tree.

## §5 Judging `drift` and `growth`

- `drift` — the cited section changed after the citing file last did. Read the section as it stands, then the sentence citing it. Fix the citer, never the cited section.
- `growth` — the file has never deleted a line (`deleted == 0`), against `doc-organization.md` §12 which requires a narrowed law's old text to be deleted. Name the rule that should have died, or record `exempt` with the reason none could. The ranked near-monotonic list is context, not a finding.

## §6 Resolving

Write each finding to `.agent-workspace/rule-health/ledger.json`:

- `fixed` — the edit is in the working tree, shown as a diff.
- `exempt` — `reason` plus `allowed_by` (a `§ID`).

An exemption expires when the text changes, because the fingerprint is keyed on normalised content. That is deliberate and replaces any date-based expiry.

A finding left unresolved reappears on the next run. That is the intended behaviour, not a bug.

## §7 What this tool cannot see

- two sentences stating one rule in entirely different words;
- a genuine contradiction phrased without shared vocabulary;
- a correct rule sitting in the wrong file.

Judge those by reading. The report shrinks the haystack; it does not find the needle.
