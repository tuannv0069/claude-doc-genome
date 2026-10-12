---
scope: portable
---

<critical>
scope: a work product has reached its audience or passed a milestone the project names as a review point, and its outcome can be measured — decide whether the method that produced it stays, changes or becomes part of the standard.
never: judge the method from the outcome alone; compare the outcome with the expectation written before release, and treat one success as a candidate, never as proof.
note: lesson capture corrects an error inside the current method; this guide questions the method itself, and its output is a record for the project owner to decide on, not a conclusion the assistant closes by itself.
</critical>

# Reviewing a working method after an outcome

The lesson stores and their escalation ladder correct an error inside the method the project already uses: a wrong query form, a skipped step, a link that should not have been made. That loop runs only when something fails and someone notices. A method can be followed exactly and still be the wrong method, and nothing in that loop asks the question. This guide adds the second loop: at a point the project names, compare what the method was expected to produce with what it produced, and decide what to keep and what to change.

The shape of the guide is borrowed rather than invented. The split between the two loops is Argyris's distinction between single-loop and double-loop learning. The four questions in §4 are the after-action review that the US Army runs after every significant event. The requirement in §3 to write the expectation down before the outcome is known follows Baron and Hershey's finding that people rate the same decision better when its outcome was good, even when they agree that they should not. The caution in §5 follows Madsen and Desai's finding that organizations learn less from success than from failure and that what they learn from success fades faster.

## §1 Two loops

The first loop belongs to `lesson-capture.md`: a step of the method failed, the failure is recorded, and on recurrence the record becomes a requirement and then a check. The second loop belongs here: the method was followed, the outcome is known, and the question is whether the method should still be the method. The two loops are triggered differently. The first is triggered by a failure someone noticed; the second is triggered by an event the project has named in advance, whether or not anything failed. A count of lesson records cannot stand in for that event, because a method can be wrong without producing a record: records are written only when someone notices a failure.

<rules section="ALWAYS">
- Route a failure of a step inside the current method to `lesson-capture.md` §2.
- Route a question about whether the method itself is right to this guide.
- Run this review at every review point named under §2, whether or not a lesson was recorded since the last one.
</rules>

<rules section="NEVER">
- Trigger this review from the number of lesson records.
</rules>

<example type="which_loop">
input: a script followed the project's hook method exactly, and the published video lost most viewers in its first thirty seconds
❌ record a lesson that the hook was written wrongly; no step of the method was skipped
✅ take the video to the review under §4, because the question is whether the hook method itself holds
</example>

## §2 Review points

A review point is an event the project names: a work product reaching its audience, an outcome measurement becoming available, or a milestone the owner accepts. An event can be observed at the moment it happens; "when enough work has been done" cannot, and a review that depends on that judgment is a review that does not happen.

<rules section="ALWAYS">
- Name each review point as an observable event, together with the outcome data the review will read and the source that data comes from.
- Record the project's review points in its own entry point or in the document that owns the method, not in this portable guide.
</rules>

<rules section="NEVER">
- Word a review point as a period of time or an amount of work that someone has to judge sufficient.
</rules>

<example type="review_point">
input: a project that publishes videos and reads their retention data
❌ review the method every few videos or whenever results look off
✅ review the method when a video has been public for the number of days the project sets and its retention data has been read into the package
</example>

## §3 Write the expectation before release

Before the work product goes to its audience, write down what the method predicts. Without that record the review compares the outcome with a story written after the outcome is known, and the story will fit the outcome. The expectation names the outcome the method predicts, the measure that will show it, and the point in the work product where the method is applied, so that the review can locate the comparison.

<rules section="ALWAYS">
- Before a work product that a review point will examine goes out, record its expectation in the work product's own area at the location the project's instructions name.
- Keep a correction made before release as a second dated line beside the first expectation, not as an edit of it.
- When no expectation was recorded before release, record the outcome, note that no expectation exists for it, and write the expectation for the next work product.
</rules>

<rules section="NEVER">
- Write or revise an expectation after the outcome it predicts is known.
</rules>

