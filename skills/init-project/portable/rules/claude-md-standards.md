---
paths:
  - "**/CLAUDE.md"
scope: portable
---

<critical>
target: CLAUDE.md (project root, loaded every turn)
optimize: claude follows project rules + min tokens (compounds across session)
ai-first: ignore human readability
note: this STANDARD file uses XML wrap; CLAUDE.md target uses plain markdown
cross-file rule placement: CLAUDE.md may carry terse pointer to substantive rule; full content lives in agent-guide §ID — see `doc-organization.md`.
</critical>

<rule_schema>
claude_md_rule:
  start: imperative_verb | `cond →`
  length: ≤ 1 line, ≤ 20 tokens
  location: claude.md OR `.claude/rules/sub.md`, not both
  abstract → ✅/❌ inline
</rule_schema>

<priority>
1. token cost (loaded every turn)
2. claude follows accurately
3. project specificity
</priority>

---

<core_rules>

### wording

```
✅ run typecheck before commit
✅ stable info → answer direct
❌ you should generally try to consider...
```

cut test: remove word → behavior unchanged → cut

### RFC2119 budget

| keyword | use | budget |
|---------|-----|--------|
| MUST/NEVER | hard limits/safety | ≤10% rules |
| SHOULD | defaults, override-able | majority |
| MAY | opt-in | minority |

### format density (most-compressed first)

1. table — 3+ rules same schema
2. arrow — simple if-then
3. bullet — independent rules
4. prose — only if nuance required

| rule type | format |
|-----------|--------|
| hard limit | bullet under `## NEVER` |
| default | bullet under `## ALWAYS` |
| conditional | table or `cond → action` |
| edge case | prose ≤ 3 sentences |

### structural rules
- one rule = one line (multi-line → split)
- one rule, one location (no duplication)
- semantic heading (= "when read this section?")
- max 2 nesting levels

</core_rules>

---

<rules section="NEVER">
- hedge: generally|typically|usually|try|consider|might|perhaps|ideally
- XML wrap entire CLAUDE.md (markdown enough; XML compounds cost per turn)
- duplicate rules from `.claude/rules/` sub-files
- self-check/schema/recap blocks in CLAUDE.md (only for rule maintenance)
- decorative md (emoji, !!!, CAPS-for-emphasis)
- vague defaults ("be helpful", "use good judgment")
- MUST/NEVER on rules with exceptions
- prose paragraph when bullet/table fits
</rules>

<rules section="ALWAYS">
- imperative verb | `cond →` start
- one rule, one location
- abstract rule → ✅/❌ pair inline
- complex rule (>5 lines or >200 tokens) → extract per `<extract_target>`
- extract affecting behavior → trigger line per `<trigger_lines>`
- conflict → explicit priority
</rules>

---

<token_budget>

| project size | claude.md tokens |
|--------------|------------------|
| small (<10 files) | < 300 |
| medium (10-100 files) | < 800 |
| large monorepo | < 1500 (split aggressively) |

over → extract per `<extract_target>` → reference

</token_budget>

---

<sections_required>

| section | order | purpose |
|---------|-------|---------|
| stack | 1 | runtime, framework, db, test tool |
| NEVER | 2 | hard limits |
| ALWAYS | 3 | non-negotiable defaults |
| conventions | 4 | naming, commit, branch, structure |
| domain-specific | 5 | testing, deployment, api (optional) |
| examples | 6 | concrete good/bad |
| see also | 7 | sub-file references |

rationale: top-attention slots → constraints. bottom → reference.

</sections_required>

---

<split_to_subfile>

| signal | action |
|--------|--------|
| section > 200 tokens | extract |
| domain-specific deep detail | extract |
| many examples | extract |

reference pattern:
```
## see also
- file reading: .claude/rules/file-reading.md
- testing: .claude/rules/testing.md
- glossary: docs/agent-guide/general/glossary.md
```

</split_to_subfile>

---

<extract_target>

decide where extracted content goes:

| content type | target | reason |
|--------------|--------|--------|
| atomic rule (imperative \| cond →) | `.claude/rules/<topic>.md` | always-loaded, must pass rule-writing-standards |
| reference data (glossary, ID map, term def) | `docs/agent-guide/<topic>.md` | on-demand, no every-turn cost |
| deep how-to / patterns / examples | `docs/agent-guide/<topic>.md` | on-demand |
| navigation index / per-task reading map | `docs/agent-guide/<topic>.md` | on-demand; only read when choosing what to read next |

