---
scope: portable
---

# Checking Markdown syntax and references

## §1 Identify the consumer

Determine which renderer or parser must consume the artifact. Tables, raw HTML, heading anchors and embedded diagrams can behave differently across applications. Use this guide for technical correctness of that representation; the project owns the editorial choices of its outputs.

## §2 Preserve intended content

Use literal-code forms when characters are data rather than Markdown syntax. Choose fences that do not close early on delimiters inside the example. Check escaping, list indentation, block boundaries and literal pipes so a parser does not create unintended cells or structure. Do not assume raw HTML or a particular extension works without checking the intended renderer.

## §3 Keep links correct

Update incoming references when a file, heading or stable section changes. Use `doc-system-mechanics.md` §2 for instruction references. For a rendered heading link, verify the actual anchor; punctuation, repeated titles and non-ASCII text can make guessed slugs wrong.

## §4 Inspect both representations

When rendering matters, inspect the rendered artifact for literal code, table cells, working links and embedded content. When a program also reads the file, run the relevant parser check on the same revision. Successful rendering does not establish that a machine's record schema is valid. Use `mermaid.md` §1 for embedded diagrams.
