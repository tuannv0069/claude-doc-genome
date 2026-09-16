---
scope: portable
---

# Creating and checking Mermaid diagrams

This guide covers diagram syntax, references and rendering. It does not assign a common palette, layout direction, label length or visual style to the project's outputs.

## §M1 Declare the diagram

For a Markdown renderer with Mermaid support, place the diagram in a fenced code block identified as `mermaid`. Begin its source with the declaration for the diagram type being used. A flowchart declaration includes its direction, for example `flowchart LR`; the direction is a property of that diagram rather than a required convention for a kind of document.

Verify that the target renderer supports the chosen diagram type and syntax. The [Mermaid syntax reference](https://mermaid.js.org/intro/syntax-reference.html) identifies the available types, but an application's bundled version may differ from the current documentation.

## §M2 Keep labels separate from syntax

Use the label syntax appropriate to the diagram type. In a flowchart, quoted label text can protect punctuation or words that the parser would otherwise interpret as structure. Check escaping and line breaks in the target renderer; a literal backslash followed by `n`, HTML line breaks and Markdown strings do not have interchangeable behavior in every context.

For example, `entry["Review (requested)"]` gives the node the identifier `entry` and a separate label. The [flowchart documentation](https://mermaid.js.org/syntax/flowchart.html) explains quoted text, links and supported label forms.

## §M3 Use identifiers consistently

Assign distinct identifiers to distinct nodes and subgraphs. Reusing an identifier refers to the same graph object; it does not create an unrelated object with the same name. In particular, do not make a subgraph its own child by using its identifier for an enclosed node.

When renaming an identifier, update the edges, styling references and other diagram statements that use it. A visible label can change without changing the identity of the object.

## §M4 Represent sequence interactions accurately

In a sequence diagram, participants identify the actors and messages connect them. Explicit participant declarations can control the displayed names and order. Select arrow syntax according to the interaction being represented and verify its meaning in the [sequence diagram reference](https://mermaid.js.org/syntax/sequenceDiagram.html).

Do not infer application behavior from a visual convention alone. A solid or dashed arrow does not prove whether a real operation is synchronous, complete or successful; the source evidence must establish that meaning.

## §M5 Check entity relationship cardinality

For an entity relationship diagram, verify both ends of every relationship against the underlying data model. The cardinality markers describe whether the relationship allows zero, one or many instances. Reversing the endpoints can produce valid syntax with the wrong meaning.

Consult the [entity relationship syntax](https://mermaid.js.org/syntax/entityRelationshipDiagram.html) for the exact markers and relationship forms supported by the renderer. Validate the relationship against the schema as well as checking that the diagram parses.

## §M6 Check state transitions

Use state-diagram syntax supported by the target renderer; `stateDiagram-v2` is one documented declaration. Verify the states, transitions and transition labels against the behavior being described. Initial and terminal markers must correspond to actual lifecycle boundaries rather than merely making the diagram look complete. The [state diagram reference](https://mermaid.js.org/syntax/stateDiagram.html) describes the syntax.

## §M7 (retired)

### §M7.1 (retired)

### §M7.2 (retired)

### §M7.3 (retired)

## §2 Validate syntax and meaning

Render the diagram with the intended application's Mermaid version. Inspect any parse error at the referenced statement, then check related identifiers, label delimiters and the diagram declaration. A successful parse is only the syntax check.

Compare the rendered objects and connections with the source material. Confirm that no required actor, branch, relationship or state is missing and that every displayed relationship is supported. If a dependency on unsupported syntax remains, report that limitation and use a supported representation within the task's scope.

## §3 Diagnose a rendering failure

An error mentioning a node's parent can indicate an identifier collision between a node and its subgraph. An unexpected token near a label can indicate that text was parsed as Mermaid syntax. A feature that works in a current editor but fails in the destination application can indicate a version or configuration difference.

Treat those patterns as investigation leads. Reproduce the failing diagram, identify the concrete statement and test the correction in the destination renderer. Do not claim a universal cause from an error message alone. For Markdown fence or embedding problems, use `markdown.md` §2.
