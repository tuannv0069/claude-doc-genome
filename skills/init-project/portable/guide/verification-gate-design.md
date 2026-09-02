---
scope: portable
---

<critical>
scope: designing or writing a machine verification gate (test / script check) for a deliverable or a process — any file whose job is to say pass/fail on an artifact.
never: compare two sides without naming the unit each side measures
note: §ID append-only (portable) — never renumber; retired sections keep their number.
</critical>

# Verification gate design

## §1 Name the unit of both sides before comparing

A comparison gate (`assert sideA == sideB`, `assert sideA in sideB`) is silently wrong when the
two sides are measured in different units — the failure does not look like a bug, it looks like
a large or total violation count, so it reads as "the artifact is broken" instead of "the gate is
broken".

<rules section="ALWAYS">
- before writing a comparison gate, state in one sentence what unit EACH side counts
- prove the two units are the same thing — same layer, same language, same grouping — before wiring the comparison
- a violation rate near 100% on first run → suspect the gate, not the artifact (a large but partial rate can ALSO hide a unit mismatch — do not stop checking once the rate looks "plausible")
</rules>

<rules section="NEVER">
- reuse a counting helper across a language/layer boundary without a dedicated pattern + fixture for the new side
- trust a gate's first-run numbers before opening a few real examples from both sides
</rules>

<example type="unit_mismatch">
input: gate compares a per-function branch count (source) against a per-entry-label count (a hand-written ledger)
❌ wire the comparison straight from each side's own counting function — both return integers, so the types match even though the concepts don't
✅ open 3 real entries from both sides, confirm they name the SAME kind of thing, only then compare counts
</example>

Widening a helper to a new domain (a new language, a new layer, a new grouping) is a new
counting problem — it earns its own pattern and its own fixture, not a parameter on the old one.

## §2 A one-direction gate leaves the other direction unmeasured — and that is where loss hides

A check of the shape "everything the builder wrote is accounted for" (no leftover, no
over-write, no orphan) proves nothing about "everything the source had made it into the
build" (no drop, no truncation, no skip). These are two different invariants that happen to
be checked by inspecting the same artifact, and a suite can hold every gate for one direction
and zero for the other while looking complete.

<rules section="ALWAYS">
- for a build/transform step, name which invariant a gate checks: "output has nothing EXTRA"
  (over-write / leftover) or "output has nothing MISSING" (under-write / drop) — never assume
  a gate checking one also covers the other
- when the input is N repeating units (blocks, tables, rows, sheets) feeding one output, add a
  gate that ties a COUNT derived from the source to a count derived from the built artifact —
  "no leftover below the last written row" cannot substitute for this, because dropped content
  never occupies a row position to begin with
</rules>

<rules section="NEVER">
- ship a build pipeline whose only gates check the over-write direction and call the suite
  complete — a silent drop reads as a clean pass on every one of them
</rules>

<example type="one_way_gate">
input: a builder writes N source blocks into M destination rows, then checks "no data below row M"
❌ treat that check as proof the builder processed all N blocks — it only proves the builder
   didn't leave stale content past wherever it stopped
✅ add a second check: total data units in the source == total data units actually written;
   name both sides' unit explicitly (§1) before wiring it
</example>

<critical_recap>
1. name the unit of both sides of a comparison gate before wiring it
2. a near-100% (or merely large) violation rate on first run is a signal to suspect the gate
3. a helper crossing a boundary (language, layer, grouping) needs its own pattern + fixture
4. a gate checking "nothing extra" does not check "nothing missing" — build pipelines need both directions named and both covered
</critical_recap>
