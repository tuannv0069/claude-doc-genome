---
scope: portable
---

# Designing a meaningful machine check

## §1 Define the invariant and units

Before writing a verification gate, identify the requirement it can decide and what each side of a comparison measures. Both sides must represent compatible units, scope, grouping and interpretation. Integers returned by two helpers are not comparable merely because they have the same data type.

Read examples from the source and output. A count of processing branches cannot be compared directly with report headings. Extending a helper to another language or artifact layer needs its own interpretation and fixtures.

## §2 Check loss and invention separately

A transformation can drop required material or add material without a source. Test both directions where both matter. Matching counts show accounting, not content correctness. For repeated units, compare source units with the units actually written; checking stale output after the last written unit does not establish that every source unit was consumed.

## §3 Challenge the gate itself

Include representative failing cases and legitimate cases the gate must accept. Check real examples when a new gate reports an unexpectedly high violation rate; a plausible partial rate can conceal a unit mismatch too. Do not automatically rewrite artifacts to satisfy a detector whose meaning has not been established.

Keep the parser's supported input and unverified conditions explicit. A schema check cannot certify factual truth or editorial quality. Use reasoning and independent review for requirements the program cannot decide reliably.
