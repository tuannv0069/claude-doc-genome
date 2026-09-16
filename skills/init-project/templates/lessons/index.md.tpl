---
scope: project
---

# Lesson index

This area records working methods that failed and what was learned from them. Recording and maintaining lessons follows `.agent-workspace/guide/general/lesson-capture.md`. Project facts and user preferences belong to their own sources rather than lesson stores.

## §1 Lesson router

Before starting work, match the action to the work types below. Read every matching store and the stores named in its `checks` cell. Follow those checking links for one hop only. If nothing matches, proceed without inventing a match. Repeat the lookup when the work type changes, not while continuing the same work with unchanged stores.

When delegating the work, pass the relevant store paths to the delegate. The delegate may not receive this project's root instructions. These lookup responsibilities are defined in `.agent-workspace/guide/general/lesson-capture.md` §7.

| file | work type | paired guide | checks |
|---|---|---|---|
| _(none yet)_ | | | |

Register a store here when creating it, and keep its paired guide reference consistent according to `.agent-workspace/guide/general/lesson-capture.md` §5. The router and store metadata are validated by `.agent-workspace/tooling/verify_lesson_router.py`. A new project with no store rows or store files is valid.

## §2 Stores without a paired guide

A store does not need a new guide merely to hold its lessons. Leave the paired-guide cell empty when no guide owns that subject. The lookup in §1 already makes the store reachable, as explained in `.agent-workspace/guide/general/lesson-capture.md` §7.
