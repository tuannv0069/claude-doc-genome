---
scope: portable
---

<critical>
scope: work whose product is text or images meant to engage a reader or viewer — scripts, narration, titles, thumbnail text, hooks, posts, essays — in any project whose main work is creative.
never: turn an owner's reaction to one passage into a general ban or an automated check, or judge creative text only by the absence of faults.
note: facts in creative text keep the evidence standard of `.claude/rules/critical-thinking.md` §2; everything else is judged by whether it works for its reader, and the owner's taste plus real examples of the format are the evidence for that.
</critical>

# Creative work

The rest of this documentation system was shaped by software work, where correctness can be tested and the costliest outcome is a defect that reaches users. Creative work has a different costliest outcome: a piece that is correct, sourced and grammatical and still dull, so nobody finishes it. The habits that protect software (record every failure as a rule, check against a list, add ceremony before acting) push creative text towards caution and flatness when they are applied unchanged. This guide states how the same system works when the product has to engage someone.

## §1 When this applies

Read this guide before drafting, revising or reviewing a creative piece, and before recording the owner's reaction to one. A project enables it by naming its creative work in its entry point; the project's own style instructions (its voice, its audience, its references) apply alongside this guide.

A creative piece has two layers. Its claims (numbers, dates, names, quotations, events, causes) keep the evidence standard of `.claude/rules/critical-thinking.md` §2 without exception. Its telling (wording, rhythm, images, hyperbole, jokes, the narrator's opinions, the order in which things are revealed) is judged by whether it works for the intended reader.

## §2 Draft first, then judge

A reader's reaction to a real draft tells more than any plan about a draft. Structural planning still helps a long piece, but it does not have to be finished before any sentence is written.

<rules section="ALWAYS">
- Offer a short draft, or two or three contrasting options, early enough that the owner can react to real text rather than to a description of it.
- Label an early draft as a sketch, and run fact checks and reviews once a draft the owner wants to keep exists.
- When the owner chooses between options, carry on with the chosen one; the choice needs no justification record.
</rules>

<rules section="NEVER">
- Withhold every sentence until all planning stages are approved when a short sketch would settle a question of voice or angle faster.
</rules>

## §3 Taste notes instead of bans

When the owner rejects or changes a piece of creative text, the reaction is about that passage in that format for that audience. Recorded as a general "do not", it spreads to places it was never about; a store of such records slowly removes every device a writer needs. A taste note keeps the reaction at the size it was.

A taste note records: the passage and its format (title, hook, narration, thumbnail text), the version the owner rejected, the version the owner preferred or approved, and the reason in the owner's words when given. It is kept in the project's taste store (§5), not in a lesson store.

<rules section="ALWAYS">
- Fix the passage the owner reacted to, and the passages built the same way, before recording anything.
- Record the reaction as a taste note with the weaker and the preferred version side by side.
- Record an owner's approval or praise of a piece as a taste note too, at once, so the store holds what works as well as what does not.
- Before generalising a taste note beyond its passage, count the device in native examples of the same format; if native writers use it, the note stays local.
</rules>

<rules section="NEVER">
- Record a taste reaction as a lesson with a ❌/✅ ban, or escalate it into a requirement or an automated check under `lesson-capture.md` §4.
- Treat a device the owner disliked in one place (a metaphor, a hyperbole, a rhetorical question, a list of three) as forbidden elsewhere.
</rules>

<example type="taste_note">
input: the owner says a title reads dry and changes it
❌ record "never write titles as neutral questions" in the lesson store; the next ten titles avoid every question
✅ record the rejected title, the approved title and the owner's reason in the taste store, and look at how real creators in that format phrase such titles before writing the next set
</example>

## §4 Learn from real examples of the format

A creative format is learned from pieces that work in it, not from rules about it. A title is written like the titles people click in that niche, a thumbnail like the thumbnails that stand out there, narration like the narrators the audience already follows. The native-speaker test in `.claude/rules/natural-language-writing.md` §1 is applied against that format's native examples, not against the register of another format.

<rules section="ALWAYS">
- Before writing a new piece in a format, look at real examples of that format in the same niche and name what makes the strong ones pull the reader.
- Keep annotated examples (the piece, where it came from, what makes it work) in the project's reference store (§5).
- Measure a craft element from a reference (a proportion, a length, a structure) instead of guessing it, when the owner points to that reference as the model.
</rules>

## §5 Where taste and references live

Taste notes and annotated references are project knowledge about what works for this audience, so they belong in the project's work-product area under `.claude/rules/doc-organization.md` §11, in a location the project names in its entry point or style instructions. They are not lessons (`lesson-capture.md` §1), not wiki claims and not rules.

A project that has not yet named a location keeps them next to its style instructions until it does.

## §6 Review for appeal as well as for faults

A fault review finds what is wrong; it cannot say whether the piece works. Every creative piece that goes to the owner also gets an appeal review, done by a reader who did not write it and who reads as the intended audience.

An appeal review answers, part by part: does the reader want the next sentence here (holds, sags, loses), what does this part make the reader feel and is that the feeling it should give, which moments are strongest and must be kept, where does it sag and what would lift it, what did it leave unused, and would the intended reader finish it. Its proposals change the telling only; a stronger line never adds a number, name or event the draft does not already carry. A finding in an appeal review is a judgment and is labelled as one.

<rules section="ALWAYS">
- Run an appeal review on a creative piece before it goes to the owner, in addition to the fault reviews the project uses.
- Give the appeal reviewer the audience, the project's references for the format and any record of real audience reactions.
- Treat "the intended reader would not finish this part" as a reason to revise before delivery, like a failed fault check.
</rules>

<rules section="NEVER">
- Present a creative piece as ready because it passed fact and wording checks alone.
</rules>

## §7 Creative roles

A role for creative work (writer, editor, creative director) keeps the role format of `role-selection.md`, and adds the reader to its perspective: its decision criteria include whether the piece works for the audience as judged by §6, and its completion criteria include that an appeal review ran. Measurements such as sentence length or question ratio are diagnostics in such a role, not conditions for completion.

## §8 Proportionate procedure

Procedure should cost less than the thing it protects. For creative turns, the following apply instead of the heavier defaults:

- The lesson and role lookups required at the start of work are stated in one line, or omitted when nothing matches.
- Choosing among drafts or options, and revising for taste, needs no decision-journal entry (`decision-journal.md`) and no root-cause analysis (`five-why.md`, `fix-impact-analysis.md`); those remain for facts, tooling and rules.
- Editing several files of one creative package in a single revision is one change, not a multi-file implementation needing a separate plan.

<rules section="NEVER">
- Run a measurement, a checklist or a record-keeping step before a draft exists when it cannot change what the draft should be.
</rules>

## §9 Review accumulated constraints

Constraints on creative text accumulate one reaction at a time. From time to time, and whenever the owner says the writing has become stiff or dry, read the project's style instructions, taste store and lesson stores together, and test each restriction on wording against native examples of the format. A restriction that native writers routinely break is narrowed or removed under `.claude/rules/doc-organization.md` §12.
