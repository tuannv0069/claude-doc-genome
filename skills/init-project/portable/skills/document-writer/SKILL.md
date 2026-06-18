---
name: document-writer
description: >
  Use this skill when creating or substantially rewriting a substantive .md document
  outside `.claude/**` and `docs/agent-guide/**` (guideline, spec, design doc, process doc),
  or when the user invokes /document-writer on such a path. Acts as a Technical Editor applying
  §A–§G writing constraints as pre-writing rules; all headings use §, cross-references use §X.Y.

  TRIGGER when: (1) creating a new substantive .md document outside `.claude/**`
  (guideline, spec, design doc, process doc); (2) rewriting or restructuring an existing
  .md document outside `.claude/**` substantially (not minor edits or typo fixes);
  (3) user explicitly invokes /document-writer on a path outside `.claude/**` and `docs/agent-guide/**`.
  DO NOT TRIGGER for: any path under `.claude/**` (skill files, agent instructions, rules)
  or `docs/agent-guide/**` (on-demand agent rule tree — governed by their own standards),
  appending small updates, fixing typos, updating version numbers, or any path the project's
  CLAUDE.md `## document writing` skip list declares out of scope (e.g. detailed-design-*.md, auto-generated content).
argument-hint: <OUTPUT_PATH> [CONTENT_BRIEF]
user-invocable: true
allowed-tools: Read Write Edit Glob
---

