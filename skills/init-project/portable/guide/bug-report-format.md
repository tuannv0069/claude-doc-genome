---
scope: portable
---

<critical>
scope: output format for any free-form audit / review / find-bug request not owned by a skill's own output contract.
core: every finding carries 4 lobe fields | expand only when a field adds info | report leads with verdict + counts.
forbidden: free-form prose findings | merged "problem/fix" cell | preamble/closing filler | pasting code back | splitting one cause into N findings.
precedence: a skill that defines its own report/finding schema wins — this file governs only un-owned, free-form requests.
output language: final report → conversation language; this guidance file → English.
</critical>

## §1 finding schema

Every finding carries exactly these **4 lobe fields** — nothing less makes it actionable, nothing more is mandatory:

| field | content |
|---|---|
| Severity | one value from §2 |
| Location | `file:line` (clickable) — list multiple sites on one finding if same cause |
| Problem | what is wrong (the defect itself) |
| Fix | one actionable direction to correct it |

**Problem and Fix are always separate fields — never merged.** Problem = "what is wrong"; Fix = "what to do". One states the defect, the other the correction.

### §1.1 optional expansion fields

Add a field ONLY when it carries information beyond the 4 lobes. Default-off:

| field | add when |
|---|---|
| ID (`BUG-01`) | report has >1 finding (needed to reference) — single finding: omit |
| Cause | root cause is NOT obvious from Problem (a defect deep enough to warrant `five-why`) |
| Impact | needed to justify a severity that looks surprising for the Problem |
| Source | the defect comes from a named rule / viewpoint / checklist item |
| Status | label `suspected` only when unverified; `confirmed` is the default and stays silent |

## §2 severity

| severity | criterion |
|---|---|
| Blocker | blocks build / deploy / a core flow; data loss or corruption |
| Critical | wrong business result or security hole, but the app still runs |
| High | incorrect behavior on a real path with no safe workaround; a rule violation that will bite |
| Medium | localized defect or edge case with a workaround; maintainability risk that is real but contained |
| Low | cosmetic, dead code, style, magic value — no behavioral impact |

## §3 report skeleton

```
Verdict: <PASS | ISSUES FOUND> — N findings: <count per severity, high→low>

<findings — table if ≥3, inline blocks if ≤2>

<Expanded detail: — only findings that use an optional field (§1.1)>
```

### §3.1 findings table (≥3 findings) — 5 columns, fixed order

| ID | Sev | Location | Problem | Fix |
|----|-----|----------|---------|-----|
| BUG-01 | Blocker | `path:line` | what is wrong | what to do |

Sort rows by severity descending. Below the table, an **Expanded detail** list carries only the findings that need an optional field — each as `BUG-0N — Cause: … / Impact: … / Source: … / suspected`.

### §3.2 inline (≤2 findings)

One block per finding: `[Severity] file:line — Problem → Fix`, optional fields appended only as needed. No table, no ID required.

## §4 scaling (quick vs deep)

One schema, self-scaling by request depth:

| request | shape |
|---|---|
| quick check (≤2 findings) | inline blocks per §3.2; still carry all 4 lobe fields |
| audit / deep review (≥3) | summary table per §3.1, expand only findings that need it |
| 0 findings | `Verdict: PASS` + one line naming what was inspected — never a bare "no bugs" |

## §5 example

<example type="report">
❌ "I reviewed the service carefully and noticed a few things. First, the API path
   seems hardcoded which might cause issues, here is the code: [20-line paste]. Also
   the cache could be stale. In conclusion there are some bugs to fix."
   — prose, narration, code paste, merged problem/fix, no severity, no location, filler conclusion.

✅ Verdict: ISSUES FOUND — 3 findings: 1 Critical · 1 High · 1 Low

   | ID | Sev | Location | Problem | Fix |
   |----|-----|----------|---------|-----|
   | BUG-01 | Critical | `useItem.ts:54` | mutation does not invalidate the list query → stale rows shown after save | invalidate the query key in `onSuccess` |
   | BUG-02 | High | `item.service.ts:71` | status compared as raw string `"1"` instead of enum | use `StatusType.Active` |
   | BUG-03 | Low | `Item.tsx:7` | unused `useMemo` import | remove import |

   Expanded detail:
   - BUG-01 — Impact: user sees the old row, assumes save failed, re-saves → overwrite/duplicate. Source: cache-invalidation checklist.
</example>

## §6 output discipline

Each line is a binary check the writer can self-verify.

<rules section="ALWAYS">
- lead with the verdict line (verdict + count per severity), then findings — no preamble
- sort findings by severity descending
- one real problem = one finding; same cause at N sites → one finding listing N locations
- cite `file:line`; quote ≤1 line of code only when the defect is invisible without it
- Fix = one actionable direction; paste a snippet only when the fix is a trivial one-liner
- confident voice for `confirmed`; hedge only on `suspected`
- every finding must be actionable without a follow-up question — location precise, fix concrete
- 0 findings → PASS + one line naming what was inspected
</rules>

<rules section="NEVER">
- prose/bulleted findings instead of the §3 skeleton
- merge Problem and Fix into one cell
- paste a code block to describe a defect that a `file:line` already pinpoints
- split one root cause into multiple findings to inflate the count
- closing paragraph that restates the verdict
</rules>

## §7 explanation clarity — Fix and Cause fields

A Fix or Cause is read to be acted on; a reader who cannot follow it cannot act. Clarity ≠ length — a terse fix stays terse, it just carries no undefined token. The reader of a bug report does not implement this component.

<rules section="ALWAYS">
- every symbol / formula / identifier in a Fix or Cause → self-evident OR glossed inline (what it is · what value · why)
- framework/domain jargon (prop, forward down, controlled, desync, blur, superRefine) → plain-language gloss on first use when the reader may not build this layer
- mechanism fix (not a value swap) → state the chain: current behavior → why wrong → what changes → why the defect is gone
- fix that is a condition/formula → give the literal expression AND its meaning in prose; verify its logic (sign, branch, null case) before writing — a plausible-but-wrong formula is worse than prose alone
</rules>

<rules section="NEVER">
- emit a bare expression (`min >= 0`, `?? -1`) with no statement of what it decides
- assume the reader codes this component
- impose a fixed template (`current→why→fix→result`) on a value swap that needs one sentence
</rules>

<example type="fix_clarity">
❌ Fix: forward `allowNegative = (min >= 0)` down.
   — undefined jargon ("forward down"), bare formula, no meaning stated, and the formula is sign-inverted (a field with `min:0` would end up permitting negatives).
✅ Fix: add prop `allowNegative` (`true` = permit negatives; default `true` to keep existing fields unchanged). The factory that builds the input computes it from config — a field declaring `min ≥ 0` → `allowNegative=false` (block negatives); no `min`, or `min < 0` → stays `true`. Expression: `allowNegative = (min ?? -1) < 0`.
</example>

<critical_recap>
1. 4 lobe fields per finding: Severity · Location · Problem · Fix — Problem and Fix never merged
2. optional fields (ID / Cause / Impact / Source / Status) added only when they add info
3. report leads with verdict + severity counts; findings sorted severity-desc
4. self-scaling: ≤2 inline, ≥3 table + selective expansion, 0 → PASS + scope line
5. skill-owned output contract wins; this file governs only un-owned free-form requests
6. Fix/Cause carry no undefined token — gloss jargon, expand + verify any formula, explain a mechanism as a chain (§7)
</critical_recap>
