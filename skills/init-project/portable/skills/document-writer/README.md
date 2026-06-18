# Skill: document-writer

Technical Editor for project documentation. Apply §A–§G writing constraints as pre-writing rules when creating or substantially rewriting a substantive `.md` document outside `.claude/**` and `docs/agent-guide/**`.

## Quick Start

```
/document-writer docs/guidelines/onboarding.md "how to onboard a new module"
/document-writer docs/specs/import-spec.md
```

**Output:** the completed document written to `<OUTPUT_PATH>`, every heading `§`-numbered and all cross-references in `§X.Y` form.

## Scope

- Apply to: guidelines, specs, design docs, process docs, READMEs, business documentation outside `.claude/**` and `docs/agent-guide/**`.
- Skip: any path under `.claude/**` or `docs/agent-guide/**` (own standards), and any path the project's CLAUDE.md `## document writing` skip list declares out of scope (e.g. `detailed-design-*.md`, auto-generated).

## How It Works

1. Parse `$ARGUMENTS` → `{OUTPUT_PATH}` + `{CONTENT_BRIEF}`.
2. Validate path; SKIP if out of scope (SKILL.md §2).
3. Existing file → rewrite mode; else new.
4. Apply §4 heading convention + §5 writing constraints (§A–§G, §H mermaid) while writing.
5. Run §6 self-check; fix in place.
6. Write to `{OUTPUT_PATH}`; return STATUS.

## Dependencies

- `docs/agent-guide/general/mermaid.md` §M7 + §2 — only when the output contains a ` ```mermaid ` block.

## Usage by Orchestrators

Subagents cannot invoke skills — embed §4–§6 directly into the subagent prompt (SKILL.md §8).

## Self-test

```bash
bash .claude/skills/skill-writer/scripts/test-skill.sh .claude/skills/document-writer/
```
