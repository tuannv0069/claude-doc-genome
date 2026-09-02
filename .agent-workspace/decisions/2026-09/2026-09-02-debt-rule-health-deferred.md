---
class: debt
subject: skills/init-project/SKILL.md
anchor: .agent-workspace/tasks/genome-integrate-2.5/ref/init-project/portable/tooling/scan_rule_health.py
---
- decided: `rule-health.md` and `scan_rule_health.py` do not ship in 2.7.0; the rest of wave 4 does
- because: the script has no test in the bundle, and run against this repo it errors on `.agent-workspace/wiki/**` matching no file — our core-rule/optional-tier split makes a declared-but-unpopulated `paths:` legal, which its scope model treats as a declaration error
- unlocked by: a test for the scan exists, and the zero-match `paths:` case is settled for a portable rule whose tier is optional
