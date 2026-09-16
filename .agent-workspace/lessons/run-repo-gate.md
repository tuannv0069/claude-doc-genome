---
scope: project
---

<critical>
scope: about to run a script or gate under `.agent-workspace/tooling/` — the command itself, before its output exists.
phase: operating
never: read the tool's guide after seeing the report | treat a gate's own output as the thing the trigger was about
always: the trigger fires on the command being about to run, not on the finding being about to be judged
</critical>

Procedure for recording / escalating / reading back: `.agent-workspace/guide/general/lesson-capture.md`.

### Read a tool's guide before the command, not after the report lands

- signal — the always-loaded surface names a tool and a guide in one line (`run <tool>, or judge one of its findings → MUST Read <guide>`), and the tool is about to be invoked as one step of a larger task.
- ❌ ran `scan_rule_health.py` as a routine post-change check and read `rule-health.md` only once the report printed findings that needed judging. It looked right because the trigger's second clause ("or judge one of its findings") reads like the operative one, and no finding exists yet at the moment of the run.
- ✅ trigger names a command → read its guide in the turn BEFORE the command runs.
- evidence — this session: `python .agent-workspace/tooling/scan_rule_health.py` ran, printed 17 `dup` findings, and only then was `rule-health.md` opened; `CLAUDE.md` ALWAYS names both clauses of that trigger.
- seen — 1

### A `dup` flood after adding a generated file means the scan's scope is wrong, not the corpus

- signal — a change introduces a generated artifact, and the next health scan reports many findings that all pair the generated file against its source.
- ❌ open a ledger entry per finding and `exempt` each one against `doc-organization.md` §4 — the duplication is by construction, so the entries can never close and the report stops being readable.
- ✅ generated artifact added → exclude it from the scan's corpus in the same change set.
- evidence — 17 `dup` findings pairing `AGENTS.md` against `CLAUDE.md`; fixed by adding the Codex surface to `FROZEN` in `scan_rule_health.py`, with two cases in `test_scan_rule_health.py`.
- seen — 1

### Resolve output paths against their owning workspace

The situation occurs when a probe runs in an isolated project but stores its evidence in the source repository. In this task, the first probe command used a relative output path while its current directory was the isolated fixture. The write failed because that task directory existed only in the source repository.

Use an absolute path for evidence owned by a different workspace, and establish the output file before starting the dependent command. The corrected command used the source repository's absolute task path. The subsequent Claude invocation reached the service and reported a usage limit, which is a separate environmental result. This method failure has been observed once.

### Exercise the host encoding when a verifier reads Git history

The first integrated rule-health run failed on Windows even though its parser fixtures passed. Git returned UTF-8 text, while a subprocess decoded it with the host's default Windows-1252 codec. The decoding error left the history comparison without valid text.

Use explicit UTF-8 decoding for Git text and include a history fixture with non-ASCII content under a different preferred host encoding. The new fixture also verifies that a later target revision reopens an earlier resolved drift finding. Parser-only success does not establish that the tool can read real history on the host. This failure has been observed once.
