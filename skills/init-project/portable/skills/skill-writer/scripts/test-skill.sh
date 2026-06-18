#!/usr/bin/env bash
# Shared skill test runner (owned by skill-writer — QA gate of the skill-authoring chain).
# Usage: bash .claude/skills/skill-writer/scripts/test-skill.sh <skill-dir>
# Base checks = official platform invariants (code.claude.com/docs/en/skills)
# + project SKILL.md standards (.claude/rules/skill-md-standards.md).
# Per-skill invariants live in <skill-dir>/docs/extra-checks.sh (sourced at the
# end; inherits SKILL_DIR, SKILL_MD, pass(), fail(), FAILED).

set -u

SKILL_DIR="${1:?usage: test-skill.sh <skill-dir>}"
SKILL_DIR="${SKILL_DIR%/}"
SKILL_MD="$SKILL_DIR/SKILL.md"
FAILED=0

pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*"; FAILED=$((FAILED + 1)); }

echo "=== test-skill: $SKILL_DIR"

# --- entrypoint ---
if [ ! -f "$SKILL_MD" ]; then
  fail "SKILL.md missing at $SKILL_MD"
  echo "RESULT: FAIL (1 failure)"
  exit 1
fi
pass "SKILL.md exists"

# --- frontmatter ---
head -1 "$SKILL_MD" | grep -q '^---$' && pass "frontmatter opens with ---" || fail "frontmatter missing opening ---"
FM=$(awk '/^---$/{c++; next} c==1{print} c>=2{exit}' "$SKILL_MD")
[ -n "$FM" ] && pass "frontmatter block non-empty" || fail "frontmatter block empty or unclosed"

NAME=$(printf '%s\n' "$FM" | grep -E '^name:' | head -1 | sed 's/^name:[[:space:]]*//')
if [ -n "$NAME" ]; then
  echo "$NAME" | grep -qE '^[a-z0-9][a-z0-9-]*$' && pass "name kebab-case ($NAME)" || fail "name not kebab-case: $NAME"
fi

printf '%s\n' "$FM" | grep -q '^description:' && pass "description present" || fail "description missing"

# description + when_to_use combined ≤ 1536 chars (official listing truncation cap)
DESC=$(printf '%s\n' "$FM" | awk '/^description:/{f=1; print; next} f && /^[A-Za-z_-]+:/{f=0} f{print}')
WTU=$(printf '%s\n' "$FM" | awk '/^when_to_use:/{f=1; print; next} f && /^[A-Za-z_-]+:/{f=0} f{print}')
LEN=$(printf '%s' "$DESC$WTU" | wc -c | tr -d '[:space:]')
if [ "${LEN:-0}" -le 1536 ]; then
  pass "description+when_to_use length $LEN ≤ 1536"
else
  fail "description+when_to_use length $LEN > 1536 (truncated in skill listing)"
fi

# unreachable invocation combo
if printf '%s\n' "$FM" | grep -q '^disable-model-invocation: true' \
   && printf '%s\n' "$FM" | grep -q '^user-invocable: false'; then
  fail "unreachable: disable-model-invocation: true + user-invocable: false"
else
  pass "no unreachable invocation combo"
fi

# --- body ---
# line budget: ≤ 500 simple, ≤ 800 orchestration (## subagents table = orchestration marker)
LINES=$(wc -l < "$SKILL_MD" | tr -d '[:space:]')
if grep -q '^## subagents' "$SKILL_MD"; then LIMIT=800; else LIMIT=500; fi
[ "$LINES" -le "$LIMIT" ] && pass "line count $LINES ≤ $LIMIT" || fail "line count $LINES > $LIMIT"

# supporting files via ${CLAUDE_SKILL_DIR}, never dot-relative
if grep -nE '\]\(\./|\.\./' "$SKILL_MD" >/dev/null; then
  fail "dot-relative path in SKILL.md (use \${CLAUDE_SKILL_DIR}/...): $(grep -nE '\]\(\./|\.\./' "$SKILL_MD" | head -2 | tr '\n' ' ')"
else
  pass "no dot-relative supporting-file refs"
fi

# zero hedges in instruction text (skill-md-standards); skip denylist lines that mention the words themselves
HEDGES=$(grep -inE '\b(generally|typically|usually|perhaps|ideally)\b' "$SKILL_MD" | grep -vi 'hedge' | head -3 || true)
[ -z "$HEDGES" ] && pass "no hedge words" || fail "hedge words: $HEDGES"

# allowed-tools declared (project rule: declare safe tools to skip permission prompts)
grep -q '^allowed-tools:' "$SKILL_MD" && pass "allowed-tools declared" || fail "allowed-tools missing"

# stale orchestration vocabulary (renames: stages→phases, items→tasks, TASK_KEY→JOB_KEY, EX range = 01..09)
! grep -q 'TASK_KEY' "$SKILL_MD" && pass "no stale TASK_KEY" || fail "stale TASK_KEY"
! grep -qE 'EX-01\.\.(EX-)?08' "$SKILL_MD" && pass "no stale EX-01..EX-08 ref" || fail "stale EX-01..EX-08 ref"
STAGE_HITS=$(grep -inE '\bstage(s|d|)\b' "$SKILL_MD" 2>/dev/null | grep -viE 'stage→phase|stages→phases' || true)
[ -z "$STAGE_HITS" ] && pass "no bare 'stage' prose" || fail "bare 'stage' prose: $(echo "$STAGE_HITS" | head -2 | tr '\n' ' ')"
STALE_FIELDS=$(grep -hnE 'stage\.agent|stage_id|item_id|total_items' "$SKILL_MD" 2>/dev/null | grep -vE '→|->|rename' || true)
[ -z "$STALE_FIELDS" ] && pass "no stale stage_id/item_id/total_items" || fail "stale fields: $STALE_FIELDS"

# no Vietnamese chars (.claude/** = English)
VN_HITS=$(grep -hn -P '[ăâđêôơưĂÂĐÊÔƠƯáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵÁÀẢÃẠẮẰẲẴẶẤẦẨẪẬÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ]' "$SKILL_MD" 2>/dev/null | head -3 || true)
[ -z "$VN_HITS" ] && pass "no Vietnamese chars in SKILL.md" || fail "Vietnamese leakage: $VN_HITS"

# referenced docs/ + scripts/ files exist
MISSING_REFS=""
for ref in $(grep -oE '\$\{CLAUDE_SKILL_DIR\}/[A-Za-z0-9_./-]+\.(md|sh|py|json|yaml|yml)' "$SKILL_MD" | sed 's|\${CLAUDE_SKILL_DIR}/||' | sort -u); do
  [ -f "$SKILL_DIR/$ref" ] || MISSING_REFS="$MISSING_REFS $ref"
done
[ -z "$MISSING_REFS" ] && pass "all \${CLAUDE_SKILL_DIR} refs exist" || fail "dead \${CLAUDE_SKILL_DIR} refs:$MISSING_REFS"

# --- per-skill extra checks ---
EXTRA="$SKILL_DIR/docs/extra-checks.sh"
if [ -f "$EXTRA" ]; then
  echo "--- extra checks: $EXTRA"
  # shellcheck disable=SC1090
  . "$EXTRA"
else
  echo "--- no extra-checks.sh (skipped)"
fi

echo "---"
if [ "$FAILED" -eq 0 ]; then
  echo "RESULT: PASS (0 failures)"
  exit 0
else
  echo "RESULT: FAIL ($FAILED failures)"
  exit 1
fi
