---
scope: portable
---

# Working in an isolated Git worktree

A worktree provides a separate checkout while sharing repository history. Use it when isolation protects concurrent work or lets a task build, test, or edit without disturbing the user's current checkout.

## §1 When isolation is useful

Create a worktree when the task or owning workflow requires an independent checkout. A single task can remain in the current checkout when that is safe and no isolation requirement applies.

Before creation, identify the branch or starting revision the task is authorized to use. Do not invent a requested branch name or include unrelated local changes without understanding the intended starting state.

## §2 Setup

1. Inspect the repository and existing worktrees. Resolve the intended branch and starting revision from the task. Fetch the required remote reference when it is needed to establish that state.
2. Choose a task-specific path beneath `.agent-workspace/worktrees/`. Include a unique session identifier so another run cannot reuse the same directory accidentally.
3. Create the worktree with `git worktree add` using the resolved path and branch or revision. If creation fails, stop before adding dependent configuration or starting work in an assumed checkout.
4. Provide only the untracked configuration the task actually needs. Use platform-appropriate links or another supported mechanism, and do not expose credentials in logs or reports.
5. Resolve the checkout's absolute path and pass it explicitly to every agent or command that works there. Do not assume a child process or subagent shares the coordinator's working directory.

Inspect an existing directory before reusing it. The presence of a path does not prove that it belongs to the current task.

## §3 Cleanup

Before removing a worktree, verify that its work has been accepted, integrated, or otherwise preserved at a recoverable location. Inspect both tracked and untracked changes. An uncommitted result can remain in the worktree until the user decides what to do with it.

Do not commit or push merely to satisfy a cleanup condition. Those actions require the user's authorization independently of the decision to create an isolated checkout.

Use Git's worktree removal for a checkout that is safe to remove, and inspect any failure instead of following it with unconditional recursive deletion. Resolve and verify the exact absolute target before a destructive filesystem operation. Preserve the checkout when ownership or recovery is uncertain, and report what remains.

Prune stale worktree metadata only after the actual checkout state has been established. Cleanup is complete when the intended disposable checkout is gone and the task's useful work remains recoverable.
