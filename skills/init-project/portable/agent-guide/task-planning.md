---
scope: portable
---

<critical>
scope: plan + verify before executing any artifact-changing task. scale rigor to size, pick form by task type.
core: plan-before-execute | size the rigor | design verification into plan | independent output-audit | genome-rule per sub-task | loop-back + off-ramp
out: pure question / explanation with no file change → answer direct, skip this
</critical>

## §1 when this applies

apply-test: does the answer change a file / produce a deliverable? no → out of scope, answer direct. yes → task, enter at scale §2.1 (even when phrased as a question).

## §2 two axes (independent)

- scale (§2.1) → depth (how many steps)
- task type (§2.2) → form (truth source + criteria shape)
- task type NEVER raises depth; depth only from scale

### §2.1 scale → depth

| scale | signal | apply |
|---|---|---|
| small | 1 step, 1 file, easily reversible (typo, rename, format, 1 const) | §3.7 inline + execute + self-check on source (§3.6); skip §4 |
| medium | few steps/files, 1 module, mid risk | §4.1+§4.2+§4.3 merged, §4.4 short, skip §4.5, §4.6 light, §4.7 with output-audit |
| full | ≥1 explicit risk signal: owner/closed module, migration, many modules, costly-irreversible, broadly reused | full §4.1→§4.7 |

unsure → medium. full only with ≥1 explicit risk signal, never on "feels big".

### §2.2 task type → form

| type | truth source | output form |
|---|---|---|
| investigate/analyze | code / DB / source docs | findings doc, each claim source-tagged (traced/inferred) |
| design | requirements + constraints + system docs | design doc / compared options |
| coding | spec + test + build/lint | code passes test+build+lint |
| migration | before ↔ after state | script + before-after report |
| bugfix/refactor | expected behavior + regression test | patch + no-break evidence |
| documentation | source facts + reader | `.md` per doc-type standard |

hybrid → form of highest-risk type, depth unchanged (§2.1). type absent → nearest by truth-source nature.

## §3 invariant principles

- §3.1 plan first, execute after — never jump in before plan confirmed; small task → plan = 1 restatement, not skipped
- §3.2 restate understanding + name false assumptions before acting → source `.claude/rules/critical-thinking.md` (always-loaded)
- §3.3 decide output location + structure upfront
- §3.4 design verification into the plan, not as a final extra step
- §3.5 acceptance criteria auditable, not subjective — form per §2.2
- §3.6 doer ≠ checker (output-audit): independent agent/human verifies the product on the task's truth source, not the doer's reasoning; small task → self-check on source (re-run build/test, reopen edited file)
- §3.7 attach genome rule per sub-task: self-investigate CLAUDE.md (NEVER/ALWAYS + scope) + `.claude/rules/` + `docs/agent-guide/` router; never lump rules into one separate block; baseline constraints (no commit/push without command) stated once at plan head

pressure resistance (no position change without new info) → source `.claude/rules/critical-thinking.md`.

## §4 seven steps + two cross-cutting branches

linear §4.1→§4.7; output N = input N+1. apply depth per §2.1, form per §2.2. two branches fire at ANY step:

- loop-back: later step exposes earlier defect → return to that step (plan-review gap → §4.3; execution breaks assumption → §4.1/§4.3)
- off-ramp: step exposes a task that should NOT run (wrong direction, owner/closed scope, infeasible, NEVER violation) → STOP, report, propose in-scope alternative — a valid outcome, not a failure

| step | do | done |
|---|---|---|
| §4.1 clarify intent | restate understanding always; ask only on real ambiguity about goal/scope, no open-ended questions | intent clear/confirmed |
| §4.2 approach + storage | propose approach + output location per artifact convention; user picks | location + approach locked |
| §4.3 plan + verification | split into sub-tasks (1 deliverable each) + per-task verification + auditable criteria (§3.5) + genome rule (§3.7) | each sub-task has IO/criteria/rule |
| §4.4 write plan deliverable | write at locked location, register at its discovery point same commit | deliverable exists + referenced |
| §4.5 plan-review (conditional) | independent review of the PLAN — mandatory only for full + costly-if-wrong (migration/wide refactor/owner scope); else self-review against §5 anti-patterns + skip independent review | BLOCKER/MAJOR resolved or user-decided |
| §4.6 refine for use | shape to deliverable-type + reader standard; split oversized units | no unit too long |
| §4.7 todo + gated execution | todo with per-task output-audit gate (§3.6) + user stop-point; execute only on user go | each sub-task passes audit + user approval |

## §5 anti-patterns

- jump to execute before plan locked → §4.1
- promise "100% correct" without verification method → §3.5
- self-verify own output then declare done → output-audit §3.6
- task type raises depth → keep depth at §2.1
- over-clarify when intent already clear → ask only on real ambiguity (§4.1)
- lump genome rules into one block → per sub-task (§3.7)
- full 7 steps on a 1-step small task → scale per §2.1
- continue despite owner/closed scope hit → off-ramp (§4)
