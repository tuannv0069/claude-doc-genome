---
name: init-project
description: Set up a new Claude Code project's documentation system when the user asks to initialize project docs, deploy the documentation standard, khởi tạo bộ tài liệu agent, or run /init-project. Use update for an initialized project. Use check and promote only in the genome's source repository to compare and synchronize its live files and distribution bundle. This skill does not author individual skills or project deliverables.
---

# Initialize the project documentation system

## §1 Purpose and boundaries

This skill installs reusable workflow guidance and the project-specific indexes that make it reachable. A project is initialized once, then maintains its own instructions and can request later bundle updates. Existing project requirements remain owned by the project throughout installation and maintenance.

Locate this skill's installed directory before reading the bundle or running a maintenance script. Paths beginning with `portable/` and `templates/` below are relative to the skill directory. The `scripts/` directory is at the plugin repository root. Never make a deployed project's guidance depend on a path inside the plugin installation.

Keep temporary scans, plans and verification output in `.agent-workspace/tasks/<task-slug>/` in the target project. Place finished project deliverables in their project-owned work-product area.

## §2 Modes

| Invocation | Target | Responsibility |
|---|---|---|
| `/init-project` | A project that has not been initialized | Install the bundle, merge project indexes and verify the result. |
| `/init-project update` | An initialized project | Bring in a newer bundle while preserving local changes and updating project-owned routing. |
| `/init-project check` | The genome source repository | Compare portable live files with their bundle copies and report drift. |
| `/init-project promote` | The genome source repository | Synchronize reviewed live changes into the bundle. |

Do not rerun initialization over an initialized project as a substitute for resolving an update. Check and promote require the source repository's live deployment; without that deployment, there is no trusted live side to compare.

## §3 Distribution map

Copy portable files without changing their contents. Templates are project-owned after rendering, so they require a different update procedure.

| Bundle group | Project destination |
|---|---|
| `portable/rules/` | `.claude/rules/` |
| `portable/guide/` | `.agent-workspace/guide/general/` |
| `portable/roles/` | `.agent-workspace/guide/roles/` |
| `portable/tooling/` | `.agent-workspace/tooling/` |
| `portable/skills/` | `.claude/skills/` |
| `portable/agents/` | `.claude/agents/` |

The bundle distributes no role. The `portable/roles/` group holds one file, the role template `_template.md`, which is copied beside the role router as `role-selection.md` §6 requires. Every role in a project is established during initialization under §4 and belongs to that project. The role router `index.md` is a rendered template, not a portable file. The `portable/tooling/` group holds the tool group `genome/`, which is copied to `.agent-workspace/tooling/genome/` with its index, its tools and their tests, as `tooling.md` §2 and §3 describe; the tool router beside it is a rendered template that lists the project's own groups. Empty optional skill or agent groups do not require placeholder files. A project's own tools, roles, skills and agents are not automatically eligible for promotion.

| Template | Rendered destination |
|---|---|
| `templates/CLAUDE.md.tpl` | `CLAUDE.md` |
| `templates/guide/index.md.tpl` | `.agent-workspace/guide/index.md` |
| `templates/docs/index.md.tpl` | `docs/index.md` |
| `templates/lessons/index.md.tpl` | `.agent-workspace/lessons/index.md` |
| `templates/roles/index.md.tpl` | `.agent-workspace/guide/roles/index.md` |
| `templates/decisions/index.md.tpl` | `.agent-workspace/decisions/index.md` |
| `templates/wiki/index.md.tpl` | `.agent-workspace/wiki/index.md` |
| `templates/tooling/index.md.tpl` | `.agent-workspace/tooling/index.md` |

Render the wiki index only when the wiki module applies. The remaining indexes are part of the core deployment. The docs index is always rendered, because the run record of §9 and, in a project without a research category, the role research record each register a category in it. The manifest tracks template source hashes even when an optional rendered index is not needed yet. The tool router template is the exception: the updater does not track it, so compare it with the rendered router by hand when the bundle changes.

## §4 Initialize a project

### Establish the project facts

Inspect the project's existing instructions, repository structure, runtime configuration and documentation. Determine which values are supported by those sources and which still need the user's input. Identify any existing files that would receive template content before writing them.

Two facts are settled with the user before any other question, in the order below, because the rest of the initialization depends on them.

**Conversation language.** Look for written material in the project first: an existing `README.md` or `CLAUDE.md`, documentation, source comments, commit messages, and the language of the user's own request. When the project contains written material, take its language as the proposed default and ask the user, in that language, to confirm or change it. When the project holds no written material — an empty repository, or only generated and configuration files — ask which language to use before asking anything else. Conduct the rest of the interview and the later reports in the confirmed language, and record it as the default conversation language in the `language` section of `CLAUDE.md`. The confirmation applies to conversation; the genome files stay in English under `claude-md-standards.md` §1.

