---
scope: portable
---

<critical>
scope: any Markdown artifact that must render or be parsed correctly, in GitHub, VS Code Markdown Preview or a program that reads the file.
never: assume that source indentation alone proves the intended structure, or leave an incoming link pointing at a renamed heading, path or section.
note: the renderer is a technical constraint; tone, headings and presentation belong to the project's own instructions. Mermaid diagrams follow `mermaid.md`.
</critical>

# Working with Markdown syntax and references

## §1 Check the intended renderer

Extensions such as tables, embedded HTML and Mermaid are not interpreted identically by every renderer. The choice of tone, headings or presentation belongs to the project's instructions for that output when such instructions exist.

<rules section="ALWAYS">
- Determine which application or parser will consume the artifact and check the syntax that application supports.
- Treat renderer behavior as a technical constraint on the artifact.
</rules>

## §2 Preserve literal content

Inline code and fenced code blocks prevent many Markdown characters from being interpreted as structure. A language identifier can enable syntax highlighting when the renderer supports it.

<rules section="ALWAYS">
- When content is meant to appear as code, ensure that the renderer treats it as literal text.
- Choose fence delimiters that do not close early on delimiters inside the example.
- Check list indentation, table separators and block boundaries in the rendered result, and add the spacing or escaping the target parser requires.
- When angle-bracket text is data rather than markup, encode it as literal content.
- Follow `mermaid.md` §M1 for embedded Mermaid blocks.
</rules>

<rules section="NEVER">
- Give a fenced block a language identifier that misrepresents its content.
- Rely on raw HTML unless the target renderer supports the required element and its behavior has been checked.
- Leave a literal pipe in a table cell unescaped; it creates another data column.
</rules>

<example type="nested_fence">
input: a code example that itself contains a three-backtick fence
❌ wrap it in a three-backtick fence; the inner fence closes the block early
✅ wrap it in a four-backtick fence, so the inner three backticks stay literal
</example>

## §3 Keep links attached to their targets

For instruction references, use the stable identifiers described in `doc-system-mechanics.md` §2. A simple lowercase-and-hyphen conversion does not handle punctuation, repeated headings or non-ASCII text in every application.

<rules section="ALWAYS">
- When a heading, file path or section identifier changes, find its incoming links and references and update them in the same change.
- For a rendered heading link, obtain or verify the anchor produced by the target renderer and open the resulting link to confirm that it reaches the intended section.
</rules>

## §4 Verify the artifact

A document can render acceptably while violating the schema of a program that also reads it.

<rules section="ALWAYS">
- Inspect the rendered document where layout or embedded content matters: code remains literal, tables retain the intended cells, links resolve and embedded diagrams load.
- When a program also reads the Markdown, run its relevant checks on the same file.
</rules>
