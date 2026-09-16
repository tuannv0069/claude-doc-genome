---
scope: portable
---

# Reading project sources

## §1 Identify the relevant source

Define the files or subsystem needed for the task before searching a shared directory. When the location is unknown, use a filename search to find candidates, then search their content for the relevant definitions and callers. Prefer a targeted search to loading unrelated material.

Inspect a file's size and structure before requesting a large reading. Read the relevant ranges together with the surrounding context needed to understand them. Read the whole file when the task requires its full meaning and the result can be retained without truncation. If a tool truncates output, retrieve the missing ranges before treating the source as fully read.

## §2 Preserve evidence across readings

Do not repeat an unchanged reading that is still available in the current context. After a file changes, read its affected ranges again before relying on the previous interpretation. Treat a cached summary as a navigation aid, not as a substitute for a definition that may have changed.

Batch independent searches and readings where the tools permit it. Keep dependent readings in order: finding a caller or interpreting a returned value may determine which source must be opened next.

## §3 Keep the investigation within its scope

When several subsystems share a directory, use the relevant subsystem's file or test roster. Do not run an unrelated suite merely because a wildcard reaches it, and do not present results from a different subsystem as evidence about the requested change.

Choose delegation according to `.agent-workspace/guide/general/orchestration-policy.md` §2. A separate agent can keep a large independent investigation out of the main context, but the number of files alone does not justify duplicating an investigation that is already understood. Persist evidence and findings when the task needs to survive a handoff or loss of context.
