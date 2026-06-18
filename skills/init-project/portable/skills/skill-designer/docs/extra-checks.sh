#!/usr/bin/env bash
# Extra invariant checks for skill-designer.
# Sourced by .claude/skills/skill-writer/scripts/test-skill.sh — inherits SKILL_DIR, SKILL_MD, pass(), fail(), FAILED.

SCAN=("$SKILL_MD" "$SKILL_DIR/docs/orchestrator-rules.md" "$SKILL_DIR/docs/design-template.md" "$SKILL_DIR/docs/plan-gate-spec.md")

# dep files exist
for f in docs/orchestrator-rules.md docs/design-template.md docs/plan-gate-spec.md; do
  test -f "$SKILL_DIR/$f" && pass "dep $f exists" || fail "dep $f missing"
done

# disable-model-invocation: true
grep -q '^disable-model-invocation: true' "$SKILL_MD" && pass "disable-model-invocation set" || fail "disable-model-invocation missing"

# design-checks block present
grep -q '^## design-checks' "$SKILL_MD" && pass "design-checks block present" || fail "design-checks block missing"

# step 12 references design-checks
grep -c '## design-checks' "$SKILL_MD" | grep -q '^[2-9]' \
  && pass "step 12 references design-checks" \
  || fail "step 12 missing ref to design-checks (should appear ≥2 times)"

# design-checks item count matches declaration
DECLARED=$(grep -oE 'all [0-9]+ items' "$SKILL_MD" | head -1 | grep -oE '[0-9]+')
ACTUAL=$(awk '/^## design-checks/,/^## anti-patterns/' "$SKILL_MD" | grep -c '^- ')
if [ "${DECLARED:-0}" = "${ACTUAL:-X}" ]; then
  pass "design-checks count match: declared=$DECLARED, actual=$ACTUAL"
else
  fail "design-checks count mismatch: declared=$DECLARED, actual=$ACTUAL"
fi

# no item-count-matches-axis (canonical: task-count-matches-axis)
! grep -q 'item-count-matches-axis' "$SKILL_MD" && pass "no item-count-matches-axis" || fail "stale item-count-matches-axis in SKILL.md"

# no stale EX-01..08 in dep files
if grep -qE 'EX-01\.\.(EX-)?08' "${SCAN[@]}" 2>/dev/null; then
  fail "stale EX-01..08 ref in dep files"
else
  pass "no stale EX-01..08 in dep files"
fi

# no Vietnamese in dep files
VN_DEP=$(grep -hn -P '[ăâđêôơưĂÂĐÊÔƠƯáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵÁÀẢÃẠẮẰẲẴẶẤẦẨẪẬÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ]' "${SCAN[@]}" 2>/dev/null | head -3 || true)
[ -z "$VN_DEP" ] && pass "no Vietnamese chars in dep files" || fail "Vietnamese leakage in dep files: $VN_DEP"

# no stale stage prose in plan-gate-spec.md
STAGE_PROSE=$(grep -inE '\bstage(s|d|)\b' "$SKILL_DIR/docs/plan-gate-spec.md" 2>/dev/null \
  | grep -viE 'stage→phase|stages→phases|`stages\[\]`|Stages section → Phases|section / component / element / stage' || true)
[ -z "$STAGE_PROSE" ] && pass "no stale stage prose in plan-gate-spec.md" || fail "stage prose in plan-gate-spec.md: $STAGE_PROSE"
