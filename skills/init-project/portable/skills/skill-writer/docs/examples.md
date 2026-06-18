<critical>
target: skill-writer agent reference
purpose: annotated example patterns; copy closest then adapt frontmatter + body
scope: 8 patterns — simple/reference/positional/dynamic/supporting/orch-seq/orch-par/anti
</critical>

<rule_schema>
example_block:
  yaml: frontmatter + body in fenced code (4-tick outer if nested)
  decisions: table "decision → reason"
  intro: ≤ 1 line "pattern: <one-liner>"
</rule_schema>

<dependencies>
- ${CLAUDE_SKILL_DIR}/docs/skill-rules-spec.md — platform spec
- ${CLAUDE_SKILL_DIR}/docs/skill-rules-orch.md — orchestration rules
- ${CLAUDE_SKILL_DIR}/docs/skill-rules-quality.md — quality gate
- .claude/rules/skill-md-standards.md — body rules
</dependencies>

---

## index

| § | pattern | key flags |
|---|---|---|
| §1 | simple task, manual invoke | `disable-model-invocation: true` + side effects |
| §2 | reference, auto-invoked | TRIGGER / DO NOT TRIGGER in description |
| §3 | positional arguments | `$0 $1 $2` |
| §4 | dynamic context injection | `context: fork` + `` !`cmd` `` |
| §5 | supporting files | `${CLAUDE_SKILL_DIR}` references |
| §6 | orchestration sequential (Model B) | state file + CONTRACT-V1 |
| §7 | orchestration parallel (Model C) | batches + per-agent staging |
| §8 | anti-patterns | what to avoid |

---

## §1 simple task, manual invoke

pattern: user invokes with arguments; side effects → `disable-model-invocation: true`

````yaml
---
name: fix-issue
description: Fix a GitHub issue by number. Reads issue, implements fix, writes tests, commits.
argument-hint: "<issue-number>"
disable-model-invocation: true
allowed-tools: Read Grep Glob Edit Write Bash
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read issue: `gh issue view $ARGUMENTS`
2. Identify affected files
3. Implement fix
4. Write tests covering the fix
5. Run tests to verify
6. Commit: `fix(#$ARGUMENTS): <description>`
````

| decision | reason |
|---|---|
| `disable-model-invocation: true` | creates commits |
| `$ARGUMENTS` (single) | no positional parsing needed |
| Edit/Write/Bash in `allowed-tools` | modifies files, runs tests |

---

## §2 reference, auto-invoked

pattern: knowledge content auto-loaded when relevant; no task, no side effects

````yaml
---
name: api-conventions
description: >
  API design patterns for this codebase. TRIGGER when writing or reviewing
  API endpoints, route handlers, or controller logic. DO NOT TRIGGER for
  frontend components, CSS, or documentation edits.
---

When writing API endpoints:

- RESTful naming: plural nouns (`/users`, `/orders`)
- Consistent error format: `{ "error": { "code": "...", "message": "..." } }`
- Validate request bodies before processing
- Correct HTTP status: 200, 201, 400, 404
- Pagination on list endpoints: `?page=1&limit=20`
- Log errors with request ID
````

| decision | reason |
|---|---|
| no `disable-model-invocation` | auto-invoked when API work detected |
| TRIGGER + DO NOT TRIGGER in description | precise activation |
| no `allowed-tools` | reference content, no tool use |
| no arguments | pure knowledge injection |

---

## §3 positional arguments

pattern: multiple arguments parsed by position

````yaml
---
name: migrate-component
description: Migrate a UI component from one framework to another, preserving behavior and tests.
argument-hint: "<component-name> <source-framework> <target-framework>"
disable-model-invocation: true
allowed-tools: Read Grep Glob Edit Write
---

Migrate **$0** from **$1** to **$2**.

1. Find component: `Glob("**/$0.*")`
2. Read component + tests
3. Analyze $1-specific patterns
4. Rewrite using $2 idioms — preserve props, handlers, visual output
5. Update imports in consumers
6. Run tests; fix failures
7. Verify no $1 imports: `Grep("import.*from.*$1")`

done: renders identically + tests pass + no $1 imports
````

| decision | reason |
|---|---|
| `$0 $1 $2` | positional template substitution |
| `argument-hint` | documents expected order |
| explicit done | task verification |

