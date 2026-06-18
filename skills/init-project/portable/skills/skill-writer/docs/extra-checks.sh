#!/usr/bin/env bash
# Extra invariant checks for skill-writer.
# Sourced by .claude/skills/skill-writer/scripts/test-skill.sh — inherits SKILL_DIR, SKILL_MD, pass(), fail(), FAILED.

SCAN_DOCS=("$SKILL_MD" "$SKILL_DIR/docs/skill-rules-spec.md" "$SKILL_DIR/docs/skill-rules-orch.md" "$SKILL_DIR/docs/skill-rules-quality.md" "$SKILL_DIR/docs/skill-rules-workflow.md" "$SKILL_DIR/docs/examples.md")

# dep files exist
for f in docs/skill-rules-spec.md docs/skill-rules-orch.md docs/skill-rules-quality.md docs/skill-rules-workflow.md docs/examples.md; do
  test -f "$SKILL_DIR/$f" && pass "dep $f exists" || fail "dep $f missing"
done

# disable-model-invocation: true
grep -q '^disable-model-invocation: true' "$SKILL_MD" && pass "disable-model-invocation set" || fail "disable-model-invocation missing"

# workflow creates .claude/agents/*.md
grep -q 'create.*\.claude/agents' "$SKILL_MD" && pass "workflow creates .claude/agents/*.md" || fail "step missing for .claude/agents/*.md creation"

# §agent-file-template section present
grep -q '^## §agent-file-template' "$SKILL_MD" && pass "§agent-file-template present" || fail "§agent-file-template missing"

# README = English (no Vietnamese mandate)
! grep -qE '100% Vietnamese|Vietnamese README' "$SKILL_MD" && pass "README rule = English" || fail "README still mandates Vietnamese"

# no stale TASK_KEY in docs (allow rename-history line)
TASK_HITS=$(grep -hn 'TASK_KEY' "${SCAN_DOCS[@]}" 2>/dev/null | grep -v 'TASK_KEY.*→.*JOB_KEY' || true)
[ -z "$TASK_HITS" ] && pass "no stale TASK_KEY in docs" || fail "stale TASK_KEY: $TASK_HITS"

# no stages/current_stage in examples
! grep -qE '"stages":|current_stage' "$SKILL_DIR/docs/examples.md" 2>/dev/null \
  && pass "examples use phases naming" \
  || fail "examples still use stages/current_stage"

# no item-count-matches-axis
! grep -q 'item-count-matches-axis' "${SCAN_DOCS[@]}" 2>/dev/null \
  && pass "no item-count-matches-axis" \
  || fail "stale item-count-matches-axis in docs"

# no Vietnamese in docs
VN_DOC=$(grep -hn -P '[ăâđêôơưĂÂĐÊÔƠƯáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵÁÀẢÃẠẮẰẲẴẶẤẦẨẪẬÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ]' "${SCAN_DOCS[@]}" 2>/dev/null | head -3 || true)
[ -z "$VN_DOC" ] && pass "no Vietnamese chars in docs" || fail "Vietnamese leakage in docs: $VN_DOC"
