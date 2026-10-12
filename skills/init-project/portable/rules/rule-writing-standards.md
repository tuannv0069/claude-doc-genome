---
paths:
  - ".claude/rules/**"
  - ".agent-workspace/guide/**"
  - ".agent-workspace/lessons/**"
scope: portable
---

<critical>
scope: writing or editing a rule, guide, role or lesson store in this documentation system.
never: dissolve a NEVER or ALWAYS block into the surrounding prose, or state the same requirement in both.
note: the structure of a file is fixed by §2; only the wording inside it is open to rewriting.
</critical>

# Writing rules and guides

A rule or guide serves two readers at once. The assistant needs a structure it can recognize before reading: which lines are hard limits, which are required actions, where an example shows the boundary. A person needs sentences that read naturally. The structure in §2 is fixed; the wording in §3 is where readability is improved.

## §1 When this applies

Apply this standard when creating or editing any file under the paths in the frontmatter. The project entry point has its own section set in `claude-md-standards.md` §1; skills and agents follow `skill-md-standards.md` and `subagent-standards.md`. Placement of the content itself is decided by `doc-organization.md` §8.3 before this standard applies.

## §2 Structure of a file

A file keeps the following elements in this order. A new rule or guide is created with all of them from its first version; a rewrite that changes the wording keeps every element that the file already has.

1. YAML frontmatter with `scope:` and, for a path-scoped rule, `paths:`.
2. A `<critical>` block of three to five lines: a `scope:` line naming when the file is read, a `never:` line with its hardest limit, and a `note:` line for the one fact a reader must not miss. It is the summary the assistant reads first. A role file's block has the two lines defined in `.agent-workspace/guide/general/role-selection.md` §3, `scope:` and `core:`, and a role states its requirements in its numbered sections rather than in `<rules>` blocks. A lesson store instead declares its protected action and phase under `.agent-workspace/guide/general/lesson-capture.md` §8; it is an append-only record and has no `<rules>` blocks of its own.
3. One H1 title.
4. Sections with stable identifiers (`## §1`, `## §2`, `### §2.1`). Identifiers are append-only; a retired section keeps its number with a `(retired)` marker under `doc-organization.md` §12.
5. Inside a section, explanatory prose first, then the section's `<rules section="ALWAYS">` block and its `<rules section="NEVER">` block where the section has requirements of that kind. A section with no hard limit has no NEVER block; a section with no required action has no ALWAYS block.
6. `<example>` blocks where a rule is abstract: an `input:` line, a ❌ line showing the failure and a ✅ line showing the correct result.

The `<critical>` block is the file's only summary. A file does not end with a recap: every rule then exists in exactly two places with distinct roles, the summary before reading and the block at the section that owns it, and a third copy would have to be kept in step with both.

The XML tags are structure, not decoration. They mark where the assistant can find the requirements without reading the explanation, and the scanner treats a tag line as a boundary between comparable units.

<rules section="ALWAYS">
- Create a new rule or guide with every element of §2, including its `<critical>` block and a `<rules>` block for each section that states a requirement.
- Keep every structural element of §2 that the file already has when rewriting its wording.
- Put a requirement in exactly one place: the prose explains why, the block states what is required, and a sentence appears in one or the other.
- Give every new section a stable identifier before another file refers to it.
- Write the `<critical>` block from the file's actual content, so that a reader who stops there still knows the file's scope and its hardest limit.
</rules>

<rules section="NEVER">
- Remove a `<critical>`, `<rules>` or `<example>` block on the grounds that the prose already covers it.
- Add a recap, self-check or other block that restates rules already present in the file.
- Renumber a section identifier or reuse a retired one for an unrelated requirement.
- Nest headings deeper than `###`.
- Wrap an entire file in a single XML tag; the tags mark zones inside plain Markdown.
</rules>

## §3 Wording inside the structure

Each bullet in a `<rules>` block is one complete sentence that a person can read without the surrounding context: it starts with a verb or with the condition that triggers it, and it states one requirement. Explanation, rationale and examples belong in the prose or in an `<example>` block, not in the bullet.

Write in the imperative and without hedges (generally, typically, consider, might, ideally). A hedge inside a rule makes the rule optional without saying so. Reserve `never` and `must` for limits without exceptions; a default that a person may override is stated as a plain instruction.

The measure of a sentence is that its information is correct and complete and its grammar is correct. Length is not a criterion: this standard sets no line or word budget for a file, a section or a bullet, because a budget makes the writer compress sentences again to meet it, and a compressed sentence is what the reader then has to expand.

<rules section="ALWAYS">
- Write each bullet as one full sentence with one requirement, complete enough to be followed without the surrounding prose.
- Begin a bullet with the action or with the condition that triggers it.
- Give an abstract rule an `<example>` block with a ❌ and a ✅ line.
- Name the priority explicitly when two rules in the same file can conflict.
</rules>

<rules section="NEVER">
- Use a hedge inside a `<rules>` block.
- Compress a sentence into a fragment or an arrow (`cond → action`) that a reader must expand in their head.
- Shorten a sentence, or drop a condition or an example, to meet a length target.
- Repeat a requirement in another section for emphasis.
- Use decorative Markdown (emoji, exclamation marks, capitalized emphasis) inside a rule or guide.
</rules>

<example type="bullet_wording">
input: a rule that the assistant must search before making claims about current state
❌ current/changeable → search
❌ You should generally search when the information might be outdated.
✅ Search before making a factual claim about a current state that can change.
</example>

## §4 Checking a change

Before finishing an edit to a rule or guide, read the file once as the assistant would: confirm that the `<critical>` block still matches the content and names the limit that actually matters most, that each requirement appears once, and that every section keeps its identifier. Run `scan_rule_health.py` under `.agent-workspace/guide/general/rule-health.md` when the edit touches more than one file.
