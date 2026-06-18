---
scope: portable
---

<critical>
scope: root cause analysis (RCA) for bug / artifact defect (code, doc, config).
core: answer 2 question groups | G2 skippable when G1 covers it | each why = falsifiable.
forbidden: free-form bullet RCA | stop at symptom | force fixed why count.
output language: final RCA report → Vietnamese; this guidance file → English.
</critical>

## §1 when to apply

| situation | apply |
|---|---|
| user asks "5 why" / "root cause" / "RCA" / "tại sao" / "vì sao" / "nguyên nhân" / "tìm lý do" / "phân tích nguyên nhân" | mandatory |
| debugging artifact AI just produced (code/doc/config) | mandatory |
| bug outside AI scope (3rd-party lib, infra) | G1 only |
| trivial fix (< 5 lines, not recurring) | skip RCA |

## §2 two question groups

| group | question | output |
|---|---|---|
| G1 — Root + Fix | What is the actual root cause? What is the fix? | root location + fix patch/diff |
| G2 — Rule + Prevention | Which rule/guideline in `.claude/` or `CLAUDE.md` caused the root? How to amend so agent does not repeat? | rule §ID + rule diff, OR "gap — no rule covers" |

<rules section="ALWAYS">
- G1 mandatory
- G2 mandatory when root lives inside AI artifact (code/doc agent produced) or inside `CLAUDE.md` / `.claude/` (agent, skill, rule, agent-guide)
- G1 already answers G2 (e.g. fix = rule fix in one step, or root unrelated to any rule) → skip G2, write a one-line reason
- each why = one falsifiable hypothesis (cite `file:line` | `§ID` | observable behavior)
- G2 finds no rule → record `gap — no rule covers <topic>` + propose location
- G2 fix targets skill/agent workflow → evaluate fix at both generative layer (implement: produce correct output) AND detective layer (verify: catch wrong output); propose both
- G2 rule edit → user confirms before apply
</rules>

<rules section="NEVER">
- emit free-form bullet list instead of §4 template
- stop G1 at symptom (`"code wrong at line X"` is not a root)
- stop G2 at `"AI misunderstood"` — must cite rule §ID or declare gap
- force 5 whys when fix converged earlier
- exceed 7 whys per group → decompose
</rules>

## §3 stop condition

```
G1: next why → fix unchanged → stop
G2: rule §ID cited → stop
    OR grep confirms no rule → stop (gap)
    OR G1 outcome already contains the rule fix → skip G2 with reason
```

## §4 output template (rendered in Vietnamese)

````md
## RCA: <bug name>

**Symptom**
`file:line` — <observed behavior in Vietnamese>

---

### G1 — Root cause & Fix

1. <Question 1>?
   → <Answer 1 @ file:line>

2. <Question 2>?
   → <Answer 2>

3. Convergence
   → <reason fix unchanged> ⇒ **stop**

| field  | value |
|--------|-------|
| Root   | `<location>` — <one-line cause> |
| Fix    | <patch / diff> |
| Verify | <test cmd \| repro> |

---

### G2 — Rule in `CLAUDE.md` / `.claude/` & Prevention

1. Which rule/guideline caused the G1 root?
   → `<rule path §ID>` — <excerpt>   *(or ⇒ **gap**)*

2. Convergence
   → **stop** | **gap**

| field          | value |
|----------------|-------|
| Root           | `<rule §ID>` — <excerpt \| "gap — no rule covers <topic>"> |
| Fix (generate) | <rule diff for implement/produce phase — correct from the start \| n/a> |
| Fix (detect)   | <rule diff for verify/check phase — safety net \| n/a> |
| Confirm        | awaiting user approval |
````

G2 skippable → keep heading `### G2 — Rule in CLAUDE.md / .claude/ & Prevention`, body = one line: `skip — G1 already covers it (<short reason>)`. Do not delete heading → grep `### G2` to audit format-complete RCAs.

### §4.1 element rules

| element | rule |
|---|---|
| numbered why | `<n>. <Q>?` line 1; `   → <A>` line 2 (3-space indent) |
| blank line | between whys; between Symptom→G1; between G1→G2 |
| `---` separator | before each `### G<n>` |
| Outcome table | 3 rows: Root / Fix / Verify (G1) or Root / Fix / Confirm (G2) |
| `` `file:line` `` / `` `§ID` `` | backtick every falsifiable ref |
| decoration | none — no emoji |
| narrative language | Vietnamese for questions/answers/cell text; backticked refs and field labels stay literal |

## §5 falsifiable why

<example type="why">
❌ "AI misunderstood context" — abstract, not falsifiable
✅ "agent read `frontend/patterns/null-safety.md` §2 — no ❌/✅ pair for optional chain → rule ignored" — cites §ID, grep-verifiable

❌ Group-merge: Root = "code emitted wrong HTTP method"; Fix = "change GET → POST"
✅ G1 Root: `UserController.cs:42` uses `[HttpGet]`; Fix: change attribute
✅ G2 Root: `patterns/response-convention.md` §3 shows only GET examples → agent defaults to GET when the report spec is ambiguous; Fix: add §3.1 "HTTP method read from report spec §endpoints, no default"
</example>

<example type="g2_two_layer_fix">
❌ G2 Fix = only detect layer → "add verify check for field name mismatch"
   (skips the generative layer — bug still gets produced, only caught later)

✅ G2 Fix (generate) = `report-section-writer §X`: when the report spec uses abstract/opaque field names,
   read the actual upstream data schema before writing the section
   G2 Fix (detect)   = `report-reviewer §Y`: compare section field names against upstream schema field names;
   REJECT if they diverge
</example>

## §6 relation

before acting → `.claude/rules/critical-thinking.md` (challenge direction). after defect → this file. both may apply same turn.

<critical_recap>
1. answer exactly the 2 question groups, no free-form
2. G2 skippable when G1 covers it — state reason, keep heading
3. each why = falsifiable hypothesis (cite file:line | §ID)
4. G2 rule fix → user confirms before apply
5. guidance file in English; final RCA report rendered in Vietnamese
</critical_recap>
