---
scope: portable
---

<critical>
scope: all *.md in repo
rendering: GitHub, VS Code Markdown Preview
companion: `docs/agent-guide/general/mermaid.md` — before creating/editing any Mermaid diagram
</critical>

<rules section="NEVER">
- bare ` ``` ` without language tag
- `*` or `+` for unordered lists
- multiple H1 per document
- skip heading levels (H1→H3, skipping H2)
- raw HTML tags in prose or tables
- `\n` in Mermaid node labels
</rules>

<rules section="ALWAYS">
- blank line before and after: headings, lists, code blocks, tables
- specify language on every fenced code block
- `-` for unordered list items
- wrap code symbols in backticks: `functionName`, `myFile.ts`
- update all anchor links and `Section X.Y` references after section rename/reorder/delete
</rules>

<conditional>
| context | rule |
|---------|------|
| code block inside list | indent 4 spaces + blank line before |
| nested code block | outer uses n+1 backticks |
| `<tag>` as code in table cell | `` `<tag>` `` |
| `<` as literal mid-text | `\<tag\>` |
| `<br>` in Mermaid node | allowed only inside ` ```mermaid ` blocks |
</conditional>

<examples>

<example type="blank_lines">
✅
```
paragraph

## Heading

- item 1
- item 2

| Col A | Col B |
|-------|-------|

next paragraph
```
❌ No blank lines between paragraph/heading/list/table.
</example>

<example type="code_language">
✅ ` ```typescript `
❌ ` ``` ` (bare, no language tag)
</example>

<example type="nested_code_blocks">
✅ outer uses 4 backticks, inner uses 3
❌ outer and inner both use 3 backticks (inner closes outer prematurely)
</example>

<example type="html_in_table">
✅ `| 51 | \`<script>alert(1)</script>\` | Validation error |`
❌ `| 51 | <script>alert(1)</script> | Validation error |` (raw angle brackets)
</example>

</examples>

## anchor integrity

After any change to section numbers, headings, or order:

1. scan entire file for anchor links and `Section X.Y` / `mục X.Y` text references
2. update slug, number, and display text to match new structure

Anchor slug: lowercase, spaces → `-`, remove all punctuation except `-`.

<example type="anchor_update">
✅ Inserted §5.2; old §5.2 → §5.3; all references updated to `5.3`.
❌ References still say `5.2` after section renumbered to `5.3`.
</example>

## table format

```markdown
| Name       | Type   | Required |
|------------|--------|----------|
| `id`       | string | Yes      |
| `isActive` | bool   | No       |
```

## scope exclusions

code comments, config files (YAML/JSON), user-provided content, tool output/logs.

<critical_recap>
1. blank line before/after every block element (heading/list/code/table)
2. always specify language on code blocks
3. `-` not `*`/`+`; one H1; don't skip heading levels
4. no raw HTML in prose (exception: `<br>` in Mermaid nodes only)
5. update all anchors and section refs after structural changes
</critical_recap>
