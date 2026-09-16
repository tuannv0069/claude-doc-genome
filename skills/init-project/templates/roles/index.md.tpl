---
scope: project
---

# Role index

This router selects the working perspectives for a task. The matching procedure is defined in `.agent-workspace/guide/general/role-selection.md` §2. Read the primary role and the checking roles' §6 after selecting a row.

## §1 Genome roles

| work type | primary role | checking roles |
|---|---|---|
| Interpreting software requirements or determining the scope of a business operation | business-analyst | project-manager |
| Choosing a software architecture or technical approach across components | tech-lead | security |
| Describing or changing software behavior, conditions or processing branches | developer | business-analyst, qa |
| Describing or changing software user needs, business rules or requirements | business-analyst | project-manager |
| Reading source code or technical specifications to explain software behavior | developer | qa |
| Writing or fixing source code, executable tooling or automation scripts | developer | qa |
| Reviewing or accepting software behavior or executable tooling | qa | business-analyst |
| Building a machine verification gate | qa | developer |
| Investigating a software defect or its root cause | developer | qa |
| Planning work, choosing its order or managing scope | project-manager | |
| Planning software work with technical dependencies | project-manager | tech-lead |
| Working with authentication, authorization, personal data or secrets | security | tech-lead |
| Translating software requirements or technical communication for a foreign customer | comtor | business-analyst |

## §1a Project roles

Add domain-specific roles here according to `.agent-workspace/guide/general/role-selection.md` §5. A matching project row takes precedence over a genome row for the same work type.

| work type | primary role | checking roles |
|---|---|---|

## §2 Routing contract

The table schema is defined in `.agent-workspace/guide/general/role-selection.md` §6 and checked by `.agent-workspace/tooling/verify_role_files.py`. Resolve a conflict between role guidance and project requirements according to the guide's §7.
