---
paths:
  - ".claude/agents/**"
scope: portable
---

<critical>
target: subagent at .claude/agents/<name>.md (auto-spawned by Claude Code orchestrator via Task tool, isolated context window)
optimize: matcher routes correctly + executes accurately + min context pollution
ai-first: ignore human readability
note: this STANDARD file uses XML wrap; subagent target body uses plain markdown
cross-file rule placement: agent body MUST NOT inline substantive code rule (canonical shape, snippet, fix template, prop list) — reference agent-guide §ID; see `doc-organization.md`.
</critical>

<rule_schema>
subagent_file:
  location: .claude/agents/<name>.md (project) | ~/.claude/agents/<name>.md (user)
  format: YAML frontmatter + markdown body
  frontmatter:
    name: kebab-case (required)
    description: when-to-invoke + scope (required)
    tools: comma-separated whitelist (optional, omit = inherit all)
    model: sonnet|opus|haiku|inherit (optional)
  body_required: [identity, voice, NEVER, capabilities, tools, conversation, output, examples]

subagent_rule:
  start: imperative_verb | `cond →`
  description: action-oriented ("Use proactively...", "Use immediately after...")
  tools: minimum necessary (least privilege)
  identity_format: "You are X. You Y."
</rule_schema>

<priority>
1. matcher accuracy (description triggers correct subagent)
2. context isolation (don't pollute parent context)
3. tool scoping (least privilege)
4. body persona consistency (identity + voice align)
5. token efficiency (loaded per spawn)
</priority>

---

<core_rules>

### wording

```
✅ Use proactively after code changes
✅ test fail → report + propose fix
❌ You should generally use this when...
```

cut test: remove word → behavior unchanged → cut

### RFC2119 budget

| keyword | use | budget |
|---------|-----|--------|
| MUST/NEVER | hard limits/safety | ≤10% rules |
| SHOULD | defaults | majority |
| MAY | opt-in | minority |

### format density (most-compressed first)

1. table — tools, conditional, frontmatter spec
2. arrow — conversation if-then
3. bullet — voice, NEVER, ALWAYS
4. numbered list — workflow if procedural

| content | format |
|---------|--------|
| frontmatter | YAML |
| identity | single sentence, body first line, no heading |
| voice | bullet under `## voice` |
| hard limits | bullet under `## NEVER` |
| tools | table `tool | use when` |
| workflow | numbered list |
| conversation | bullet or arrow |
| examples | full conversation flow |

### structural rules
- one rule = one line
- semantic heading
- max 2 nesting levels
- no rule duplication across sections

</core_rules>

---

<rules section="NEVER">
- hedge: generally|typically|usually|try|consider|might|perhaps|ideally
- vague description (orchestrator can't auto-route)
- description overlaps another subagent (matcher ambiguity)
- omit name in frontmatter (subagent won't load)
- inherit-all-tools by default for read-only agents (security risk)
- give Bash/Edit/Write to reviewer/auditor agents
- decorative md (emoji, !!!, CAPS-for-emphasis)
- duplicate CLAUDE.md content in body (already inherited)
- inline substantive code rule in body (canonical code shape, prop list, ✅/❌ snippet, fix template) — use pointer to agent-guide §ID per `doc-organization.md`
- omit identity statement in body (agent loses persona)
- list tools without orchestration guidance
- multi-page prose for instructions
- MUST/NEVER on rules with exceptions
- XML wrap subagent target body (over-engineering)
- filler in example agent responses
- persona drift (identity ↔ voice ↔ examples must align)
</rules>

<rules section="ALWAYS">
- frontmatter: name + description (required)
- description: action-oriented + when-to-invoke + scope boundary
- tools whitelist for security-sensitive agents
- body identity first line: "You are X. You Y."
- body voice/tone explicit section
- body NEVER section for hard limits
- tool orchestration table (`tool | use when`)
- conversation flow: clarify + error + end
- output format structured (sections, priorities), not prose dump
- restart Claude Code session after editing on disk
- include 1-3 example invocations in description
</rules>

---

<frontmatter_spec>

```yaml
---
name: <kebab-case-id>
description: <when to invoke + scope + trigger phrases>
tools: <Read, Grep, Glob, Bash>  # optional, omit = inherit all
model: sonnet                     # optional: sonnet|opus|haiku|inherit
---
```

| field | required | rule |
|-------|----------|------|
| name | yes | kebab-case, unique across project + user agents |
| description | yes | action-oriented, includes "Use X when Y" or "Use proactively for Z" |
| tools | no | omit = inherit parent tools; specify = whitelist only |
| model | no | default = inherit; override for cost/quality balance |

</frontmatter_spec>

---

<description_patterns>

description drives auto-delegation. write as routing rule:

| pattern | when |
|---------|------|
| "Use proactively after <action>" | auto-trigger on event (post-edit, post-commit) |
| "Use immediately when <condition>" | reactive trigger (error, test fail) |
| "Use for <task type> involving <domain>" | scope-specific routing |
| "Do NOT use for <out-of-scope>" | prevent wrong routing |

include 1-3 concrete invocation examples for ambiguous cases.

</description_patterns>

---

<tools_scoping>

principle: minimum necessary tools.

| agent role | recommended tools |
|------------|-------------------|
| reviewer / auditor / linter | Read, Grep, Glob |
| researcher / analyst | Read, Grep, Glob, WebFetch, WebSearch |
| implementer / developer | Read, Write, Edit, Bash, Grep, Glob |
| tester | Read, Edit, Bash, Grep |
| documentation writer | Read, Write, Edit, Grep, Glob |
| orchestrator | inherit (omit tools field) |

omitting tools field → inherit all parent tools (use only when general-purpose).

</tools_scoping>

---

<body_required_sections>

| order | section | purpose |
|-------|---------|---------|
| 1 | identity | "You are X. You Y." (first line, no heading) |
| 2 | voice | how agent communicates |
| 3 | NEVER | hard limits (refusal/safety) |
| 4 | capabilities | what agent does |
| 5 | tools | orchestration table |
| 6 | workflow | numbered steps if procedural |
| 7 | conversation | clarify + error + end |
| 8 | output | format defaults |
| 9 | examples | full conversation flows (3-5) |

</body_required_sections>

---

<conversation_patterns>

```markdown
## conversation
### clarification
- vague scope → ask 1 specific question, list options (max 3)
- vague target → propose default, confirm before action

### error
- tool/op fails → report failure + reason in 1 sentence + propose alternative
- expensive op fail → ask before retrying

### completion
- report result in 1-2 sentences
- list next actionable step (if any)
- no filler ("Let me know if you need anything else!")
```

</conversation_patterns>

---

<token_budget>

| complexity | tokens (frontmatter + body) |
|------------|------------------------------|
| narrow (single task type) | < 800 |
| general (multi-task domain) | < 2500 |
| complex (multi-tool orchestration) | < 5000 |

over → split into narrower subagents, OR extract patterns to project skill

note: prompt loaded each spawn → frequent-use subagents prioritize compactness

</token_budget>

---

<reference_vs_embedded>

| content | location |
|---------|----------|
| identity, voice | embedded in body |
| tool orchestration | embedded in body |
| domain procedures | extract to skill |
| reference data (long lists, schemas) | extract to companion file under `docs/agent-guide/` |
| few-shot examples | embedded (max 3-5) |

over token budget → extract domain knowledge to skills, prompt only orchestrates

</reference_vs_embedded>

---

<location_priority>

```
session-defined > project (.claude/agents/) > user (~/.claude/agents/) > plugin
```

| scope | use |
|-------|-----|
| project (`.claude/agents/`) | team-shared specialists (commit to git) |
| user (`~/.claude/agents/`) | personal tools across all projects |
| plugin | distributed via plugin system |
| session | temporary, defined via `--agents` JSON |

name collision → higher priority wins.

</location_priority>

---

<example type="description_action_oriented">

✅ output:
```yaml
description: Expert code review specialist. Use proactively immediately
  after writing or modifying code to ensure quality, security, and
  maintainability. Reviews diffs, identifies vulnerabilities, suggests
  improvements. Do NOT use for initial implementation or refactoring.
```

❌ output: `description: Reviews code`
verdict: no trigger phrase, no scope, no action orientation

❌ output: `description: Helps with code in various ways`
verdict: too vague, overlaps with implementer agents

</example>

<example type="tools_scoping">

✅ output:
```yaml
---
name: security-auditor
description: Use proactively after code changes to scan for security
  vulnerabilities, OWASP violations, hardcoded secrets, and unsafe
  patterns. Read-only analysis, no modifications.
tools: Read, Grep, Glob
---
```

❌ output:
```yaml
---
name: security-auditor
description: Security audits
# tools omitted — inherits Bash, Edit, Write
---
```
verdict: read-only agent shouldn't have write/exec tools (privilege escalation)

</example>

<example type="full_skeleton">

✅ output:
```markdown
---
name: code-reviewer
description: Expert code review specialist. Use proactively after 
  writing or modifying code. Reviews for quality, security, performance,
  and maintainability. Do NOT use for initial implementation or 
  generating new code.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer ensuring high standards of code quality,
security, and maintainability across the codebase.

## voice
- direct, no preamble
- evidence-based: cite file:line for every finding
- no apologies, no filler

## NEVER
- modify code (read-only review)
- approve without running git diff first
- conflate style preferences with bugs
- skip security checks for "quick" reviews

## workflow
1. Run `git diff --name-only` to identify changed files
2. Read each changed file
3. Analyze: security, performance, correctness, maintainability
4. Cross-reference with project conventions (CLAUDE.md)
5. Output structured findings (see output format)

## review checklist
| category | check |
|----------|-------|
| security | hardcoded secrets, SQL injection, XSS, CSRF, auth bypass |
| performance | N+1 queries, unbounded loops, missing indexes |
| correctness | error handling, edge cases, race conditions |
| maintainability | naming, complexity, dead code, duplication |

## output format
group findings by priority:

🔴 CRITICAL (must fix before merge):
- file:line — description + suggested fix

🟡 WARNING (should fix):
- file:line — description

🟢 SUGGESTION (consider):
- file:line — description

end with: summary count + recommendation (approve / changes-needed / block)

## examples

### good finding
🔴 CRITICAL — auth.ts:47
Hardcoded JWT secret in source. Move to env var.

### bad finding (style preference, not bug)
❌ "Variable name `data` is too generic"
→ unless project convention requires specific naming, this is style noise
```

</example>

---

<anti_patterns>

```
❌ description without trigger
description: "Code reviewer"
→ orchestrator can't decide when to invoke

❌ tools field omitted for read-only agent
→ privilege escalation risk (inherits Bash/Edit/Write)

❌ subagent duplicating CLAUDE.md
[body restates "we use Next.js, TypeScript..."]
→ already inherited; remove duplication

❌ subagent as workflow runner without isolation
[implementer agent that also reviews + tests + deploys]
→ split into specialized subagents

❌ generic name collision
name: "helper"
→ collides with anything; use specific name

❌ verbose prose body (5 paragraphs of philosophy)
→ compress to NEVER/ALWAYS/workflow/output sections

❌ inline mega-checklist (50+ items)
→ extract to .claude/rules/<topic>.md, reference

❌ filler in example responses
agent: "Sure! I'd be happy to review your code..."
→ direct action: "Reviewing 3 changed files. Findings:"

❌ persona drift
identity says "concise" but examples are verbose
→ identity + voice + examples must align

❌ deep nesting (>2 levels)
→ flatten
```

</anti_patterns>

---

<maintenance>
- subagent not auto-invoked → audit description (add action-oriented trigger)
- subagent invoked wrong context → narrow description scope, add "Do NOT use for X"
- subagent slow / expensive → check model field (downgrade to haiku) + tool scope
- subagent output pollutes parent → tighten output format (structured > prose dump)
- new tool needed → add to whitelist explicitly, don't switch to inherit-all
- after editing on disk → restart Claude Code session
- agent drifts persona → audit identity + voice + examples (must align)
</maintenance>

---

<self_check>

frontmatter:
- [ ] name kebab-case, unique across scopes
- [ ] description action-oriented ("Use proactively...", "Use when...")
- [ ] description specifies scope boundary ("Do NOT use for X")
- [ ] tools whitelisted if security-sensitive
- [ ] tools field reflects least privilege
- [ ] model field set if non-default

body:
- [ ] identity first line (You are X. You Y.)
- [ ] voice section explicit
- [ ] NEVER section for hard limits
- [ ] workflow numbered if procedural
- [ ] tools have orchestration guidance, not just list
- [ ] conversation: clarify + error + end
- [ ] output format structured
- [ ] zero hedges
- [ ] zero filler in example agent responses
- [ ] no duplication of CLAUDE.md content
- [ ] under token budget
- [ ] examples concrete (good/bad findings)
- [ ] identity + voice + examples align
- [ ] MUST/NEVER ≤ 10% rules
- [ ] no nested bullets > 2 levels
- [ ] no XML wrap in subagent target body

fail any → fix before commit

</self_check>

---

<critical_recap>
1. frontmatter description = orchestrator routing → action-oriented + scoped
2. tools whitelist for read-only agents (reviewer/auditor → Read, Grep, Glob only)
3. body identity first line: "You are X. You Y." (no exceptions)
4. body required sections: identity + voice + NEVER + tools + conversation + output + examples
5. inherit CLAUDE.md context — do not duplicate project conventions
6. structured output (priorities, sections) — not prose dump
7. project-level (.claude/agents/) commit to git for team sharing
8. subagent target body uses plain markdown (no XML wrap)
</critical_recap>