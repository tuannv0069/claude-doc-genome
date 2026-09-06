---
paths:
  - "**/AGENTS.md"
  - "**/AGENTS.override.md"
scope: portable
---

<critical>
target: AGENTS.md — the root of the Codex instruction chain, loaded at the start of every session.
first law: AGENTS.md is GENERATED — it is never typed into; the generator composes it and the next render overwrites any hand edit.
wording: `rule-writing-standards.md` owns imperative form, hedge ban, and smallest-format choice. This file owns only what the instruction chain adds.
slot map, and why each Codex delta exists: `.agent-workspace/guide/general/harness-adapter.md` §2, §3.
language: English regardless of conversation language.
</critical>

<rules section="NEVER">
- hand-edit `AGENTS.md` — the next render overwrites it and the edit leaves no diff behind
- let the rendered chain exceed the `project_doc_max_bytes` the shipped project config declares — the overflow is dropped with no warning, and the loss lands on whichever file came next, never on the one whose size caused it
- write prose into a `.rules` file — that extension is the Starlark command-approval format; prose there is fed to the policy engine
- rely on a nested `AGENTS.md` to scope a standard to a file type — nesting scopes by working directory, not by the file being edited
- name a rule file the chain does not carry — a trigger pointing at an absent file is a dead read
</rules>

<rules section="ALWAYS">
- a rule that must hold every turn → carried in `AGENTS.md` in full, because the chain is the only surface that loads on its own
- a rule needed only for one file type → left in the rule directory and reached by a trigger line at the root, keyed to the action and its concrete object
- ship the cap beside the file: a project `config.toml` sized to the rendered chain, with headroom
- one rule, one location — a rule carried in the chain is not repeated in a file the chain also names
</rules>

<size_budget>

Two budgets, both counted, never estimated. The tighter one binds.

| budget | measured by | why |
|---|---|---|
| `project_doc_max_bytes` | `wc -c AGENTS.md` | the platform stops adding files once the combined chain reaches it; default 32768, raisable from project config |
| readable length | `wc -l AGENTS.md` | past a few hundred lines of index material, adherence drops — the always-loaded rule sections that follow the index are not counted against this |

Over the byte budget → raise the declared cap if the content earns it, or move a rule out of the
always-loaded set and give it a trigger line instead. Never let it silently truncate.

</size_budget>

<trigger_lines>

- a file outside the chain that affects behaviour → one line: `cond → MUST Read <file>`
- `cond` is decided without judgment, in one of three shapes:

| shape | decided by | example |
|---|---|---|
| message-triggered | scanning the user's message alone | `commit / branch / merge` |
| work-state | a count the agent keeps of its own work | `past the 3rd file read` |
| action-triggered | the action about to be taken and its concrete object | `about to edit **/AGENTS.md` |

- abstract task classification (`complex task`, `multi-step task`) and intent interpretation
  (`when X is needed`) are not conditions — they decide nothing

</trigger_lines>

<example type="always_loaded_rule">
input: a guardrail the agent must hold on every turn
❌ leave it in a rule file and hope a trigger fires — the file loads only if the agent chooses to read it
✅ carry the rule's full text inside the chain; the file stays as the editable copy
</example>

<example type="edit_target">
input: the agent keeps skipping a rule; the fix is one more line of guidance
❌ add the line to AGENTS.md — gone at the next render, with nothing to show it was ever there
✅ add it to the generated file's source, re-render, commit both
</example>

<critical_recap>
1. AGENTS.md is generated — never the file you type into
2. the chain is the only surface that auto-loads; an always-loaded rule lives inside it, in full
3. two budgets, both counted; the byte cap truncates silently and is shipped beside the file
4. a file outside the chain earns a trigger line, and its condition is decided without judgment
5. `.rules` is command-approval policy, never prose
</critical_recap>
