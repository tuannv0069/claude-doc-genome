---
paths:
  - ".agent-workspace/wiki/**"
scope: portable
---

<critical>
scope: the wiki tier — claims already established about the project's subject material, written back so a later run does not derive them again; content lives in `.agent-workspace/wiki/<subject>/<cluster>.md`, routed by `.agent-workspace/wiki/index.md`.
never: store a measurement as a claim, answer an investigation from a `hypothesis` edge, or let a contradiction at the deliverable boundary pass unresolved.
note: an investigation opens with a lookup and closes with a write-back (§6 R1); the gate checks structure and locators, never truth (§6 R8); every project-specific value is declared by the project under §7.
</critical>

# Established knowledge about subject material

The optional wiki stores claims established about material the project investigates. It helps a later task reuse that knowledge without repeating the investigation. It is separate from instructions about how the assistant works and from finished deliverables.

## §1 Decide what belongs in the wiki

A claim enters the wiki when it establishes something about the subject material and no other knowledge tier already owns it. The useful content is structure, authority and location: which source defines a set of valid values, what those values are, where a thing lives, which artifact governs it. A count or size observed at one moment can become false while its source still exists; such observations belong in the task evidence or deliverable that records their context.

<rules section="ALWAYS">
- Store structure and position: the catalogue of valid values, where a thing lives, which artifact governs it.
- Before writing a claim, ask whether omitting it would cause a later task to investigate the same question again.
</rules>

<rules section="NEVER">
- Store a measurement such as a count, a total or a size as a durable claim; a query used as evidence may return one, but the number does not enter the claim field.
- Record a fact encountered incidentally when it answers no question the investigation looked up.
</rules>

<example type="structure_vs_measurement">
input: an investigation established which catalogue is the authority for an attribute
✅ `<catalogue>` is the authority for `<attribute>`, and it lists `<v1>`, `<v2>` and `<v3>`
❌ `<catalogue>` holds exactly four rows at lookup time
</example>

## §2 Place the claim in a lookup cluster

A cluster is a Markdown file under `.agent-workspace/wiki/<subject>/` that groups claims answering a shared lookup topic, what gets asked as a single block. It is not one file per source artifact and not one per unit of the material's own organisation. Different lookup topics can lead to the same fact; duplicate detection keys on the evidence locator under §6 R6, not on the cluster.

<rules section="ALWAYS">
- Write a claim into the cluster that the opening query of §6 R1 already searched.
- When no cluster covers the topic, create it and register its router row in `.agent-workspace/wiki/index.md` in the same change.
- Write the router row's cluster name as a Markdown link whose target is the cluster path relative to the wiki root, together with what the cluster answers.
- Search by evidence locator before adding a new claim.
</rules>

<example type="router_row">
input: registering a new cluster in the wiki router
✅ `| <subject> | [<lookup topic>](<subject>/<cluster>.md) | <what it answers> |`
❌ `| <subject> | <cluster>.md | <what it answers> |`, a plain filename that the router scan reads as an orphaned cluster
</example>

## §3 Preserve the claim-record schema

The machine-readable record is called an edge. Its table has the following columns in this order:

| Column | Required information |
|---|---|
| `id` | A stable identifier allocated by the tool in the form `<cluster>-<5 chars>`. |
| `claim` | The assertion established by the investigation. Its language belongs to the project. |
| `class` | A claim class declared by the project under §7. |
| `confidence` | Either `hypothesis` or `sourced`, according to §6 R2. |
| `evidence` | The supporting items expressed in the syntax defined in §4. |

The schema is an interface for the wiki tools. It does not prescribe how an unrelated report or user-facing document must be written. A change to these fields requires coordinated changes to the parser, existing records and tests.

## §4 Record evidence that can be revisited

Every evidence item begins with a form name and a colon. The forms describe an item, not an edge: one edge carries items of several forms when its claim class requires several sources. A claim class whose required sources have no carrying form can never reach `sourced`; adding the class means adding its form.

| Form | Required values and interpretation |
|---|---|
| `located` | A source `path`, its `line` and a verbatim `anchor` used to check the recorded position. |
| `absent` | The `query`, search `scope` and `expected` result that would have contradicted the absence claim. |
| `stored-data` | The `dataset`, `object`, `field` and exact `query` used to inspect stored data. |
| `running-system` | The `account` or session context, `screen` or entry point and what was `observed`. |

The parser reads `located` in the form ``located: `<path>:<line>` anchor=`<verbatim text>` ``. The other forms use named `key=value` pairs, and a value may be enclosed in backticks or double quotes. The path identifies the source; the anchor helps detect changed positions. A match of the same text in a different file does not by itself invalidate the recorded locator.

The locator check compares the recorded and observed sets of matching positions within the cited file and reports missing as well as extra positions. For the other forms, the tool checks the recorded structure and declares what it has not rerun or observed, so an absence or an observation that has become false stays green until §6 R3 catches it at the deliverable boundary.

<rules section="ALWAYS">
- Open every evidence item with its form name and a colon.
- Separate the items of one cell with `<br>`; the parser also accepts `<br/>` and `<br />`.
- Write a `located` position inside the first pair of backticks as `<path>:<line>`; separate `path=` and `line=` values are not read for this form.
- Provide a separate `located` item for each position when a claim has several positions in the same source file.
- Resolve each source path relative to the project's `source_root` declaration, which is itself relative to the directory containing the wiki router.
</rules>

<rules section="NEVER">
- Give a `stored-data` or `running-system` item an `anchor`; a source-text search does not establish what a database or running system contained.
- Interpret a structural check of an `absent`, `stored-data` or `running-system` item as a new execution of the query or a new observation of the system.
</rules>

## §5 Keep cluster files compatible with the parser

