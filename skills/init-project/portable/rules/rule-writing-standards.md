---
paths:
  - ".claude/rules/**"
  - "docs/agent-guide/**"
  - ".claude/skills/**/docs/**"
scope: portable
---

<critical>
optimize: claude accuracy + min tokens. ai-first.
core: imperative verbs | cond → action | one rule one location | smallest format
forbidden: hedges | duplication | decoration | nesting >2 | prose-when-bullet-fits
cross-file placement: substantive rule lives in ONE source-of-truth file with stable §ID; agent/skill/catalog reference via §ID, never inline — see `doc-organization.md`.
</critical>

<rule_schema>
atomic_rule:
  start: imperative_verb | `cond →`
  length: ≤ 1 line, ≤ 20 tokens
  location: exactly one section
  abstract → require ✅/❌ pair
</rule_schema>

<priority>
1. safety/hard limits (NEVER)
2. non-negotiable defaults (ALWAYS)
3. conditional behavior
4. override-able defaults
</priority>

---

<rules section="NEVER">
- hedge: generally|typically|usually|try|consider|might|perhaps|ideally
- duplicate rule across sections
- decorative md (emoji, !!!, CAPS-for-emphasis)
- nest > 2 levels
- prose when bullet/table/arrow fits
- MUST/NEVER on rules with exceptions
- multi-line bullets → split
- restate for emphasis
</rules>

<rules section="ALWAYS">
- start: imperative verb | `cond →`
- one rule, one location
- semantic heading (= "when read this?")
- abstract rule → ✅/❌ pair
- conflict → explicit priority
- wrap critical zones in xml tags
</rules>

---

<wording>

<example type="imperative">
input: rule about searching for current info
✅ output: search before factual claims about current state
❌ output: you should generally search when info might be outdated
</example>

<rfc2119>
| kw | use | budget |
|----|-----|--------|
| MUST/NEVER | safety/hard limits | ≤10% rules |
| SHOULD | defaults, override-able | majority |
| MAY | opt-in | minority |
</rfc2119>

cut_test: remove word → behavior unchanged → cut

</wording>

---

<format>

<density order="most-compressed first">
1. table — parallel rules, shared schema
2. arrow — simple if-then
3. bullet — independent rules
4. prose — only if nuance required
</density>

default: bullet
promote_to_table: 3+ rules same schema
demote_to_prose: only if conditional needs context

<format_by_type>
| rule type | format |
|-----------|--------|
| hard limit | bullet under `<rules section="NEVER">` |
| default | bullet under `<rules section="SHOULD">` |
| conditional | table \| `cond → action` |
| workflow | numbered list |
| edge case | prose ≤ 3 sentences |
| example | `<example>` block ✅/❌ |
</format_by_type>

<example type="atomic_rule">
input: complex multi-condition rule
❌ output: when user asks current events or anything changed recently, search before answering, unless stable historical knowledge
✅ output:
- current/changeable → search
- stable (history/math) → answer direct
</example>

<example type="heading">
input: section about refusal logic
✅ output: ## when to refuse
❌ output: ## 🔥 important rules
</example>

</format>

---

<template>
```
<critical>           [3-5 lines top recap]
<rule_schema>        [atomic rule shape]
<priority>           [numbered list]
<rules section="NEVER">    [≤10 bullets]
<rules section="ALWAYS">   [non-negotiable]
<conditional>        [table | arrows]
<defaults>           [override-able]
<examples>           [✅/❌ I/O pairs]
<edge_cases>         [prose ≤ 2 paragraphs]
<critical_recap>     [3-5 hardest rules, end of doc]
```
</template>

---

<maintenance>

add: search existing → modify if similar | else add to correct section | smallest format | abstract → example

edit: preserve wording if cross-referenced | update dependent examples | delete redundant

complex (>3 prose sentences): split atomic | extract subsection | replace prose with example

conflict: document priority | merge | reject new

</maintenance>

---

<anti_patterns>

```
❌ bullet-prose hybrid
- when considering whether you might search, it's generally advisable...

❌ decorative
## 🔥 **CRITICAL** rules ⚠️

❌ repetition
## search → "always search current info"
## reminder → "remember: search current info!"

❌ deep nesting (>2 levels)
❌ vague: "be helpful", "use good judgment", "format appropriately"
```

</anti_patterns>

---

<budget>
| component | tokens |
|-----------|--------|
| doc | < 2000 |
| rule | < 20 |
| section | < 200 |
| example | < 100 |

over → consolidate | cut hedges | extract
</budget>

---

<self_check>
- [ ] every rule: imperative | `cond →`
- [ ] zero hedges
- [ ] no duplication across sections
- [ ] no multi-line bullets
- [ ] headings semantic
- [ ] MUST/NEVER ≤ 10%
- [ ] abstract has ✅/❌
- [ ] priority explicit on conflicts
- [ ] critical zones in xml tags
- [ ] under budget

fail → fix before commit
</self_check>

---

<reference_example>

<example type="full_section">

input: writing rules for tool usage in a codebase

✅ output:
```
<rules section="NEVER">
- destructive cmd (rm -rf, DROP TABLE) without confirm
- commit secrets
</rules>

<conditional>
| situation | tool |
|-----------|------|
| search codebase | rg |
| read file | view |
| multi-file edit | plan → batch |
</conditional>

<defaults>
- rg > grep
- read before edit
- test after non-trivial change
</defaults>
```

❌ output:
```
## about using tools 🛠️
when working with tools, it's generally a good idea to think carefully
about which tool might be most appropriate. you should typically
consider whether the operation might have destructive consequences...
```

verdict: bad = 3x tokens, 0.5x signal, conflates 4 rules

</example>

</reference_example>

---

<critical_recap>
hardest rules (recap for end-of-doc attention):
1. NEVER use hedge words (generally|try|consider|might|perhaps|ideally)
2. one rule = one line = one location
3. abstract rule MUST have ✅/❌ pair
4. MUST/NEVER ≤ 10% of rules (signal inflation kills priority)
5. fail self-check → fix before commit
</critical_recap>