---

## §4 dynamic context injection

pattern: shell commands run before content reaches Claude; output injected as context

````yaml
---
name: pr-summary
description: Summarize changes in the current pull request, including diff and comments.
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## context

- title/body: !`gh pr view --json title,body --jq '.title + "\n\n" + .body'`
- changed files: !`gh pr diff --name-only`
- diff (truncated): !`gh pr diff | head -500`
- comments: !`gh pr view --comments`

## task

1. **what changed** — key changes by area
2. **why** — infer from title, body, diff
3. **risk areas** — files needing extra review
4. **missing** — gaps (tests, docs, error handling)

≤ 20 lines summary.
````

| decision | reason |
|---|---|
| `context: fork` | self-contained; no conversation context |
| `agent: Explore` | read-only |
| `` !`cmd` `` | dynamic context injection |
| `Bash(gh *)` | only GitHub CLI permitted |

---

## §5 supporting files

pattern: SKILL.md references `docs/` and `scripts/` via `${CLAUDE_SKILL_DIR}`

````yaml
---
name: generate-api-docs
description: Generate OpenAPI documentation from source code annotations.
argument-hint: "<source-directory>"
disable-model-invocation: true
allowed-tools: Read Grep Glob Bash
---

Generate OpenAPI docs for `$ARGUMENTS`.

1. Read template: `Read("${CLAUDE_SKILL_DIR}/docs/openapi-template.yaml")`
2. Scan handlers: `Grep("@(Get|Post|Put|Delete|Patch)", path="$ARGUMENTS")`
3. For each route, extract: method, path, params, body, response
4. Run extraction: `python3 ${CLAUDE_SKILL_DIR}/scripts/extract-routes.py $ARGUMENTS`
5. Merge into template
6. Write `$ARGUMENTS/openapi.yaml`

verification:
- valid YAML: `python3 -c "import yaml; yaml.safe_load(open('$ARGUMENTS/openapi.yaml'))"`
- route count = source annotation count
````

| decision | reason |
|---|---|
| `${CLAUDE_SKILL_DIR}/docs/` | template lives with skill |
| `${CLAUDE_SKILL_DIR}/scripts/` | extraction script as supporting file |
| no relative paths (`./`, `../`) | breaks when loaded from unexpected dir |

---

## §6 orchestration sequential (Model B)

pattern: multi-stage subagents in sequence; orchestrator manages flow only

````yaml
---
name: code-review
description: >
  Multi-stage code review: lint, security, logic, summary. Sequential subagents.
  Usage: /code-review [branch or PR number]
argument-hint: "[branch or PR-number]"
disable-model-invocation: true
allowed-tools: Read Write Bash
---

# code-review orchestrator (Model B)

> orchestrator manages flow + state; does NOT read code

## STEP 0 init

1. Parse `$ARGUMENTS` as branch or PR number → derive `JOB_KEY` (PR number or branch slug)
2. SESSION_ROOT = `.agent/tmp/codereview/sessions/${JOB_KEY}/${CLAUDE_SESSION_ID}/`
3. `mkdir -p ${SESSION_ROOT}/{staging,artifacts,logs}`
4. Create state: `${SESSION_ROOT}/state.json`
5. Update latest pointer: `ln -sfn ${CLAUDE_SESSION_ID} .agent/tmp/codereview/sessions/${JOB_KEY}/latest`
6. Init: `{ "phase": "planning", "phases": [], "current_phase": 0 }`

## STEP 1 plan

Spawn `.claude/agents/codereview-planner.md`:
- input: branch/PR ref
- output: `${SESSION_ROOT}/plan.json`

Validate 4 phases; approve/reject.

## STEP 2 execute (sequential)

| phase | agent | input |
|---|---|---|
| 1 lint | `codereview-lint.md` | changed file list |
| 2 security | `codereview-security.md` | changed file list |
| 3 logic | `codereview-logic.md` | files + lint/security staging |
| 4 summary | `codereview-summary.md` | all phase staging paths |

Each returns CONTRACT-V1.

After each phase:
1. Parse CONTRACT-V1
2. Update state file
3. critical FAILURE → halt
4. else → next phase

## STEP 3 report

