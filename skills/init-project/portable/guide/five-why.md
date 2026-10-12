---
scope: portable
---

<critical>
scope: root cause analysis of a defect in code, a document, a configuration or a rule, and of the working method that let it through.
never: stop at the symptom, or explain a cause as the assistant having misunderstood.
note: two questions, G1 about the artifact and G2 about prevention; each answer must be falsifiable; the number of whys is decided by the evidence, not by a template.
</critical>

# Root cause analysis

Use this guide to investigate an artifact defect and determine whether the working method or governing instructions also need to change.

## §1 When this applies

An isolated correction whose cause and remedy are already established does not need a ceremonial chain of questions. When the defect lies entirely in an external system, investigate that system's cause and the appropriate response.

<rules section="ALWAYS">
- Apply root cause analysis when the user asks for it, when a defect recurs, or when an apparent local fix leaves the cause uncertain.
- Treat an owner's taste reaction to creative text as a revision under `creative-work.md` §3, not as a defect needing root cause analysis.
</rules>

<rules section="NEVER">
- Invent a genome-rule cause merely to complete a second part of the analysis.
</rules>

## §2 Two questions to investigate

The first question, G1, concerns the artifact: what causes the observed defect, and what change would remove that cause? The second question, G2, concerns prevention: did an instruction, missing check, or working method contribute to the defect? Prevention and detection protect different parts of the process.

<rules section="ALWAYS">
- For G1, establish the triggering conditions, trace the mechanism, and identify the location that needs to change.
- Investigate G2 when the defect arose in an AI-produced artifact or in the genome itself, and cite the instruction and stable section when one exists.
- When no instruction covers the failure, describe the gap and identify an appropriate owner for a proposed remedy.
- When a proposed workflow change affects how an artifact is produced, also examine how verification would detect the same mistake.
- Apply changes within the authorization already given for the task, and explain a remedy that would change a separate policy before requesting the additional decision.
</rules>

<rules section="NEVER">
- Duplicate the analysis when G1 already resolves G2.
</rules>

## §3 When to stop

An unresolved hypothesis should remain unresolved rather than becoming a conclusion because the analysis has reached a planned length.

<rules section="ALWAYS">
- Continue asking why while the next answer could change the diagnosis or remedy, and stop when further questions add no useful causal distinction.
- Investigate independent causes as separate branches.
</rules>

<rules section="NEVER">
- Force a fixed number of questions.
</rules>

## §4 The analysis record

Use the task's reporting requirements for the resulting artifact. These information needs do not require fixed headings, tables, separators, field labels, or a particular output language.

<rules section="ALWAYS">
- Preserve the observed symptom, the evidence supporting the causal explanation, the proposed correction, and the way the correction will be checked.
- Record any prevention change and the authority needed to apply it.
</rules>

### §4.1 (retired)

## §5 Falsifiable explanations

A source location, stable rule section, observed result, or reproducible condition can provide the evidence that could show an explanation to be wrong. A proposed detector alone does not repair the method that creates the defect.

<rules section="ALWAYS">
- Connect each causal explanation to evidence that could show it to be wrong.
- When a writer invents schema names, examine both the writer's source lookup and the comparison between the completed artifact and the schema.
</rules>

<rules section="NEVER">
- Accept "the assistant misunderstood the task" as a cause; it identifies no mechanism that can be checked.
</rules>

<example type="falsifiable_cause">
input: an agent wrote a field name that does not exist in the schema
❌ the agent misunderstood the schema
✅ the agent inferred the field name from a neighboring example instead of opening the defining schema; the investigation can test whether the schema lookup would prevent the demonstrated failure
</example>

## §6 Related procedures

Use `.claude/rules/critical-thinking.md` to check assumptions before acting. Use `fix-impact-analysis.md` §3 before applying the remedy, because a correct diagnosis does not establish that a change is safe for its dependents. Record a repeatable method failure under `lesson-capture.md` §2.
