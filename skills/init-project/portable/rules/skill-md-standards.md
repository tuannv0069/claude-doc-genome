---
paths:
  - ".claude/skills/**"
scope: portable
---

<critical>
target: SKILL.md (auto-loaded when description matches task)
optimize: matcher accuracy + claude executes procedurally + min tokens
ai-first: ignore human readability
note: this STANDARD file uses XML wrap; SKILL.md target uses plain markdown
cross-file rule placement: SKILL.md MUST NOT inline substantive code rule (canonical shape, snippet, fix template, prop list) — reference agent-guide §ID; see `doc-organization.md`.
</critical>

<rule_schema>
skill_md:
  frontmatter: { name: kebab-case, description: <triggers + scope> }
  primary_structure: numbered workflow (procedural)
  required_sections: [purpose, dependencies, workflow, examples]
  optional_sections: [conditional, edge_cases, reference_files]

skill_rule:
  start: imperative verb | numbered step
  length: ≤ 1 line per step
  workflow: must end with verification step
</rule_schema>

<priority>
1. matcher accuracy (description triggers correct skill)
2. workflow correctness (steps + verification)
3. dependency clarity
4. token efficiency
</priority>

---

<core_rules>

### wording

```
✅ Read source PDF: `view <path>`
✅ encoding error → retry with latin-1
❌ You should generally start by reading...
```

cut test: remove word → behavior unchanged → cut

### RFC2119 budget

| keyword | use | budget |
|---------|-----|--------|
| MUST/NEVER | hard limits | ≤10% rules |
| SHOULD | defaults | majority |
| MAY | opt-in | minority |

### format density (most-compressed first)

1. table — parallel branches
2. arrow — simple if-then
3. numbered list — workflow (order matters)
4. bullet — independent rules
5. prose — only if nuance

| content | format |
|---------|--------|
| workflow | numbered, imperative |
| branching | conditional table |
| dependencies | bullet under `## dependencies` |
| frontmatter | YAML |
| examples | code block ✅/❌ |
| edge cases | prose ≤ 3 sentences |

### structural rules
- one step = one line
- semantic heading
- max 2 nesting levels
- no rule duplication across sections

</core_rules>

---

