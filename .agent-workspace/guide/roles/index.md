---
scope: project
---

<critical>
scope: map task → which role file to wear. Mechanism: `general/role-selection.md`.
never: substantive rule in this hub — pointer + table only
always: one primary role per row; checking roles contribute §6 only
</critical>

## §1 router — work type → role (genome roles)

| work type | primary role | checking roles |
|---|---|---|
| interpreting a requirement, fixing scope before design | business-analyst | project-manager |
| choosing a technical approach or structure across components | tech-lead | security |
| writing or fixing content that describes what the system does — behaviour, processing branch, condition | developer | business-analyst, qa |
| writing or fixing content that describes what a user needs — requirement, business rule, scope | business-analyst | project-manager |
| reading code or an artifact to answer a question about how it behaves | developer | qa |
| writing or fixing code, tooling, script | developer | qa |
| reviewing or accepting an artifact already written | qa | business-analyst |
| building a machine verification gate | qa | developer |
| investigating a defect, RCA | developer | qa |
| planning, splitting work, deciding order and scope | project-manager | tech-lead |
| touching authentication, authorization, personal data, secrets | security | tech-lead |
| translating content between two languages, or writing a sentence sent straight to a foreign customer | comtor | business-analyst |

## §1a router — project roles

Roles this project added for its own domain (`general/role-selection.md` §5). A row here outranks a §1 row on the same work type. Empty until the project creates one — a `scope: project` role file under `roles/`, registered here in the same commit.

| work type | primary role | checking roles |
|---|---|---|

## §2 matching rule

- the matching procedure, step by step → `general/role-selection.md` §2
- the table's own format, a contract the gate `.agent-workspace/tooling/verify_role_files.py` reads → `general/role-selection.md` §6
- a role file colliding with a project guide or an always-loaded rule → `general/role-selection.md` §7
