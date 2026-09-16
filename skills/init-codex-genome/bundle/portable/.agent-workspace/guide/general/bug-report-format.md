---
scope: portable
---

# Evidence needed for a review finding

## §1 Make the finding assessable

When reporting an established defect, identify its location, triggering condition, demonstrated problem, consequence and proposed correction. The recipient must be able to inspect the evidence and distinguish what is wrong from what would change. Add the governing requirement or cause when needed to judge the conclusion.

Use a source span, stable section or reproducible runtime state as the location. Give findings stable identifiers when later work needs to refer to them. Group repeated locations of the same cause without inflating the number of distinct defects. Suspected findings remain labeled as unresolved rather than becoming confirmed to fit a reporting template.

## §2 Assess severity within the domain

A blocker prevents the core workflow or causes data loss or corruption. A critical defect produces a wrong essential result or a security exposure while other work remains usable. A high-severity defect affects a reachable path with substantial consequence and no safe workaround. Medium severity covers a contained failure or maintenance risk with a workable alternative. Low severity covers limited issues with no established behavioral impact.

Use the project's established severity scale when one applies. For non-software work, assess the effect on that artifact's purpose. A false factual claim can materially damage a document without involving a program. Severity needs reachable conditions and demonstrated consequence, not an alarming hypothesis.

## §3 Distinguish a proposal from a verified fix

Explain the meaning of a formula, condition or identifier when that meaning is needed to assess the correction. Check boundary and missing-value cases before proposing logic. A proposed fix does not prove it has been implemented or that its consumers remain compatible; use `fix-impact-analysis.md` §2 before applying it.

## §4 State what the review established

Identify inspected scope, available evidence and unresolved limits. The information requirements apply to both a small review and a broad audit, but do not impose a common layout or writing style. When no finding survives verification, report that result without implying certainty about unexamined behavior.
