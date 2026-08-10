---
scope: project
documentType: Category Router
purpose: Category-level router for docs/ — locate a document group; file-level discovery via naming convention or per-category index
status: Final
---

# docs/ — Category Router

Router stops at **category level** (per `.claude/rules/doc-organization.md §11`). Find a specific file via naming convention or a category's own `index.md`/`README.md`.

Agent guidance ("how to do it right") lives in `.agent-workspace/guide/` (own router: `.agent-workspace/guide/index.md`) — **not** under `docs/`. Categories here are project **work product**.

## §1 categories

| category | content | read when |
|---|---|---|
{{CATEGORY_ROWS}}

## §2 rules (work product)

- new category → create + register one row in §1 in the same commit (`doc-organization.md §11`).
- every `.md` in `docs/` carries YAML frontmatter; content rules per `.agent-workspace/guide/general/` documentation standard.