rule of thumb: agent needs every turn? → `rules/`. else → `docs/agent-guide/`.

extracted to `rules/` → must conform `rule-writing-standards.md` (xml wrap, NEVER/ALWAYS, imperative, no hedges).
extracted to `docs/agent-guide/` → plain reference allowed; conform `documentation.md` only.
extracted on-demand + affects behavior → trigger line in CLAUDE.md per `<trigger_lines>`.

</extract_target>

---

<trigger_lines>

- on-demand file affecting behavior → CLAUDE.md carries trigger line: `cond → MUST Read <file>`
- no trigger line AND not in any index → dead content (agent never reads it)
- trigger cond = observable signal at decision time: user keywords | task type | file type touched
- 1 trigger line buys whole on-demand file → cheaper than always-loading content

<example type="trigger_cond">
input: on-demand RCA guide must be read before any root-cause analysis
✅ output: debug / RCA / "why" / "root cause" → MUST Read docs/agent-guide/rca-guide.md first
❌ output: when deep analysis is needed → read rca-guide.md  # not recognizable at decision time
</example>

</trigger_lines>

---

<example type="full_skeleton">

input: medium project (Next.js + Postgres)

✅ output:
```markdown
# my-app

## stack
- node 20, pnpm
- next.js 15 app router
- postgres + drizzle, vitest

## NEVER
- commit .env, secrets
- use `any` without justification
- mutate props
- skip tests for new features

## ALWAYS
- run `pnpm typecheck && pnpm test` before commit
- check `lib/` for existing utility before creating
- naming: kebab-case files, PascalCase components

## conventions
| domain | rule |
|--------|------|
| commit | conventional (feat/fix/chore) |
| branch | feat/*, fix/*, chore/* |
| component | one per file, server-first |
| api route | validate with zod, return typed |

## file structure
- app/ → routes only, no business logic
- lib/ → shared utilities, pure functions
- components/ → UI, server components default

## see also
- file reading: .claude/rules/file-reading.md
- testing: .claude/rules/testing.md
```

❌ output:
```markdown
# Welcome to My Awesome Project! 🚀

## About
This is a Next.js application that we use for...
[3 paragraphs of history]

## Some Important Things ⚠️
You should generally try to make sure when working on the codebase, 
you consider whether the code follows our typical patterns...

## Guidelines
- Be helpful
- Write good code
```

verdict: prose history + hedges + vague + emoji + no NEVER/ALWAYS

</example>

---

<anti_patterns>

```
❌ duplicate rule from sub-file
claude.md: "use rg, not grep"
.claude/rules/file-reading.md: "rg > grep"
→ pick one location

❌ load-heavy reference
claude.md: [1500 tokens of test patterns]
→ extract per <extract_target> (rules/ if atomic; docs/agent-guide/ if how-to/data)

❌ stale paths/tools/conventions
→ audit on every refactor

❌ deep nesting (>2 levels)
- search rules
  - when to search
    - current info
      - specifically when...
→ flatten or extract
```

</anti_patterns>

---

<maintenance>
- audit on refactor: stale paths/tools → fix
- new rule: check sub-files first → extend if similar exists
- conflict claude.md vs sub-file → claude.md wins
</maintenance>

---

<self_check>
- [ ] every rule: imperative | `cond →`
- [ ] zero hedges in instruction text
- [ ] no duplication with sub-files
- [ ] under token budget for project size
- [ ] required sections present (stack, NEVER, ALWAYS, conventions)
- [ ] heavy detail extracted to sub-file
- [ ] every behavior-affecting extract has trigger line | index entry
- [ ] no decorative md, no XML wrap in CLAUDE.md target
- [ ] MUST/NEVER ≤ 10% rules
- [ ] no nested bullets > 2 levels

fail → fix before commit
</self_check>

---

<critical_recap>
1. CLAUDE.md target: plain markdown, no XML wrap (compounds per turn)
2. one rule = one location (claude.md OR sub-file)
3. token budget enforced (<300/<800/<1500 by project size)
4. extract sections >200 tokens to .claude/rules/
5. zero hedges, zero decoration
</critical_recap>