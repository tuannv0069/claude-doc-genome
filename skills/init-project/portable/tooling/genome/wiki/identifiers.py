"""Edge identifiers: allocating a new one, and checking that a merge lost none.

Called by the entry point for `--new-id` and `--merge-check`.
"""
import secrets
from pathlib import Path

from lib.git import run_git
from wiki.cluster import _all_ids, _iter_ids, _parse_cluster_text

ALPHABET = "abcdefghijkmnpqrstuvwxyz23456789"     # l/o/0/1 dropped - too easy to misread


class GitError(Exception):
    """A git command R9 needs returned a real error code (bad ref, bad path, ...)."""


def new_id(cluster, root):
    """R5: machine-allocated, never derived from content, unique tier-wide.

    People do not invent 5 random characters: a string a human or an LLM makes up skews the
    distribution and collides far sooner than real randomness.
    """
    taken = _all_ids(root)
    while True:
        cand = f"{cluster}-" + "".join(secrets.choice(ALPHABET) for _ in range(5))
        if cand not in taken:
            return cand


def _run_git(args, cwd, what):
    """`args` does NOT include "git" - this function adds it, along with
    `-c core.quotePath=false` (C-quoting of non-ASCII file names is on by default;
    `ls-tree`/`show` must both turn it off, or a name `ls-tree` wrapped in quotes goes straight
    into `show` and the path no longer matches).

    `returncode != 0` is an error, with no exception: `ls-tree`/`show`/`rev-parse` (unlike `git
    grep`, which was dropped from this module) have no "1 means no match but still valid" - a
    pathspec matching nothing in `ls-tree` still returns 0 with empty stdout (measured
    directly). Tolerating code 1 would only turn a real git failure into a silent `[]`, exactly
    the shape of the C3 defect just closed.
    """
    out = run_git(["-c", "core.quotePath=false", *args], cwd)
    if out.returncode != 0:
        raise GitError(f"{what} failed ({out.returncode}): {out.stderr.strip()}")
    return out.stdout


def _repo_context(root):
    """(repo_root, prefix) of `root` within the git tree containing it.

    The relpath is NOT computed with `os.path.relpath` - on Windows, `root` (a `Path` the caller
    built, possibly in 8.3 short-name form) and `git rev-parse --show-toplevel` (always
    normalized) can name the SAME directory while spelling it differently, which makes relpath
    produce a path that "escapes" the repo when it does nothing of the sort. `git rev-parse
    --show-prefix` asks git itself, run with `cwd=root`, so it is right regardless of short or
    long names, symlinks or worktrees.
    """
    top = _run_git(["rev-parse", "--show-toplevel"], root, "git rev-parse --show-toplevel").strip()
    prefix = _run_git(["rev-parse", "--show-prefix"], root, "git rev-parse --show-prefix").strip()
    return Path(top), prefix


def _ids_at(ref, root):
    """Read the tier id set at a git ref - through EXACTLY the path `check_tier` uses
    (`parse_cluster`/`_parse_cluster_text`), never a parallel hand-rolled regex (C4): the old
    `_ids_at` demanded padding whitespace around each cell (`| id |`), so a row written
    `|id|claim|...|` - valid to `parse_cluster` - slipped past it.

    `-z` plus splitting on NUL: a non-ASCII file name (the project domain here is Japanese) run
    through a plain `--name-only` (no `-z`) is C-quoted into an octal string in double quotes;
    feeding that straight into `git show <ref>:<quoted string>` makes the path stop matching -
    `show` then reports a path that does not exist on a perfectly healthy merge.
    """
    root = Path(root)
    repo_root, prefix = _repo_context(root)
    pathspec = f"{prefix}wiki" if prefix else "wiki"
    listing = _run_git(
        ["ls-tree", "-r", "-z", "--name-only", ref, "--", pathspec],
        repo_root, f"git ls-tree {ref}",
    )
    ids = set()
    for relpath in listing.split("\0"):
        relpath = relpath.strip()
        if not relpath or Path(relpath).name == "index.md":
            continue
        text = _run_git(["show", f"{ref}:{relpath}"], repo_root, f"git show {ref}:{relpath}")
        ids.update(_iter_ids(_parse_cluster_text(text)))
    return ids


def check_merge(root, parents):
    """R9: an id present in ANY parent branch must be present in the merge result.

    This is the "missing" direction. All six checks in check_tier belong to the "surplus"
    direction, so an edge lost in a merge leaves the gate perfectly green. A ref or path that
    cannot be read is a FAILURE OF THIS CHECK, not "the tier is empty at that ref" - say so,
    never degrade it into green.
    """
    here = _all_ids(root)
    errors = []
    for ref in parents:
        try:
            ids_at_ref = _ids_at(ref, root)
        except GitError as exc:
            errors.append(f"check_merge could not read ref {ref!r}: {exc}")
            continue
        for missing in sorted(ids_at_ref - here):
            errors.append(f"edge disappeared in the merge: {missing} (present at {ref})")
    return errors