**Nature of the work and the assistant's role.** Ask what the main work of the project is and which role the assistant takes in it. The repository's technical contents do not answer this question: a project with `package.json` may exist to publish videos, and a project of Markdown files may exist to specify software. Offer common kinds of work as examples and accept an answer outside the list: software development; content creation for video, audio, blog or social channels; writing and editing of books, articles or documentation; research and analysis; translation and localization; teaching and course design; data analysis and reporting; product, project or business management; marketing and sales; graphic, interface or product design; legal, finance or accounting work; operations and automation; consulting and advisory work; personal knowledge management. A project often combines several of these; establish which one is the main work and which are supporting tools. Ask also how the assistant should work in it: a job title, a persona the project defines, or a plain description of the perspective to take. This answer describes the assistant's standing identity in the project; the working roles it takes task by task are established in "Establish the roles" below.

Each of these questions — the main work, the supporting tools, the assistant's role — ends with the same last option: "I am not sure; suggest one from what is already known about the work." A user who has not settled the direction can choose it instead of guessing. When it is chosen, propose one concrete answer with a short reason, built from the evidence gathered so far — the repository's contents, the answers already given, the user's request — and ask the user to accept or change it. The proposal is a suggestion until the user confirms it; a value settled this way is recorded like any other answer, and §8 treats it as coming from the user because the user accepted it.

Record the answer in three places. First, the purpose paragraph of `CLAUDE.md` (the `PROJECT_PURPOSE` slot) states what the project exists to produce, the kind of work that produces it, the role the assistant takes, and which technical parts of the repository are tools serving that work rather than the work itself, as `claude-md-standards.md` §1 requires. Second, the confirmed main work and its supporting work are the input to the role research in "Establish the roles" below, whatever the kind of work is. Third, the answer is evidence for the optional modules in §7.

Fill `AGENT_MODEL_TIERS` with a table that maps the standard, strong and highest tiers of `orchestration-policy.md` §3 to a model and a reasoning effort the installed environment supports, and confirm the mapping with the user; add a sentence naming any model the user reserves for their own explicit choice, and one saying where the environment sets effort.

Establish how code is written in the project, because `writing-code.md` §2 and `tooling.md` §2 read these facts from the entry point. Inspect the repository for the languages its code and scripts are written in, for a configured formatter, linter and test runner, and for folders of tools that serve the product. Record in the `stack` slots, for each language, the style standard the project follows and the commands that format, lint and test the code, and record each product tool folder; ask the user about a language whose standard the repository does not show. Record a command only after confirming that the tool it calls is installed or declared by the project. Fill `TOOL_GROUP_ROWS` and `PRODUCT_TOOL_ROWS` of the tool router with the `genome/` group and with the product tool folders found, and write that no product tool folder exists when none does.

Use the available evidence and the user's stated preferences to fill the remaining template slots. Ask only about necessary information that remains unresolved, such as ownership boundaries or a wiki source root. Do not invent a port, language choice or source directory. If a value cannot be established, preserve an explicit TODO and report that the corresponding setup is incomplete.

Select optional modules using §7. A module needs evidence from the project or the user's request; uncertainty alone does not justify adding it.

### Install the shared files

Create the required destinations in §3, then copy the bundle's portable files into them. Preserve existing local files that differ from the incoming content until their differences have been reviewed. Installation must not silently erase project work.

When a complete project genome already exists under `.agent-workspace/`, reuse its guide, role, lesson, decision and wiki files instead of copying or rendering another set over them. Install only the Claude-specific adapter, rules, skills, agents and non-conflicting tooling. Verify that every shared portable file and required router named in §3 exists; a partial workspace requires reviewed migration rather than selective filling. This is the deployed collaboration space for every supported agent, not a Codex-owned foreign tree.

Add `.agent-workspace/tasks/` and `.agent-workspace/worktrees/` to the project's ignore rules without replacing its existing ignore entries. These locations hold working state and temporary checkouts rather than distributed guidance.

### Establish the roles

The roles are established after the main work is confirmed and the role template is installed. `role-selection.md` §8 owns the method: what is researched, how the proposal is derived, what the user decides and what a role file must trace to. This subsection gives the order of the work and what each step hands to the next.

When the shared workspace was reused under "Install the shared files" and its role index already has rows, skip this subsection and report the existing roles to the user, who can ask for them to be established again under `role-selection.md` §8.

