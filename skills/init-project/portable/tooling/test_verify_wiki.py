"""Test verify_wiki against FAKE tiers.

The real tier must be green, so running the gate on it only proves it does not cry wolf. The
other half - does the gate catch a real defect - is built by mutation: each case breaks exactly
one rule and must go red with THAT rule message - red for another reason does not count as
checked. The GREEN cases are real cases too: a gate that cries wolf on a legal auxiliary table
is broken exactly as badly as one that silently swallows a mistyped edge table.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".agent-workspace/tooling")
import verify_wiki as V  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


ROUTER = """---
scope: project
source_root: ../src
---

# wiki — router

| subject | cluster | status |
|---|---|---|
| legacy-system | [permission](legacy-system/permission.md) | growing |
"""

CLUSTER = """---
scope: project
subject: legacy-system
---

# permission

| id | claim | class | confidence | evidence |
|---|---|---|---|---|
| permission-a1b2c | Code 8 switches off the paper-decision reason check | code-behaviour | sourced | located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"` |
"""


def build(router=ROUTER, cluster=CLUSTER, src_line='\t\t\t\tElseIf RoleCd(0) = "8" Then\n',
          gitignore=None):
    d = Path(tempfile.mkdtemp())
    (d / "wiki" / "legacy-system").mkdir(parents=True)
    (d / "wiki" / "index.md").write_text(router, encoding="utf-8")
    (d / "wiki" / "legacy-system" / "permission.md").write_text(cluster, encoding="utf-8")
    f = d / "src" / "ASP" / "Common" / "asp"
    f.mkdir(parents=True)
    (f / "FB_GetNinsho.asp").write_text("x\n" * 122 + src_line, encoding="utf-8")
    if gitignore is not None:
        (d / "src" / ".gitignore").write_text(gitignore, encoding="utf-8")
        # `rg` honours .gitignore only when a REAL .git sits at or above the search
        # directory - with no .git the .gitignore is inert, and the mutation case would go
        # green while proving nothing (verified directly with rg before writing this case).
        subprocess.run(["git", "init", "-q"], cwd=d, check=True, capture_output=True)
    return d


def build_repo(cluster=CLUSTER):
    """A real git repo, needed by R9 (`check_merge` reads content at a ref)."""
    d = Path(tempfile.mkdtemp())
    run = lambda *a: subprocess.run(a, cwd=d, check=True, capture_output=True)
    run("git", "init", "-q")
    run("git", "config", "user.email", "t@example.com")
    run("git", "config", "user.name", "t")
    (d / "wiki" / "legacy-system").mkdir(parents=True)
    (d / "wiki" / "index.md").write_text(ROUTER, encoding="utf-8")
    (d / "wiki" / "legacy-system" / "permission.md").write_text(cluster, encoding="utf-8")
    run("git", "add", "-A")
    run("git", "commit", "-q", "-m", "seed")
    return d


# ================= the six §8 rules =================

# case 0 - a healthy tier must be green
check(V.check_tier(build()) == [], "the gate cried wolf on a healthy tier")

# case 1 - the path does not exist
d = build()
(d / "src" / "ASP" / "Common" / "asp" / "FB_GetNinsho.asp").unlink()
check(any("path" in m for m in V.check_tier(d)), "a dead path was not caught")

# case 2 - the anchor is gone from the file
check(any("anchor" in m for m in V.check_tier(build(src_line="khong co gi\n"))),
      "a vanished anchor was not caught")

# case 3 - anchor still present but the line drifted
d = build()
p = d / "src" / "ASP" / "Common" / "asp" / "FB_GetNinsho.asp"
p.write_text("y\n" + p.read_text(encoding="utf-8"), encoding="utf-8")
check(any("drifted" in m or "line" in m for m in V.check_tier(d)), "line drift was not caught")

# case 4 - tier-wide duplicate id
dup = CLUSTER + "| permission-a1b2c | A different claim | code-behaviour | hypothesis | located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = \"8\"` |\n"
check(any("id" in m for m in V.check_tier(build(cluster=dup))), "a duplicate id was not caught")

# case 5 - a cluster with no router row
check(any("router" in m for m in V.check_tier(build(router=ROUTER.replace("| legacy-system | [permission](legacy-system/permission.md) | growing |\n", "")))),
      "an orphan cluster was not caught")

# case 6 - stored-data carries an anchor (forbidden)
sd = CLUSTER.replace(
    "located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = \"8\"`",
    "stored-data: dataset=X object=PARTMASTER field=CODE query=`SELECT CODE FROM PARTMASTER` anchor=`PARTMASTER`",
)
check(any("stored-data" in m for m in V.check_tier(build(cluster=sd))),
      "stored-data carrying an anchor was not caught")


# ========== R7: match anchor positions WITHIN the item own file, never across the tree ==========
# The case that produced R7: FB_GetNinsho.asp repeats the 役割コード block twice IN THE SAME file
# - R7 demands a position-set comparison to catch the second position being left out. The old
# implementation widened that comparison to the whole `source_root` tree; on a codebase that
# copy-pastes across sibling screen modules, that turned EVERY live duplicate living in another
# file into a false alarm. The three cases below pin the boundary: compare inside the file `path`

# names. case-scope-a - the anchor also matches in ANOTHER file: must be GREEN (duplicated code
# is a fact about the codebase, not a defect of the edge - this is the behaviour the patch added)
d = build()
(d / "src" / "ASP" / "Common" / "asp" / "FB_Other.asp").write_text(
    "x\n" * 50 + '\t\t\t\tElseIf RoleCd(0) = "8" Then\n', encoding="utf-8",
)
check(V.check_tier(d) == [],
      "case-scope-a: an anchor duplicated in ANOTHER FILE was wrongly reported - must be green once the comparison is scoped to the file")

# case-scope-b - the anchor is GONE from the very file `path` names, though intact in another:
# it must still be RED - "still visible somewhere in the tree" is never enough
d = build(src_line="khong co gi\n")
(d / "src" / "ASP" / "Common" / "asp" / "FB_Other.asp").write_text(
    "x\n" * 50 + '\t\t\t\tElseIf RoleCd(0) = "8" Then\n', encoding="utf-8",
)
check(any("anchor" in m for m in V.check_tier(d)),
      "case-scope-b: an anchor gone from the file `path` names (though present elsewhere) was not caught - it must still be red")

# case-scope-c - the anchor repeats TWICE in the SAME file and only one position is recorded:
# it must still be RED (R7 old behaviour - scoping to the file must not relax the same-file case)
d = build()
p = d / "src" / "ASP" / "Common" / "asp" / "FB_GetNinsho.asp"
p.write_text(p.read_text(encoding="utf-8") + '\t\t\t\tElseIf RoleCd(0) = "8" Then\n', encoding="utf-8")
check(any("anchor" in m for m in V.check_tier(d)),
      "case-scope-c: an anchor repeated twice in the SAME file with only one position recorded must still be red (old behaviour preserved)")

# case-peredge - two edges cite the SAME anchor+file, one recording BOTH positions and one
# recording one SHORT: `want` must be compared PER EDGE, never merged tier-wide - otherwise the
# complete edge masks the short one (observed: one edge masked a simulated edge that was missing
# a position in the real tier, before this patch)
two_edge_cluster = """---
scope: project
subject: legacy-system
---

