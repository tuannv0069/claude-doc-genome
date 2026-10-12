---
scope: portable
---

<critical>
scope: any natural-language text produced for a person to read, in whatever language it is written — narration, documentation, chat replies, and the rule or guide prose the assistant itself writes.
never: judge a word, phrase or sentence by whether it matches a list of previously caught examples; the list is evidence of the failure mode, not its boundary, and a language model can coin an unlimited number of instances no fixed list will ever contain.
note: the only test is whether a fluent native writer of that language would actually produce this text, including a term or sentence produced for the very first time in the current output.
</critical>

# Writing text a native speaker would actually produce

Training data rewards phrasing that reads as compressed, punchy or aphoristic — quotable lines, marketing copy, translated content — so a language model's default register drifts toward invented idioms, literal translations from another language, and sentences trimmed past what a native writer of the target language would produce. This is a property of how the text was generated, not a property of any one language, so the same test applies wherever the assistant produces text for a person to read. The same bias that produces a coinage also approves it when the same writer reads it back, so a smooth self-read is not evidence that the test is met.

## §1 The native-speaker test

<rules section="ALWAYS">
- Ask, before producing or accepting any short vivid phrase, idiom, technical-sounding coinage or unusual sentence shape, whether a fluent native writer of that language would actually produce it and what wording is already common for the same idea.
- Apply the same question to a word or sentence produced for the first time in the current output, exactly as to one already recorded as a past failure.
- Read a finished piece of text as its reader will actually encounter it — aloud for narration, exactly as it will be sent for a reply — before treating it as finished.
- Check a claim about how native speakers write something against an actual corpus of native writing on the same topic when one is available, rather than trusting a self-read alone.
- Judge an expressive phrase in a script or other creative text by this test, and leave the question of literal precision to the claim boundary in `critical-thinking.md` §2.
- Apply the test against native examples of the same format (a title against real titles, a hook against real hooks, narration against real narration), and ask whether the text pulls its reader as well as whether it sounds native (`.agent-workspace/guide/general/creative-work.md` §4 and §6).
</rules>

<rules section="NEVER">
- Treat the absence of a match against previously recorded examples as evidence that a new word, phrase or sentence passes the test.
- Approve a sentence structure because it reads smoothly to the writer who produced it.
</rules>

<example type="novel_coinage">
input: summarizing, in a reply to the project owner, a rule that bans reordering a chain of dependent argument points
❌ coin a new technical-sounding term for the property and use it as though it were established vocabulary
✅ quote the rule's own wording, or spell out the property as a full sentence, instead of naming it
</example>

## §2 Recognizing a structurally compressed sentence

A sentence is compressed when it has been shortened to hit some metric — fewer words or syllables, a punchier rhythm, a rule of "short is stronger" — at the cost of its subject, a connective word or a natural clause boundary, to the point that a reader must stop and re-parse it, or that it reads like a note rather than something a person would actually say.

<rules section="ALWAYS">
- Rewrite a sentence that fails this test as a full clause with its subject, verb and connective restored, rather than trimming it further.
</rules>

<example type="compressed_sentence">
input: stating a stadium capacity requirement in text meant to be read aloud
❌ "40,000-seat stadium, FIFA standard, this country has one."
✅ "FIFA requires a group-stage stadium to seat at least 40,000, and this country has exactly one ground that meets it."
</example>

## §3 Project-specific instantiation

A project states the native-speaker question in its own working language, names its own corpus of native writing when it keeps one, and records its own catalogue of caught instances as evidence. This rule states the general test and the general failure mode; a project's own instructions state the concrete wording, the corpus location and the evidence trail for its material. The genome does not invent those project-specific values.

<rules section="ALWAYS">
- Read the project's own style or entry-point instructions for the concrete wording of this test and the location of any corpus it keeps, and apply those in addition to this rule rather than in place of it.
</rules>
