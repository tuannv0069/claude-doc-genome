---
scope: portable
---

# Verifying Mermaid diagrams

## §1 Use the target renderer's syntax

Confirm that the intended application supports the chosen Mermaid type and syntax. A current online example may depend on a newer version than the destination. In Markdown, identify the diagram block as Mermaid and supply the declaration required by its type. Direction and visual choices belong to the individual diagram's purpose.

Separate labels from identifiers using the syntax supported by that diagram type. Quote or escape label text when punctuation would be interpreted as syntax. Check line breaks in the actual renderer rather than assuming HTML breaks, literal newline escapes and Markdown strings are interchangeable.

## §2 Preserve identity and meaning

Give distinct objects distinct identifiers and update edges and references when renaming them. Reusing a node or subgraph identifier refers to that object and can accidentally create an invalid parent relationship.

For sequences, compare participants and messages with the source behavior. Arrow appearance alone does not prove an operation is synchronous or successful. For entity relationships, verify cardinality at both ends against the schema. For state diagrams, check states, transitions and lifecycle boundaries against the actual system. Valid syntax can still describe false behavior.

## §3 Validate the final artifact

Render with the destination's Mermaid version and inspect errors at the stated source location. Check related delimiters, identifiers and declarations before accepting a symptom-based diagnosis. Compare rendered objects and relationships with source evidence to find both missing elements and unsupported additions.

If required syntax is unavailable, use a supported representation within the task's scope and state the limit. Use `markdown.md` §2 for embedding errors. A parse success is syntax evidence, not proof that the diagram represents the right system.