```text
CODE REVIEW COMPLETE
Phases: 4/4
Status: SUCCESS | PARTIAL_SUCCESS | FAILURE
See: ${SESSION_ROOT}/artifacts/summary.md
```
````

| decision | reason |
|---|---|
| orchestrator never reads code | EX-01 |
| phase = own agent file | EX-02 |
| state file per phase | resume capability |
| staging files between phases | EX-03 |

---

## §7 orchestration parallel (Model C)

pattern: independent subtasks in parallel; results aggregated

````yaml
---
name: multi-file-translate
description: >
  Translate multiple Markdown files in parallel. One subagent per file.
  Usage: /multi-file-translate <glob-pattern> <target-language>
argument-hint: "<glob-pattern> <target-language>"
disable-model-invocation: true
allowed-tools: Read Write Glob Bash
---

# multi-file-translate (Model C)

> orchestrator manages batches + state; does NOT read content

## STEP 0 init

1. Parse: `$0` glob, `$1` target lang
2. Discover: `Glob($0)`
3. JOB_KEY = 8-hex hash of `${0}:${1}` (uniform-task workflow, not per-function)
4. SESSION_ROOT = `.agent/tmp/translate/sessions/${JOB_KEY}/${CLAUDE_SESSION_ID}/`
5. `mkdir -p ${SESSION_ROOT}/{staging,artifacts,logs}` + update `sessions/${JOB_KEY}/latest` symlink
6. State: `${SESSION_ROOT}/state.json` — init with file list, batch size 3

## STEP 1 plan

uniform tasks → no planner; direct plan: 1 file = 1 subtask, batch 3

## STEP 2 execute batches

per batch of 3:

1. Report start
2. Spawn 3 `.claude/agents/translate-file.md` parallel:
   - input: source path, target lang
   - output: translated file with `-{lang}` suffix
   - returns: CONTRACT-V1
3. Collect outputs
4. Update state per item
5. Report batch result
6. Next batch

write safety: each agent owns output file; no shared writes

## STEP 3 report

```text
TRANSLATION COMPLETE
Total: N
Success: X
Failure: Y (list)
Skipped: Z
```
````

| decision | reason |
|---|---|
| batch 3 | safe parallel default |
| each agent owns output | no write conflicts |
| progress per batch | resume capability |

---

## §8 anti-patterns

| anti-pattern | why fails | fix |
|---|---|---|
| 1000-line schema in SKILL.md | bloats context, breaks 500-line | move to `docs/`, ref via `${CLAUDE_SKILL_DIR}` |
| `context: fork` when result needed | fork isolated, output lost | remove fork, inline subagent spawn |
| parallel agents writing same file | race condition | per-agent file, sequential aggregator |
| no `disable-model-invocation` on deploy | auto-triggers deploy | set `disable-model-invocation: true` |
| relative paths to supporting files | breaks unexpected load dir | use `${CLAUDE_SKILL_DIR}/...` |
| description+when_to_use > 1536 chars, key info at end | truncated in listing, triggers lost | front-load use case |
| orchestrator reads domain files | violates EX-01 | delegate reads to subagents |
| missing done condition | runs forever or stops early | define explicit done |
| state file no skill prefix | multi-skill collision | namespace `.agent/tmp/{prefix}/` |
| flat layout `{prefix}/state-${SESSION}.json` | concurrent runs cross-function collide visually | `{prefix}/sessions/{JOB_KEY}/{SESSION}/state.json` |
| timestamp in filename inside session dir | redundant noise; session dir already timestamped | drop timestamp suffix; use `state.json`, `plan.json` |
| no retention spec | stale sessions accumulate forever | archive 7d → delete 30d (cleanup_ready gated) |
| agent prompt no Avoid section | drifts from format | explicit Avoid with known errors |

---

<critical_recap>
1. example block = yaml fenced + decisions table + ≤ 1 line intro
2. orchestration → orchestrator never reads domain content
3. supporting files → `${CLAUDE_SKILL_DIR}/...`, never relative
4. side effects → `disable-model-invocation: true`
5. parallel writes → per-agent file, sequential aggregator
6. layout → `.agent/tmp/{prefix}/sessions/{JOB_KEY}/{SESSION}/{state.json,plan.json,staging/,artifacts/,logs/}` + `latest` symlink
</critical_recap>
