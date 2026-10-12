---
scope: portable
---

<critical>
scope: designing or writing a machine verification gate — a test or script whose job is to accept or reject an artifact or a process.
never: compare two sides without first naming the unit each side measures.
note: a very high violation rate on the first run is a reason to suspect the gate before the artifact.
</critical>

# Designing verification gates

A verification gate is a program that accepts or rejects an artifact. Its result is useful only when the comparison represents the requirement being checked.

## §1 Compare the same unit on both sides

Two helpers can both return integers while counting different things. A count of processing branches in source code cannot be compared directly with a count of headings in a report. When the two sides of a comparison measure different units, the failure does not look like a bug in the gate; it looks like a large or total violation count, so it reads as a broken artifact instead of a broken gate.

<rules section="ALWAYS">
- Before implementing a comparison, define in one sentence what each side measures.
- Confirm that the two sides represent the same unit, at the same layer, with compatible grouping and interpretation, before wiring the comparison.
- Inspect representative examples from both sides before treating their totals as equivalent.
- Treat an unexpectedly high violation rate on the first run as a reason to inspect the gate as well as the artifact; a plausible partial rate can also hide a unit mismatch, so keep checking real examples.
</rules>

<rules section="NEVER">
- Reuse a counting helper across a language, layer or grouping boundary without giving the new side its own pattern and fixture.
- Accept a gate's first-run numbers before opening real examples from both sides.
</rules>

<example type="unit_mismatch">
input: a gate compares a per-function branch count from source code against a per-entry count from a hand-written ledger
❌ wire the comparison straight from each side's own counting function; both return integers, so the types match even though the concepts do not
✅ open three real entries from both sides, confirm they name the same kind of thing, and only then compare the counts
</example>

When a helper is extended to a new language, artifact layer or grouping, that is a new counting problem. Reusing a parameter name does not establish that the same counting logic remains valid.

## §2 Check for missing and extra output separately

A transformation can fail by adding something that does not belong or by dropping something that the source requires. These are two different invariants that happen to be checked by inspecting the same artifact, and a suite can hold every gate for one direction and none for the other while looking complete.

<rules section="ALWAYS">
- For a build or transformation step, name which invariant each gate establishes: that the output has nothing extra, or that the output has nothing missing.
- When the input is a number of repeating units feeding one output, add a gate that ties a count derived from the source to a count derived from the built artifact.
- Cover both directions where both matter, and treat matching counts as evidence that units were accounted for, not that their content is correct.
</rules>

<rules section="NEVER">
- Call a suite complete when its only gates check the extra-output direction; a silent drop passes every one of them.
- Substitute a check that no stale rows remain after the last written row for a source-to-output count; dropped content never occupies a row position.
</rules>

<example type="one_way_gate">
input: a builder writes N source blocks into M destination rows, then checks that there is no data below row M
❌ treat that check as proof that the builder processed all N blocks; it only proves that nothing stale was left past the point where it stopped
✅ add a second check that the total units in the source equal the total units actually written, naming both sides' unit under §1 before wiring it
</example>
