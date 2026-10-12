---
scope: portable
---

<critical>
scope: creating, using and removing an isolated Git worktree under `.agent-workspace/worktrees/`.
never: remove a worktree before its work is preserved at a recoverable location, or commit or push merely to satisfy a cleanup condition.
note: one path convention, the resolved absolute path passed to every child agent or command, only the configuration the task needs linked in.
</critical>

# Working in an isolated Git worktree

A worktree provides a separate checkout while sharing repository history. Use it when isolation protects concurrent work or lets a task build, test, or edit without disturbing the user's current checkout.

## §1 When isolation is useful

A single task can remain in the current checkout when that is safe and no isolation requirement applies.

<rules section="ALWAYS">
- Create a worktree when the task or owning workflow requires an independent checkout.
- Before creation, identify the branch or starting revision the task is authorized to use.
</rules>

<rules section="NEVER">
- Invent a requested branch name, or include unrelated local changes without understanding the intended starting state.
</rules>

## §2 Setup

1. Inspect the repository and existing worktrees. Resolve the intended branch and starting revision from the task. Fetch the required remote reference when it is needed to establish that state.
2. Choose a task-specific path beneath `.agent-workspace/worktrees/`. Include a unique session identifier so another run cannot reuse the same directory accidentally.
3. Create the worktree with `git worktree add` using the resolved path and branch or revision. If creation fails, stop before adding dependent configuration or starting work in an assumed checkout.
4. Provide only the untracked configuration the task actually needs. Use platform-appropriate links or another supported mechanism, and do not expose credentials in logs or reports.
5. Resolve the checkout's absolute path and pass it explicitly to every agent or command that works there.

<rules section="ALWAYS">
- Inspect an existing directory before reusing it; the presence of a path does not prove that it belongs to the current task.
</rules>

<rules section="NEVER">
- Assume that a child process or subagent shares the coordinator's working directory.
</rules>

## §3 Cleanup

An uncommitted result can remain in the worktree until the user decides what to do with it. Committing and pushing require the user's authorization independently of the decision to create an isolated checkout. Cleanup is complete when the intended disposable checkout is gone and the task's useful work remains recoverable.

<rules section="ALWAYS">
- Before removing a worktree, verify that its work has been accepted, integrated, or otherwise preserved at a recoverable location, inspecting both tracked and untracked changes.
- Use Git's worktree removal for a checkout that is safe to remove, and inspect any failure.
- Resolve and verify the exact absolute target before a destructive filesystem operation.
- Preserve the checkout when ownership or recovery is uncertain, and report what remains.
- Prune stale worktree metadata only after the actual checkout state has been established.
</rules>

<rules section="NEVER">
- Commit or push merely to satisfy a cleanup condition.
- Follow a failed worktree removal with unconditional recursive deletion.
</rules>
