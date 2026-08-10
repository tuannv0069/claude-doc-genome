<critical>
target: skill-writer agent reference — platform spec
purpose: terminology, directory layout, frontmatter fields, resolution, context loading, substitutions, dynamic context, subagent execution, permissions, writing rules, bundled skills, troubleshooting
scope: §0-§9, §12-§13 — orchestration → skill-rules-orch.md, quality gate → skill-rules-quality.md, dynamic workflow → skill-rules-workflow.md
</critical>

<rule_schema>
field_table: name | required | type | default | spec
behavior_table: trigger → effect
</rule_schema>

<dependencies>
- ${CLAUDE_SKILL_DIR}/docs/skill-rules-orch.md — orchestration rules
- ${CLAUDE_SKILL_DIR}/docs/skill-rules-quality.md — quality gate
- ${CLAUDE_SKILL_DIR}/docs/examples.md — annotated patterns
</dependencies>

---

## §0 terminology

| term | definition |
|---|---|
| skill | dir with `SKILL.md` + optional supporting files; instructions, not hard-coded logic |
| SKILL.md | sole entrypoint; YAML frontmatter + markdown body |
| frontmatter | YAML between two `---` at top; controls behavior |
| supporting files | files in skill dir; read only when SKILL.md references them |
| bundled skill | built into Claude Code; available every session |
| built-in command | fixed system command (`/help`, `/compact`); not a skill |
| dynamic workflow | JS script orchestrating many subagents via background runtime; saved under `.claude/workflows/` → `/name` command; NOT a skill — see skill-rules-workflow.md |

name collision `.claude/commands/X.md` vs `.claude/skills/X/SKILL.md` → skill wins

---

## §1 directory structure

```text
<skill-name>/
├── SKILL.md           # entrypoint (required)
├── docs/              # reference, guidelines, templates
├── examples/          # sample outputs
└── scripts/           # executable code
```

<rules section="ALWAYS">
- one skill = one directory
- SKILL.md required (only auto-read file)
- supporting files referenced via `${CLAUDE_SKILL_DIR}/...`
</rules>

<rules section="NEVER">
- relative paths (`./`, `../`) to supporting files
</rules>

---

## §2 frontmatter spec

### §2.1 fields

| field | required | type | default | spec |
|---|---|---|---|---|
| `name` | no | string | dir name | display label only — command name comes from skill DIRECTORY name (exception: plugin-root SKILL.md, where `name` sets the command) |
| `description` | rec | string | first paragraph | drives auto-activation; listing shows description + when_to_use truncated at 1536 chars (cap: `maxSkillDescriptionChars`); front-load use case |
| `when_to_use` | no | string | — | extra trigger phrases / example requests; appended to description in listing; counts toward 1536 cap |
| `argument-hint` | no | string | — | autocomplete hint, e.g. `[issue-number]` |
| `arguments` | no | string/list | — | named positional args; names map to positions in order → enables `$name` substitution |
| `disable-model-invocation` | no | bool | `false` | `true` → user-invoke only; also blocks preloading into subagents |
| `user-invocable` | no | bool | `true` | `false` → hidden from `/`, Claude-only |
| `allowed-tools` | no | string/list | — | grants permission while skill active — does NOT restrict tool pool; project skill: effective only after workspace trust |
| `disallowed-tools` | no | string/list | — | tools removed from pool while skill active; clears on next user message |
| `model` | no | string | session | same values as `/model`, or `inherit`; override lasts rest of current turn only |
| `effort` | no | enum | session | `low | medium | high | xhigh | max` — available levels depend on model |
| `context` | no | string | — | `fork` → isolated subagent, no history |
| `agent` | no | string | `general-purpose` | subagent type when `context: fork` |
| `hooks` | no | object | — | lifecycle hooks |
| `paths` | no | string/list | — | glob patterns limiting auto-activation |
| `shell` | no | enum | `bash` | `bash | powershell`; powershell requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` |

### §2.2 field interactions

| combination | effect |
|---|---|
| `disable-model-invocation: true` + `user-invocable: false` | unreachable — never set both |
| `disable-model-invocation: true` + subagent `skills:` preload | skill cannot be preloaded (preload draws from model-invocable set) |
| `context: fork` + no explicit task | returns empty |
| `paths` set | affects auto-activation only, not manual `/name` |
| `allowed-tools` | applies only while skill active |

---

## §3 resolution priority

| priority | scope | path | applies to |
|---|---|---|---|
| 1 | enterprise | managed settings | all org users |
| 2 | personal | `~/.claude/skills/<name>/SKILL.md` | all user projects |
| 3 | project | `.claude/skills/<name>/SKILL.md` | current project |
| 4 | plugin | `<plugin>/skills/<name>/SKILL.md` | where plugin enabled |

| conflict | resolution |
|---|---|
| same name, different scopes | higher scope wins |
| plugin namespace `plugin:skill` | no conflict with other scopes |
| commands vs skills, same name | skill wins |
| monorepo edit `packages/X/Y` | scans `packages/X/.claude/skills/` |

---

## §4 context loading

| frontmatter | user invoke | claude invoke | behavior |
|---|---|---|---|
| (defaults) | yes | yes | description in context; full content on invoke |
| `disable-model-invocation: true` | yes | no | description NOT in context; full content on user invoke |
| `user-invocable: false` | no | yes | description in context; full content on invoke |

exception: subagents with preloaded skills → full content injected at startup

description budget: 1% of model context window (`skillListingBudgetFraction` setting, or fixed `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var); per-entry cap 1536 chars = description + when_to_use (`maxSkillDescriptionChars`); overflow drops least-invoked skills first — diagnose with `/doctor`