# permission

| id | claim | class | confidence | evidence |
|---|---|---|---|---|
| permission-full01 | Records both positions | code-behaviour | sourced | located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"`<br>located: `ASP/Common/asp/FB_GetNinsho.asp:124` anchor=`RoleCd(0) = "8"` |
| permission-part01 | Records one position short | code-behaviour | sourced | located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"` |
"""
d = build(cluster=two_edge_cluster)
p = d / "src" / "ASP" / "Common" / "asp" / "FB_GetNinsho.asp"
p.write_text(p.read_text(encoding="utf-8") + '\t\t\t\tElseIf RoleCd(0) = "8" Then\n', encoding="utf-8")
errs = V.check_tier(d)
check(any("permission-part01" in m for m in errs),
      f"case-peredge-a: the short edge (permission-part01) must be red; a complete edge is masking it: {errs!r}")
check(not any("permission-full01" in m for m in errs),
      f"case-peredge-b: the complete edge (permission-full01) was reported because of another edge being short: {errs!r}")


# ================= gaps outside the six §8 rules =================

# C1a - empty evidence: a claim with no evidence must be red
cluster_no_ev = """---
scope: project
subject: legacy-system
---

| id | claim | class | confidence | evidence |
|---|---|---|---|---|
| permission-noev1 | A claim with no evidence | code-behaviour | hypothesis |  |
"""
check(any("evidence" in m for m in V.check_tier(build(cluster=cluster_no_ev))),
      "C1a: empty evidence was not caught")

# C1b - evidence is prose with no prefix ("as I recall") - the shortest route for an unsourced
# claim to slip through a gate that only checks "the cell has content"
cluster_prose_ev = """---
scope: project
subject: legacy-system
---

| id | claim | class | confidence | evidence |
|---|---|---|---|---|
| permission-prose1 | A claim carrying prose only | code-behaviour | hypothesis | as I recall, with no source |
"""
errs = V.check_tier(build(cluster=cluster_prose_ev))
check(any("evidence" in m for m in errs), "C1b: prefix-less prose still slipped through")
check(any("malformed" in m for m in errs), "C1b: a malformed item is not reported on its own")

# C2 - a row with only 4 cells (no evidence column): red for the missing column, AND its id must
# still be visible to _all_ids/seen_ids (R5/R9), so new_id can never hand that id out again
cluster_short_row = CLUSTER + "| permission-short1 | Missing the evidence column | code-behaviour | hypothesis |\n"
d_short = build(cluster=cluster_short_row)
errs = V.check_tier(d_short)
check(any("columns" in m for m in errs), "C2: a row missing columns was not caught")
check("permission-short1" in V._all_ids(d_short),
      "C2: a row missing columns never reached _all_ids - new_id could hand out a duplicate (R9 breaks)")

# C3 - check_merge on a ref THAT DOES NOT EXIST must be red, never degrade into green
d_repo = build_repo()
errs = V.check_merge(d_repo, ["khong-ton-tai-nhanh-xyz"])
check(len(errs) > 0, "C3: a non-existent git ref was swallowed into green")
check(any("could not read ref" in m or "malformed" in m for m in errs),
      "C3: the message does not say this is a git failure")

# C4 - an id with NO padding whitespace around its cell (`|id|claim|...|`) must still be seen by R9
cluster_nopad = """---
scope: project
subject: legacy-system
---

