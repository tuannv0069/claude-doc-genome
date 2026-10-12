---
scope: portable
---

<critical>
scope: creating or editing any Mermaid diagram, rendered by GitHub, VS Code Markdown Preview or another application with its own bundled Mermaid version.
never: reuse an identifier for two graph objects, or leave label text that the parser would read as syntax unquoted.
note: a successful parse is only the syntax check; the rendered objects and connections are then compared with the source material. Embedding rules are in `markdown.md` §2.
</critical>

# Creating and checking Mermaid diagrams

This guide covers diagram syntax, references and rendering. It does not assign a common palette, layout direction, label length or visual style to the project's outputs.

## §M1 Declare the diagram

The [Mermaid syntax reference](https://mermaid.js.org/intro/syntax-reference.html) identifies the available types, but an application's bundled version may differ from the current documentation. A flowchart's direction is a property of that diagram rather than a required convention for a kind of document.

<rules section="ALWAYS">
- Place the diagram in a fenced code block identified as `mermaid` for a Markdown renderer with Mermaid support.
- Begin the source with the declaration for the diagram type, and include the direction in a flowchart declaration, for example `flowchart LR`.
- Verify that the target renderer supports the chosen diagram type and syntax.
</rules>

## §M2 Keep labels separate from syntax

In a flowchart, `entry["Review (requested)"]` gives the node the identifier `entry` and a separate label. The [flowchart documentation](https://mermaid.js.org/syntax/flowchart.html) explains quoted text, links and supported label forms. A literal backslash followed by `n`, HTML line breaks and Markdown strings do not have interchangeable behavior in every context.

<rules section="ALWAYS">
- Use the label syntax appropriate to the diagram type, and quote label text that contains punctuation or words the parser would otherwise interpret as structure.
- Check escaping and line breaks in the target renderer.
</rules>

<example type="quoted_label">
input: a node whose label contains parentheses
❌ `entry[Review (requested)]`
✅ `entry["Review (requested)"]`
</example>

## §M3 Use identifiers consistently

Reusing an identifier refers to the same graph object; it does not create an unrelated object with the same name. A visible label can change without changing the identity of the object.

<rules section="ALWAYS">
- Assign distinct identifiers to distinct nodes and subgraphs.
- When renaming an identifier, update the edges, styling references and other diagram statements that use it.
</rules>

<rules section="NEVER">
- Make a subgraph its own child by using its identifier for an enclosed node.
</rules>

## §M4 Represent sequence interactions accurately

In a sequence diagram, participants identify the actors and messages connect them. Explicit participant declarations can control the displayed names and order. The [sequence diagram reference](https://mermaid.js.org/syntax/sequenceDiagram.html) gives the meaning of each arrow form.

<rules section="ALWAYS">
- Select arrow syntax according to the interaction being represented and verify its meaning in the reference.
</rules>

<rules section="NEVER">
- Infer application behavior from a visual convention alone; a solid or dashed arrow does not prove whether a real operation is synchronous, complete or successful.
</rules>

## §M5 Check entity relationship cardinality

The cardinality markers describe whether the relationship allows zero, one or many instances. Reversing the endpoints can produce valid syntax with the wrong meaning. The [entity relationship syntax](https://mermaid.js.org/syntax/entityRelationshipDiagram.html) lists the exact markers and relationship forms.

<rules section="ALWAYS">
- Verify both ends of every relationship against the underlying data model.
- Validate the relationship against the schema as well as checking that the diagram parses.
</rules>

## §M6 Check state transitions

`stateDiagram-v2` is one documented declaration; the [state diagram reference](https://mermaid.js.org/syntax/stateDiagram.html) describes the syntax.

<rules section="ALWAYS">
- Use state-diagram syntax supported by the target renderer.
- Verify the states, transitions and transition labels against the behavior being described.
- Make initial and terminal markers correspond to actual lifecycle boundaries.
</rules>

## §M7 (retired)

### §M7.1 (retired)

### §M7.2 (retired)

### §M7.3 (retired)

## §2 Validate syntax and meaning

A successful parse is only the syntax check.

<rules section="ALWAYS">
- Render the diagram with the intended application's Mermaid version.
- Inspect any parse error at the referenced statement, then check related identifiers, label delimiters and the diagram declaration.
- Compare the rendered objects and connections with the source material, confirming that no required actor, branch, relationship or state is missing and that every displayed relationship is supported.
- When a dependency on unsupported syntax remains, report that limitation and use a supported representation within the task's scope.
</rules>

## §3 Diagnose a rendering failure

An error mentioning a node's parent can indicate an identifier collision between a node and its subgraph. An unexpected token near a label can indicate that text was parsed as Mermaid syntax. A feature that works in a current editor but fails in the destination application can indicate a version or configuration difference. For Markdown fence or embedding problems, use `markdown.md` §2.

<rules section="ALWAYS">
- Treat those patterns as investigation leads: reproduce the failing diagram, identify the concrete statement and test the correction in the destination renderer.
</rules>

<rules section="NEVER">
- Claim a universal cause from an error message alone.
</rules>
