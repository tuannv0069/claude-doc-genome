---
scope: project
---

<critical>
scope: store of agent working-technique lessons — raw records, append-only, never auto-loaded.
never: paste a record into a guide file | store a project fact here (→ `docs/` work product) | store user identity or preference here (→ harness memory)
always: read the work type's file AND every store its `checks` cell names, BEFORE starting that work | record in the same turn as the correction | write records to `.claude/rules/rule-writing-standards.md` — this folder is inside its `paths:`
</critical>

Procedure for recording / escalating / reading back: `.agent-workspace/guide/general/lesson-capture.md` (§7 = the dispatch law this file implements, §8 = which store a record belongs to).

## §1 router — work type → file

Lookup protocol — CLAUDE.md sends a task here, and this table is the only dispatch point:

1. name the work about to start as an ACTION (reading source, reviewing content, building a gate, answering a review comment, …)
2. scan the `work type` column → the matching row's file, **plus every store its `checks` cell names**, are read before the first substantive step — one hop only, never the `checks` of those
3. two rows match → read BOTH; a narrower row never cancels a broader one, because missing a store is the failure this router exists to prevent
4. **no row matches → skip and proceed.** A forced near-match costs a read and plants irrelevant caution — worse than no read
5. already looked up in this session and the work type has not changed → do not look up again
6. dispatching the work to a subagent → pass the matched file path AND every path in its `checks` cell in the dispatch prompt; the subagent may not inherit CLAUDE.md (`lesson-capture.md` §7)

| file | work type | paired guide | checks |
|---|---|---|---|
| `verify-context-rule-change.md` | about to verify that an edit to `CLAUDE.md` / `.claude/rules/*` changed agent behaviour | — | — |

Add / rename / delete a store file → update this table **and** the pointer line at the top of its paired guide in the same commit (`lesson-capture.md` §5). This table is the **only** router a store is registered in — never add a second entry elsewhere (`lesson-capture.md` §7).

The gate `.agent-workspace/tooling/verify_lesson_router.py` reads this table as a contract: the header row, four cells per row, `checks` targets that exist, no cycle, one row per store, and a `<critical>` block in every store declaring `scope:` and `phase:`.

## §2 store file with no paired guide

A work type without its own guide holds the store file alone — register it in §1 with the guide column blank. That row is the whole cost: no CLAUDE.md trigger of its own, no row in `.agent-workspace/guide/index.md`, because the unconditional lookup already reaches it (`lesson-capture.md` §7).
