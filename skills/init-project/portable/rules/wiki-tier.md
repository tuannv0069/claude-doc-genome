---
paths:
  - ".agent-workspace/wiki/**"
scope: portable
---

# Established knowledge about subject material

The optional wiki stores claims established about material the project investigates. It helps a later task reuse that knowledge without repeating the investigation. It is separate from instructions about how the assistant works and from finished deliverables.

## §1 Decide what belongs in the wiki

Store a claim when it establishes something about the subject material and another existing knowledge tier does not already own it. The claim should identify useful structure, authority or location: for example, which source defines a set of valid values and what those values are.

Do not store transient measurements as durable claims. A count or size observed at one moment can become false while its source still exists. Keep such observations in the task evidence or deliverable that records their context. A query used as evidence may return a measurement, but that does not make the measurement suitable for the wiki's claim field.

Before adding a claim, ask whether omitting it would cause a later task to investigate the same question again. A fact encountered incidentally does not need its own record if it answers no question the investigation looked up.

## §2 Place the claim in a lookup cluster

A cluster is a Markdown file under `.agent-workspace/wiki/<subject>/` that groups claims answering a shared lookup topic. Choose the cluster from the question being investigated rather than creating one file per source artifact.

Use the cluster searched at the start of the investigation. If no cluster covers that topic, create it and register its link in `.agent-workspace/wiki/index.md` in the same change. The router link uses a path relative to the wiki root and identifies what the cluster answers. A filename written as plain text is not a router link.

Before adding a new claim, also search by its evidence locator under §6 R6. Different lookup topics can lead to the same fact; that does not require duplicate claim records.

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

Every evidence item begins with a form name and a colon. The available forms identify different sources of evidence:

| Form | Required values and interpretation |
|---|---|
| `located` | A source `path`, its `line` and a verbatim `anchor` used to check the recorded position. |
| `absent` | The `query`, search `scope` and `expected` result that would have contradicted the absence claim. |
| `stored-data` | The `dataset`, `object`, `field` and exact `query` used to inspect stored data. |
| `running-system` | The `account` or session context, `screen` or entry point and what was `observed`. |

The parser reads `located` in the form ``located: `<path>:<line>` anchor=`<verbatim text>` ``. The first pair of backticks contains the path and line; writing separate `path=` and `line=` values is not equivalent for this form.

The other forms use named `key=value` pairs. Values may be enclosed in backticks or double quotes. For example, an absence item begins with `absent:` and includes `query=`, `scope=` and `expected=`. Stored-data and running-system items do not use an `anchor`; a source-text search would not establish what a database or running system contained.

Separate multiple items in a cell with `<br>`. The parser also accepts `<br/>` and `<br />` as that boundary. For a claim with several positions in the same source file, provide a separate `located` item for each path, line and anchor combination.

Resolve each source path relative to the project's `source_root` declaration. That declaration is itself relative to the directory containing the wiki router. The path identifies the source; the anchor helps detect changed positions. A match elsewhere in a different file does not by itself invalidate the recorded locator.

The locator check compares the recorded and observed sets of matching positions within the cited file. It reports missing as well as extra positions. For other evidence forms, the current tool checks the recorded structure and declares what it has not rerun or observed. The assistant must not interpret those structural checks as a new execution of the query or a new observation of the system.

## §5 Keep cluster files compatible with the parser

The first Markdown table in a cluster is its edge table. Its header is exactly `id | claim | class | confidence | evidence`, and each data row supplies those fields. Keep one edge table per cluster. The parser does not treat a table inside a code fence as cluster data, and it does not read auxiliary tables after the first as edge records.

These requirements determine which data the tool reads. Putting a summary table before the edge table changes the parser's input even if the document remains readable. A missing table, mismatched header, incomplete row or second edge table must be corrected before relying on the check.

Every cluster has a router link, and every router link resolves to a cluster. Keep illustrative cluster links out of the real router: its link scan can treat an example as a reference even when the example appears inside a fence.