content lifecycle: invoked skill content stays in context for the whole session (file NOT re-read on later turns) → write standing instructions, not one-time steps; after auto-compaction each invoked skill re-attaches with first 5000 tokens, shared budget 25000 tokens, most-recent first (older skills may drop)

---

## §5 string substitutions

| variable | behavior |
|---|---|
| `$ARGUMENTS` | full arg string; auto-appended as `ARGUMENTS: <value>` if absent |
| `$ARGUMENTS[N]` | positional arg (0-based) |
| `$N` | shorthand `$ARGUMENTS[N]` — `$0`=first |
| `$name` | named arg declared in `arguments` frontmatter; names map to positions in order |
| `${CLAUDE_SESSION_ID}` | session ID; use in temp file names |
| `${CLAUDE_EFFORT}` | active effort level `low..max` (ultracode reports `xhigh`) |
| `${CLAUDE_SKILL_DIR}` | dir containing SKILL.md; required for supporting refs |

example: `/migrate-component SearchBar React Vue` → `$0=SearchBar`, `$1=React`, `$2=Vue`

indexed args use shell-style quoting: `/skill "two words" b` → `$0=two words`, `$1=b`. literal `$` before digit / `ARGUMENTS` / declared name → escape `\$1.00`

---

## §6 dynamic context injection

### §6.1 inline command

`` !`<cmd>` `` → runs shell before content reaches Claude; output replaces placeholder

```markdown
- PR diff: !`gh pr diff`
- changed: !`gh pr diff --name-only`
```

`!` recognized only at line start or after whitespace (`` KEY=!`cmd` `` stays literal); substitution is single-pass — command output is not re-scanned for placeholders

### §6.2 multi-line block

````markdown
```!
node --version
git status --short
```
````

### §6.3 disable shell

`"disableSkillShellExecution": true` → disabled for user/project/plugin; commands replaced with `[shell command execution disabled by policy]`; bundled/managed unaffected

### §6.4 extended thinking

word **"ultrathink"** anywhere in skill content → enables extended thinking

---

## §7 subagent execution

`context: fork` → isolated subagent; skill content = prompt; no conversation history

| approach | system prompt | task | also loads |
|---|---|---|---|
| skill + `context: fork` | from agent type | SKILL.md content | CLAUDE.md — except `agent: Explore`/`Plan` (skip CLAUDE.md + git status) |
| subagent + `skills:` field | subagent body | delegation message | preloaded + CLAUDE.md |

| use `context: fork` when | do NOT use when |
|---|---|
| task fully self-contained | orchestrator needs result for routing |
| orchestrator does not need output | task needs conversation context |
| want clean context | skill is guidelines-only |

