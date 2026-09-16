---
class: rule
subject: skills/init-project/templates/CLAUDE.md.tpl
anchor: docs/genome/so-sanh-dau-ra-claude.md
---

decided: State the existing task-start lookup as an explicit file-reading action that also applies to conversational questions and writing requests. Apply the same instruction to the source repository's entry point.

because: In six fresh writing sessions, the rewritten template produced no tool calls, while the original template caused both router files to be read in all six sessions. Two fresh conversation probes with the explicit instruction read both files. The cause inside the model is not observable, but this controlled wording change supports making the operation and its scope explicit. Further writing probes check the same obligation. The change restores an existing workflow requirement without prescribing output style.

rejected: Treating successful static checks as proof that the rewritten workflow was followed, or restoring compressed imperative notation throughout the genome.