1. Research. Take the confirmed main work and each supporting kind of work that the assistant will actually perform. Research each one under `role-selection.md` §8 and write the role research record at the location that section names. When that location is a new category, keep its row for `CATEGORY_ROWS` of the docs index, which is rendered in "Merge the project indexes". This step needs a search or browsing tool; when the environment has none, ask the user for sources, and follow the fallback in `role-selection.md` §8 when none are supplied.
2. Proposal. Present the proposal that `role-selection.md` §8 defines to the user as one table in the confirmed conversation language, with the responsibilities that were left out and their reasons listed below it.
3. Selection. The user selects, renames, merges or adds roles, and states the decision authority of each role whose work ends in a decision. The assistant does not continue to the next step on an assumed selection.
4. Authoring. Write one role file for each selected role from `.agent-workspace/guide/roles/_template.md`, in the group folder of the work it serves, and render `.agent-workspace/guide/roles/index.md` from its template with the group tables as `ROLE_GROUP_TABLES`. Give the project's creative roles the additions in `creative-work.md` §7 when the creative work module applies.
5. Check. Dispatch the independent reader that `role-selection.md` §8 requires, at the strong tier of the mapping settled for `AGENT_MODEL_TIERS`, with the role research record, the user's selection, the role files and the rendered role index. The reader reports each statement in a role that the record or a project source does not support, each selected responsibility that no role carries, and each role that the index names as a checking role for its own work.
6. Correction. Correct the role files and the role index from the reader's report, then run `python .agent-workspace/tooling/genome/verify_role_files.py`.

This subsection ends with a short report to the user: the roles written, the authority recorded for each role whose work ends in a decision, and any role whose basis is still marked `unverified`.

### Merge the project indexes

Render the applicable templates using the established project values. When a target already exists, merge the new structure with its existing requirements instead of replacing the file. Preserve release procedures, scope boundaries, domain requirements and other project-owned facts unless the user has authorized changing them.

The lesson template needs no slot values. The role index was rendered in "Establish the roles"; its slot `ROLE_GROUP_TABLES` holds one `### §1.N <Group name> — \`<group-folder>/\`` subsection for each work group, holding one sentence that says what work the group covers and a table with the header `| work type | primary role | checking roles |` and one row for each work type. The decision index needs the project's entry-count review threshold. The wiki index needs the material root, subjects, claim classes, evidence axes and conservation checkpoint. Fill `WIKI_CLASS_SEPARATOR` with a Markdown table delimiter row containing one cell for each of the two fixed columns and each evidence axis. Check that every claim-class row has the same number of cells. Validate those values against the evidence model in `.claude/rules/wiki-tier.md` before accepting the wiki setup.

Create project-specific optional guidance only for confirmed modules. Give each new guide a router entry and determine whether it also needs a pre-action trigger according to `.claude/rules/doc-organization.md` §10. Keep the trigger and its target in the same change.

### Record and verify the deployment

After the files and indexes are correct, generate their manifest with:

```sh
node <plugin-root>/scripts/init-manifest.mjs --project <project-root> --modules <comma-separated-modules>
```

When §4 reused an existing shared genome, add `--reuse-shared-workspace`. The manifest then records only the files this Claude adapter installed and updates continue to leave the shared files under their existing updater ownership.

The manifest records the installed bundle version, file hashes, template source hashes and selected modules. Generate hashes from the actual installed files; do not invent them or use a manifest refresh to conceal unreviewed differences.

Run the verification in §8. Initialization is complete only when required values are resolved, routing works and the deployed gates accept the installed artifacts. A copied tool that fails against its copied data is a deployment problem to investigate, not proof that the tool should be ignored.

## §5 Check and promote in the source repository

Compare every portable file in §3 with its live counterpart using content hashes. Check both directions so that a removed file or a new candidate is visible. Distinguish project-owned additions from portable changes; a filename alone does not establish ownership.

For a wording or behavior change, edit the live source first and verify it there. Promote the reviewed content into the matching bundle path. If a portable file is removed or renamed, update its referrers and migration handling in the same change. Keep project-owned routers out of the portable copy operation.

Template and skill-body edits are made directly in their source files. They are not recovered by copying the live project phenotype back into the templates, because that would distribute project-specific values.

When preparing a version change, use `node scripts/sync-version.mjs set X.Y.Z`. A removed or renamed portable contract requires a major version; additive compatible content requires a minor version; wording corrections without contract changes require a patch version. Version preparation does not authorize a commit, push, tag or release.

## §6 Update an initialized project

