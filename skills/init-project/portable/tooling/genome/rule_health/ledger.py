"""The ledger of reviewed findings and of when each file was last scanned.

A finding whose fingerprint is in the ledger is no longer reported. Called by the entry point.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from rule_health.units import normalize

LEDGER = ".agent-workspace/rule-health/ledger.json"
VALID_STATUS = {"fixed", "exempt"}


def _fp_path(p: str, root: Path | None = None) -> str:
    """Repo-relative POSIX form of a path.

    Every ledger key goes through here. An absolute key is machine-specific: it
    misses on a clone, on a renamed directory and in a worktree, so the run
    appends a parallel set instead of updating the existing one.
    """
    s = str(p).replace("\\", "/")
    base = str((root or Path(".")).resolve()).replace("\\", "/")
    # `base` is resolved, so an absolute `p` must be resolved too or the prefix misses:
    # on Windows a temp/8.3 short name and its long form denote one directory and spell
    # it differently, and the key would come out absolute (machine-specific).
    if Path(s).is_absolute():
        try:
            s = str(Path(p).resolve()).replace("\\", "/")
        except OSError:
            pass
    if s.startswith(base):
        s = s[len(base):]
    return s.lstrip("/")


def _is_absolute_key(k: str) -> bool:
    return k.startswith("/") or (len(k) > 1 and k[1] == ":")


def fingerprint(finding: dict) -> str:
    key = "|".join([
        finding["signal"],
        ",".join(sorted(_fp_path(p) for p in finding["paths"])),
        " ".join(normalize(finding.get("text", ""))),
    ])
    if finding.get("target_sha256"):
        key += "|" + finding["target_sha256"]
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def load_ledger(root: Path) -> dict:
    p = root / LEDGER
    if not p.exists():
        return {"entries": {}, "git_cache": {}, "last_scanned": {}}
    data = json.loads(p.read_text(encoding="utf-8"))
    data.setdefault("entries", {})
    data.setdefault("git_cache", {})
    data.setdefault("last_scanned", {})
    # drop keys written by an older revision that used the absolute path
    data["last_scanned"] = {k: v for k, v in data["last_scanned"].items()
                            if not _is_absolute_key(k)}
    return data


def save_ledger(root: Path, data: dict) -> None:
    p = root / LEDGER
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True),
                 encoding="utf-8")


def ledger_problems(ledger: dict) -> list[str]:
    out = []
    for fp, e in ledger.get("entries", {}).items():
        st = e.get("status")
        if st not in VALID_STATUS:
            out.append(f"{fp}: invalid status: {st!r}")
        if st == "exempt" and not e.get("allowed_by"):
            out.append(f"{fp}: an exempt entry has no allowed_by (the §ID that permits it)")
        if st == "exempt" and not e.get("reason"):
            out.append(f"{fp}: an exempt entry has no reason")
    return out


def open_findings(findings: list[dict], ledger: dict) -> list[dict]:
    entries = ledger.get("entries", {})
    return [f for f in findings if fingerprint(f) not in entries]