| id | claim | class | confidence | evidence |
|---|---|---|---|---|
|permission-nopad|Claim khong co khoang trang dem|code-behaviour|sourced|located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"`|
"""
d_repo2 = build_repo(cluster=cluster_nopad)
# drop that edge from the current working tree and commit - "here" no longer holds this id
(d_repo2 / "wiki" / "legacy-system" / "permission.md").write_text(ROUTER, encoding="utf-8")
subprocess.run(["git", "add", "-A"], cwd=d_repo2, check=True, capture_output=True)
subprocess.run(["git", "commit", "-q", "-m", "drop"], cwd=d_repo2, check=True, capture_output=True)
errs = V.check_merge(d_repo2, ["HEAD~1"])
check(any("permission-nopad" in m for m in errs),
      "C4: an unpadded id was missed by R9 parallel regex")

# C5 - a file hidden by .gitignore must still be visible to the gate (rg honours .gitignore by
# default, Path.exists() does not) - this case must be GREEN, not red
d_ignored = build(gitignore="ASP/\n")
check(V.check_tier(d_ignored) == [],
      "C5: the gate cried wolf when a real source file was hidden by .gitignore (missing -uu)")

# I1 - a non-numeric `line` must turn the gate RED, never KILL it (crash)
cluster_bad_line = CLUSTER.replace(
    "ASP/Common/asp/FB_GetNinsho.asp:123", "ASP/Common/asp/FB_GetNinsho.asp:abc"
)
try:
    errs = V.check_tier(build(cluster=cluster_bad_line))
    crashed = False
except ValueError:
    errs = []
    crashed = True
check(not crashed, "I1: a non-numeric line crashed the gate instead of returning an error")
check(any("not a number" in m or "line" in m for m in errs), "I1: a non-numeric line was not clearly reported")

# I2 - a ONE-dash separator (`|-|-|-|-|-|`, perfectly legal GFM) must not make the whole table
# invisible. Asserted DIRECTLY on parse_cluster, never through `check_tier == []`: if the table
# vanishes there is no edge left to raise an error, so check_tier returns [] whatever rule was
# broken - an assertion that holds with or without the patch tests nothing.
cluster_sep1 = """---
scope: project
subject: legacy-system
---

| id | claim | class | confidence | evidence |
|-|-|-|-|-|
| permission-sep1 | Bang dung separator mot gach | code-behaviour | sourced | located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"` |
"""
edges_sep1 = V.parse_cluster(build(cluster=cluster_sep1) / "wiki" / "legacy-system" / "permission.md")
check(len(edges_sep1) == 1 and edges_sep1[0].get("id") == "permission-sep1",
      "I2: a one-dash separator (legal GFM) made the whole table vanish from parse_cluster")

# I3 - `<br/>` (self-closing) AND `<br />` (with a space) must both split into 2 evidence items,
# exactly like `<br>`
for variant, label in (("<br/>", "I3a"), ("<br />", "I3b")):
    cluster_br = CLUSTER.replace(
        'located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"`',
        'located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"`'
        f'{variant}absent: query=`X` scope=`Y` expected=`Z`',
    )
    edges = V.parse_cluster(build(cluster=cluster_br) / "wiki" / "legacy-system" / "permission.md")
    check(len(edges) == 1 and len(edges[0]["evidence"]) == 2,
          f"{label}: `{variant}` did not split into 2 evidence items")

# I4 - a table with a different header (not an edge table) must be SKIPPED, never an error
cluster_extra_table = CLUSTER + """
| name | description |
|---|---|
| Note | This is not the edge table; column 2 carries no valid evidence prefix at all |
"""
check(V.check_tier(build(cluster=cluster_extra_table)) == [],
      "I4: a table not matching the edge header was misread as the edge table")

# I5 - an `absent:` item missing a mandatory field (query/scope/expected) must be red, and the
# class must be declared schema-only just like stored-data (R8)
cluster_absent_bad = """---
scope: project
subject: legacy-system
---

| id | claim | class | confidence | evidence |
|---|---|---|---|---|
| permission-absent1 | Khong co dong chuyen quyen rieng cho ma 9 | code-behaviour | hypothesis | absent: query=`SELECT * FROM ROLE WHERE CODE='9'` |
"""
d_absent = build(cluster=cluster_absent_bad)
errs = V.check_tier(d_absent)
check(any("absent" in m and "missing field" in m for m in errs), "I5: an absent item missing a field was not caught")
check(any("absent" in n for n in V.schema_only_classes(d_absent)),
      "I5: the absent class was not declared schema-only (R8, second class)")

# ============ header mismatch: a mistyped edge table vs an auxiliary table ============

# #2a - a MISMATCHED header on a table with ALL 5 COLUMNS (typo "confidance") must be an ERROR, never silence
cluster_header_typo = """---
scope: project
subject: legacy-system
---

