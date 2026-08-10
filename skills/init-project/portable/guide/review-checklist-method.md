---
scope: portable
---

<critical>
scope: route a free-form audit / review / find-bug request to the review instrument that fits (§7), and run the bug-finding checklist yourself over the layer no instrument reaches — on any artifact (code / doc / config) not owned by a skill's own method. The two compose; one request often needs both.
core: every item = a concrete falsifiable bug hypothesis the AI tries to prove EXISTS — gated by a real candidate site | absence-defect sweep runs first on fresh attention | confirmation honest about execution limits | findings → bug-report-format.
forbidden: positive "verify X is correct" items | a standing accusation with no candidate site | `present` verdict without a traced/executed evidence span | severity fixed before reachability shown | letting an enumerated hunt starve the absence sweep.
output language: final report → conversation language; this guidance file → English.
first: pick the instrument (§7) before §1 — instrument and method compose, neither replaces the other; a code diff hunted for what is MISSING takes both.
</critical>

## §1 Principle — hunt bugs, don't confirm correctness

Have not run §7 yet → go there first. Building a checklist an instrument would have built better is the most common way this file gets misused.

Each checklist item is a **concrete, falsifiable, binary bug hypothesis the AI actively tries to prove EXISTS** — never a correctness criterion to confirm.

Why: bug-phrasing forces concreteness + falsifiability + an adversarial stance. "Verify X is done right" invites confirmation bias — the AI pattern-matches "looks correct" and rationalizes a pass.

<example type="item_framing">
❌ "Verify the list query sorts correctly." — abstract, confirm-stance, AI gives a cheap pass.
✅ "Bug: list query ORDER BY diverges from the spec's `updatedAt desc`. Site: the repository query. Confirm: read the ORDER BY clause, compare to spec." — concrete, hunting-stance, binary.
</example>

## §2 Calibration priors (hold these before hunting)

- **Base rate.** For a competent artifact, MOST hypotheses are `absent`. Require a higher evidence bar for `present` than for `absent`. A report full of `suspected` buries the one real bug.
- **Confirmation honesty.** The AI often cannot execute the artifact → "confirm" must be a real semantic trace, not a guess dressed as a check. Each item declares its confirmation type (§4).
- **Spec is not ground truth.** The spec may be wrong, ambiguous, or self-contradictory. Where code and spec disagree, emit a `discrepancy` finding — do not auto-blame the code.

## §3 Procedure (phased)

| phase | action |
|---|---|
| **P0 Spec sanity** | Scan the spec for internal contradiction / ambiguity. Code ≠ spec → `discrepancy` finding, not auto-blame. |
| **P1 Absence sweep (FIRST, fresh attention)** | This is where the highest-value bugs live and what the AI is worst at — run it first, on fresh context (a separate subagent when the artifact is non-trivial — per `orchestration-policy.md` §7, delegation for unprimed attention, which is the exception to its §2 no-double-read rule). For each required behavior: "show the code path that guarantees it" → no path = absence finding (missing validation / branch / requirement). |
| **P2 Build the hunt list (gated)** | Derive candidates two ways: (A) spec-inversion — each requirement → "what does its violation look like?"; (B) failure-mode classes for the artifact type (code: null deref, off-by-one, race, missing validation, N+1, stale cache; doc: contradiction, missing mandatory section, dead ref). **Gate:** admit an item ONLY if a concrete candidate site / precondition exists (N+1 only where a loop+query exists; race only where shared mutable state exists). No site → drop, never carry as a standing accusation. Bound to top-K by hypothesized-severity × plausibility; defer the rest and name them in the output — never a silent cap. Persist the list + verdicts to `.agent-workspace/tasks/<task-slug>/` so context compaction can't drop state. |
| **P3 Hunt** | Per item: confirmation type = `executed` \| `traced` \| `inferred`. Confirm = a semantic trace citing the exact lines, NOT a syntactic presence check a regex could satisfy. Verdict: `present` (needs traced/executed + a quoted evidence span) \| `suspected` (inferred — capped here, cannot be `present`) \| `absent`. |
| **P4 Precision gate** | Each `present`/`suspected` must survive a "steelman why this is actually correct" rebuttal before it ships. Fails the rebuttal → drop or downgrade. |
| **P5 Output** | Runs on every review, including one that found nothing — **read `bug-report-format.md` now** and emit per its §3 (this is the only step that needs it — don't load it earlier). Zero surviving findings → `Verdict: PASS` + one line naming what was inspected, never a bare "no bugs" (that file's §4). Severity = **confirmed-severity** (reachability + trigger condition shown), not the P2 hypothesized-severity. Map confidence onto the format's Status: `traced`/`executed` → `confirmed`; `inferred` → `suspected`. A `confirmed`/`present` finding ships with its evidence span. |

