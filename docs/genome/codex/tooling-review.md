# Independent tooling review

Review target: `codex/.agent-workspace/codex/tooling/genome.py`, against implementation plan §4 and §6. This review was performed while the implementation agent was still changing the file. No product files were edited by the reviewer. Reproduction script: `review_tooling.py`; machine evidence: `tooling-review-evidence.json` in this task directory.

## Final disposition

All seven concrete findings below are resolved on the independently rechecked snapshot `d699a4a7eaabb9f3812c835788bd3d8cd86c7f4e373356bcf4271aa28694ee4e`. The history below explains the findings; it does not list open release blockers. The final evidence JSON records eleven scenarios, including a passing baseline and the appropriate failures, conflicts or warnings for adversarial cases. Truncated bundle init leaves the target empty; corrupted recovery payloads are rejected before replay; unreachable guide cycles fail; nested overrides are observed and preserved.

The reviewer also ran `python -m unittest discover -s codex/tests -p test_genome.py -v`: 28 tests ran, 27 passed and one symlink creation test was skipped because Windows did not grant that privilege. The actual Windows junction test passed. The suite includes truncated init/update, safe retirement versus changed bundles, source additions, conflict resolution, locks and interrupted recovery.

No unresolved reproduced defect remains in this bounded tooling review. This is not a guarantee against an adversarial process racing every filesystem operation, and it does not replace live Codex behavior, distribution, coexistence or the parent review. In particular, nested project instructions are surfaced for separate integration review rather than rewritten automatically.

An additional smoke used the actual complete product bundle at snapshot `daae1127eeac82f36573160a6bf0cf77aa192a5b10cff64c4d0808a35293d112`. It initialized a disposable project with 39 manifest entries, verified 37 Markdown files, and produced zero conflicts or changes on the repeated update. Neither `.claude` nor `CLAUDE.md` was created. See `review_actual_bundle.py` and `tooling-actual-bundle-evidence.json`. The independent adversarial fixtures were rerun after this source change and retained their expected results.

## Findings

### 1. Source and bundle inventory could pass with missing or retired content

The initial reviewed implementation (`714b1dde6fd38dbaccb2f7900da592aaacd88cf6b76b2363273a35c3ef3b02c1`) checked only entries already present in the bundle map. Adding a live rule without a map entry and an extra retired file in `bundle/portable` still returned `status: pass`. Promotion with map refresh retained the retired file and the next check also passed.

The implementation agent corrected this during review. At `94a787e3983d70847ea37c23a90ae265ead0b8fbe2eb56e29ea8eff5fb0279ee`, the reproduction correctly rejects these two untracked cases before mutation. Retirement now depends on the old map's hash. This particular reproduction is resolved, subject to final regression tests.

The inventory still scans a fixed set of flat directories. The product's `doc-system-mechanics.md` §3 permits new guide work areas. Such a portable file under `guide/<new-area>/` is outside `refreshed_map` discovery, and verification only requires general-guide leaves to be routed. The inventory and reachability gate must cover the supported area model or reject unsupported areas explicitly.

### 2. The verification command can report pass with the entire core missing

Fixture: create only root AGENTS with a managed region mentioning the three primary routers and five empty router files with project frontmatter. Omit every rule, general guide and role. `verify()` reports `pass`, six files and zero errors. The current unit test treats this skeleton as valid.

This is a release-gate false positive if `verify` is used as install or package completeness evidence. Add a separate required-core contract and validate it, or distinguish a narrowly named pointer-lint result from a mandatory completeness gate. Root routing obligations also need checking against their intended targets; the presence of a filename substring anywhere in AGENTS does not show that the required managed entrypoint exists.

### 3. Foreign ownership does not protect generated `.gitignore` edits

Fixture: a Claude manifest records `.gitignore` in its file roster and the file already exists. The current legacy inventory ignores that entry because its heuristic only collects strings containing a slash or equal to AGENTS.md. The resulting Codex init plan has no conflicts and proposes a write to `.gitignore`.

