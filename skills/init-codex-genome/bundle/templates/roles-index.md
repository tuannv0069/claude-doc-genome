---
scope: project
---

# Codex role router

## §1 Select a perspective

Read both tables before selecting. Apply `.agent-workspace/guide/general/role-selection.md` §1: a project match takes precedence, and a more specific action takes precedence within a table. Read the primary role in full and §6 of its checking roles. Do not turn a role match into an automatic subagent invocation.

When no row matches, continue without forcing a role. In particular, narrative writing and editorial scripts are not software development, and creative review is not software runtime QA.

### Genome roles

| work type | primary role | checking roles |
|---|---|---|
| Establishing software requirements or business operations | business-analyst | project-manager |
| Choosing software architecture or changing contracts across components | tech-lead | security |
| Implementing or explaining source code, executable tooling or software automation | developer | qa |
| Changing software processing behavior or branches | developer | business-analyst, qa |
| Verifying executable behavior or building a software verification gate | qa | developer |
| Investigating a software defect | developer | qa |
| Planning deliverables, work order and scope | project-manager | |
| Planning software changes with technical dependencies | project-manager | tech-lead |
| Assessing authentication, authorization, data exposure or secret access | security | tech-lead |
| Translating software requirements or technical communication | comtor | business-analyst |

### Project roles

| work type | primary role | checking roles |
|---|---|---|

## §2 Maintenance

Add domain roles when project work actually needs them. Every referenced name must resolve to a role file in this directory, and each role keeps §6 for checking criteria. The routing schema and project-extension procedure are in `.agent-workspace/guide/general/role-selection.md` §3 and §5.
