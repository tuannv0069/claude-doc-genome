---
scope: portable
---

# Root cause analysis

Use this guide to investigate an artifact defect and determine whether the working method or governing instructions also need to change.

## §1 When this applies

Apply root cause analysis when the user asks for it, when a defect recurs, or when an apparent local fix leaves the cause uncertain. An isolated correction whose cause and remedy are already established does not need a ceremonial chain of questions.

When the defect lies entirely in an external system, investigate that system's cause and the appropriate response. Do not invent a genome-rule cause merely to complete a second part of the analysis.

## §2 Two questions to investigate

The first question, G1, concerns the artifact: what causes the observed defect, and what change would remove that cause? Establish the triggering conditions, trace the mechanism, and identify the location that needs to change.

The second question, G2, concerns prevention: did an instruction, missing check, or working method contribute to the defect? Investigate it when the defect arose in an AI-produced artifact or in the genome itself. Cite the instruction and stable section when one exists. When no instruction covers the failure, describe the gap and identify an appropriate owner for a proposed remedy.

If G1 already resolves G2, do not duplicate the analysis. If a proposed workflow change affects how an artifact is produced, also examine how verification would detect the same mistake. Prevention and detection protect different parts of the process.

Apply changes within the authorization already given for the task. If a remedy would change a separate policy or exceed that authorization, explain the proposed change before requesting the additional decision.

## §3 When to stop

Continue asking why while the next answer could change the diagnosis or remedy. Stop when further questions add no useful causal distinction. If the investigation branches into independent causes, investigate those branches separately.

Do not force a fixed number of questions. An unresolved hypothesis should remain unresolved rather than becoming a conclusion because the analysis has reached a planned length.

## §4 The analysis record

Preserve the observed symptom, the evidence supporting the causal explanation, the proposed correction, and the way the correction will be checked. Record any prevention change and the authority needed to apply it.

Use the task's reporting requirements for the resulting artifact. These information needs do not require fixed headings, tables, separators, field labels, or a particular output language.

### §4.1 (retired)

## §5 Falsifiable explanations

Each causal explanation must connect to evidence that could show it to be wrong. A source location, stable rule section, observed result, or reproducible condition can provide that evidence.

“AI misunderstood the task” does not identify a mechanism that can be checked. A stronger explanation might establish that an agent inferred a field name from a neighboring example instead of opening the defining schema. The investigation can then test whether the schema lookup would prevent the demonstrated failure.

A proposed detector alone does not repair the method that creates the defect. If a writer invents schema names, examine both the writer's source lookup and the comparison between the completed artifact and the schema.

## §6 Related procedures

Use `.claude/rules/critical-thinking.md` to check assumptions before acting. Use `fix-impact-analysis.md` §3 before applying the remedy, because a correct diagnosis does not establish that a change is safe for its dependents. Record a repeatable method failure under `lesson-capture.md` §2.
