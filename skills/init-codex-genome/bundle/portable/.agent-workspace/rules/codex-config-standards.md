---
scope: portable
---

# Codex configuration boundaries

## §1 Change only the configuration the task needs

The genome's core workflow does not require changing the user's model, sandbox, approvals, trust, hooks or MCP servers. Before adding a module that needs configuration, establish which supported client reads it and which specific settings the module owns. Do not replace built-in model instructions to append project guidance.

Inspect configuration precedence and the effective project trust state. A project file can be syntactically valid and still be ignored. Official documentation describes the platform contract; observations of the installed client establish whether the feature works in that environment.

## §2 Preserve existing settings

Treat configuration outside explicitly owned keys or regions as project or user data. A merge must preserve unrelated keys, comments and values. If the available writer cannot do that, prepare a reviewed diff rather than regenerating the whole file. Do not alter user-wide configuration to make a project test pass.

Resolve project roots explicitly in tools. A nested product's source root is not necessarily the enclosing Git root, and the installed package location is not necessarily the target project. Check links and path boundaries before writes under the deployment tooling's contract.

## §3 Distinguish extension mechanisms

Execution-policy `.rules` files govern command permission decisions; they are not a Markdown instruction tier. Hooks run event-driven operations and may require separate trust. MCP provides external tools or resources. Each mechanism needs its own verified ownership, capability and failure handling when a project chooses to enable it.

Do not depend on an optional hook as the only route to a required workflow check. Provide a direct way to perform that check and state when automation is unavailable. Never store secrets in distributed instructions or test output.

## §4 Test what the claim requires

Use an isolated fixture for configuration experiments. Separate parsing, discovery, trusted execution and resulting behavior. Record the client version and working context, and do not generalize a CLI result to desktop, IDE, remote or cloud without corresponding evidence.

An unavailable feature is a capability limit, not a reason to weaken the user's security settings. Keep the core task functional where possible and report the part that remains unverified.
