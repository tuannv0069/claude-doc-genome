---
class: debt
subject: .agent-workspace/guide/general/rule-health.md
supersedes: 2026-09-02-debt-rule-health-deferred
anchor: .agent-workspace/tooling/test_scan_rule_health.py
---
- decided: the rule-health debt is paid — the guide, the scan and a 20-case mutation test all ship
- because: the two unlock conditions were met by building them, not by waiting: the test now exists, and a single zero-match `paths:` glob became a `paths_no_match` finding while an entirely empty scope stays a hard error
- rejected: keep deferring — the missing safety net was the reason to build one, not a reason to stop
