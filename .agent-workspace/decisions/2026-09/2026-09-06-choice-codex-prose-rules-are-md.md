---
class: choice
subject: .codex/rules
anchor: codex-manual.md:28973,29097,15257 · 202ee4e
---
- decided: the Codex prose rule tier is `.codex/rules/*.md`
- because: the same directory already holds `*.rules`, which the platform loads into its Starlark command-approval engine for a trusted project; the engine selects by extension, so markdown beside it is inert
- rejected: `.codex/rules/*.rules` as requested — prose in that extension is fed to the policy engine, and the breakage would land in the user's other work rather than in the genome
