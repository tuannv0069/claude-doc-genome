---
scope: portable
---

<critical>
scope: determine the impact scope (blast radius) BEFORE applying a fix — for a bug in any artifact (code / docs / rule / config) on a free-form fix request not owned by a skill's own workflow.
core: never fix-to-description blindly | probe dependents before editing | map regression surfaces | smallest fix for the root | verify the whole radius, not just the symptom.
forbidden: editing before finding what depends on the changed thing | changing a shared contract / owner code silently | declaring "fixed" on symptom-gone alone | analysis depth that ignores the fix's reach.
output language: report → conversation language; this guidance file → English.
</critical>

## §1 Principle — scope before fix

Before changing anything to fix a bug, determine **what depends on the thing you change** and **what could degrade**. A fix applied to the description alone, blind to its blast radius, trades one bug for another or breaks the chain downstream.

Why this is acute for an AI: the default move is a local pattern-fix — change the wrong-looking line — without tracing callers/dependents, and it will "fix to the description" even when the description itself is wrong. A junior dev misses the same way; dev-miss + AI-miss compound into regression.

## §2 Dependents are artifact-agnostic

The discipline is identical across artifact types; only *what you trace* differs:

| artifact | dependents to find first | degrade risk |
|---|---|---|
| code | callers, importers, consumers of the contract (signature / return shape / side effect / DB / shared state) | breakage at call sites, silent behavior change |
| docs / rule | `§ID` referrers, links pointing in, sections that cite this | dead pointer, rule now contradicts its referrers |
| config | every reader of the value | behavior shifts wherever it is read |

For docs/rule this IS the genome's existing link-integrity law (update every linking node) — this guide generalizes that instinct to all artifacts and moves it to BEFORE the edit.

## §3 Procedure

| phase | action |
|---|---|
| **P0 Validate the bug** | Confirm the root / reproduce — do not fix to the description blindly (a wrong description → a "fix" that is itself a new bug). Root unclear → `five-why.md`. |
| **P1 Reach probe** (cheap, mandatory) | Find the dependents (§2): grep callers / `§ID` referrers / config readers. Is the target shared / a contract / owner code / widely referenced? This step's result sets the depth of P2–P4. |
| **P2 Blast-radius map** | Enumerate the regression surfaces: who relies on the current behavior, which contract/invariant the fix changes, which shared paths it sits on, which doc referrers shift meaning. |
| **P3 Choose the fix** | Smallest change that fixes the ROOT without unnecessary blast. Root-fix vs symptom-patch = a conscious choice (symptom-patch → recurrence; root-fix → wider radius). Touches owner / shared / a contract → FLAG + name the affected consumers, never change silently. |
| **P4 Verify the radius** | Confirm the bug is gone AND each P2 surface still holds — for docs, no dead pointer / no new contradiction. Never stop at "the symptom disappeared." |

## §4 Proportionality (don't over-analyze)

P1 reach-probe is cheap and mandatory; the analysis self-scales from what it reveals:
- no dependents / leaf / pure-local change → fix directly, skip P2–P4.
- many dependents / shared / contract / owner / widely-referenced → run P2–P4 in full.

Never force a heavy blast-radius map onto a trivial local fix; never skip the reach-probe on a shared/contract change.

## §5 examples

<example type="code">
❌ change a shared util's return shape to satisfy one caller's bug → the other 4 callers break silently.
✅ grep callers first → 5 consumers rely on the current shape → fix at the caller's site, or extend without breaking the contract; then verify all 5.
</example>

<example type="docs_rule">
❌ rewrite rule `§X`'s wording to fix one ambiguity → 3 files cite `§X` with the old meaning → now contradictory.
✅ grep `§X` referrers first → reconcile/update them in the same change; verify no referrer now contradicts.
</example>

## §6 relation

- `five-why.md` — root cause of *why the bug happened*; this guide = *impact of the fix*. P0 invokes five-why when the root is unclear.
- `doc-organization` link-integrity law — the docs/rule instance of this discipline (referrers updated same-commit); this guide generalizes it to all artifacts and to BEFORE the edit.
- `critical-thinking.md` — "list out-of-scope effects" / "never proceed with scope side-effects unexamined" is the posture this operationalizes into a fix-time procedure.
- A skill that owns its own fix workflow takes precedence; this governs un-owned free-form fixes.

<critical_recap>
1. before any fix, probe what depends on the thing you change — never edit blind to dependents.
2. validate the root first; a fix to a wrong description is a new bug.
3. analysis depth self-scales from the reach probe — trivial-local → fix directly; shared/contract/owner → full blast-radius map.
4. touching a shared contract / owner code → flag + name affected consumers, never silent.
5. verify the whole radius, not just that the symptom disappeared.
</critical_recap>