These requirements determine which data the tool reads. Putting a summary table before the edge table changes the parser's input even if the document remains readable. Every table after the first is auxiliary and is never inspected. The router's link scan does not read fences, so an illustrative cluster link anywhere in the real router is read as a reference to a cluster that does not exist.

<rules section="ALWAYS">
- Write the edge table as the first Markdown table of the cluster file.
- Match its header exactly: `id | claim | class | confidence | evidence`, with every data row supplying those five fields.
- Keep one edge table per cluster, with every auxiliary table below it.
- Give every cluster a router link, and make every router link resolve to a cluster.
- Correct a missing table, a mismatched header, an incomplete row or a second edge table before relying on the check.
</rules>

<rules section="NEVER">
- Write the edge table inside a code fence; a fenced table is illustration, not cluster data.
- Put a sample cluster link in the real router, fenced or not.
</rules>

<example type="first_table">
input: a cluster file that also explains its subject in a table
✅ the edge table first, then the table explaining the subject
❌ a summary table first and the edge table below it; the summary is read as the edge table and reported as a header mismatch
</example>

## §6 Investigation and record lifecycle

### R1: Look up knowledge before investigating

A hit ends the investigation early. An investigation that establishes nothing writes nothing.

<rules section="ALWAYS">
- Begin an investigation by querying the wiki for the question being asked, and use an applicable established claim when its evidence is sufficient for the current work.
- End the investigation by recording what it established in the relevant cluster.
</rules>

### R2: Match confidence to evidence

A recent successful locator check can establish that recorded source text remains at the stated positions. It cannot establish that the interpretation of that text is correct.

<rules section="ALWAYS">
- Keep a new record at `hypothesis` until it has reproducible evidence for every evidence class required by its declared claim class, then promote it to `sourced` when the missing evidence is obtained and confirmed.
- Reopen the source when the claim itself is uncertain or when the deliverable check under R3 requires it.
</rules>

<rules section="NEVER">
- Answer a question as established fact from a `hypothesis` edge; a hypothesis can only guide further investigation.
</rules>

### R3: Resolve contradictions before using a claim

A prior confidence label does not override new evidence.

<rules section="ALWAYS">
- Before a claim enters a deliverable, compare it with the relevant evidence.
- When they disagree, pause the dependent work, resolve the contradiction and correct the wiki in the same turn.
</rules>

### R4: Record the questions actually investigated

<rules section="ALWAYS">
- Use the looked-up question as the unit of knowledge, and when the investigation separates into subquestions, look up and record each resulting claim at that level.
</rules>

<rules section="NEVER">
- Turn every incidental observation into a new edge.
</rules>

### R5: Keep identity stable

<rules section="ALWAYS">
- Allocate an edge identifier once and keep it unique across the tier.
- On a merge collision, allocate a new identifier for the later record and update its intra-wiki references together.
</rules>

<rules section="NEVER">
- Derive an edge identifier from editable claim text.
</rules>

### R6: Update an existing fact

<rules section="ALWAYS">
- Search by subject and locator before writing, and update an existing record that already represents the same fact.
</rules>

<rules section="NEVER">
- Create a second record for the same fact because the current task used a different lookup phrase.
</rules>

### R7: Compare locator sets at the right scope

The evidence path establishes which file is being checked.

<rules section="ALWAYS">
- Compare the recorded and observed positions for each cited anchor within the cited file.
</rules>

<rules section="NEVER">
- Merge matches from unrelated files into the comparison.
- Discard additional positions that should have been recorded.
</rules>

### R8: Distinguish structural validation from truth

Passing a schema or locator check does not certify a claim class or the truth of a claim.

<rules section="ALWAYS">
- Make the tool state which checks it performs and which evidence it cannot validate.
- Keep the assistant responsible for the evidence obligations the tool does not evaluate.
</rules>

### R9: Preserve knowledge across merges

Ordinary deletion on one branch is a separate operation; it does not establish that a merge preserved both parents' knowledge.

<rules section="ALWAYS">
- Check that identifiers present in any merge parent remain represented in the merge result.
- Resolve intentional removals explicitly using the supported merge procedure.
</rules>

<rules section="NEVER">
- Lose a record silently in a merge.
</rules>

### R10: Limit references to individual edges

This boundary allows an obsolete fact to be corrected or removed without leaving external deliverables dependent on its internal identifier. Git retains the previous content; the active wiki records what remains applicable.

<rules section="ALWAYS">
- Refer to clusters, not individual edge identifiers, from artifacts outside the wiki.
- Correct a false claim in place, and remove a claim about something that no longer exists after resolving any intra-wiki references.
</rules>

<rules section="NEVER">
- Reference an edge identifier from outside the wiki.
</rules>

## §7 Declare project-specific knowledge boundaries

The project supplies its subjects, allowed subject material and claim-class vocabulary. For each claim class, it also declares which kinds of evidence are needed. The genome does not invent those domain values.

Declare `source_root:` in the wiki router's frontmatter to locate the material used by source-text evidence. Declare `source_encodings:` when the locator search must decode additional text encodings; without it, the default search pass is used. When additional encodings are declared, their matches are combined with the default pass.

The project also determines when the merge conservation check runs and how an intentional resolution is reviewed. Install the wiki only when a project has subject material and a knowledge workflow that use these declarations.

## §8 Interpret the tool's limits

The current verifier does not establish that a `class` value belongs to the project's vocabulary, or that every evidence form required by that class has been supplied. It also cannot decide which of several files under `source_root` is the live authority and which is an obsolete copy. An anchor in an obsolete file may pass the locator check.

The assistant checks those obligations when assigning confidence and before using a claim in a deliverable. Absence queries, stored data and running-system observations have the additional execution limits described in §4. A report must retain those distinctions so that a structural success is never mistaken for a fresh factual confirmation.
