#!/usr/bin/env python3
"""Exercise the scanner on real text units and temporary instruction trees.

Each duplicate comparison uses paragraph content on both sides. The fixtures
also show that an empty scope and broken references cannot pass silently.
"""
import sys
import tempfile
import subprocess
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scan_rule_health as S

fails = []
def check(condition, message):
    if not condition: fails.append(message)

def put(root, name, text):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path

with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    check(bool(S.resolve_scope(root)[1]), "an empty scope was accepted")
    put(root, "CLAUDE.md", "# Project\n\nRead the registered source before making changes.\n")
    put(root, ".claude/rules/paths.md", '---\nscope: portable\npaths:\n  - "extra/**"\n---\n\nRead the extra material.\n')
    put(root, ".agent-workspace/guide/general/example.md", "## §1\n\nA complete explanation.\n")
    put(root, "extra/material.md", "Project-specific material.\n")
    put(root, ".agent-workspace/tasks/task/notes.md", "Unfinished working notes.\n")
    paths, errors = S.resolve_scope(root)
    names = {path.relative_to(root).as_posix() for path in paths}
    check(not errors, f"the known trees did not establish scope: {errors}")
    check(".agent-workspace/guide/general/example.md" in names, "the known guide tree was omitted")
    check("extra/material.md" in names, "the declared extension was omitted")
    check(not any("/tasks/" in name for name in names), "task notes entered the corpus")
    (root / ".claude/rules/paths.md").unlink()
    check(not S.resolve_scope(root)[1], "scope depended on a particular rule or paths declaration")

    paragraph = "Read the source file before changing its public interface and verify every existing caller."
    wrapped = "Read the source file before changing\nits public interface and verify every existing caller."
    a, b = S.rule_lines(paragraph), S.rule_lines(wrapped)
    check(len(a) == len(b) == 1 and a[0][1:] == b[0][1:], "line wrapping changed the duplicate unit")
    check(len(S.rule_lines("Short.\n\n" + paragraph)) == 2, "short prose was silently discarded")
    rows = S.rule_lines("- " + wrapped + "\n- Preserve the call result.\n")
    check(len(rows) == 2 and rows[0][1] == paragraph, "a multiline list item was not kept together")
    masked = "---\nscope: portable\n---\n# Heading\n```text\n" + paragraph + "\n```\n<example>\n" + paragraph + "\n</example>\n\n" + paragraph
    check(len(S.rule_lines(masked)) == 1, "metadata, examples, or fenced code became rule units")
    tables = "| name | meaning |\n|---|---|\n| source | Read the defining artifact. |\n"
    check(len(S.rule_lines(tables)) == 1, "table header was compared as an instruction")
    found = S.signal_dup({"first/a.md": a, "second/b.md": b})
    check(any(item["signal"] == "dup" for item in found), "a duplicate wrapped paragraph was missed")
    unrelated = S.rule_lines("Use the final scene to reveal the result of the character's choice.")
    check(not S.signal_dup({"first/a.md": a, "second/b.md": unrelated}), "unrelated paragraphs were reported as duplicates")

    put(root, ".claude/rules/paths.md", '---\npaths:\n  - "missing/**"\n---\n')
    check(any("paths_no_match" in item["detail"] for item in S.scope_findings(root)), "an unmatched declared path was not reported")
    bad = put(root, ".claude/rules/broken.md", "Read `gone.md` §8 before acting.\n")
    check(any(item["signal"] == "dead" for item in S.signal_dead([bad], root)), "a dead section pointer was missed")
    check(S.ledger_problems({"entries": {"x": {"status": "unknown"}}}), "an invalid ledger status was accepted")
    check(S.ledger_problems({"entries": {"x": {"status": "exempt", "reason": "none"}}}), "an exemption without its authority was accepted")
    check(not S.ledger_problems({"entries": {"x": {"status": "fixed"}}}), "a valid fixed entry was rejected")
    put(root, S.LEDGER, "invalid json")
    check(S.main(["--root", str(root)]) == 1, "unreadable ledger did not fail explicitly")

# Source history is UTF-8 even when the host's preferred encoding is Windows-1252.
with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    content = "## §1 Evidence\n\nTiếng Việt: “đọc nguồn trước”.\n"
    target = put(root, ".agent-workspace/guide/general/source.md", content)
    caller = put(root, "CLAUDE.md", "Read `.agent-workspace/guide/general/source.md` §1.\n")
    def git(*args):
        subprocess.run(["git", "-c", "core.hooksPath=", *args], cwd=root,
                       check=True, capture_output=True)
    git("init", "-q")
    git("add", "CLAUDE.md", ".agent-workspace/guide/general/source.md")
    git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-q", "-m", "Record Unicode source history")
    with patch("subprocess._text_encoding", return_value="cp1252"):
        check(S._git_show(root, "HEAD", target) == content,
              "historical UTF-8 content was decoded with the host's default encoding")
        check(S.signal_drift([caller], root) == [], "unchanged Unicode history reported drift")
        target.write_text(content.replace("đọc nguồn trước", "kiểm tra bản mới"), encoding="utf-8")
        check(any(item["signal"] == "drift" for item in S.signal_drift([caller], root)),
              "a changed Unicode source section was not detected")
        reviewed = S.signal_drift([caller], root)
        ledger = {"entries": {S.fingerprint(item): {"status": "fixed"} for item in reviewed}}
        check(not S.open_findings(reviewed, ledger), "a reviewed source revision remained open")
        target.write_text(content.replace("đọc nguồn trước", "đối chiếu cả hai phía"), encoding="utf-8")
        check(bool(S.open_findings(S.signal_drift([caller], root), ledger)),
              "a later target change was hidden by an earlier drift resolution")

for failure in fails: print("FAIL:", failure)
print(f"{len(fails)} failures")
sys.exit(1 if fails else 0)