---

## §8 permission control

| level | syntax | effect |
|---|---|---|
| disable Skill tool | `Skill` | all skills off |
| exact match | `Skill(commit)` | one skill |
| prefix + args | `Skill(review-pr *)` | one skill + any args |
| deny prefix | `Skill(deploy *)` | block one skill |
| hide individual | `disable-model-invocation: true` in frontmatter | affects context loading per §4 |
| visibility via settings | `skillOverrides: { "<name>": "on \| name-only \| user-invocable-only \| off" }` | hide/collapse without editing frontmatter (`/skills` menu writes it); plugin skills unaffected |

note: `user-invocable: false` controls menu visibility only, NOT Skill tool access

---

## §9 writing rules

<rules section="NEVER">
- entire schemas/scripts inline in SKILL.md → split to `docs/`, `scripts/`
- cram all instructions in CLAUDE.md instead of skills
- side-effect skill without `disable-model-invocation: true`
</rules>

<rules section="ALWAYS">
- SKILL.md ≤ 500 lines (simple) / ≤ 800 (orchestration)
- declare `allowed-tools` for safe tools (Read, Grep, Glob)
- task skills include verification / done criteria
- classify content: reference (knowledge) vs task (action)
</rules>

---

## §12 bundled skills

| skill | description |
|---|---|
| `/batch <instruction>` | decompose 5-30 units, 1 background agent per unit in worktree, each implements + tests + opens PR |
| `/claude-api` | loads Claude API ref for project lang + Agent SDK; auto on `anthropic`/`@anthropic-ai/sdk`/`claude_agent_sdk` imports |
| `/code-review [effort]` | diff review for correctness bugs + cleanups; `ultra` = multi-agent cloud review |
| `/debug [description]` | enables debug logging from invocation |
| `/deep-research <question>` | bundled DYNAMIC WORKFLOW — multi-source research, cross-checked claims, cited report |
| `/loop [interval] <prompt>` | runs prompt repeatedly at interval while session open |
| `/run` / `/verify` | launch app / confirm a change works against the running app |
| `/run-skill-generator` | records project launch recipe as `.claude/skills/run-<name>/` for `/run` + `/verify` |
| `/simplify [focus]` | 3 parallel review agents (reuse, quality, efficiency) on changed files |

built-in commands also reachable via Skill tool: `/init`, `/review`, `/security-review`

never recreate bundled — use directly or extend

---

## §13 troubleshooting

| symptom | cause | fix |
|---|---|---|
| skill does not trigger | description does not match intent | add keywords; test with "What skills are available?" |
| triggers too often | description too broad | narrow it, or set `disable-model-invocation: true` |
| description truncated | description+when_to_use over 1536 chars, or listing budget overflow | front-load use case; check `/doctor`; raise `skillListingBudgetFraction` / `SLASH_COMMAND_TOOL_CHAR_BUDGET`; collapse low-priority skills via `skillOverrides: name-only` |
| SKILL.md edit not picked up | new top-level skills dir created mid-session | SKILL.md text hot-reloads in-session; NEW top-level skills dir needs restart; `.claude/agents/*.md` disk edits need restart |
| skill stops influencing behavior | content still in context; model prefers other path | strengthen description/instructions; re-invoke after compaction; enforce via hooks |
| `context: fork` no output | violates fork constraint | add explicit task |
| permission prompts | missing `allowed-tools` | declare safe tools |
| path errors | relative path used | replace with `${CLAUDE_SKILL_DIR}/...` |
| subagent context bloat | output not trimmed | add CONTRACT-V1 instruction (see orch §4) |
| parallel file conflicts | shared file write | per-agent staging file |
| skill unreachable | `disable-model-invocation: true` + `user-invocable: false` | never set both |

---

<critical_recap>
1. SKILL.md required, supporting files only loaded when referenced
2. supporting files → `${CLAUDE_SKILL_DIR}/...`, never relative
3. unreachable trap: never `disable-model-invocation: true` + `user-invocable: false`
4. side effects → `disable-model-invocation: true`
5. front-load use case in description; description + when_to_use ≤ 1536 chars in listing (matcher)
</critical_recap>