<rules section="NEVER">
- hedge: generally|typically|usually|try|consider|might|perhaps|ideally
- vague description (matcher fails)
- overlap description with another skill (matcher ambiguity)
- skip frontmatter (skill won't load)
- hardcode paths varying by environment
- decorative md (emoji, !!!, CAPS-for-emphasis)
- restate workflow steps for emphasis
- MUST/NEVER on rules with exceptions
- XML wrap SKILL.md target body (over-engineering)
</rules>

<rules section="ALWAYS">
- frontmatter with name + description (required)
- description: trigger keywords + use cases + scope boundary
- workflow as primary structure (numbered, imperative)
- declare tool/library dependencies upfront
- companion files → reference with explicit path
- abstract step → ✅/❌ example
- include verification step at end of workflow
</rules>

---

<frontmatter_spec>

```yaml
---
name: <kebab-case-id>
description: <when to trigger + scope + keywords>
---
```

description rules:
- start with "Use when..." or "Use this skill when..."
- list concrete trigger phrases
- specify scope boundary ("Do NOT use for X")
- 2-4 sentences max

</frontmatter_spec>

---

<token_budget>

| complexity | tokens |
|------------|--------|
| simple (single workflow) | < 500 |
| medium (multiple workflows) | < 1500 |
| complex (many branches) | < 3000 |

over → split into narrower skills, OR extract examples/templates to companion files

</token_budget>

---

<companion_files>

| content size | location |
|--------------|----------|
| 1-2 line example | inline |
| 5-20 line example | inline if essential, else companion |
| > 20 line example | companion file always |
| reusable template | companion file always |

reference pattern:
```
## reference files
- templates: ./templates/*.json
- scripts: ./scripts/extract.py
```

</companion_files>

---

<workflow_rules>
- numbered list (order matters)
- each step: 1 imperative action
- verification step at end (mandatory)
- branch points → conditional table, not inline if-else prose
- step depends on prior output → reference explicitly ("from step 2: ...")
- declare dependencies upfront (no hidden requirements)
</workflow_rules>

---

<example type="description">

input: PDF processing skill

✅ output:
```yaml
description: Use when user asks to read, extract text from, merge, split,
  rotate, watermark, or fill PDF files. Trigger keywords: PDF, .pdf,
  extract pages, combine PDFs, OCR. Do NOT use for creating non-PDF
  documents (use docx skill instead).
```

❌ output: `description: Helps with PDF stuff`
verdict: vague, no triggers, no scope

❌ output: `description: Use this skill for any document work`
verdict: too broad, overlaps docx/xlsx/pptx

</example>

<example type="full_skeleton">

input: skill for cleaning CSV files

✅ output:
```markdown
---
name: csv-clean
description: Use when user asks to clean, normalize, deduplicate, or 
  validate CSV/TSV files. Trigger keywords: CSV, TSV, clean data, 
  remove duplicates, normalize columns. Do NOT use for Excel files 
  (use xlsx skill).
---

# csv-clean

## purpose
Clean and normalize CSV/TSV: trim whitespace, dedupe rows, 
standardize column names, validate types.

## dependencies
- pandas >= 2.0
- ./templates/column-mappings.json (optional)

## workflow
1. Read CSV: `pd.read_csv(path, dtype=str)` (preserve original strings)
2. Trim whitespace: `df = df.apply(lambda c: c.str.strip())`
3. Standardize columns: `df.columns.str.lower().str.replace(' ', '_')`
4. Drop duplicates: `df.drop_duplicates()`
5. Validate: report row count before/after
6. Write output: `df.to_csv(out_path, index=False)`

## conditional
| situation | action |
|-----------|--------|
| header missing | infer from first row, prompt confirm |
| mixed delimiters | detect with `csv.Sniffer()` |
| encoding errors | retry with `encoding='latin-1'` |

## edge cases
For files > 1GB, use chunked: `pd.read_csv(path, chunksize=10000)`.
```

❌ output:
```
## workflow
You should generally start by reading the PDF, and then maybe consider
extracting text. After that, it's a good idea to put the text together
somehow, and then check if it worked...
```
verdict: hedges + vague + no verification + prose

</example>

---

<anti_patterns>

```
❌ description overlaps other skills
description: "Use for working with documents"
→ which type? overlaps docx/pdf/xlsx

❌ workflow as prose
"First open the file, then probably parse, after that..."
→ numbered imperative list

❌ missing verification step
1. Extract data
2. Format output
[silent failures possible]
→ add: "3. Verify: row count matches source"

❌ hidden dependencies
[uses pypdf without declaring]
→ list in `## dependencies`

❌ inline mega-example (200+ lines)
→ extract to ./examples/full-flow.py

❌ deep nesting (>2 levels)
1. main step
   - sub step
     - sub sub step
→ flatten or split workflow
```

</anti_patterns>

---

<maintenance>
- skill silent fail → audit description (matcher missed it?)
- skill triggers wrong task → narrow description scope
- workflow step ambiguous → add ✅/❌ example
- skill > 3000 tokens → split by sub-task
- new tool/library → update `## dependencies` first
</maintenance>

---

<self_check>
- [ ] frontmatter present (name + description)
- [ ] description has triggers + scope + use cases
- [ ] dependencies declared explicitly
- [ ] workflow numbered + imperative + verification at end
- [ ] companion files referenced with explicit paths
- [ ] zero hedges in instruction text
- [ ] heavy examples → companion files
- [ ] under token budget
- [ ] no overlap with other skills' descriptions
- [ ] MUST/NEVER ≤ 10% rules
- [ ] no nested bullets > 2 levels
- [ ] no XML wrap in SKILL.md target body

fail → fix before commit
</self_check>

---

<critical_recap>
1. frontmatter description = matcher (triggers + scope + keywords)
2. workflow = numbered imperative + verification at end
3. dependencies declared explicit (no hidden requirements)
4. SKILL.md target body uses plain markdown (no XML wrap)
5. > 20 line examples → companion files
</critical_recap>