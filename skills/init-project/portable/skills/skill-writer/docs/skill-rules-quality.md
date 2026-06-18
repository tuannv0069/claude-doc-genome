<critical>
target: skill-writer agent reference — quality gate
purpose: 2-step writer verification, audit handoff, self-test, release gate, common failures
scope: applied before any skill marked ready-for-deployment
</critical>

<rule_schema>
gate_check: single-line verifiable condition
failure_row: failure | cause | fix
</rule_schema>

<dependencies>
- ${CLAUDE_SKILL_DIR}/docs/skill-rules-spec.md — platform spec
- ${CLAUDE_SKILL_DIR}/docs/skill-rules-orch.md — orchestration rules
</dependencies>

---

## §1 writer 2-step verification

### §1.1 syntax + structure audit

| check |
|---|
| YAML frontmatter complete |
| markdown syntax valid (headings, links, code blocks) |
| mermaid diagrams parse |
| paths use `${CLAUDE_SKILL_DIR}/...` |
| code blocks have language tag |
| env vars use `$VAR` or `${VAR}` |
| no refs to non-existent files |

### §1.2 runtime with mock input

| check |
|---|
| runs start-to-finish without intervention |
| all branches tested (success, error, edge) |
| output matches spec |
| no unhandled exceptions |
| cleanup works (temp deleted, state reset) |
| within token budget |

---

## §2 audit handoff

```text
Writer → SKILL.md + supporting files
   ↓
Audit → reads files, runs §1
   ├─ syntax/structure
   ├─ runtime (mock if expensive)
   └─ report: PASS / REJECT
PASS  → ready-for-deployment
REJECT → loop back to Writer
```

audit is explicit step; never skip

---

## §3 self-test

every skill includes one of:

| option | form |
|---|---|
| A test script | `bash .claude/skills/skill-writer/scripts/test-skill.sh <skill-dir>` (+ per-skill `docs/extra-checks.sh`) |
| B hook | `hooks: { onInit: <validate + smoke> }` |
| C CI/CD | pipeline runs `bash .claude/skills/skill-writer/scripts/test-skill.sh <skill-dir>` |

---

## §4 release gate

| gate |
|---|
| writer called audit (explicit) |
| audit ran syntax + runtime |
| skill has self-test |
| `## testing` section if manual test needed |
| zero syntax violations |
| runtime passes all branches |
| token budget estimated (long-running) |
| no orphans / broken state |
| matches project conventions |

missing any → return to writer; never release incomplete

---

## §5 common failures

| failure | cause | fix |
|---|---|---|
| YAML parse error | invalid frontmatter | fix indent, quote special chars |
| markdown render fail | broken heading, bad table | fix per markdown rules |
| file not found | wrong `${CLAUDE_SKILL_DIR}/` path | verify file exists |
| code block parse | missing language tag | add `python`, `bash`, ... |
| runtime fail | timeout, missing dep, wrong format | debug with mock, add error handling |
| cleanup fail | orphans after test | fix cleanup logic |

---

<critical_recap>
1. audit is explicit step in writer workflow; never skip
2. release gate has 9 checks; missing any → return to writer
3. every skill includes self-test (script | hook | CI/CD)
4. runtime test covers all branches, not just happy path
5. cleanup verified — no orphan temp files, state reset
</critical_recap>
