---
scope: portable
---

<critical>
scope: a working technique just failed — user correction, repeat failure, a probe that lied. Record it so the next run of the SAME work type does not repeat it.
core: record in the turn it failed | one store per work type, never inside a curated guide | escalate by recurrence: record → rule → machine check.
forbidden: work-technique lesson in harness memory | record pasted into a guide | record promoted straight to always-loaded | a store nothing reads.
note: §ID append-only (portable) — never renumber; retired sections keep their number.
</critical>

# Lesson capture

## §1 Which store — three destinations, no overlap

Record = raw, dated, unvalidated, append-only. Rule = curated law, small, stable, read every time. Different content classes, so they live apart.

| what was learned | store |
|---|---|
| how to DO a kind of work (query form, tool choice, step order, a probe that lied) | `.agent-workspace/lessons/<work-type>.md` |
| a fact ABOUT the project (term, decision, official knowledge) | the project's work product — `docs/<category>/` per `doc-organization.md §11` |
| who the user is / a preference outliving this project | harness memory |

<example type="store_choice">
input: user says "stop globbing the shared test dir — run only this task's tests"
❌ write to harness memory — dies outside this harness, invisible to the next agent in-repo
✅ record under the work type; distil into the file-reading rule on recurrence
</example>

## §2 When to capture

<rules section="ALWAYS">
- user corrects the method / rejects the output / redirects the approach → record
- same failure class returns despite an existing rule → record + escalate (§4)
- probe or script answered confidently and proved wrong → record the query FORM
- fix shows the earlier diagnosis was wrong → record what made it look right
- record in the turn the signal appears — deferred to end-of-task = lost
</rules>

<rules section="NEVER">
- record a one-off fact about the artifact worked on — belongs in the work product
- record the same lesson twice — increment `seen` on the existing entry
- ask permission to record — the store is a capture layer, not Truth
</rules>

## §3 Record shape

<rules section="ALWAYS">
- one store file per work type, kebab-case, named after the ACTION
- name the file to match the trigger of the guide it pairs with
- register the file in `.agent-workspace/lessons/index.md` in the same commit
- write records in the language of the guide the store pairs with — English by default
- write every record to `rule-writing-standards.md` — the store is inside its `paths:`
- heading = the lesson as ONE imperative line; it is the rule a promotion will lift verbatim
- `✅` line = imperative | `cond →`, ≤ 20 words; longer means two rules, so split the record
</rules>

<example type="file_name">
input: naming the store for lessons about reading legacy source
❌ `legacy-source.md` — names the subject, matches no trigger
✅ `read-legacy-source.md` — names the action the trigger fires on
</example>

```markdown
### <lesson as one imperative line>
- signal — how to recognize the situation next time
- ❌ what was done, and why it looked right
- ✅ what to do instead
- evidence — `file:line`, command, or the correction that produced it
- seen — 1
```

`❌`/`✅` is not decoration: `rule-writing-standards.md` requires the pair on any abstract rule, so a record already carries the shape its promotion (§4, `seen` 2) needs. Same language as the target guide is what keeps the lift a copy instead of a translation — a translated promotion is a hand step where meaning drifts.

## §4 Escalation ladder

| `seen` | action |
|---|---|
| 1 | record only (§3) |
| 2 | distil into a rule with a `§ID` in the work type's guide; record stays put |
| 3, or mechanically decidable at any count | build a check that fails on it; rule stays as the human-readable why |

Prose gets skipped; a failing check cannot be.

<rules section="NEVER">
- promote a record to an always-loaded rule — that tier is pre-decision guardrails only (`doc-organization.md §8.2`)
- ship a check that fires on correct work — a gate that cries wolf gets ignored
- copy record text into a guide — distil to an atomic rule per `rule-writing-standards.md`
</rules>

<example type="escalation">
input: the same wrong query form has now cost three passes
❌ append a 3rd near-identical record — the store grows, the next run repeats it anyway
✅ `seen — 3` → write the check that fails on that form; keep the rule as the why
</example>

## §5 Read-back — the store must be reachable

<rules section="ALWAYS">
- read the store file BEFORE starting the work, not after failing
- work type has a paired guide → that guide carries ONE pointer line at its top
- work type has no guide → register in `lessons/index.md` + route from the guide router
- split a store file only when it covers more than one work type
</rules>

<example type="pointer_line">
input: routing a store so the agent reaches it without a new always-loaded line
❌ add a second trigger for the store — pays budget twice for one work type
✅ `lessons already paid for → .agent-workspace/lessons/<work-type>.md` at the top of the paired guide; its existing trigger reaches both
</example>

The store is never loaded per turn, so it may grow without limit.

## §6 relation

- `doc-organization.md §11` — the work-product layer where a fact ABOUT the project lands; §1 draws the boundary so neither store holds the other's content.
- `five-why.md` — run it when the record's `wrong` line cannot explain itself; the root cause is what gets recorded, not the symptom.
- `doc-organization.md §1` — content classification; §8.3 branch 5 routes a record here, and §4's step 2 is what turns it into a substantive rule with a `§ID`.

<critical_recap>
1. record in the SAME turn as the correction — deferred means lost.
2. three stores, no overlap: work technique → `lessons/`; project fact → `docs/` work product; user identity → memory.
3. records never live inside a curated guide — that is what makes guides bloat.
4. escalate by recurrence: record → rule → machine check; a check beats prose because it cannot be skipped.
5. a gate that fires on correct work is worse than no gate.
</critical_recap>
