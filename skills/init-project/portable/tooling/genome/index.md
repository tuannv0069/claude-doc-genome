---
scope: portable
---

# Tool group: genome

The tools in this group check the documentation system that the genome installs. The genome's updater owns the group; a project's own tools belong to another group under `.agent-workspace/guide/general/tooling.md` §2. Every tool is run with `python .agent-workspace/tooling/genome/<entry point>`, from any directory, and imports the Python standard library alone; `verify_wiki.py` also needs `rg` (ripgrep) on the path, and the tools that read version history need `git`.

Run every test of the group with `python .agent-workspace/tooling/genome/run_tests.py`.

## §1 Tools

| entry point | what it does | reads | prints or changes | run when |
|---|---|---|---|---|
| `verify_lesson_router.py` | Checks the lesson router and the metadata of each lesson store | `.agent-workspace/lessons/` | Problems found; changes nothing | After editing the lesson router or a lesson store |
| `verify_role_files.py` | Checks the role router, the role folders, each role's §6 and the roles its handoffs name | `.agent-workspace/guide/roles/` | Problems found; changes nothing | After adding, renaming, removing or routing a role |
| `verify_decision_log.py` | Checks the names, metadata and subjects of the decision entries | `.agent-workspace/decisions/` and version history | Problems and warnings; changes nothing | After writing a decision entry |
| `verify_wiki.py` | Checks the wiki's claims, evidence fields and identifiers; `--new-id` proposes an identifier and `--merge-check` compares identifiers across revisions | `.agent-workspace/wiki/` and the material it cites | Failures found; changes nothing | After editing a wiki cluster, and before merging wiki changes |
| `verify_no_task_links.py` | Finds tracked or about-to-be-added files that cite a path under the task workspace | Every tracked file and every untracked file that is not ignored | Problems found; changes nothing | Before committing |
| `scan_rule_health.py` | Scans rules and guides for duplicated requirements, growth, dead references and drift; read `.agent-workspace/guide/general/rule-health.md` first | Rules, guides and version history | A report; updates `.agent-workspace/rule-health/ledger.json` | When an edit touches more than one rule or guide |
| `archive_decisions.py` | Lists the superseded decision entries of one year and moves them to the archive after the answer `y`, or at once with `--yes` | `.agent-workspace/decisions/` | The candidates; moves files with `git mv` once confirmed | When the decision journal's volume warning appears |
| `verify_tool_groups.py` | Checks that every tool group has the shape `tooling.md` §2 to §5 defines, and for Python files that imports sit at the top and calls go downward | `.agent-workspace/tooling/` | Problems found; changes nothing | After adding, moving or removing a tool, a file of a tool or a group |
| `run_tests.py` | Runs the test files of this group | `tests/test_*.py` | One line for each test file and the output of each failure | After changing any tool of this group |

## §2 Maintaining the group

Add, change or remove a row in the same change as its tool, as `.agent-workspace/guide/general/tooling.md` §5 requires.
