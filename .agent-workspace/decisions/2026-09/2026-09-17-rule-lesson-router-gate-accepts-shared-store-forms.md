---
class: rule
subject: .agent-workspace/tooling/verify_lesson_router.py
anchor: .agent-workspace/guide/general/lesson-capture.md
---

decided: The lesson-router gate accepts both store forms that the shared guidance documents: a `<critical>` block with `scope:` and `phase:`, or frontmatter `work_scope:` and `phase:`. Router file cells and `checks` pointers may be bare or backticked. The Claude live guide names the frontmatter form as accepted.

because: Initializing the Claude adapter into a project whose `.agent-workspace/` was deployed by the Codex adapter (tuan-c-story, 17/09/2026) failed only in this gate: its eleven stores and router follow the Codex generation of `lesson-capture.md` §3, which documents frontmatter `work_scope`/`phase` as the primary form, and the Codex checker already accepts both forms. The README commits both adapters to one shared workspace, so a Claude gate that rejects a documented shared form is a defect of the gate, not of the data (`verification-gate-design.md` §3). Widening the parser keeps the invariant (one protected action, one legal phase per store, acyclic checks) and avoids rewriting project-owned stores to satisfy a tool.

rejected: Rewriting the deployed project's stores into the `<critical>` form (churn in shared files, and every later store written under the live guide would fail again); leaving the gate failing in the reused-workspace path; making the frontmatter form the only accepted form (would break existing Claude-deployed stores).
