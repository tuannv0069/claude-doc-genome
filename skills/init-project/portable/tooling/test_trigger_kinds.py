#!/usr/bin/env python3
"""§10 must define ALL the trigger-condition kinds it relies on.

A rule that must make the agent act before it touches any file cannot be expressed as a
condition decided from the user message; without the other kinds named, such a rule has no
legal footing in the standard.

This gate covers ONLY what a machine can check: the required tokens and phrases must be
present, and present inside the §10 slice specifically (not anywhere else in the file). The
gate does NOT read prose quality and does not judge whether the law is right — that is for the
human reading §10.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / ".claude" / "rules" / "doc-organization.md"

# Slice from "## §10" up to (not including) the next "## §..." heading, or EOF.
SECTION_RE = re.compile(r"^## §10\b.*?(?=\n## §|\Z)", re.S | re.M)

NEEDLES = [
    ("action-triggered", "the §10 slice does not carry the action-triggered kind"),
    ("message-triggered", "the §10 slice does not name the message-triggered kind"),
    ("before the tool call", "the §10 slice: the action-triggered kind has no test of its own"),
]

# The three examples §10 must keep stating as forbidden, across every trigger kind.
FORBIDDEN_EXAMPLES = ["complex task", "when X is needed", "multi-step task"]


def extract_section_10(src: str) -> str:
    m = SECTION_RE.search(src)
    return m.group(0) if m else ""


def check(src: str) -> list[str]:
    """Return failure messages for the §10 slice of `src`. Empty = pass.

    Every check below is scoped to the §10 slice on purpose — a token planted elsewhere in the
    file (inside §3, say) must NOT satisfy it. See the mutation check in main() for a live
    proof of that scoping.
    """
    fails: list[str] = []
    section = extract_section_10(src)
    if not section:
        return ["§10 section not found"]

    for needle, msg in NEEDLES:
        if needle not in section:
            fails.append(msg)

    for example in FORBIDDEN_EXAMPLES:
        if f"`{example}`" not in section:
            fails.append(f"the §10 slice: the forbidden example `{example}` is not stated there")

    # The action-triggered "Its test:" sentence must itself carry the concrete-object
    # requirement -- not merely somewhere nearby in the bullet.
    test_sentence = re.search(r"Its test:[^.?]*[.?]", section)
    if not test_sentence or "concrete object" not in test_sentence.group(0):
        fails.append(
            "the §10 slice: the action-triggered `Its test:` sentence does not itself require a "
            "concrete object"
        )

    return fails


# A deliberately broken §10 (empty body) sitting next to a decoy line in §11 that carries every
# literal token the checks above look for. If `check()` passed on this, the gate would be proven
# unscoped -- it must fail.
MUTANT_DOC = (
    "## §10 Placement laws\n\n"
    "- placeholder, no trigger-kind content in this slice\n\n"
    "## §11 Project work-product layer (docs/)\n\n"
    "decoy line carrying every needle so an unscoped check would wrongly pass: "
    "action-triggered message-triggered before the tool call concrete object "
    "Its test: `complex task` `when X is needed` `multi-step task`\n"
)


def main() -> int:
    src = TARGET.read_text(encoding="utf-8")
    fails = check(src)
    for f in fails:
        print("FAIL:", f)
    print(f"{len(fails)} fail")

    mutant_fails = check(MUTANT_DOC)
    if not mutant_fails:
        print("FAIL: the mutation check did not catch an empty §10 slice -- the gate is NOT scoped to §10")
        fails.append("mutation-not-caught")
    else:
        print(
            f"mutation check caught the empty §10 slice ({len(mutant_fails)} fail) "
            "-- the gate is scoped to §10, the decoy in §11 correctly ignored"
        )

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