Run the updater from its installed plugin location. It finds the bundle relative to its own script, while `--project` selects the project to update.

```sh
node <plugin-root>/scripts/update.mjs --project <project-root>
```

Review additions, updates, retired files, local conflicts and template changes before applying them. The updater compares the new bundle, current project files and hashes recorded at deployment. A local edit is preserved when it cannot be identified as the unchanged deployed copy. Retired portable files can be removed automatically only when manifest ownership and the current hash prove that they are unchanged genome files.

A project initialized from a bundle older than 7.0.0 holds roles that its manifest records as genome files. The current bundle distributes no role, so the plan lists each unchanged one under `remove` and each locally edited one under `conflict`. Those roles now belong to the project and an update does not delete them. Before applying, change `scope: portable` to `scope: project` in the frontmatter of each such role file and delete that file's entry from `files` in `.claude/init-manifest.json`, then run the plan again and confirm that no role file appears under `remove` or `conflict`. Remove a role only when the user asks for it, together with its router rows and handoffs, as `role-selection.md` §5 requires. The roles a project already has are not rewritten by an update; the user can ask for them to be re-established under `role-selection.md` §8.

A project initialized from a bundle older than 8.0.0 has its genome tools directly under `.agent-workspace/tooling/` and no tool router. The plan lists each unchanged old tool under `remove` and its replacement in `genome/` under `add`. Compare a tool listed under `conflict` with its replacement, carry over a local change that is still needed, then delete the old file. Move the project's own scripts from that folder into a project group under `tooling.md` §2. Render `.agent-workspace/tooling/index.md` from `templates/tooling/index.md.tpl`, establish the code facts of §4 in the `stack` section, and replace every remaining reference to an old tool path.

Resolve conflicts by comparing their actual content. Merge useful local changes or promote them upstream when appropriate. Do not replace a locally edited file merely to obtain a clean status. Unknown or legacy paths need an explicit ownership review rather than automatic deletion.

Merge changed templates into their project-owned targets manually, preserving slot values and project requirements. Remove references to retired files, add routes for new guides and roles, and create any required storage roots. When merging `roles/index.md.tpl`, the project's existing group tables under §1 are the value of `ROLE_GROUP_TABLES` and are kept; a role transferred to the project as described above is not a retired file. A portable copy alone does not make a new guide reachable.

Apply the reviewed portable changes with:

```sh
node <plugin-root>/scripts/update.mjs --apply --project <project-root>
```

After reviewing and merging all template changes, acknowledge their source hashes with:

```sh
node <plugin-root>/scripts/update.mjs --apply --acknowledge-templates --project <project-root>
```

The acknowledgement records a completed manual template review; it does not perform the merge. Do not use it to dismiss unhandled template changes. The updater keeps the previous completed version while conflicts or unacknowledged template changes remain. Read the complete report rather than using the version field alone to judge success.

Finally, run §8 against the resulting project and verify both new and removed references. Do not rerun the manifest generator solely to make conflicts disappear.

## §7 Optional modules

| Module | Evidence that it is relevant | Project-owned result |
|---|---|---|
| Runtime | The project runs a development server, as shown by its scripts or runtime configuration. | Write a local runtime guide describing the actual startup, ports and shutdown procedure. |
| Browser tests | The project contains an installed browser test tool, its configuration or an existing test suite. | Write guidance for that tool and connect it to the tasks that run those tests. |
| Wiki | The project investigates external subject material and needs established claims preserved across tasks. | Render the wiki index using the project's material root, claim classes and evidence requirements. |
| Creative work | The project's main work is text or images meant to engage an audience (scripts, narration, titles, thumbnails, posts), as stated in its purpose paragraph. | Name the creative work, the audience and the locations of the taste store and reference store in `CLAUDE.md` or the project's style instructions, and point its creative-writing trigger to `.agent-workspace/guide/general/creative-work.md`; create an appeal-review agent that performs `creative-work.md` §6 for the project's audience; give the project's creative roles the additions in `creative-work.md` §7. |

A project can add a skipped module later when evidence of the need appears. Detailed Git or release policies also belong to the project. Only a pattern proven useful across projects becomes a candidate for the portable bundle.

## §8 Verification and completion

