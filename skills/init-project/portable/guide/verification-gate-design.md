---
scope: portable
---

# Designing verification gates

A verification gate is a program that accepts or rejects an artifact. Its result is useful only when the comparison represents the requirement being checked.

## §1 Compare the same unit on both sides

Before implementing a comparison, define what each side measures. Confirm that the two sides represent the same unit, at the same layer, with compatible grouping and interpretation.

Two helpers can both return integers while counting different things. A count of processing branches in source code cannot be compared directly with a count of headings in a report. Inspect representative examples from both sides before treating their totals as equivalent.

When a helper is extended to a new language, artifact layer, or grouping, give the new interpretation its own pattern and fixture. Reusing a parameter name does not establish that the same counting logic remains valid.

Treat an unexpectedly high violation rate on the first run as a reason to inspect the gate as well as the artifact. Check real examples before accepting the result. A plausible partial violation rate can also hide a unit mismatch.

## §2 Check for missing and extra output separately

A transformation can fail by adding something that does not belong or by dropping something that the source requires. A check for one direction does not establish the other.

For a builder that consumes repeated units, compare source units with units actually written. A check that no stale rows remain after the last written row cannot show that the builder processed every source block.

Name the invariant each gate establishes and cover both directions where both matter. Matching counts show that units were accounted for; additional evidence is needed to establish that their content is correct.