## dependencies
- `docs/agent-guide/general/mermaid.md` §M7 + §2 — required only when the output document contains a ` ```mermaid ` block (applied in §5.8).

## §1 Role

You are a Technical Editor. Write every document to be precise, self-contained, and unambiguous:

- Every sentence is either an instruction or a fact the reader needs.
- No implicit context — state everything explicitly.
- Readers include both humans and LLM Agents executing the document.

## §2 Input Validation

Parse `$ARGUMENTS`: first token = `{OUTPUT_PATH}`, remainder = `{CONTENT_BRIEF}`.

If `{OUTPUT_PATH}` is missing → stop:

```
Error: OUTPUT_PATH is required.
Usage: /document-writer <OUTPUT_PATH> [CONTENT_BRIEF]
```

If `{OUTPUT_PATH}` is under `.claude/**` → stop:

```
SKIP: .claude/** files are out of scope (each file type has its own standard under .claude/rules/).
```

If `{OUTPUT_PATH}` is under `docs/agent-guide/**` → stop:

```
SKIP: docs/agent-guide/** is the on-demand agent rule tree — out of scope (governed by doc-organization.md).
```

If `{OUTPUT_PATH}` matches a pattern in the project's document-writing skip list (the project CLAUDE.md `## document writing` section — e.g. `detailed-design-*.md`, auto-generated files) → stop:

```
SKIP: {OUTPUT_PATH} is in the project's document-writing skip list.
```

If `{OUTPUT_PATH}` already exists → read it first. Mode = **rewrite** (preserve intent, apply §4–§5 constraints). Otherwise mode = **new**.

## §3 Scope

Apply to any `.md` document in the project outside `.claude/**`: guidelines, specs, design docs, process docs, READMEs, business documentation.

**Excluded:**
- Any path under `.claude/**` (skills, agents, rules — governed by their own standards in `.claude/rules/`).
- Any path under `docs/agent-guide/**` (on-demand agent rule tree — governed by `doc-organization.md`, not these §A–§G constraints).
- Any path the project declares out of scope in its CLAUDE.md `## document writing` skip list (e.g. `detailed-design-*.md`, auto-generated files) — governed by that project's own rules.

## §4 Heading Convention

- Every heading = `§N` or `§N.M` prefix (e.g., `## §1 Overview`, `### §2.1 Step`).
- No plain numbered headings (`## 1.`, `## Step 1`) and no unnumbered headings.
- `§` numbers are unique across the entire document — no duplicates.
- All internal cross-references use `§X.Y` form only — never heading text.

## §5 Writing Constraints

Apply all seven constraints **while writing**, not as a post-review pass.

### §5.1 §A — Minimalism

- Delete any sentence removable without losing information.
- Each bullet states exactly one fact or instruction — never two.
- No example that illustrates something already obvious from the rule.
- Introduction / purpose section: maximum 2 lines.

### §5.2 §B — Accuracy & Consistency

- Every statement must be factually correct and current.
- No term collision between sections — same word = same meaning throughout.
- Every cross-reference (`§X.Y`, file path, ID) must exist and be contextually correct.
- No task defined in two separate places — one canonical location per task.

### §5.3 §C — Structure & Navigability

- Section order = execution order — top-down = step-by-step.
- Each heading is descriptive enough for an agent to decide skip/read without reading the body.
- Scope declared explicitly: what is included AND what is excluded.

### §5.4 §D — § Identifiers

- Every heading carries `§N` or `§N.M` — see §4.
- All internal cross-references use `§X.Y` — never heading text.
- `§` numbers are unique in the document.
- After adding, removing, or reordering sections: update all `§` references.

### §5.5 §E — Executability

- Every instruction uses imperative, active voice.
- No point that forces the agent to infer or decide unguided.
- Every step declares its Input and Output explicitly.
- Schema / template / example is complete enough that the agent needs no external lookup.

### §5.6 §F — Autonomy

- Agent can complete end-to-end without asking.
- Output of step N is a valid Input for step N+1.
- Done condition defined explicitly: "done = when X".
- Fallback defined for every ambiguity or missing-information scenario.

### §5.7 §G — Dynamic Compatibility

- All branch conditions (`if/else`, conditional overrides) stated explicitly — agent must not infer them.
- If sections apply only under certain conditions (version, context), scope is stated in the heading or opening line.

### §5.8 §H — Mermaid Diagrams

For each ` ```mermaid ` block in output, apply `docs/agent-guide/general/mermaid.md` §M7 + §2:

- `%%{init}%%` baseline present per §M7.3 (mandatory; sets `lineColor` so arrows are not gray default).
- `classDef` palette matches §M7.2 (6 semantic colors only: `process`/`decision`/`terminal`/`warning`/`error`/`external`); no custom hex outside whitelist.
- Total nodes ≤ 15 per diagram (§M7.1); split if exceeds.
- Labels ≤ 6 words per line; line break via `<br>`, never `\n`.
- No emoji inside diagram nodes (emoji allowed in prose only per §M7.1).
- Labels containing `()`, `,`, `:`, `{}`, Unicode, or reserved words → quoted per §M2.
- Direction: `TD` for process flows, `LR` for pipeline/layer per §M7.1.
- Subgraph ID must not collide with any node ID in the same diagram (§M3).

## §6 Self-Check Before Output

After drafting, verify each item. Fix in-place. Do not skip.

- [ ] §D: every heading has `§N` or `§N.M` — no plain numbered or unnumbered headings
- [ ] §D: all internal cross-references use `§X.Y` form
- [ ] §D: no duplicate `§` numbers in the document
- [ ] §A: no sentence removable without information loss
- [ ] §B: no term collision between sections
- [ ] §B: no cross-reference pointing to a non-existent section or file
- [ ] §C: section order matches execution order
- [ ] §C: scope section present and states both inclusions and exclusions
- [ ] §E: every instruction is imperative and active
- [ ] §E: every step has explicit Input and Output
- [ ] §F: done condition defined
- [ ] §F: fallback defined for ambiguity scenarios
- [ ] §G: all branch conditions stated explicitly
- [ ] §H: every ` ```mermaid ` block has `%%{init}%%` baseline (§M7.3)
- [ ] §H: `classDef` fills/strokes match §M7.2 palette only (no custom hex)
- [ ] §H: node count ≤ 15 per diagram (§M7.1)
- [ ] §H: labels ≤ 6 words per line, no emoji inside nodes (§M7.1)
- [ ] §H: special-char / Unicode labels quoted (§M2)
- [ ] §H: subgraph ID ≠ any node ID (§M3)

## §7 Output

Write the completed document to `{OUTPUT_PATH}`.

Return:

```
STATUS: DONE
FILE: {OUTPUT_PATH}
MODE: new | rewrite
CONSTRAINTS APPLIED: §A §B §C §D §E §F §G §H
```

If any §5 constraint could not be satisfied (e.g., missing source information to fill a required Input/Output), report:

```
STATUS: PARTIAL
FILE: {OUTPUT_PATH}
GAPS: [list each unresolved constraint with reason]
```

---

## §8 Usage by Orchestrators

When an orchestrator (e.g., a write-dd agent) needs a subagent to produce a document following these constraints, **embed §4–§6 directly into the subagent prompt** — do not reference this file path. Subagents cannot invoke skills or spawn agents.

Embed pattern:

```
Apply the following document writing constraints when producing {OUTPUT_PATH}:
[paste §4 Heading Convention]
[paste §5 Writing Constraints]
[paste §6 Self-Check]
```

## §9 Examples

§4 — heading convention:
✅ `## §2.1 Input Validation`
❌ `## Step 2: Input Validation` (plain numbered, no §)

§5.1 §A — Minimalism:
✅ `Trim whitespace from every column.`
❌ `It is important to note that the whitespace should be trimmed.`

§5.5 §E — Executability (explicit Input/Output):
✅ `Step 3 — Input: parsed rows. Output: deduped rows at {OUT_PATH}.`
❌ `Then clean up the data somehow.`

§5.6 §F — Autonomy (done condition + fallback):
✅ `Done = file written + self-check §6 all pass. Missing source field → emit STATUS: PARTIAL with the gap.`
❌ `Finish when the document looks complete.`
