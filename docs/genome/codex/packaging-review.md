# Independent review of the Codex skill and packaging surface

Reviewed by the guidance executor, which did not author the reviewed implementation. Scope: the initialization skill, its references and wrapper, package and version scripts, source README and contribution/compatibility documentation, packaging tests and Codex CI. The review compares those files with the accepted independent-product plan and the current deployment CLI. It does not review the main updater's internals or certify fresh model behavior.

## Findings

### PR1 — High: version writes can mutate files outside the selected product

At the reviewed revision, `codex/scripts/sync-version.py` writes each JSON mirror and VERSION through `Path.write_text` without checking links, hard-link count or linked ancestors. A legitimate-looking manifest path can therefore share its backing file with another product. The path-prefix boundary does not protect the other product in this case.

Executed reproduction: a temporary product had its `.codex-plugin/plugin.json` hardlinked to a sibling `other-product.json`, with name `codex-genome` and version `1.0.0`. Calling `run(product, 'set', '1.2.3')` completed and changed the sibling file to `1.2.3`. The reproduction used only disposable files and no real configuration. This contradicts the command's claim to change only the selected independent product.

Correction: validate every input and write target, including VERSION and existing ancestors, before the first write; reject links and unsafe aliases; use safe replacement. Add refusal tests that compare external bytes before and after the attempted version change. Root acknowledged the finding and is implementing a shared product-script safety helper; that remedy has not yet been rereviewed in this record.

### PR2 — Medium: a package output inside its source skill reaches recursive self-copy

At the reviewed revision, `codex/scripts/package.py` permits any nonexistent output directory. It creates that output and then recursively copies the entire source skill. When output is a descendant of `.agents/skills/init-codex-genome`, the just-created destination is inside the tree being copied. This can recursively copy the growing package until a path or resource limit fails, leaving a partial artifact inside the source.

The source trace establishes the recursion. A controlled execution replaced only the external source check and copy primitive: the actual `build` path reached `copytree` with a destination that was a descendant of its source. The probe stopped at that call instead of producing an uncontrolled recursive copy. This is a traced defect with an executed reachability check, not a claim that a full runaway copy was performed.

Correction: reject an output within any recursively copied source tree before creating directories, after resolving safe existing ancestors. Test that refusal leaves the source unchanged. Root acknowledged the finding and is implementing the boundary check.

### PR3 — Medium: the distributed README links to files absent from the distribution

The package builder copies the source README unchanged, but its distribution contains only the plugin metadata, the initialization skill under `skills/`, README, LICENSE and VERSION. The README links to `CONTRIBUTING.md`, `docs/workflow-obligations.md`, `docs/compatibility.md`, `CHANGELOG.md` and `.agents/skills/init-codex-genome/SKILL.md`. None of those links resolves in the packaged layout. The install/update guidance's skill link is therefore unusable for an external consumer even though the skill itself is present elsewhere.

This is established by tracing the builder's copy inventory against the README links. Source links remain correct in the development checkout; the defect is specific to the generated distribution.

Correction: produce a distribution-specific README with the actual `skills/` location and reachable references, or deliberately include and adapt the referenced documentation. Extend packaging tests to validate the built README's local links.

## Checks and non-findings

The skill wrapper resolves its bundle relative to its installed location and supplies that package root for init/update. Recover and source maintenance use their own explicit roots. The skill's two command examples are explicitly alternatives and its apply step reuses the reviewed plan hash. It tells the agent to use existing authorization rather than obtain another permission for a clean installation.

The source-to-package skill layout difference is documented and the compatible manifest points at `skills/`. Production packaging copies from the independent Codex product. CI's independent-product job copies only that product to a temporary parent before running the suite, while coexistence tests are separate and intentionally require the other product. Compatibility documentation distinguishes CLI observations from unavailable desktop certification and does not claim custom-agent registration from parsing alone.

Running `python -m unittest discover -s codex/tests -p test_packaging.py` during this review ran two tests. The version boundary test passed. The external-package test was blocked because the tooling executor was actively changing the live tool and its bundle copy was temporarily stale. The package builder reported that exact drift and refused to build. This is an expected integration-state limit and is not a product finding. Rerun after promotion when the source settles.

The plan hash and adoption CLI were inspected against the current tool parser. Local-edit adoption is still being implemented by the tooling executor, so this review does not certify that unfinished branch. Fresh model execution probes remain owned by the coordinator. No reviewed implementation file was edited by this review.

## Follow-up acceptance

Before closing these findings, execute link/hard-link refusal fixtures for version writes, a nested-output refusal fixture, and a local-link check over the generated README. Then rerun packaging tests after live/bundle synchronization. Reopen the changed code to assess the integrated remedy rather than treating the proposed fix as already verified.

## Recheck of the integrated remedies

All three findings are closed for the reviewed conditions. The reviewer reopened `product_files.py`, `sync-version.py`, `package.py`, the new `PACKAGE.md` and all four packaging tests after the remedies landed.

PR1 is resolved: the version command preflights the selected root, VERSION, plugin metadata and bundle map before changing a mirror. The shared path helper rejects links, reparse points, hardlinks and case aliases along existing path ancestry. Each write uses a checked temporary replacement instead of overwriting a linked target in place. The refusal test reproduces the original hardlink setup and confirms both the outside file and canonical version remain unchanged.

PR2 is resolved: packaging validates the output and skill root, then rejects an output beneath the recursively copied skill before creating output or calling the source check and copy. The regression test uses the formerly dangerous destination and confirms it remains absent after refusal.

PR3 is resolved: the builder now copies `PACKAGE.md` as the distribution's README. Its links use the actual `skills/` tree and included license. The external-package test builds the distribution, checks every local README link, initializes a project through the packaged wrapper and runs the installed verifier.

Executed recheck: `python -m unittest discover -s codex/tests -p test_packaging.py` completed with four tests passing and no skips. The earlier tooling/bundle drift no longer blocks this suite. No reviewed implementation file was changed by the reviewer.

This closes the three reported packaging findings. It does not broaden the review into hostile concurrent filesystem mutation, every possible interruption between version-mirror writes, the deployment updater's separate recovery design or desktop behavior. Those are outside the evidence established by this bounded recheck.
