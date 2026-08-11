---
scope: project
---

<critical>
scope: store of agent working-technique lessons — raw records, append-only, never auto-loaded.
never: paste a record into a guide file | store a project fact here (→ `docs/` work product) | store user identity or preference here (→ harness memory)
always: match §1 against the work about to start, BEFORE starting it — no match → skip, lookup done | record in the same turn as the correction | write records to `.claude/rules/rule-writing-standards.md` — this folder is inside its `paths:`
</critical>

Procedure for recording / escalating / reading back: `.agent-workspace/guide/general/lesson-capture.md`.

## §1 router — work type → file

CLAUDE.md routes every artifact task here first. Match the `work type` cell against the work about to be done — no row matches → skip, lookup done, read nothing. Never fall back to a near-miss file (`lesson-capture.md §7`).

| file | work type — the action about to be performed | paired guide |
|---|---|---|
| `verify-context-rule-change.md` | about to verify that an edit to `CLAUDE.md` / `.claude/rules/*` changed agent behaviour | — |

Add / rename / delete a store file → update this table — this table IS the read-back wiring (`lesson-capture.md §7`) — **and** the pointer line at the top of its paired guide, in the same commit (`lesson-capture.md §5`).

## §2 store file with no paired guide

A work type without its own guide holds the store file alone — register it in §1 with the guide column blank. That row is the whole reachability wiring (`lesson-capture.md §7`): no entry in `.agent-workspace/guide/index.md`, no trigger of its own.