**Existing checklist provided** (user already has one) → skip P0–P2, start at P3 — the hunt + confirmation + output discipline still applies.

## §4 Checklist item shape

| field | content |
|---|---|
| bug hypothesis | the defect, phrased negatively + concretely |
| candidate site | where it would live — **gates admission** (no site → not admitted) |
| confirm-by | the semantic trace required + type (`executed`/`traced`/`inferred`) |
| hypothesized-severity | triage / ordering only — never reported as-is |
| verdict | `present` / `suspected` / `absent` |
| evidence span | quoted line(s) proving it — **required for `present`** |

## §5 examples

<example type="gating">
❌ standing accusation: list "Bug: race condition exists" with no shared-state site found → AI spends attention dispositioning a phantom, drifts toward `suspected` to satisfy the hunt.
✅ gated: no shared mutable state located → the race hypothesis is never admitted; attention goes to real candidate sites.
</example>

<example type="confirmation_honesty">
❌ "Null check missing at line X?" → AI sees `if (x != null)` and answers `absent` from syntax alone — never traced that `x` was dereferenced two lines above on a null path.
✅ confirm-by = "trace `x` from assignment to use; confirm a dereference on a path where `x` can be null" → `present` only with the quoted dereference line as evidence; otherwise `inferred` → capped at `suspected`.
</example>

## §6 relation

- Pairs with `bug-report-format.md` — this file = how to GENERATE findings; that file = how to PRESENT them (§3 skeleton, severity scale, output discipline). Read it **only at P5 (output)**, not while building the checklist — different step, different time.
- A skill that owns its own review method takes precedence; this governs un-owned free-form requests.
- Spawning a fresh subagent for P1 / a large P2 hunt = per `orchestration-policy.md` §7 (delegation for unprimed attention, not for throughput), with the plan persisted to `.agent-workspace/tasks/` per its §4.

## §7 Pick the instrument first

A dedicated review skill beats this method wherever one fits — it is built for that shape and usually goes deeper. Pick from the rows below; **they compose, they do not exclude each other.**

| the request | instrument |
|---|---|
| find defects in a diff / PR / branch of CODE | the harness review command (`/code-review`), at the depth the stakes warrant |
| security exposure of pending changes | the harness security review (`/security-review`) |
| "does it actually work when run" | the harness runtime verification (`/verify`) — observation at the running surface, not a diff read |
| code is correct, make it cleaner | the harness cleanup command (`/simplify`) |
| a skill owns this workflow (review checkpoints inside its own loop) | follow that skill for WHEN to review; still pick the instrument from the rows above for HOW deep |
| a CODE diff **and** the question is what is MISSING | **both, in this order** — the instrument over the changed lines, then §3 P1 over the requirement set for the absence layer |
| any admission condition below holds | §1–§6 — on its own, or as the second layer over an instrument |

A named instrument absent from this harness → treat its row as unmatched and fall through. The command set varies by harness version; a row that cannot be run routes nowhere.

§1–§6 is admitted when at least one holds:

- the artifact is **not code** — a spec, a design doc, a rule file, a config
- the scope is **not a diff** — audit an existing module, review something never committed as a change, or build a checklist to hand to someone else
- the hunt is for the **absence defect** — what should exist and does not
- the user **supplied a checklist** — §3 P3 runs on it whatever the artifact is; the hunt, confirmation and precision discipline are exactly what a handed-over checklist does not carry (§3, line after the phase table)

The third condition is why the rows compose rather than exclude. A diff-scoped instrument sees what changed; it structurally cannot see what was never written. So "code diff" and "hunt the absence" are both true at once often enough to be the common case, and the answer is both layers, never one instead of the other.

<rules section="NEVER">
- hand a non-code artifact to a code-diff review instrument and call the result an audit
- skip §7 and start building a checklist when an instrument already covers the request
- let a skill's review checkpoint decide the DEPTH — it decides the timing, the instrument decides the depth
- treat an instrument's clean verdict on a diff as coverage of the absence layer — it never was
</rules>

<critical_recap>
0. pick the instrument (§7) before anything else — the rows compose: a code diff plus an absence hunt takes the instrument AND §3 P1, never one instead of the other.
1. every item = a bug hypothesis to prove EXISTS, gated by a real candidate site — never a "verify correct" item, never a siteless accusation.
2. run the absence sweep FIRST on fresh attention — that is where the AI's worst misses (missing validation/branch/requirement) live.
3. confirmation is honest: `traced`/`executed` → may be `present` with an evidence span; `inferred` → capped at `suspected`. Reject regex-satisfiable surface checks.
4. base rate = most hypotheses are `absent`; every `present`/`suspected` survives a steelman rebuttal before shipping.
5. severity is confirmed only after reachability is shown; output flows into bug-report-format.
</critical_recap>
