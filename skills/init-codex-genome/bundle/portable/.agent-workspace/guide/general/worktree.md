---
scope: portable
---

# Isolating work in a Git worktree

## §1 Establish why and where to isolate

Use a worktree when the task requires a separate checkout or when isolation protects concurrent edits and tests. A single safe task can remain in its current checkout. Inspect existing worktrees and establish the authorized starting branch or revision before creating another one.

Choose a unique task path under `.agent-workspace/worktrees/` unless the task names another location. Do not silently include unrelated local changes or invent a user-requested starting branch. Fetch a remote reference only when needed to establish the intended state.

## §2 Verify setup before continuing

Create the checkout through Git and confirm success before adding dependent configuration or executing work there. Resolve its absolute path and provide it explicitly to tools and delegates. An existing directory is not proof of ownership by this task.

Provide only untracked configuration the task needs, using supported platform mechanisms. Do not expose credentials in task output. Preserve persistent plans and evidence outside the disposable checkout so cleanup cannot erase the only record.

## §3 Preserve work before cleanup

Inspect tracked and untracked changes before removal. Confirm that useful work is accepted, integrated or recoverable elsewhere. Do not commit or push merely to make cleanup easier; those actions need their own user authorization.

Use Git's worktree removal and investigate a refusal rather than following it with unconditional recursive deletion. Verify the resolved absolute target and its ownership before a destructive filesystem action. Retain the checkout when recovery or ownership is uncertain. Only prune stale metadata after establishing the real checkout state.
