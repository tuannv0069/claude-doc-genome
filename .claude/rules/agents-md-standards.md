---
paths:
  - "**/AGENTS.md"
  - "**/AGENTS.override.md"
scope: portable
---

<critical>
target: AGENTS.md — the Codex root index, loaded on every Codex turn.
first law: the root AGENTS.md is GENERATED from CLAUDE.md — edit the source, re-render, never type into the target.
format: identical to CLAUDE.md — `claude-md-standards.md` owns every wording, density, section and trigger law; this file holds only the Codex deltas.
slot map + why each delta exists: `.agent-workspace/guide/general/harness-adapter.md` §2, §3.
language: English regardless of conversation language.
</critical>

<rules section="NEVER">
- hand-edit the root `AGENTS.md` — it is overwritten by the next render and the edit leaves no diff (`harness-adapter.md` §4)
- inline the always-loaded rule tier into `AGENTS.md` to imitate Claude Code's auto-load — the tier exceeds the byte cap and the overflow is dropped without a warning (`harness-adapter.md` §3.1)
- write genome content into `.codex/rules/` — that directory is Starlark shell-command policy, not a rule tier (`harness-adapter.md` §3.3)
- rely on a nested `AGENTS.md` to scope a standard to a file type — nesting scopes by working directory, not by the file being edited (`harness-adapter.md` §3.2)
</rules>

<rules section="ALWAYS">
- change the rules Codex must load → edit `CLAUDE.md` and the rule file, then re-render
- always-loaded rule → reaches Codex only as a `MUST Read <file>` trigger line, wording per `claude-md-standards.md` `<trigger_lines>`
- path-scoped standard that must hold on Codex → give it a root trigger keyed to action + concrete object, not only a nested file
- a hand-written nested `AGENTS.md` (a project's own, below the root) → same format law as `CLAUDE.md`; it is additive to the chain, so it repeats nothing the root already carries
</rules>

<size_budget>

Two budgets apply at once, and the tighter one wins.

| budget | measured by | source |
|---|---|---|
| < 200 lines | `wc -l AGENTS.md` | the format law inherited from `claude-md-standards.md` |
| < 32 KiB | `wc -c AGENTS.md` | Codex `project_doc_max_bytes`, default 32768 |

The byte budget is the one the platform enforces silently: past it Codex stops adding files to
the instruction chain, so the loss lands on whichever nested file came next — never on the root
file whose size caused it. Counted, never estimated.

over → extract per `claude-md-standards.md` `<extract_target>`, then re-render.

</size_budget>

<example type="always_loaded_rule">
input: a guardrail that Claude Code loads every turn from `.claude/rules/`
❌ AGENTS.md: [the rule's full text pasted in]
✅ AGENTS.md: `<observable cond> → MUST Read .claude/rules/<file>.md`
</example>

<example type="edit_target">
input: the Codex agent keeps skipping a rule; the fix is one more line of guidance
❌ add the line to AGENTS.md — gone at the next render
✅ add the line to CLAUDE.md, re-render, commit both
</example>

<critical_recap>
1. AGENTS.md is generated — CLAUDE.md is the file you edit
2. format law is `claude-md-standards.md`; only the deltas live here
3. two budgets: < 200 lines AND < 32 KiB, both counted
4. Codex has no always-loaded tier — every such rule arrives as a trigger line
5. `.codex/rules/` is shell-command policy, never genome content
</critical_recap>