| id | claim | class | confidance | evidence |
|---|---|---|---|---|
| permission-typo1 | Claim voi header sai chinh ta | code-behaviour | sourced | located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"` |
"""
errs = V.check_tier(build(cluster=cluster_header_typo))
check(any("header" in m for m in errs), "#2a: a mismatched header (typo, 5 columns) was skipped silently")
check(any("confidance" in m for m in errs),
      "#2a: the message does not say what header was actually read")
# control: the same table with a CORRECT header and a path to a file that does NOT exist - it must
# report a dead path, proving the row was read as a real edge rather than a header mismatch
cluster_header_ok = cluster_header_typo.replace("confidance", "confidence").replace(
    "ASP/Common/asp/FB_GetNinsho.asp:123", "KHONG/TON/TAI.asp:1")
errs_ok = V.check_tier(build(cluster=cluster_header_ok))
check(any("dead path" in m for m in errs_ok) and not any("header" in m for m in errs_ok),
      "#2a: the correct-header control must read an edge (dead path), not a mismatch")

# #2b - a header with the columns REORDERED (all 5 present, every name "valid" but in the wrong place)
cluster_header_reordered = """---
scope: project
subject: legacy-system
---

| claim | id | class | confidence | evidence |
|---|---|---|---|---|
| Claim bi doi cho id | permission-reord1 | code-behaviour | sourced | located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"` |
"""
errs = V.check_tier(build(cluster=cluster_header_reordered))
check(any("header" in m for m in errs), "#2b: a reordered header was skipped silently")
check(any("claim | id | class" in m for m in errs),
      "#2b: the message does not say what header was actually read")

# #2c - a cluster file whose FIRST table is an auxiliary one: by convention the first table IS the
# edge table, so its header not matching is an error
cluster_no_table_at_all = """---
scope: project
subject: legacy-system
---

| name | description |
|---|---|
| Note | This file carries no edge table at all |
"""
errs = V.check_tier(build(cluster=cluster_no_table_at_all))
check(any("header" in m for m in errs),
      "#2c: a cluster whose first table is auxiliary (header is not the edge header) was not caught")
check(any("name | description" in m for m in errs),
      "#2c: the message does not say what header was actually read")

# ============ an auxiliary table AFTER the edge table must be GREEN ============
# Three auxiliary tables that really do appear in a cluster file. All three sit after the edge
# table, so by convention none is inspected - the gate never has to guess which table is the edge one.

# a テーブル definition table: 5 columns, NO name colliding with id/claim/class/confidence/evidence
cluster_extra_table_def = CLUSTER + """
| table | column | type | null | description |
|---|---|---|---|---|
| PARTMASTER | CODE | varchar | no | Part code |
"""
check(V.check_tier(build(cluster=cluster_extra_table_def)) == [],
      "#NEW1a: a テーブル definition table (5 columns, 0 colliding names) was wrongly reported")

# a 画面ID list: its first column is named "id" - colliding with the edge table, still not inspected
cluster_extra_table_ids = CLUSTER + """
| id | description |
|---|---|
| S001 | Login screen |
"""
check(V.check_tier(build(cluster=cluster_extra_table_ids)) == [],
      "#NEW1b: a 画面ID list sitting after the edge table was wrongly reported")

# a 3-column auxiliary table whose "class" column name collides - green for the same reason
cluster_extra_table_class = CLUSTER + """
| name | class | note |
|---|---|---|
| Role | admin | Holds every permission |
"""
check(V.check_tier(build(cluster=cluster_extra_table_class)) == [],
      "#NEW1c: a 3-column auxiliary table (colliding 'class' name) after the edge table was wrongly reported")

# a header FULLY TRANSLATED into Japanese: it is the first table of the file, so it IS the edge
# table and its header must match exactly
FRONTMATTER = """---
scope: project
subject: legacy-system
---

"""
TABLE_HEADER_JP = """| ID | 主張 | 分類 | 確度 | 根拠 |
|---|---|---|---|---|
| permission-jp1 | Claim bang tieng Nhat | code-behaviour | sourced | located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"` |
"""
errs = V.check_tier(build(cluster=FRONTMATTER + TABLE_HEADER_JP))
check(any("header" in m for m in errs),
      "#NEW1d: a fully Japanese header on the first table was skipped silently")
check(any("主張" in m for m in errs),
      "#NEW1d: the message does not say what header was actually read")

# ======= a file-level note applies only to a file the router declares as a cluster =======

PROSE_PAGE = """---
scope: project
---

# Overview

