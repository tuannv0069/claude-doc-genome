---
class: debt
subject: docs/codex/compatibility.md
anchor: Codex implementation P0 probes on codex-cli 0.154.0-alpha.6.2 and the available desktop tool surface on 2026-09-16.
---

The subject was originally assessed at `codex/docs/compatibility.md`. Before this pending change was committed, the user requested removal of the root product directory and the document moved to `docs/codex/compatibility.md`. This pointer follows that move; the client-verification debt remains unchanged.

decided: Deliver the independently executable Codex core and its verified CLI/package behavior with an explicit client qualification limit. Do not describe native desktop UI loading, IDE, remote or cloud behavior as verified. Keep standalone custom-agent definitions out of the core distribution until their registration and invocation can be established on the target client.

because: The configuration and loading probes succeeded, but two bounded custom-agent execution probes returned unavailable without spawning. The available desktop automation surface does not permit controlling or opening a fresh native desktop test session for this task. Repeating CLI checks would not close that UI evidence gap. The core workflow works through project instructions and role guides without those optional agent files.

unlocked by: Run the recorded fresh-session acceptance cases through the target desktop UI, and separately verify custom-agent registration, invocation, context and permissions before certifying or distributing that optional component. Record the actual client version and resulting evidence. Publication still requires its own authorization and evaluation of these limits.