Check that each distributed file reached the destination in §3, portable content matches the bundle, metadata is valid and template slots have been resolved. Confirm that the purpose paragraph and the default conversation language in `CLAUDE.md` come from the user's answers in §4, not from inference. Confirm that the role index has a work group for the main work with at least one row and that every role file carries `scope: project`. For each role established under `role-selection.md` §8 in this run, confirm that the locators in its §8 resolve into the role research record or a project source and that a role whose work ends in a decision states the authority the user gave it; report a role whose basis is marked `unverified` as unresolved setup. After an update, report a role that predates `role-selection.md` §8 as not yet established from research and leave it unchanged. Confirm that the `stack` section names the style standard and the format, lint and test commands of each language the project's code uses, or says that the project has none, and that the tool router lists the `genome/` group and each product tool folder. Confirm that root triggers resolve to real files and that each guide or role is reachable through the appropriate router. Check that retired files no longer have active referrers.

Run these tools from the target project root:

```sh
python .agent-workspace/tooling/genome/verify_lesson_router.py
python .agent-workspace/tooling/genome/verify_role_files.py
python .agent-workspace/tooling/genome/verify_decision_log.py
python .agent-workspace/tooling/genome/verify_wiki.py
python .agent-workspace/tooling/genome/verify_no_task_links.py
python .agent-workspace/tooling/genome/verify_tool_groups.py
python .agent-workspace/tooling/genome/run_tests.py
```

The last command runs every test of the `genome/` tool group; `.agent-workspace/tooling/genome/index.md` describes each tool. Read `.agent-workspace/guide/general/rule-health.md` before using `scan_rule_health.py`; its report requires interpretation and does not certify every aspect of the project.

A fresh lesson store and decision journal are valid with no entries. A project without the wiki module may have no wiki directory. Missing required data in an enabled module remains incomplete work.

Record which checks actually ran and any unresolved setup. Completion requires the installed content, routing and manifest to agree; a command that exits successfully is only one part of that evidence.

## §9 Run record

Initialization and update keep a per-step record of active time and token cost under `.agent-workspace/guide/general/workflow-measurement.md` §3. The record is appended as JSON Lines to `docs/workflow-runs/init-project.jsonl` in the target project, one line for each execution of a step; the `docs/workflow-runs/` category gets its row in `docs/index.md` when that index is rendered, or on the first update that finds no such row. The `workflow` field is `init-project` followed by the bundle version in `VERSION`.

Take the start and end times from the system clock when a step starts and ends. Take token counts from the usage record of the environment that ran the step, after checking that it exists as `workflow-measurement.md` §4 requires: Claude Code keeps a usage block for each model response in the session transcript and reports the total tokens and duration of a delegated agent in that agent's result. Write the token fields as not measured, with the reason, when the environment keeps no such record. A step that a script performs records its duration and has no token count. Waiting for the user's answer is not active time, and a step that a person performs has its time and token fields written as not applicable.

| mode | step | covers | performer | starts when | ends when |
|---|---|---|---|---|---|
| init | `facts` | Inspecting the project for §4 | main agent | the skill is invoked | the supported values and the open questions are listed |
| init | `interview` | Conversation language, main work, assistant's identity, model tiers and remaining slots | main agent, with a person answering | the first question is asked | the last answer is confirmed |
| init | `install` | Copying the shared files and adding the ignore rules | main agent | the first destination is created | the last portable file is copied |
| init | `role-research` | Step 1 of "Establish the roles" | main agent or a delegated agent | the first source is searched for | the role research record is written |
| init | `role-proposal` | Step 2 | main agent | the record is complete | the proposal is shown to the user |
| init | `role-selection` | Step 3 | a person | the proposal is shown | the selection and the authorities are stated |
| init | `role-authoring` | Step 4 | main agent | the selection is stated | the last role file is written |
| init | `role-check` | Step 5 | a delegated agent | the reader is dispatched | the reader's report is returned |
| init | `role-correct` | Step 6 | main agent | the report is returned | the role verifier exits |
| init | `indexes` | Rendering and merging the remaining templates and optional guidance | main agent | the first template is rendered | the last index is merged |
| init | `manifest` | Generating the manifest | a script | the command starts | the command exits |
| init | `verify` | §8 | main agent and scripts | the first check starts | the checks and unresolved setup are recorded |
| update | `plan` | The updater's dry run | a script | the command starts | the command exits |
| update | `review` | Reading the plan, resolving conflicts and keeping the project's roles | main agent | the plan is printed | no unreviewed item remains |
| update | `apply` | Applying the portable changes | a script | the command starts | the command exits |
| update | `template-merge` | Merging changed templates into their targets | main agent | the first template is compared | the last target is merged |
| update | `template-acknowledge` | Acknowledging the merged templates | a script | the command starts | the command exits |
| update | `verify` | §8 | main agent and scripts | the first check starts | the checks are recorded |

A step that runs again in the same run gets a new line. After the first run under this design, confirm that the record has a line for every step that ran, as `workflow-measurement.md` §6 requires.