A prose page with no table at all.
"""


def build_second_page(listed, second=PROSE_PAGE):
    """A minimal tier: one valid cluster (permission.md) plus a second file (overview.md).
    `listed=True` has the router declare overview.md a cluster; `listed=False` does not."""
    d = Path(tempfile.mkdtemp())
    (d / "wiki" / "legacy-system").mkdir(parents=True)
    prose_line = (
        "| legacy-system | [overview](legacy-system/overview.md) | growing |\n" if listed else ""
    )
    (d / "wiki" / "index.md").write_text(ROUTER + prose_line, encoding="utf-8")
    (d / "wiki" / "legacy-system" / "permission.md").write_text(CLUSTER, encoding="utf-8")
    (d / "wiki" / "legacy-system" / "overview.md").write_text(second, encoding="utf-8")
    f = d / "src" / "ASP" / "Common" / "asp"
    f.mkdir(parents=True)
    (f / "FB_GetNinsho.asp").write_text("x\n" * 122 + 'ElseIf RoleCd(0) = "8" Then\n', encoding="utf-8")
    return d


# #NEW2a - a prose page the router DOES list as a cluster -> declared a cluster, it must carry an edge table
errs = V.check_tier(build_second_page(listed=True))
check(any("has no edge table" in m and "overview.md" in m for m in errs),
      "#NEW2a: a prose page listed as a cluster with no edge table was not caught")

# #NEW2b - a prose page the router does NOT list -> red only as an orphan, NOT for a missing table
# (a page never declared a cluster is not forbidden to exist; "orphan cluster" already catches it)
errs = V.check_tier(build_second_page(listed=False))
check(any("orphan cluster" in m and "overview.md" in m for m in errs),
      "#NEW2b: an orphan prose page was not caught by the orphan check")
check(not any("has no edge table" in m for m in errs),
      "#NEW2b: a prose page the router does not list is still forbidden to exist (double-caught with orphan)")

# #3 - a NON-ASCII cluster file name: git ls-tree C-quoting by default makes check_merge falsely
# red on a healthy merge unless core.quotePath is off and splitting is done on NUL
CLUSTER_JP_NAME = """---
scope: project
subject: legacy-system
---