<example type="expectation">
input: a video whose opening follows the project's hook method
❌ after the retention chart is in, write that the hook was expected to hold viewers because it followed the method
✅ before publishing, write that the method predicts at least the project's target share of viewers still watching at thirty seconds, that the platform's retention chart is the measure, and that the hook runs from 0:00 to 0:28
</example>

## §4 The four questions and the record

At the review point, answer four questions in order, each with its evidence: what was expected, from the record under §3; what happened, from the measured outcome and its source; why the two differ, naming whether the evidence points at a step of the method, at the content of this particular work product or at a factor outside both, and saying when the evidence cannot separate them; and what to sustain and what to change. The first work product measured after a method is written is often one the method did not produce, because the work existed before the method did; its outcome is then the project's baseline for the measure and says nothing about the method, and the method's own first test is the next work product. The answer to the fourth question is one of three: keep the method as it is, change it, or mark it as a candidate for promotion under §5. The record lives with the work product it reviews, in the location the project's instructions name.

<rules section="ALWAYS">
- Answer the four questions in order, each with its evidence.
- State, before answering the third question, whether the method under review produced the work product, and when it did not, record the outcome as a baseline for the measure.
- Write the record with the work product it reviews.
- Present the record to the project owner as the basis for a decision on the method.
- When the fourth answer changes a governing requirement, record the change as a `rule` entry in the decision journal and edit the guide or product document that owns the method in the same turn.
</rules>

<rules section="NEVER">
- Attribute a difference to the method when the evidence cannot separate the method from the content or from an outside factor; record the uncertainty instead.
- Attribute an outcome to a method that did not produce the work product being reviewed.
- Close a review with the conclusion that the method worked or failed when the expectation, the measure or the explanation is missing.
</rules>

<example type="third_question">
input: a video held viewers well past the thirty-second mark, and it was also the channel's first video on a topic that was in the news that week
❌ record that the hook method held the viewers
✅ record the retention figure, note that the topic's timing is a second explanation the data cannot rule out, and mark the method as a candidate that needs a second video on an ordinary topic
</example>

## §5 Sustain a method that met its expectation

A method that met its expectation is worth keeping, and a record of it is worth as much as a record of a failure. This ladder is for methods judged by a measured outcome; an owner's approval of a creative piece is recorded at once as a taste note under `creative-work.md` §3. It also needs more caution. One success can come from the content, the timing or the audience rather than from the method, and a method promoted on one success is defended afterwards as though it had been proven. The ladder below mirrors the escalation ladder in `lesson-capture.md` §4, with the same shape on the success side.

| occurrence | action |
|---|---|
| first work product that meets its recorded expectation | mark the method as a candidate in the review record, with the expectation, the measure and the outcome |
| second work product that meets the same expectation under comparable conditions | promote the method into the standard in the guide or product document that owns it, through a `rule` decision entry |
| a later work product that does not meet the expectation | note it in that work product's review record and reconsider the standard under §4 |

<rules section="ALWAYS">
- Cite both review records in the decision entry that promotes a method into the standard.
- State in the standard the conditions under which the method held, so that a later reader can tell whether they still apply.
</rules>

<rules section="NEVER">
- Promote a method into the standard from one outcome, however large.
- Count a work product the method did not produce as an occurrence on the ladder.
</rules>

<example type="promotion">
input: two videos in a row met the expectation the hook method predicted, one on a topic in the news and one on an ordinary topic
❌ write into the standard that the hook method works
✅ write into the standard that the hook method met its thirty-second expectation on two videos of different topicality, cite both review records in the decision entry, and name the conditions that held for both
</example>

## §6 Related procedures

`lesson-capture.md` §2 records a failed step and §4 escalates it; `decision-journal.md` §2 defines the `rule` entry that records a change to the method or a promotion into the standard; `five-why.md` §2 applies when the third question cannot yet explain the difference; `orchestration-policy.md` §7 applies when the owner wants the review read by someone who did not produce the work.
