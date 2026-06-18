---
scope: project
---

<critical>
scope: map task → which `docs/agent-guide/` file to read on-demand.
never: auto-load any agent-guide file | duplicate content from sub-files
always: read explicitly when task in column matches
</critical>

## §1 placement data (per `doc-organization.md §10`)

| key | value |
|---|---|
| always-loaded budget | {{ALWAYS_LOADED_BUDGET}} lines (total of `.claude/rules/*.md` without `paths:`) |

Migration ledger — top-level files not yet at standard location (target = empty ledger, no permanent exemption):

| file | target area | move at |
|---|---|---|
| _(none — fresh init)_ | | |

## §2 router

### general (`docs/agent-guide/general/`)

| file (`docs/agent-guide/`) | read when |
|---|---|
| `general/five-why.md` | RCA / "5 why" / "root cause" request; debug bug in AI-produced artifact (code/doc) |
| `general/markdown.md` | edit any `*.md` (GFM rules) |
| `general/mermaid.md` | create/edit Mermaid diagram |
| `general/orchestration-policy.md` | ad-hoc free-session multi-step / multi-agent task (main model drives directly, no skill) — orchestrate-vs-execute model split, effort selection, plan persistence |
{{GENERAL_OPTIONAL_ROWS}}

<!-- areas (frontend/, backend/, bd/, dd/, ...) grow per doc-organization.md §7 as the project accumulates content; register each new file here in the same commit -->
