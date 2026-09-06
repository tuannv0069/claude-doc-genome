---
scope: portable
---

<critical>
scope: a repeatable procedure is being run with no skill and no subagent owning it — decide whether to package it, and propose that to the human.
core: detect the procedure where it is already WRITTEN, not by counting runs | agent proposes, human approves, the approved candidate is authored against the standards | one candidate per task, raised at the end.
forbidden: create a skill or agent file without approval | make run-counting the primary detector | package a procedure whose trigger, steps or output is not already written down.
note: §ID append-only (portable) — never renumber; retired sections keep their number.
</critical>

# Capability packaging

What a packaged artifact must look like is already settled: `.claude/rules/skill-md-standards.md`
governs a skill file, `subagent-standards.md` governs an agent file. Both take effect only once a
human has named the thing to build. This file supplies the missing half — **when the agent itself
raises the question.**

## §1 What is a capability

Three properties, all of them written down somewhere before the question is asked:

1. a fixed trigger — the condition the work is reached by
2. an ordered step sequence
3. a defined output the procedure **creates or changes** — a file, a set of cells, a diagram, a
   report shape. An answer the reader forms in their own head is not an output

Miss one and there is nothing to package. A rule with no steps is a rule; steps with no defined
output are a habit; steps with no trigger are a one-off.

Property 3 is the one that decides most cases, and it is the one read carelessly. A guide can be
long, numbered and precise and still produce nothing: a map, a glossary, an evidence policy and a
routing table all answer a question the reader then acts on. Packaging one of those wraps a lookup
in a workflow and makes it slower to reach.

## §2 Detector A — a guide that already states a procedure

Runs at the moment the router already sends you into a guide. Four checks, each answered by reading:

<rules section="ALWAYS">
- the guide states its own trigger, an ordered step sequence, and a named output (§1) → hold
- no file in `.claude/skills/` and none in `.claude/agents/` owns that flow → candidate
- name the candidate by its guide file — two agents then raise the same one, not two
- carry it to the end of the task and raise it per §5
</rules>

<rules section="NEVER">
- treat a guide that only states criteria as a candidate — criteria are read, not executed
- read a numbered list as an ordered step sequence — a numbered list of conditions is still criteria
- re-raise a candidate already recorded as declined (§6)
- interrupt the task in hand to package anything
</rules>

| ❌ | ✅ | why |
|---|---|---|
| a map or glossary with 15 numbered rules → candidate | not a candidate | the reader leaves with an answer, not with a changed artifact |
| a policy stating which evidence a claim needs → candidate | not a candidate | it is a criterion applied at one point (§4, row 3) |
| a guide whose steps end in named cells written into a named workbook | candidate | the output exists on disk after the run and can be checked |

This is `doc-organization.md` §8.3 branch 1 read from the other side: branch 1 asks the question
when content is being written; this section asks it when the work is being done.

### §2.1 What Detector A does not require

No counting, no per-run bookkeeping, no memory of earlier sessions. Reading the guide the task
already opened is the whole cost. An agent that starts logging runs "to be sure" has replaced a
free check with an expensive one.

## §3 Detector B — the sweep, for procedures never written down

Detector A cannot see a procedure that is re-derived from scratch each time. That one is found by
sweeping — **on request, never inside an ordinary task.**

Sources, strongest signal first:

1. `.agent-workspace/tasks/` — directory names, grouped by kind of work
2. `.agent-workspace/lessons/index.md` §1 — every row is a work type this project has already declared repeatable
3. `git log --format=%s` — commit scopes recurring with the same shape

Threshold: a kind of work appearing **3 or more times** with no skill and no agent owning it is a
candidate. Three is the step the lesson ladder already uses (`lesson-capture.md` §4) — once is an
event, twice is a rule, three times is worth a mechanism.

<rules section="NEVER">
- group workspace slugs by subject — group by kind of work
- run the sweep as part of an ordinary task — it reads dozens of names to answer a question nobody asked
</rules>

| ❌ | ✅ | why |
|---|---|---|
| `shiteki-rd031` and `fix-comment-kian-orange-9c3b` counted as two kinds of work | both counted as one — answering a review comment | the slug names the subject and the round; the work is the same |
| "the sweep found 9 candidates" | the sweep names the top one and stops | a list of nine is a backlog nobody answers |

## §4 Which form — skill, subagent, or neither

| the candidate | form |
|---|---|
| ordered steps, one context, defined output | skill |
| a pass that must run on a context of its own — review, audit, verification of another phase's output | subagent |
| judgement applied at a single point, no step order | leave it a guide `§ID` |
| steps that differ every run except in name | neither — it is not a procedure |

A candidate needing both — a flow that dispatches an isolated pass — is still one proposal; the
split between skill and subagent is settled when the artifact is authored, not here.

<rules section="NEVER">
- package a procedure as a subagent because it is long — length is not isolation
- restate what a skill or agent file must contain — `skill-md-standards.md` and `subagent-standards.md` own that
</rules>

## §5 The proposal — agent raises, human decides

<rules section="ALWAYS">
- raise it at the END of the task it was noticed in — the work in hand is what the user asked for
- state four things: the candidate's name, which detector found it, the form proposed (§4), what it would replace
- keep it to five lines — the design belongs to the build, not to the proposal
- one candidate per task
- approved → author the artifact against `skill-md-standards.md` (skill) or `subagent-standards.md` (agent)
</rules>

<rules section="NEVER">
- create a skill or an agent file because the candidate looked obvious — approval is the human's, and it is the gate
- raise a candidate the same session declined
</rules>

<example type="proposal">
input: a guide with a fixed trigger, 7 ordered sections and a tool that writes defined cells, owned by no skill
❌ write the skill file, then report it — the human never chose to spend the turn
✅ "Candidate: `<guide>.md` — Detector A (trigger + ordered steps + defined output, no owner). Proposed form: skill. It would replace the manual read-and-follow of that guide each run. Build it?"
</example>

## §6 A declined candidate is recorded

Declined once → record it in the store `lessons/index.md` §1 routes this work type
to, in the shape `lesson-capture.md` §3 defines: the heading is the imperative (`do not propose
packaging X`), the `✅` line carries the reason. Without the record the next session spends the same
turn on the same candidate and gets the same answer.

## §7 relation

- `doc-organization.md` §8.3 — the placement tree; branch 1 is §2 seen from the writing side
- `lesson-capture.md` §4 — the escalation ladder §3's threshold is taken from
- `skill-md-standards.md` · `subagent-standards.md` — what the packaged artifact must look like

<critical_recap>
1. detect where the procedure is written; counting runs is Detector B only, and only on request
2. four readable checks: trigger, ordered steps, defined output, no current owner
3. sweep groups by kind of work, threshold 3, names one candidate
4. propose at task end, five lines, one candidate; the human approves
5. declined once → recorded, never re-raised
</critical_recap>
