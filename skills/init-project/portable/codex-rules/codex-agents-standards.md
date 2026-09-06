---
paths:
  - ".codex/agents/**"
scope: portable
---

<critical>
target: a subagent definition — one TOML file per agent under `.codex/agents/` (project) or the user's agent directory.
optimize: the parent delegates the right work to it, it returns a usable answer, and it costs a fresh context rather than a second copy of the parent's.
wording: `rule-writing-standards.md` owns imperative form, the hedge ban, and format choice. This file owns the definition's shape and what belongs in it.
note: a subagent runs in a context of its own. Nothing the parent read is inherited — say it in the definition or it is not there.
</critical>

<schema>
required:
  name                     the identifier the parent spawns it by
  description              WHEN to use this agent — read before the body, and it is what routing keys on
  developer_instructions   the agent's behaviour, in full
optional:
  model                    override the default subagent model
  model_reasoning_effort   override the default effort
  sandbox_mode             narrow what it may do — `read-only` for anything that only inspects
  mcp_servers              the external servers this agent may reach
  skills.config            which skills it may use
</schema>

<rules section="NEVER">
- write `description` as a summary of what the agent IS — routing reads it to decide WHEN, and a summary answers a question nobody asked
- assume the parent's context: no file the parent opened, no earlier turn, no conclusion already reached, is visible here
- give an inspecting agent write access — an agent that only reads gets `sandbox_mode = "read-only"`, and the definition says why
- restate a rule the always-loaded chain already carries — the agent inherits the chain, not the parent's reasoning
- leave the return shape unstated — an agent whose output shape is improvised cannot be consumed by the caller that spawned it
</rules>

<rules section="ALWAYS">
- `description` names the trigger condition and the exclusion: when to use it, and the near-miss case it must not absorb
- `developer_instructions` states the task, the boundary (what it must not decide), and the exact shape of what it returns
- an agent that verifies or audits another phase's output is defined so it never sees that phase's reasoning — unprimed attention is the deliverable
- one agent, one job; a definition that needs "and also" is two definitions
- narrow `model` / `model_reasoning_effort` / `sandbox_mode` deliberately, or leave them out and inherit — never set them to look thorough
</rules>

<example type="description">
input: an agent that reads code and reports evidence, proposing nothing
❌ description = "A read-only codebase explorer agent."
✅ description = "Trace execution paths and cite files when a question needs evidence from the codebase. Not for proposing or applying fixes."
</example>

<example type="context_isolation">
input: the parent has already read three files and formed a hypothesis
❌ developer_instructions = "Verify the hypothesis above."
✅ developer_instructions states the claim in full, names the files to open, and asks for a verdict with evidence — nothing is "above"
</example>

<example type="return_shape">
input: an agent that reviews a change
❌ "Report any problems you find."
✅ "Return one block per finding: file, line, the defect in one sentence, and the concrete input that triggers it. Return an empty list when nothing survives verification."
</example>

<critical_recap>
1. one TOML file, one agent, one job — `name`, `description`, `developer_instructions` are all required
2. `description` answers WHEN, with its exclusion; it is what routing reads
3. nothing from the parent's context arrives — state it or lose it
4. an inspecting agent is read-only and unprimed, on purpose
5. the return shape is part of the definition, never improvised
</critical_recap>