The generated ignore-region branch also sits outside the bundle loop's foreign-owner check. Parse manifest file ownership, including root paths, and apply the ownership check to generated files too. A shared file owned as a whole by another updater cannot safely acquire a region owner without a reviewed transfer or coexistence contract.

### 4. Nested instruction overrides are not inventoried

Fixture: an otherwise empty project contains `subproject/AGENTS.override.md`. Codex init reports no warning or conflict and does not record the nested file in its observations. The plan explicitly requires checking nested AGENTS and overrides because they change the effective chain for later CWDs.

The installer should inventory and surface these files with the appropriate integration/verification requirement. It must preserve them; an unconditional removal or overwrite would not resolve the issue. The existing root override guard works, but does not cover this case.

## Safety properties inspected without a new defect in this pass

The main deployment path uses explicit project roots, rejects traversal, Windows aliases, reparse points and hard links, preserves unowned files, hashes managed regions rather than the full AGENTS file, keeps project-owned seed contents, blocks source-template changes without acknowledgment, checks file observations before apply, uses an exclusive update lock, retains a journal after interrupted writes, and refuses recovery over later edits. Current tests cover representative cases of these mechanisms. This inspection is not an adversarial OS-level race proof.

Remaining review limits include malformed or manually modified recovery journals, filesystem races outside the updater lock, and behavioral proof that a newly installed instruction chain is followed. The core verification finding above means a clean mechanical result alone is not completion evidence.

## Follow-up findings and fixes in progress

### 5. Recovery did not verify stored payload hashes

Reproduction: interrupt init after AGENTS is written, change only the journal entry's `before_base64` to different bytes while keeping `before_sha256` unchanged, then run the recovery dry-run and apply with its reported plan hash. Recovery returned `recovered`, wrote the corrupted bytes over the original human AGENTS instructions, and deleted the journal. Evidence case: `recovery_payload_hash_mismatch`.

This is a payload-integrity problem even when no adversary is involved: a damaged journal should fail closed, not become a trusted restore source. The tooling agent is adding schema, path uniqueness, strict base64 and hash validation before replay.

### 6. A generic incoming-link check accepts unreachable router cycles

After generalizing guide-area validation, a new fixture creates two area hubs that point to each other. One hub points to a leaf. Neither hub is reachable from the root guide router. Verification still passes. The fixture first verifies the same core corpus without the cycle, then verifies it with the unreachable cycle; both passed. Evidence case: `unreachable_router_cycle`.

Reachability must be computed from the root router with the allowed hub depth, not from the existence of any incoming pointer. The finding was sent to the tooling agent.

### 7. A truncated bundle map can authorize removal of the core

The parent reviewer identified that the bundle loader currently requires only the AGENTS region. Code inspection confirms that an init with such a map can be marked complete, and an update from a complete installation would regard omitted portable core files as retired. Verification catches missing core files only after deployment.

The deployment preflight must require the core corpus and necessary router seeds before proposing writes or retirement. The same structural contract should serve bundle validation and install verification. This is separate from the missing-core verification finding: a failing after-the-fact gate does not prevent destructive retirement from an incomplete package.

### Recheck status during implementation

The original unmapped/orphan inventory fixture, missing-core verification fixture, foreign-owned `.gitignore` fixture, nested override fixture and new portable guide-area discovery fixture now fail safely or report the expected observation on the evolving implementation. The broader rule corpus unit run passed 22 tests, with the Windows symlink-creation case skipped due to host privileges; an actual Windows junction guard test passed. The payload, router-cycle and truncated-bundle follow-ups still require final rerun after their fixes land.

## Coordination

Findings were sent directly to `/root/codex_tooling` as they were reproduced. Final acceptance requires rerunning the independent fixtures and the implementation tests after that agent's fixes. The hashes and findings above describe observed snapshots, not a claim that the evolving final implementation still contains all listed issues.
