---
scope: portable
---

# Reading sources for the current task

## §1 Locate the evidence

Identify the subsystem or artifacts needed for the task before searching a shared directory. Use filename and content searches to locate definitions and their consumers. Inspect the size and structure of a large file, then read the relevant ranges with enough surrounding context to understand the contract. Read a whole file when the task requires it and the tool can return it without losing content.

A truncated response is an incomplete reading. Retrieve the missing material before claiming to have examined it. A search hit locates evidence; it does not establish the meaning of the surrounding procedure.

## §2 Keep readings current

Reuse an unchanged reading that remains in context. Reread changed ranges before relying on them. A cached summary can locate a definition but cannot certify that definition's current value.

Batch independent reads when the tool supports it. Preserve order when one result determines what to inspect next. Read both sides of an interface before describing what their interaction means, as required by `critical-thinking.md` §2.

## §3 Preserve scope and continuity

Use the task's named file or test roster instead of a broad wildcard that includes unrelated subsystems. Do not describe another subsystem's results as verification of this task.

Use `.agent-workspace/guide/general/orchestration-policy.md` §2 when an independent investigation could be delegated. Save developing findings under its §4 when research must survive context loss or a handoff. File count alone is not a reason to repeat an investigation in another agent.