| id | claim | class | confidence | evidence |
|---|---|---|---|---|
| permission-jpname1 | Ten cum tieng Nhat khong duoc lam merge check do gia | code-behaviour | sourced | located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"` |
"""


def build_repo_jp_name():
    d = Path(tempfile.mkdtemp())
    run = lambda *a: subprocess.run(a, cwd=d, check=True, capture_output=True)
    run("git", "init", "-q")
    run("git", "config", "user.email", "t@example.com")
    run("git", "config", "user.name", "t")
    (d / "wiki" / "legacy-system").mkdir(parents=True)
    (d / "wiki" / "index.md").write_text(ROUTER, encoding="utf-8")
    (d / "wiki" / "legacy-system" / "ぶんしょ.md").write_text(CLUSTER_JP_NAME, encoding="utf-8")
    f = d / "src" / "ASP" / "Common" / "asp"
    f.mkdir(parents=True)
    (f / "FB_GetNinsho.asp").write_text("x\n" * 122 + 'ElseIf RoleCd(0) = "8" Then\n', encoding="utf-8")
    run("git", "add", "-A")
    run("git", "commit", "-q", "-m", "seed nhat")
    return d


d_jp = build_repo_jp_name()
errs = V.check_merge(d_jp, ["HEAD"])
check(errs == [],
      f"#3: a non-ASCII cluster name made check_merge falsely red on a healthy merge: {errs!r}")
# POSITIVE assertion: check_merge returns [] because _ids_at REALLY reads the id through the
# non-ASCII path, not for some other reason (the shape that once made case I2 vacuous - [] proves nothing on its own)
check("permission-jpname1" in V._ids_at("HEAD", d_jp),
      "#3: _ids_at could not read the id through a non-ASCII cluster name (errs==[] proves nothing)")


# ============ convention: the FIRST table of the file IS the edge table ============
# No signal separates `table | column | type | null | description` from `iD_ | clam | clss |
# confidance | evidance`, and none separates a table ABOUT evidence from a table CARRYING
# evidence. So the format declares instead of the gate inferring: the first table is the edge
# table, its header must match exactly, every table after it is auxiliary and is never inspected.

EDGE_TABLE = CLUSTER[CLUSTER.index("| id |"):]

TABLE_BROKEN_HEADER = """| iD_ | clam | clss | confidance | evidance |
|---|---|---|---|---|
| permission-brkn1 | Claim voi header hong nang | code-behaviour | sourced | located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"` |
"""
# the same table but with NO cell carrying an evidence prefix - one level more broken
TABLE_BROKEN_NO_PREFIX = """| iD_ | clam | clss | confidance | evidance |
|---|---|---|---|---|
| permission-brkn2 | Claim khong mang tien to evidence | code-behaviour | sourced | xem trong ma nguon |
"""
TABLE_NOTE_2COL = """| name | description |
|---|---|
| Note | An auxiliary table placed before the edge table |
"""

# #HA - first table with a mismatched header, rows carrying NO evidence prefix, and the file DOES
# hold a correct edge table below. Being more broken must not make it easier to slip through; its
# id is still taken, so it must reach _all_ids (R5/R9)
d_ha = build(cluster=FRONTMATTER + TABLE_BROKEN_NO_PREFIX + "\n" + EDGE_TABLE)
errs = V.check_tier(d_ha)
check(any("header" in m for m in errs),
      "#HA: a mismatched first-table header (rows with no evidence prefix) was swallowed silently")
check(any("evidance" in m for m in errs),
      "#HA: the message does not say what header was actually read")
check(V._all_ids(d_ha) == set(),
      "#HA: a file with a mismatched first-table header still yielded an id - the ids of a broken file are UNKNOWN")

# #HA2 - the same shape, this time with rows that DO carry an evidence prefix
errs = V.check_tier(build(cluster=FRONTMATTER + TABLE_BROKEN_HEADER + "\n" + EDGE_TABLE))
check(any("header" in m for m in errs),
      "#HA2: a mismatched first-table header (rows with an evidence prefix) was swallowed silently")
check(any("evidance" in m for m in errs),
      "#HA2: the message does not say what header was actually read")

# #HA3 - the mismatched first table is the ONLY table in the file
errs = V.check_tier(build(cluster=FRONTMATTER + TABLE_BROKEN_HEADER))
check(any("header" in m for m in errs),
      "#HA3: a mismatched first-table header (the only table in the file) was skipped silently")
check(any("evidance" in m for m in errs),
      "#HA3: the message does not say what header was actually read")

# #HB - an auxiliary table EXPLAINING the evidence syntax: its cells open with `absent:`. A page
# ABOUT evidence is perfectly normal in this tier, and it sits after the edge table
cluster_explains_evidence = CLUSTER + """
| form | meaning |
|---|---|
| absent: used when a query returns nothing | Records an absence that was checked |
"""
check(V.check_tier(build(cluster=cluster_explains_evidence)) == [],
      "#HB: an auxiliary table explaining the evidence syntax was misread as a broken edge table")

# #HC - an auxiliary table carrying a domain code `<word>-<5 chars>` in its first column (文書番号,
# 起案番号 ...). That is the natural shape of a code in this domain, not a wiki-tier id
cluster_domain_codes = CLUSTER + """
| code | description |
|---|---|
| bunsyo-00001 | The first document number |
| kian-00010 | A drafting number |
"""
d_hc = build(cluster=cluster_domain_codes)
check(V.check_tier(d_hc) == [],
      "#HC: a domain code in an auxiliary table first column was misread as a broken edge table")
check("bunsyo-00001" not in V._all_ids(d_hc),
      "#HC: a domain code from an auxiliary table leaked into the tier id set (new_id/check_merge read it wrong)")

# #HD - a duplicate id sitting in a mismatched first table must raise BOTH errors: the header
# mismatch and the duplicate against another cluster. check_tier/_all_ids/_ids_at must share ONE
# id-reading path, or an id in a mismatched table takes only the header error and slips the duplicate check
ROUTER_TWO = ROUTER + "| legacy-system | [broken](legacy-system/broken.md) | growing |\n"


def build_two_clusters(header_fixed=False):
    d = build(router=ROUTER_TWO)
    table = TABLE_BROKEN_HEADER.replace("permission-brkn1", "permission-a1b2c")
    if header_fixed:
        table = table.replace(
            "| iD_ | clam | clss | confidance | evidance |",
            "| id | claim | class | confidence | evidence |",
        )
    (d / "wiki" / "legacy-system" / "broken.md").write_text(
        FRONTMATTER + table, encoding="utf-8",
    )
    return d


errs = V.check_tier(build_two_clusters())
check(any("header" in m and "evidance" in m for m in errs),
      "#HD: the mismatched first-table header of the second cluster was not caught")
# The duplicate check for that file WAITS until the header is fixed: the ids of a broken file are
# unknown, and a guessed id makes R9 cry wolf (#C). The file is already red on its header, so nothing slips
check(not any("duplicate id" in m for m in errs),
      "#HD: the gate still guessed an id from a mismatched-header file to conclude a duplicate")
# and the moment the header is fixed the duplicate surfaces - the deferral covers only the broken file
errs_fixed = V.check_tier(build_two_clusters(header_fixed=True))
check(any("duplicate id" in m and "permission-a1b2c" in m for m in errs_fixed),
      "#HD: the header was fixed and the duplicate id was still not reported")

# #HE - a DECLARED consequence of the convention: an edge-shaped table placed AFTER the edge table
# is auxiliary and is not inspected. Position decides, which is why the matching red cases
# (#HA/#HA2) put the broken table FIRST. This case pins the other direction so nobody closes it unseen
check(V.check_tier(build(cluster=CLUSTER + "\n" + TABLE_BROKEN_HEADER)) == [],
      "#HE: a table after the edge table is still inspected - the 'first table only' convention no longer holds")

# #HF - the accepted cost of the convention: an auxiliary table placed BEFORE the edge table turns
# the gate red. The author sees it at once and reorders; in exchange the gate has no grey area
errs = V.check_tier(build(cluster=FRONTMATTER + TABLE_NOTE_2COL + "\n" + EDGE_TABLE))
check(any("header" in m for m in errs), "#HF: an auxiliary table placed before the edge table was not reported")
check(any("name | description" in m for m in errs),
      "#HF: the message does not say what header was actually read")

# #H2 - consistent with the "orphan cluster" rule: a file the router does NOT declare a cluster takes
# exactly one error whatever tables it holds; once declared, a mismatched header becomes its own error
errs = V.check_tier(build_second_page(listed=False, second=FRONTMATTER + TABLE_BROKEN_HEADER))
check(any("orphan cluster" in m and "overview.md" in m for m in errs),
      "#H2: a file the router does not declare a cluster was not caught by the orphan check")
check(not any("header" in m for m in errs),
      "#H2: a file the router does NOT declare a cluster took two errors for one cause (orphan + header)")
errs = V.check_tier(build_second_page(listed=True, second=FRONTMATTER + TABLE_BROKEN_HEADER))
check(any("header" in m and "evidance" in m for m in errs),
      "#H2: a file the router DOES declare a cluster with a mismatched header was not caught")


# ============ the region AFTER the first table ============
# The "only the first table is inspected" convention kills every header grey area, but stopping
# there would turn everything after the first table into a silent blind spot. The three rules below
# close it, each one an exact comparison, none of them reviving inference.

# #A - a legal sample edge table inside a ``` fence, placed BEFORE the real edge table. A fence is
# illustration; reading it as a table makes the sample the first one and the real table below is
# never inspected - the cluster carries a dead path while the gate stays green
CLUSTER_FENCED_EXAMPLE = FRONTMATTER + """The edge-table format of a cluster:

```markdown
| id | claim | class | confidence | evidence |
|---|---|---|---|---|
| permission-vidu1 | An example claim inside the documentation | code-behaviour | sourced | located: `ASP/Common/asp/FB_GetNinsho.asp:123` anchor=`RoleCd(0) = "8"` |
```

""" + EDGE_TABLE.replace("permission-a1b2c", "permission-real1").replace(
    "ASP/Common/asp/FB_GetNinsho.asp:123", "KHONG/TON/TAI.asp:1"
)
check(any("dead path" in m for m in V.check_tier(build(cluster=CLUSTER_FENCED_EXAMPLE))),
      "#A: a fenced sample table was read as the first table - the real edge table is no longer inspected")

# #B - a correct edge table, then a SECOND table whose header matches the edge header exactly.
# Without this rule the second table is swallowed whole: no evidence check, no path/anchor check,
# no duplicate-id check, and its ids never reach _all_ids so `--new-id` can hand them out again
SECOND_EDGE_TABLE = EDGE_TABLE.replace("permission-a1b2c", "permission-scnd1")
errs = V.check_tier(build(cluster=CLUSTER + "\n" + SECOND_EDGE_TABLE))
check(any("only ONE edge table" in m for m in errs),
      "#B: a second edge table (exact header match) was swallowed silently")
check(any("must be the first" in m for m in errs),
      "#B: the message does not say a cluster holds only one edge table and it must be the first")

# #C - a mismatched first table carrying LABEL rows: that file must yield no id at all. A label
# cell is not an id, and a fabricated id like that makes `check_merge` cry wolf about a vanished
# edge the moment the author fixes the column order - R9 red on a correct patch
d_c = build(cluster=FRONTMATTER + TABLE_NOTE_2COL)
errs = V.check_tier(d_c)
check(any("header" in m for m in errs), "#C: a mismatched first-table header was not caught")
check(V._all_ids(d_c) == set(),
      "#C: a file with a mismatched first-table header still produced a fake id from a label cell")


def build_repo_fixed_header():
    """A git repo: the first commit carries a mismatched first-table header (label rows) and the
    working tree has been fixed into a correct edge table. R9 must not report a vanished edge for a label."""
    d = Path(tempfile.mkdtemp())
    run = lambda *a: subprocess.run(a, cwd=d, check=True, capture_output=True)
    run("git", "init", "-q")
    run("git", "config", "user.email", "t@example.com")
    run("git", "config", "user.name", "t")
    (d / "wiki" / "legacy-system").mkdir(parents=True)
    (d / "wiki" / "index.md").write_text(ROUTER, encoding="utf-8")
    (d / "wiki" / "legacy-system" / "permission.md").write_text(
        FRONTMATTER + TABLE_NOTE_2COL, encoding="utf-8")
    run("git", "add", "-A")
    run("git", "commit", "-q", "-m", "header lech")
    (d / "wiki" / "legacy-system" / "permission.md").write_text(CLUSTER, encoding="utf-8")
    return d


errs = V.check_merge(build_repo_fixed_header(), ["HEAD"])
check(not any("disappeared in the merge" in m for m in errs),
      f"#C: check_merge cried wolf about a vanished edge from a fake id in a mismatched-header file: {errs!r}")



# -- the fourth evidence form: an observation on the running system ------------------
# The three older forms carry source text (located), stored data (stored-data) and an absence
# (absent). A claim class about "what the user SEES" needs the running system, which none of them
# can carry - so such an edge could never reach `sourced` while the gate stayed green, exactly what R8 forbids.

EOL = chr(10)
RS_HEAD = FRONTMATTER + "# permission" + EOL * 2 + (
    "| id | claim | class | confidence | evidence |" + EOL
    + "|---|---|---|---|---|" + EOL)

# #RS1 - all three mandatory keys present: a healthy cluster, and running-system counts as VALID
# evidence (the edge is not reported as evidence-less) even though the gate never opens the running system
rs_ok = RS_HEAD + ("| permission-rs001 | The 削除 button is hidden for 権限 4 | screen-display | sourced | "
                   "running-system: account=`u_test01` screen=`起案一覧` "
                   "observed=`the 削除 button is not displayed` |" + EOL)
d_rs = build(cluster=rs_ok)
errs = V.check_tier(d_rs)
check(errs == [], f"#RS1: the gate cried wolf on a valid running-system item: {errs!r}")
check(any("running-system" in n and "running system is NOT re-opened" in n
          for n in V.schema_only_classes(d_rs)),
      "#RS1: schema_only_classes did not declare the running-system class schema-only (R8)")

# #RS2 - a mandatory key missing: must be RED and name the missing key
rs_miss = RS_HEAD + ("| permission-rs002 | The 削除 button is hidden for 権限 4 | screen-display | sourced | "
                     "running-system: account=`u_test01` observed=`hidden` |" + EOL)
errs = V.check_tier(build(cluster=rs_miss))
check(any("running-system" in m and "screen" in m for m in errs),
      f"#RS2: a running-system item missing `screen` was not caught: {errs!r}")

# #RS3 - `anchor` is forbidden for the same reason as stored-data: an anchor is a drift probe on a
# SOURCE FILE, and an observation has no file position to drift
rs_anchor = RS_HEAD + ("| permission-rs003 | The 削除 button is hidden for 権限 4 | screen-display | sourced | "
                       "running-system: account=`u_test01` screen=`起案一覧` "
                       "observed=`hidden` anchor=`RoleCd(0)` |" + EOL)
errs = V.check_tier(build(cluster=rs_anchor))
check(any("running-system" in m and "anchor" in m for m in errs),
      f"#RS3: a running-system item carrying an anchor was not rejected: {errs!r}")

# #RS4 - a misspelled prefix must not degrade silently into a generic error
rs_typo = RS_HEAD + ("| permission-rs004 | The 削除 button is hidden for 権限 4 | screen-display | sourced | "
                     "running_system: account=`u_test01` screen=`起案一覧` observed=`hidden` |" + EOL)
errs = V.check_tier(build(cluster=rs_typo))
check(any("malformed" in m for m in errs),
      f"#RS4: a misspelled prefix (`running_system`) is not reported as an unreadable item: {errs!r}")


# -- R8 on the `class` axis: the gate does not check it, so it must DECLARE that --------
# The class vocabulary is a human law. Not checking it is a decision; staying silent about not
# checking is "passing on a proxy", exactly what R8 calls a defect of the gate.

d_cls = build()
notices = V.unverified_class_checks(d_cls)
check(len(notices) == 2, f"#CL1: there must be EXACTLY two declarations on the class axis, got {len(notices)}")
check(any("class vocabulary" in n for n in notices),
      "#CL1: it never declares that the `class` value is NOT matched against the project vocabulary")
check(any("sources its class requires" in n and "required source" in n for n in notices),
      "#CL1: it never declares that evidence forms are NOT matched against the sources the class requires")

# #CL2 - a made-up class: the gate is GREEN (by design) but the declaration must still be there
cluster_fake_class = CLUSTER.replace("| code-behaviour |", "| banana-class |")
d_fake = build(cluster=cluster_fake_class)
check(V.check_tier(d_fake) == [], "#CL2: the gate suddenly checks `class` - that check does not exist")
check(len(V.unverified_class_checks(d_fake)) == 2,
      "#CL2: a made-up class passed with no declaration at all")

# #CL3 - a tier with no edge: declare nothing; a declaration must not become noise
d_empty = Path(tempfile.mkdtemp())
(d_empty / "wiki").mkdir()
check(V.unverified_class_checks(d_empty) == [],
      "#CL3: the class limits were declared on a tier holding no edge")

# -- §7 `source_encodings`: the source material encodings are a PROJECT value ----------
# The gate used to hardcode an `-E sjis` pass. A per-instance value inside a portable file is what
# `doc-organization.md` §9 forbids; the project now declares it in the router frontmatter.
# The case builds exactly the pair that is needed: a Shift-JIS source file plus a Japanese anchor.
# Declared -> green, undeclared -> red. Without that pair the "one default pass" would be green for
# another reason (an ASCII anchor matches in both encodings), and the case would measure nothing.
JP_ANCHOR = "起案の目録"
_CL_SJIS = CLUSTER.replace('anchor=`RoleCd(0) = "8"`', "anchor=`" + JP_ANCHOR + "`")


def build_sjis(declare):
    d = Path(tempfile.mkdtemp())
    router = ROUTER.replace("source_root:", "source_encodings: sjis\nsource_root:") if declare else ROUTER
    (d / "wiki" / "legacy-system").mkdir(parents=True)
    (d / "wiki" / "index.md").write_text(router, encoding="utf-8")
    (d / "wiki" / "legacy-system" / "permission.md").write_text(_CL_SJIS, encoding="utf-8")
    f = d / "src" / "ASP" / "Common" / "asp"
    f.mkdir(parents=True)
    (f / "FB_GetNinsho.asp").write_bytes(b"x\n" * 122 + ("' " + JP_ANCHOR + "\n").encode("cp932"))
    return d


_d_dec = build_sjis(True)
check(V.check_tier(_d_dec) == [],
      "#ENC1: `source_encodings: sjis` was declared and the Shift-JIS anchor still was not found")
_d_undec = build_sjis(False)
check(any("no longer found" in e for e in V.check_tier(_d_undec)),
      "#ENC2: `source_encodings` was NOT declared yet the sjis pass still ran - the gate still hardcodes an encoding")


for f in fails:
    print("FAIL:", f)
print(f"{len(fails)} fail")
sys.exit(1 if fails else 0)
