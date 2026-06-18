---
scope: portable
---

<rules section="file_reading">

## NEVER

- Read full file when grep/glob can locate target
- cat/less/full Read without offset on file > 200 lines
- re-read file unchanged since last read in current context
- sequential Read when files independent (use parallel calls)

## ALWAYS

- file edited since last read → re-read affected range (stale context = bugs)
- unknown file size → `wc -l` before Read
- exploration → small-output cmds (grep, head, wc, tail)
- heavy research (10+ files, deep search) → delegate to Task subagent

## conditional

| situation                           | action                              |
| ----------------------------------- | ----------------------------------- |
| unknown file location               | Glob/find                           |
| known file, > 200 lines (~2000 tok) | grep -n → Read(offset, limit)       |
| known file, < 200 lines             | Read direct                         |
| multiple files needed               | parallel Read calls, not sequential |
| file just edited                    | re-read changed range               |
| 10+ files exploration               | Task subagent (isolated context)    |

## examples

<example type="large_file_search">
input: find getUserById in user.service.ts (800 lines)
❌ output: Read("user.service.ts")  # dumps 800 lines into context
✅ output:
  1. grep -n "getUserById" user.service.ts  → line 234
  2. Read("user.service.ts", offset=230, limit=40)
</example>

<example type="parallel_reads">
input: need to read config.ts, types.ts, utils.ts
❌ output: Read(config.ts) → wait → Read(types.ts) → wait → Read(utils.ts)
✅ output: Read(config.ts) + Read(types.ts) + Read(utils.ts)  # one round-trip
</example>

<example type="post_edit_read">
input: edited auth.ts at line 50, now need line 50 content for next edit
❌ output: reference prior Read output  # stale, edit not reflected
✅ output: Read("auth.ts", offset=45, limit=15)  # current state
</example>

<example type="heavy_exploration">
input: trace all usages of UserContext across codebase
❌ output: Glob → Read 15 files → main context polluted
✅ output: Task("trace UserContext usages, return summary")  # isolated
</example>

</rules>
