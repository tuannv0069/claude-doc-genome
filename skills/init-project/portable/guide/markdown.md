---
scope: portable
---

# Working with Markdown syntax and references

## §1 Check the intended renderer

Use this guide when a Markdown artifact must render or be parsed correctly. Determine which application or parser will consume it and check the syntax that application supports. Extensions such as tables, embedded HTML and Mermaid are not interpreted identically by every renderer.

Treat renderer behavior as a technical constraint on the artifact. The choice of tone, headings or presentation belongs to the project's instructions for that output when such instructions exist.

## §2 Preserve literal content

When content is meant to appear as code, ensure that the renderer treats it as literal text. Inline code and fenced code blocks prevent many Markdown characters from being interpreted as structure. Choose fence delimiters that do not close early on delimiters inside the example. A language identifier can enable syntax highlighting when the renderer supports it; the identifier must not misrepresent the content.

Check list indentation, table separators and block boundaries in the rendered result. Add the spacing or escaping required by the target parser instead of assuming that source indentation alone proves the intended structure. A literal pipe in a table cell, for example, must not accidentally create another data column.

Do not rely on raw HTML unless the target renderer supports the required element and its behavior has been checked. When angle-bracket text is data rather than markup, encode it as literal content. Follow `mermaid.md` §M1 for embedded Mermaid blocks.

## §3 Keep links attached to their targets

When a heading, file path or section identifier changes, find its incoming links and references and update them in the same change. For instruction references, use the stable identifiers described in `doc-system-mechanics.md` §2.

For rendered heading links, obtain or verify the anchor produced by the target renderer. Do not assume that a simple lowercase-and-hyphen conversion handles punctuation, repeated headings or non-ASCII text in every application. Open the resulting link to confirm that it reaches the intended section.

## §4 Verify the artifact

Inspect the rendered document where layout or embedded content matters. Check that code remains literal, tables retain the intended cells, links resolve and embedded diagrams load. If a program also reads the Markdown, run its relevant checks on the same file; a document can render acceptably while violating that program's schema.