## §6 Investigation and record lifecycle

### R1: Look up knowledge before investigating

Begin an investigation by querying the wiki for the question being asked. Use an applicable established claim when its evidence is sufficient for the current work. End the investigation by recording what it established in the relevant cluster. If nothing was established, there is no claim to add.

### R2: Match confidence to evidence

A new record remains `hypothesis` until it has reproducible evidence for every evidence class required by its declared claim class. A hypothesis can guide further investigation; it cannot answer the question as established fact. Promote it to `sourced` when the missing evidence is obtained and confirmed.

A recent successful locator check can establish that recorded source text remains at the stated positions. It cannot establish that the interpretation of that text is correct. Reopen the source when the claim itself is uncertain or when the deliverable check under R3 requires it.

### R3: Resolve contradictions before using a claim

Before a claim enters a deliverable, compare it with the relevant evidence. If they disagree, pause the dependent work, resolve the contradiction and correct the wiki in the same turn. A prior confidence label does not override new evidence.

### R4: Record the questions actually investigated

Use the looked-up question as the unit of knowledge. If the investigation separates into subquestions, look up and record each resulting claim at that level. Do not turn every incidental observation into a new edge.

### R5: Keep identity stable

Allocate an edge identifier once and keep it unique across the tier. Do not derive it from editable claim text. On a merge collision, allocate a new identifier for the later record and update its intra-wiki references together.

### R6: Update an existing fact

Search by subject and locator before writing. When an existing record already represents the same fact, update that record instead of creating another merely because the current task used a different lookup phrase.

### R7: Compare locator sets at the right scope

The evidence path establishes which file is being checked. Compare the recorded and observed positions for each cited anchor within that file. Do not merge matches from unrelated files into the comparison, and do not discard additional positions that should have been recorded.

### R8: Distinguish structural validation from truth

The tool must state which checks it performs and which evidence it cannot validate. Passing a schema or locator check does not certify a claim class or the truth of a claim. The assistant remains responsible for the evidence obligations the tool does not evaluate.

### R9: Preserve knowledge across merges

Check that identifiers present in any merge parent remain represented in the merge result. Resolve intentional removals explicitly using the supported merge procedure rather than silently losing records. Ordinary deletion on one branch is a separate operation; it does not establish that a merge preserved both parents' knowledge.

### R10: Limit references to individual edges

Artifacts outside the wiki refer to clusters rather than individual edge identifiers. References between edges remain inside the wiki. This boundary allows an obsolete fact to be corrected or removed without leaving external deliverables dependent on its internal identifier.

Correct a false claim in place. Remove a claim about something that no longer exists after resolving any intra-wiki references. Git retains the previous content; the active wiki records what remains applicable.

## §7 Declare project-specific knowledge boundaries

The project supplies its subjects, allowed subject material and claim-class vocabulary. For each claim class, it also declares which kinds of evidence are needed. The genome does not invent those domain values.

Declare `source_root:` in the wiki router's frontmatter to locate the material used by source-text evidence. Declare `source_encodings:` when the locator search must decode additional text encodings; without it, the default search pass is used. When additional encodings are declared, their matches are combined with the default pass.

The project also determines when the merge conservation check runs and how an intentional resolution is reviewed. Install the wiki only when a project has subject material and a knowledge workflow that use these declarations.

## §8 Interpret the tool's limits

The current verifier does not establish that a `class` value belongs to the project's vocabulary, or that every evidence form required by that class has been supplied. It also cannot decide which of several files under `source_root` is the live authority and which is an obsolete copy. An anchor in an obsolete file may pass the locator check.

The assistant checks those obligations when assigning confidence and before using a claim in a deliverable. Absence queries, stored data and running-system observations have the additional execution limits described in §4. A report must retain those distinctions so that a structural success is never mistaken for a fresh factual confirmation.
