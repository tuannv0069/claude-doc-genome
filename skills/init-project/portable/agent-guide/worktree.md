---
scope: portable
---

<critical>
scope: isolated git worktree lifecycle — create, symlink, use, cleanup.
core: one path convention | pass realpath to child agents | symlink only what the workflow uses | cleanup only after push verified
note: §ID append-only (portable) — never renumber; retired sections keep their number.
</critical>

# Isolated git worktree

## §1 when to use

Create an isolated worktree when:
- parallel-safe build/test/edit without touching the user's main working tree
- a skill or agent must run isolated from concurrent changes in the main tree

Skip when single-thread work where modifying the main tree is safe.

## §2 setup

1. Resolve branch:
   - exists on remote → `git fetch origin <branch>` + checkout (resume)
   - missing → `git fetch origin <base-branch>` + create from `origin/<base-branch>`
2. Worktree path: `.agent/worktrees/<ID>-<TAG>-<SESSION>/` — `<TAG>` = workflow tag (e.g. `FS`, `BE`); `<SESSION>` = unique caller run id (prevents collision across reruns).
3. `git worktree add <worktree-path> <branch>`
4. Symlink non-tracked config (`.env`, runtime settings, credentials) the workflow needs — only items it will actually use.
5. Resolve absolute path once: `WORKTREE_ABS=$(realpath <worktree-path>)`. Child agents do NOT inherit CWD — pass `WORKTREE_ABS` explicitly so they `cd` into the same tree.

Edge cases:

| situation | action |
|---|---|
| path already present from prior run | new `<SESSION>` differs → no conflict |
| main tree has uncommitted changes | unaffected (worktrees are independent) |
| `git worktree add` fails | fail-fast, abort, create nothing else |

## §3 cleanup

Idempotent; each line tolerates prior failure. Guard removal on a verified push.

```bash
# precondition: code committed AND pushed (commit_sha non-null).
# commit_sha null → SKIP removal, print:
#   "WARN: commit_sha missing — worktree preserved at <path>"
cd <root>
git worktree remove -f <worktree-path> 2>/dev/null || true
rm -rf <worktree-path>
git worktree prune
```

Never remove a worktree whose code was not pushed — preserve it so work is recoverable.

<critical_recap>
1. worktree path: `.agent/worktrees/<ID>-<TAG>-<SESSION>/`; pass `realpath` abs to child agents
2. symlink only non-tracked config the workflow will actually use
3. cleanup removes worktree ONLY after commit pushed — else preserve + warn
</critical_recap>
