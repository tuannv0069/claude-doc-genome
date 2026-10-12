---
scope: portable
---

<critical>
scope: writing, changing or reviewing source code or an executable script, in any language and for any purpose, including a tool, a test and product code.
never: report code as finished without a check that was run and its result, or leave the author of a change as its only reviewer when the change is more than a small isolated edit.
note: the project's declared standard decides matters of style (§2); look for an existing implementation before writing a new one (§3); the review asks whether the change makes the code clearly better, not whether it is perfect (§6).
</critical>

# Writing code

An instruction to write clean code changes nothing, because it names no action and no check. Each requirement in this guide is therefore one of three things: a check that can be run, a failure that an assistant writing code is known to be prone to, or a question that a reviewer answers. The guide stays short on purpose: an assistant follows fewer of its instructions as their number grows, so a requirement that a machine can check belongs in a check and not in this text.

## §1 When this applies

This guide covers every piece of code the assistant writes or changes: product code, a tool, a test, a build or automation script. Where a tool is placed and how a tool folder is organized is the subject of `tooling.md`. What a verification gate must compare is the subject of `verification-gate-design.md`. A script meant to be read or heard, such as narration, is creative text and is outside this guide.

## §2 The project's standard decides style

A project names, in the `stack` section of its entry point, the languages its code is written in, the style standard it follows for each, and the commands that format, lint and test the code. Those are the authority on style. Where the standard is silent, the code already in the file is the next authority, because consistency inside a file matters more to its next reader than any one preference.

<rules section="ALWAYS">
- Read the style standard and the format, lint and test commands in the project's entry point before writing code in that language.
- Follow the conventions already used in the file being changed where the project's standard does not decide the matter.
- Run the project's formatter and linter on the changed files when the project has them, and fix what they report.
- Check that a formatter, linter or test runner is installed before relying on it.
</rules>

<rules section="NEVER">
- Reformat or rename code outside the requested change to match a personal preference.
- Add a formatter, a linter, a test runner or any other dependency that the project has not declared without the user's decision.
</rules>

## §3 Reuse before writing

An assistant writes a new copy of logic more readily than it looks for the one that exists, and copies of the same logic drift apart: one is corrected and the other is not. The opposite error is as costly. A shared function that gains a parameter for each caller that needs something slightly different ends up serving none of them well.

<rules section="ALWAYS">
- Search the codebase, and the tool index when the code is a tool, for an existing implementation before writing a function.
- When a second place needs the same logic under the same contract, move that logic to a shared location in the same change and make both places call it.
- When a caller needs different behavior from a shared function, give that caller its own implementation and state the difference in a comment.
</rules>

<rules section="NEVER">
- Copy a block of code and edit the copy.
- Add a switch parameter to a shared function so that one caller can change what the function does.
</rules>

<example type="second_caller">
input: a second script needs to split the rows of a Markdown table, and another script already contains a line that does it
❌ copy the line into the second script; the two copies now change separately
✅ move the row-splitting function to the shared library of the tool group and call it from both scripts
</example>

## §4 Keep the change as small as the requirement

Complexity that the requirement did not ask for is the most common way a working change makes a codebase worse. Code is too complex when its next reader cannot understand it quickly.

<rules section="ALWAYS">
- Implement what the requirement needs now.
- Give each function one job and each file one responsibility that can be changed without understanding the rest.
- Split a file when it has gained a second responsibility; a block of imports or declarations in the middle of a file, and a change that needs the whole file read in order to edit one part, are the observable signs.
- Name a thing with full words that say what it is or does.
- Write a comment where the reason for the code is not visible in the code.
- Make an error message say what failed and what the reader can do about it.
</rules>

<rules section="NEVER">
- Add an abstraction layer, a configuration option or handling for a case that the requirement does not contain.
- Put reading input, deciding and printing output in one function.
- Split a file, or refuse to split one, on the strength of a line count alone.
- Write a comment that repeats what the code already says.
</rules>

<example type="unrequested_flexibility">
input: the requirement is a script that renames the files in one named folder
❌ add a plugin interface for other renaming rules and a configuration file for the folder
✅ write the rename for that folder, and add the second rule when a requirement for it exists
</example>

## §5 Verify with a check that runs

Code that looks finished and code that works are told apart only by something that returns pass or fail: a test, a build, a linter, or a comparison of output with an expected result.

<rules section="ALWAYS">
- Decide, before writing the code, which check will show that it works.
- Write or update the test in the same change as the behavior it covers.
- Run the check and report the command and its result.
- Before a change that is meant to keep behavior the same, record the output and exit status of the code on real input, and compare them after the change.
</rules>

<rules section="NEVER">
- Change a test to make it pass without first establishing that the test was wrong.
- Treat tests that were edited in the same change as the only evidence that a restructuring kept the behavior.
</rules>

## §6 Review by a reader who did not write it

The author of a change reads their intention into it. A reviewer looks at a change in this order: its design, whether it does what was asked, its complexity, its tests, its names, its comments, its style, and its documentation. The reviewer approves a change that clearly leaves the code better than it was; there is no perfect code to wait for. A reviewer who is asked for gaps reports some even when the work is sound, and acting on all of them adds the unrequested complexity that §4 forbids.

<rules section="ALWAYS">
- For a change that is more than a small isolated edit, have an independent reader under `orchestration-policy.md` §7 review the diff against the requirement in the order given above.
- Tell the reviewer to report as findings only the gaps that affect correctness or a stated requirement, and to label everything else as optional.
- Fix the findings, and decide each optional remark on whether it serves the requirement.
- Settle a disagreement on style by the project's standard, and a disagreement on behavior by evidence from running the code.
</rules>

<rules section="NEVER">
- Act on every optional remark of a review.
- Report a preference as a finding where the project's standard does not decide the matter.
</rules>
