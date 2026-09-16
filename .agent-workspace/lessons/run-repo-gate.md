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

### Check command output encoding as well as file encoding

The independent Codex updater handled UTF-8 files correctly, but its first CLI test with a Vietnamese project path failed while printing the JSON plan on Windows. The command still inherited a legacy output encoding, so correct file handling did not establish that a caller could receive its result.

Set the CLI's text streams to UTF-8 and exercise the real process with a non-ASCII target path. Verify the parsed output and exit status, not only the in-process functions. The corrected Codex tests cover this through an external invocation. This failure has been observed once.

### Retain partial evidence when a model-backed check times out

Three first-run Codex behavior probes reached their time limit, but the probe's exception handler saved only the timeout flag. It discarded partial events, leaving no way to tell from those records whether the model had started, selected a tool or stalled before completion. Treating those records as an instruction-following failure would have been unsupported.

Retain filtered events and diagnostics on timeout, and explicitly close unused standard input for a noninteractive CLI. Use an independent minimal tool probe to distinguish a general execution problem from the behavior under test. A later conversation probe completed with the genome routers read; it does not retroactively establish the cause of the three earlier timeouts. This instrumentation failure has been observed once.

### Resolve distribution-document links in the built package

A final ad hoc link check resolved `codex/PACKAGE.md` links relative to the source directory and reported two missing targets. That document becomes the package README, whose `skills/` paths exist only after packaging. The external-package test had already checked that layout successfully.

Validate a distribution document at its actual output location after the build, while checking source documents against their source directories. A missing source-relative target does not prove a broken package link. The corrected check used the built README and found no missing targets. This method failure has been observed once.

### Preserve managed bytes when testing an unrelated edit

An independent portability probe prepended project-owned context to AGENTS using a text read/write round trip. On Windows, that operation also normalized line endings inside the managed region. The next updater correctly reported a conflict, even though the probe intended to change only content outside the region.

Construct an outside-region edit without changing the managed bytes, and compare those bytes before interpreting a conflict as a product defect. The corrected byte-preserving fixture passed initialization, source refresh, update and local-conflict checks. Evidence is retained in the Codex single-source forward-test record. This instrumentation failure has been observed once.
