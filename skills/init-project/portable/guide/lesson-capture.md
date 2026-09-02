---
scope: portable
---

<critical>
scope: a working technique just failed — user correction, repeat failure, a probe that lied. Record it so the next run of the SAME work type does not repeat it.
core: record in the turn it failed | one store per work type, never inside a curated guide | escalate by recurrence: record → rule → machine check | read-back is unconditional, routed by `lessons/index.md` §1 alone (§7) | store chosen by the phase the lesson protects (§8).
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
- inspecting another phase's product and the defect traces to that phase's METHOD → record into that phase's store (§8), not into the inspector's
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
- new record's `signal` names an action outside the store's own `<critical>` scope line → widen that scope line in the same commit
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

> Routing model superseded by §7 — the store router is the single dispatch point, reached unconditionally.
> The pointer line below survives as the secondary path (agent entering from the paired guide, not from the router).

<rules section="ALWAYS">
- read the store file BEFORE starting the work, not after failing
- work type has a paired guide → that guide carries ONE pointer line at its top
- work type has no guide → register in `lessons/index.md` + route from the guide router (retired — §7 makes registration alone sufficient)
- split a store file only when it covers more than one work type
</rules>

<example type="pointer_line">
input: routing a store so the agent reaches it without a new always-loaded line
❌ add a second trigger for the store — pays budget twice for one work type
✅ `lessons already paid for → .agent-workspace/lessons/<work-type>.md` at the top of the paired guide; its existing trigger reaches both
</example>

Primary read-back path = §7 (router lookup at task start). The pointer line above is the secondary entrance — it fires when the agent enters from the paired guide rather than from the start of a task.

The store is never loaded per turn, so it may grow without limit.

## §6 relation

- `doc-organization.md §11` — the work-product layer where a fact ABOUT the project lands; §1 draws the boundary so neither store holds the other's content.
- `five-why.md` — run it when the record's `wrong` line cannot explain itself; the root cause is what gets recorded, not the symptom.
- `doc-organization.md §1` — content classification; §8.3 branch 5 routes a record here, and §4's step 2 is what turns it into a substantive rule with a `§ID`.

## §7 Dispatch law — one unconditional lookup, not one trigger per work type

Per-work-type routing (§5) prices read-back at O(N) on the always-loaded budget: every new store must buy its own trigger, so a store's default state is unreachable. The lookup is unconditional instead — the cost stops growing and registration alone makes a store live.

<rules section="ALWAYS">
- always-loaded surface carries ONE unconditional line: start a task → read `lessons/index.md` §1, read the matching store
- store registered in `lessons/index.md` §1 → reachable; no further routing artifact needed
- write the router's work-type cell as the ACTION about to be performed, not the topic name
- no row matches the work about to start → skip and proceed; a forced near-match is worse than no read
- read the router once per task, not once per turn
- subagent doing the work → the dispatcher passes the matching store path AND every path in that row's `checks` cell, because the subagent may not inherit the always-loaded surface
- fan-out of subagents → each returns candidate records in its report and the orchestrator writes them; N agents appending to one store file lose writes
</rules>

<rules section="NEVER">
- add a per-work-type trigger for a store — the unconditional line already reaches it
- register a store in a second router — `lessons/index.md` §1 is the only one
- read a near-miss store because no row matched — a wrong lesson costs more than no lesson
- make the condition a task class (`substantive task`, `complex task`) — a class needs judgment and fails `doc-organization.md §10`
</rules>

<example type="work_type_cell">
input: router cell for the store about verifying a design before implementing
❌ `design verification` — a topic name; the agent must guess whether its work belongs to it
✅ `about to verify a design / write a verification gate` — the action, matched against what the agent is doing
</example>

<example type="new_store_cost">
input: a lesson store for a work type that has no guide
❌ new store + new CLAUDE.md trigger + new row in the guide router
✅ new store + one row in `lessons/index.md` §1 — the unconditional line already routes to it
</example>

That is why §5's per-work-type routing is the secondary entrance, not the mechanism — it needed a trigger per store, and this needs none.

## §8 Which phase does the lesson belong to

A store is chosen by the phase the record protects, never by the task that happened to be running when the record was written. The two coincide for self-contained work; they diverge whenever a task inspects the output of another phase, and that is where records land in the wrong store.

<rules section="ALWAYS">
- choosing a store → ask "the next run of WHICH phase avoids this because of the record?"; that phase's store takes it
- every store DECLARES its phase in `<critical>` as `phase: <one value>` from the closed set (writing · reviewing · answering · building-gate · orchestrating · investigating · operating); a store that would need two values is two stores
- task inspecting another phase's product (review, answering a reviewer's comment, building a gate, verify, audit, acceptance) → the record belongs to the INSPECTED phase, unless what broke was the inspection technique itself
- both phases broke, or the lesson binds every phase → the INSPECTED phase's store takes it; the inspecting phase still reaches it through its `checks` entry, so choosing the earlier phase loses nothing
- record only a repeatable METHOD failure — a one-off slip is not a record (§2)
- one record, one store; a store whose readers still hit a moved lesson carries `[[wikilink]]` pointer lines — never a copy of the record; group them into ONE line per destination phase when several lessons left for the same place
- read the matched store plus the stores its router `checks` cell names — exactly one hop, never the `checks` of those
- record moved between stores → `seen` carries over unchanged, never resets
</rules>

<rules section="NEVER">
- let the `checks` relation form a cycle
- update an old store name inside a frozen task archive (`.agent-workspace/tasks/**`, `.agent-workspace/worktrees/**`) — that text records what happened, and a stale name there is not a dead pointer
</rules>

<example type="phase_choice">
input: a review pass finds a section whose coverage was scoped from a sibling section instead of from the source
❌ record it in the review store because the review found it — the writer never reads that store before writing, so the next section repeats it
✅ record it in the writing store; the review store carries a `[[wikilink]]` if reviewers also need the signal
</example>

<critical_recap>
1. record in the SAME turn as the correction — deferred means lost.
2. three stores, no overlap: work technique → `lessons/`; project fact → `docs/` work product; user identity → memory.
3. read-back is unconditional — registering the row in `lessons/index.md` §1 IS the wiring, no per-store trigger (§7).
4. the store is picked by the phase the lesson protects, not by the task that found it (§8); every store declares `phase:`.
5. escalate by recurrence: record → rule → machine check; a check beats prose because it cannot be skipped.
</critical_recap>
