---
scope: portable
---

<critical>
scope: reading, searching and delegating the reading of project sources on every task.
never: repeat an unchanged reading already in context, or present a result from outside the task's scope as the task's result.
note: locate before loading, re-read a range after it changes, and keep an investigation inside the subsystem the task owns.
</critical>

# Reading project sources

## §1 Identify the relevant source

Prefer a targeted search to loading unrelated material. Read the whole file when the task requires its full meaning and the result can be retained without truncation.

<rules section="ALWAYS">
- Define the files or subsystem needed for the task before searching a shared directory.
- When the location is unknown, use a filename search to find candidates, then search their content for the relevant definitions and callers.
- Inspect a file's size and structure before requesting a large reading, and read the relevant ranges together with the surrounding context needed to understand them.
- When a tool truncates output, retrieve the missing ranges before treating the source as fully read.
</rules>

<rules section="NEVER">
- Load a whole large file when a search can locate the target.
</rules>

<example type="large_file_search">
input: find `getUserById` in an 800-line service file
❌ read the whole file into context
✅ search for the symbol to get its line, then read a short range around it
</example>

## §2 Preserve evidence across readings

A cached summary is a navigation aid, not a substitute for a definition that may have changed. Finding a caller or interpreting a returned value may determine which source must be opened next.

<rules section="ALWAYS">
- After a file changes, read its affected ranges again before relying on the previous interpretation.
- Batch independent searches and readings where the tools permit it.
- Keep dependent readings in order.
</rules>

<rules section="NEVER">
- Repeat an unchanged reading that is still available in the current context.
</rules>

<example type="post_edit_read">
input: line 50 of a file was just edited and its current content is needed for the next edit
❌ reference the earlier read output; the edit is not reflected in it
✅ read the changed range again
</example>

## §3 Keep the investigation within its scope

Choose delegation according to `.agent-workspace/guide/general/orchestration-policy.md` §2. A separate agent can keep a large independent investigation out of the main context, but the number of files alone does not justify duplicating an investigation that is already understood.

<rules section="ALWAYS">
- When several subsystems share a directory, use the relevant subsystem's file or test roster.
- Persist evidence and findings when the task needs to survive a handoff or loss of context.
</rules>

<rules section="NEVER">
- Run an unrelated suite merely because a wildcard reaches it.
- Present results from a different subsystem as evidence about the requested change.
</rules>

<example type="shared_dir_glob">
input: run the test suite of subsystem A; its directory also holds subsystem B's tests
❌ run every test file in the directory; B's pre-existing failure lands in the report, and a turn is spent proving it is unrelated
✅ run A's named roster; B's file is never executed, so its state never enters the result
</example>
