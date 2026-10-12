---
scope: portable
---

<critical>
scope: creating, placing, changing or removing an executable script or tool that the assistant runs, and organizing a folder of tools.
never: write a new tool before reading the tool index for one that already does the work, or leave a tool without a row in its group's index.
note: a script lives in one of three places (§1); every tool group has the same shape (§3); a call goes downward only (§4); how the code itself is written is `writing-code.md`.
</critical>

# Organizing tools

A tool is an executable script that is run again: a verifier, a scanner, a converter, a fetcher. Without a fixed place and an index, an assistant cannot find out whether a tool already exists, so it writes the same one twice, and without a fixed shape each tool grows in its own direction until changing one means reading all of it.

## §1 Three places for a script

A script written for one task is not yet a tool. Most scripts are used once, and giving each of them a test and an index row would cost more than they return.

| place | holds | used by |
|---|---|---|
| `.agent-workspace/tasks/<task-slug>/` | A script written for one task | That task |
| The package of a skill | A script that is part of one skill's implementation, under `.claude/rules/skill-md-standards.md` §4 | That skill |
| A tool group or a product tool folder (§2) | A tool that is run again | Any task |

<rules section="ALWAYS">
- Read `.agent-workspace/tooling/index.md` and the index of the fitting group before writing a script, and use or extend the tool that already does the work.
- Write a script that serves one task in that task's workspace.
- When a later task needs a script that was written for an earlier one, promote it to a tool in the same change: place it in a group, give it a test and add its row to the group's index.
</rules>

<rules section="NEVER">
- Rewrite a script from memory of an earlier task when the earlier script can be promoted.
- Place a script that only one skill uses in a tool group.
</rules>

## §2 Tool groups

Tools are grouped by the kind of work they serve, so that the path shows which work a tool belongs to and who owns it. A group is a folder directly under `.agent-workspace/tooling/`. The group `genome/` holds the tools that check the documentation system; the genome's updater owns it. A project adds a group for each kind of work that needs tools of its own. A folder of tools that serves the project's product may stay beside the product, such as a `tools/` folder inside an application; the project names it in its entry point, and it has the shape of a group.

The router `.agent-workspace/tooling/index.md` lists every group and every product tool folder, with the kind of work each one serves.

<rules section="ALWAYS">
- Place a new tool in the group of the work it serves, and create a group, with its row in the router, when no existing group fits.
- Split a group into two when its index holds tools for two different kinds of work.
</rules>

<rules section="NEVER">
- Put a tool file directly under `.agent-workspace/tooling/`, or a group inside a group.
- Add a project's tool to the `genome/` group.
</rules>

## §3 The shape of a group

Every group has the same shape, in whatever language its tools are written. The file extensions below are examples. Where a language's toolchain fixes the place of a test or of an entry point, the toolchain decides, and the group's index states the difference.

```
<group>/
  index.md              one row for each tool
  verify_links.py       an entry point: one file for each tool
  scan_health.py
  lib/                  code that two or more tools of the group use
  health/               the parts of one tool that has several, one part in each file
  tests/                a test file for each tool or module, shared test support, and fixtures/ for sample data
```

Entry points lie flat in the group. The command that runs a tool then has one predictable form, and a language that looks for modules beside the running script finds `lib/` and the tool's folder without any change to its search path. A prefix that names the action, such as `verify_`, `scan_` or `fetch_`, keeps related entry points together.

A tool that has several parts keeps its entry point in the group and its parts in one folder beside it. The folder is named after what the tool works on, and does not share the entry point's name.

<rules section="ALWAYS">
- Give each tool exactly one entry point in the group folder.
- Keep a tool with a single responsibility in its entry point, calling `lib/` for anything shared.
- Give a tool that has gained a second responsibility a folder beside its entry point, with one file for each part, under `writing-code.md` §4.
- Put every test in `tests/`, in a file named after the tool or the module it tests.
</rules>

<rules section="NEVER">
- Create a folder inside `lib/`, inside a tool's folder or inside `tests/` other than `tests/fixtures/`.
- Give a tool's folder the same name as its entry point.
</rules>

## §4 Levels and the direction of calls

| level | holds | does not hold |
|---|---|---|
| Entry point | Reading arguments, calling modules, printing the result, returning the exit status | The logic of the tool, once the tool has a folder |
| A tool's folder | The parts of that tool, each changeable on its own | Code that another tool also needs |
| `lib/` | Code that two or more tools use under the same contract | A rule that belongs to one tool |

A call goes downward only: an entry point calls its tool's folder and `lib/`, and a tool's folder calls `lib/`. When one tool reaches into another, a change to the second breaks the first without anyone having looked at it.

<rules section="ALWAYS">
- Move code to `lib/` when a second tool needs it, under `writing-code.md` §3.
- Let the parts of one tool call each other and `lib/`.
</rules>

<rules section="NEVER">
- Import one tool's entry point or folder from another tool.
- Import a tool from `lib/`.
- Share code between two groups by importing across them; keep an implementation in each group and name the other one in a comment.
</rules>

## §5 The index and the contract of a tool

The index is how an assistant learns what a tool does without opening it. Each row of a group's `index.md` gives the tool's entry point, what it does, what it reads, what it prints or changes, and when it is run. The entry point opens with a comment or documentation string that states the same contract and the meaning of each exit status.

<rules section="ALWAYS">
- Add, change or remove a tool's index row in the same change as the tool.
- State in the index the one command that runs every test of the group.
</rules>

<rules section="NEVER">
- Describe in the index a behavior the tool does not have.
</rules>

## §6 The command-line contract

The reader of a tool's output is usually an assistant that has to act on it, and that reader works worse on long, unstructured output than on a short, directed one.

<rules section="ALWAYS">
- Exit with status 0 when the tool ran and found nothing wrong, 1 when it ran and found a problem, and 2 when it could not run or could not read its input.
- Print each finding on one line that gives the file, the line where there is one, what is wrong and what to change.
- Print results to standard output and diagnostics about the tool itself to standard error.
- Limit long output: print the number of findings, the first of them, and how to see the rest.
- Find the project root from the tool's own location or from the version-control root.
- Make a tool that changes files print its plan by default and change them only when an explicit option asks for it, and say what it changed.
- Answer a help option with the tool's contract.
</rules>

<rules section="NEVER">
- Report success when the tool read no input.
- Print a stack trace or a bare error code as the only explanation of a failure.
- Depend on the directory the tool happens to be run from.
</rules>

<example type="finding_line">
input: a verifier finds a router row that names a file which does not exist
❌ `Error: validation failed (code 3)`
✅ `guide/index.md:42: row names missing-guide.md, which does not exist — remove the row or restore the file`
</example>

## §7 Dependencies

A tool in the `genome/` group is copied into projects whose installed software is unknown. A project's own tools run only in that project.

<rules section="ALWAYS">
- Write a tool of the `genome/` group with the standard library of its language alone.
- Write a project's tool with the dependencies the project has already declared.
</rules>

<rules section="NEVER">
- Add a dependency for a tool without the user's decision.
- Run a tool from a distribution bundle or any other copy that is not its deployed location; a run can leave generated files inside the copy.
</rules>
