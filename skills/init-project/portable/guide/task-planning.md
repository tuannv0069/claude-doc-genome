---
scope: portable
---

<critical>
scope: plan + verify before executing any artifact-changing task. scale rigor to size, pick form by task type.
core: plan-before-execute | size the rigor | design verification into plan | independent output-audit | genome-rule per sub-task | loop-back + off-ramp | sub-task contract (§6) + plan self-review (§7)
defer: a skill owns the planning workflow → its flow governs §6–§8; §2/§3/§4 still apply (§1)
out: pure question / explanation with no file change → answer direct, skip this
</critical>

## §1 when this applies

apply-test: does the answer change a file / produce a deliverable? no → out of scope, answer direct. yes → task, enter at scale §2.1 (even when phrased as a question).

precedence: an installed skill that owns the planning workflow governs the craft — run its flow, and §6–§8 stand down as the fallback for when no such skill is present. The governance layer never stands down: scale (§2.1), principles (§3), off-ramp and loop-back (§4) apply either way, because a skill flow states neither when to skip the ceremony nor when to refuse the task.

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
- §3.7 attach genome rule per sub-task: self-investigate CLAUDE.md (NEVER/ALWAYS + scope) + `.claude/rules/` + `.agent-workspace/guide/` router; never lump rules into one separate block; baseline constraints (no commit/push without command) stated once at plan head

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
- hand-roll a plan while an installed skill owns the workflow → §1 precedence
- step states a duty without its content → §6.3
- sub-task names a type or field no sub-task defines → §6.2 consumes/produces
- plan self-review counted as the result's output-audit → §7 closing line

## §6 sub-task contract

Fills §4.3. A sub-task is what one executor receives; this section is what must be inside it.

### §6.1 right-sizing

- a sub-task = the smallest unit that carries its own verification AND is worth an independent gate
- fold setup, config, scaffolding, doc updates into the sub-task whose deliverable needs them — never split them out
- split only where a checker could reject one sub-task while approving its neighbour
- each sub-task ends in an independently verifiable deliverable

<example type="right_sizing">
input: a change needing a config flag, the logic, and a doc line
❌ 3 sub-tasks — the flag and the doc line cannot be rejected on their own
✅ 1 sub-task delivering all three, verified as one behaviour
</example>

### §6.2 required fields

The executor sees ONLY its own sub-task — a fresh subagent, or the same agent after compaction. Whatever it cannot see, it invents.

| field | content |
|---|---|
| targets | exact paths + create/modify, never "the relevant files" |
| consumes | what earlier sub-tasks produce that this one uses — exact names, signatures, values, copied verbatim |
| produces | what later sub-tasks will rely on — same verbatim rule |
| criteria | auditable acceptance per §3.5, in the form of §2.2 |
| rule | the genome rule attached to this sub-task per §3.7 |
| effort | per sub-task, not one level for the batch |

### §6.3 no placeholder

A plan step must carry the content its executor needs. These are plan failures, not shorthand:

- `TBD` / `TODO` / "fill in later"
- "handle errors appropriately" / "add validation" / "cover edge cases" — names a duty, states no content
- "same as sub-task N" — the executor may read out of order, and often reads only one
- a step that says WHAT without WHICH: which file, which value, which command
- a name, type, or field referenced by no sub-task that defines it

<example type="placeholder">
input: a step covering an error path
❌ "add appropriate error handling to the parser"
✅ "parser hits an unclosed quote → raise `ParseError` with the line number; test asserts the line number is in the message"
</example>

## §7 plan self-review

Run before execution, against the task's truth source (§2.2). Fix inline; no second round.

1. coverage — walk each requirement of the source; point at the sub-task that delivers it. None → add a sub-task, not a note.
2. placeholder — scan for §6.3.
3. naming — one thing, one name, across every sub-task. Same field called two names is a defect already shipped into the plan.
4. order — every `consumes` is produced by an earlier sub-task.

This reviews the PLAN. It does not replace the output-audit of the RESULT (§3.6) — same agent, different artifact, and self-review of a result is what §3.6 forbids.

## §8 design exploration

Applies when §2.2 type = design, or when the source does not already determine the approach. Does NOT raise depth — a small task still exits inline per §2.1.

<rules section="ALWAYS">
- read the existing artifact before proposing a change to it — follow what is there
- ask one question per message; prefer multiple-choice; only on real ambiguity about goal / constraint / success criteria (§4.1)
- produce 2-3 viable approaches with trade-offs, recommendation first with its reason → posture source `critical-thinking.md`
- cut from every approach what the stated goal does not need
- present in sections scaled to complexity; confirm per section, not once at the end
- approach settled → it becomes the input of §4.3, not a separate deliverable unless the user asked for one
</rules>

<example type="approaches">
input: user asks where to store a new kind of state
❌ propose one storage location and start writing
✅ 2-3 locations with what each costs, lead with a recommendation and why; user picks
</example>
