#!/usr/bin/env node
// update — pull newer portable files from this plugin's bundle into an
// already-initialized project, WITHOUT clobbering un-promoted local edits.
//
// Direction: bundle (genome) → project (live). The reverse of `promote`.
// Only the verbatim portable set is touched; rendered phenotype files
// (CLAUDE.md, index.md, project-authored guides) are never overwritten.
//
// Safety — 3-way compare per file using the project's init-manifest.json:
//   live == bundle                 → UP-TO-DATE (skip)
//   live missing                   → ADD        (copy)
//   live == manifest sha (≠bundle) → UPDATE     (clean overwrite)
//   live ≠ manifest sha (≠bundle)  → CONFLICT   (local edit — skip, report)
//   no manifest entry & live≠bundle→ CONFLICT   (cannot prove untouched)
//
// Usage:
//   node scripts/update.mjs [--project <path>]    # dry-run: report the plan
//   node scripts/update.mjs --apply [--project <path>]   # apply ADD + UPDATE, rewrite manifest
//
// Exit: 0 = up-to-date or applied cleanly · 1 = conflicts need resolution · 2 = setup error.

import { readFileSync, writeFileSync, existsSync, readdirSync, mkdirSync, copyFileSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const BUNDLE_BASE = join(repoRoot, 'skills/init-project/portable');
const TEMPLATE_BASE = join(repoRoot, 'skills/init-project/templates');
const VERSION_FILE = join(repoRoot, 'skills/init-project/VERSION');

// bundle group → live target dir (relative to project root)
const GROUPS = [
  ['rules', '.claude/rules'],
  ['agent-guide', 'docs/agent-guide/general'],
  ['skills', '.claude/skills'],
  ['agents', '.claude/agents'],
];

// template (.tpl) → live rendered file (relative to project root).
// update never overwrites these (rendered phenotype — slots filled per project);
// it only WARNS when the .tpl changed since deploy so the user can re-render manually.
const TEMPLATES = [
  ['CLAUDE.md.tpl', 'CLAUDE.md'],
  ['agent-guide/index.md.tpl', 'docs/agent-guide/index.md'],
  ['docs/index.md.tpl', 'docs/index.md'],
];

function fail(msg) { console.error(`update: ${msg}`); process.exit(2); }

const argv = process.argv.slice(2);
const apply = argv.includes('--apply');
const projIdx = argv.indexOf('--project');
const PROJECT = projIdx >= 0 ? argv[projIdx + 1] : process.cwd();
if (projIdx >= 0 && !PROJECT) fail('--project needs a path');

const MANIFEST = join(PROJECT, '.claude/init-manifest.json');

const sha = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');
const toPosix = (p) => p.split('\\').join('/');

function listFiles(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir, { recursive: true })
    .map((e) => join(dir, e.toString()))
    .filter((p) => statSync(p).isFile());
}

if (!existsSync(BUNDLE_BASE)) fail(`bundle not found at ${BUNDLE_BASE}`);
if (!existsSync(MANIFEST)) {
  fail(`no manifest at ${MANIFEST} — project not initialized by this plugin (run /init-project first).`);
}

const manifest = JSON.parse(readFileSync(MANIFEST, 'utf8'));
const manifestSha = new Map((manifest.files || []).map((f) => [toPosix(f.path), f.sha256]));
const templateSha = new Map((manifest.templates || []).map((t) => [toPosix(t.path), t.sha256]));
const bundleVersion = readFileSync(VERSION_FILE, 'utf8').trim();

const plan = { upToDate: [], add: [], update: [], conflict: [] };

// Template drift: .tpl changed in the bundle since this project was deployed.
// Detect-only — never rewrites the rendered live file (slots are project-specific).
const templateDrift = [];   // { tpl, live, recorded:boolean }
for (const [tplRel, liveRel] of TEMPLATES) {
  const tplFile = join(TEMPLATE_BASE, tplRel);
  if (!existsSync(tplFile)) continue;
  const recorded = templateSha.get(toPosix(tplRel));
  if (recorded === undefined) {
    templateDrift.push({ tpl: tplRel, live: liveRel, recorded: false });   // pre-this-feature manifest
  } else if (recorded !== sha(tplFile)) {
    templateDrift.push({ tpl: tplRel, live: liveRel, recorded: true });
  }
}

for (const [group, liveDir] of GROUPS) {
  const bundleDir = join(BUNDLE_BASE, group);
  for (const bundleFile of listFiles(bundleDir)) {
    const rel = toPosix(relative(bundleDir, bundleFile));        // path within the group
    const livePath = join(PROJECT, liveDir, rel);
    const relLive = toPosix(relative(PROJECT, livePath));         // manifest key
    const bSha = sha(bundleFile);
    const item = { rel: relLive, bundleFile, livePath };

    if (!existsSync(livePath)) { plan.add.push(item); continue; }
    const lSha = sha(livePath);
    if (lSha === bSha) { plan.upToDate.push(item); continue; }
    const mSha = manifestSha.get(relLive);
    if (mSha && lSha === mSha) plan.update.push(item);
    else plan.conflict.push(item);
  }
}

// ---- report ----
const cur = manifest.version || '(unknown)';
console.log(`update plan — project ${cur} → bundle ${bundleVersion}`);
if (cur !== bundleVersion) console.log(`  changelog: see CHANGELOG.md for what changed between ${cur} and ${bundleVersion}`);
console.log(`  up-to-date: ${plan.upToDate.length}  add: ${plan.add.length}  update: ${plan.update.length}  conflict: ${plan.conflict.length}`);
function show(label, arr) {
  if (!arr.length) return;
  console.log(`\n${label}:`);
  for (const i of arr) console.log(`  ${i.rel}`);
}
show('ADD', plan.add);
show('UPDATE', plan.update);
if (plan.conflict.length) {
  console.log('\nCONFLICT (local edit since deploy — not overwritten):');
  plan.conflict.forEach((i) => console.log(`  ${i.rel}`));
  console.log('  → resolve: promote the local change upstream, or overwrite manually after review.');
}
if (templateDrift.length) {
  console.log('\nWARN — template changed since deploy (rendered file NOT auto-updated):');
  for (const t of templateDrift) {
    const why = t.recorded ? '.tpl changed in bundle' : 'no deploy sha in manifest — cannot prove unchanged';
    console.log(`  ${t.tpl} → ${t.live}  (${why})`);
  }
  console.log('  → re-render manually: diff the .tpl against your live file and re-apply structural changes,');
  console.log('    keeping project-specific slot values; or re-run /init-project to regenerate.');
}

if (!apply) {
  const pending = plan.add.length + plan.update.length;
  console.log(`\ndry-run — ${pending} file(s) would change. Re-run with --apply to write.`);
  process.exit(plan.conflict.length ? 1 : 0);
}

// ---- apply ----
let written = 0;
for (const i of [...plan.add, ...plan.update]) {
  mkdirSync(dirname(i.livePath), { recursive: true });
  copyFileSync(i.bundleFile, i.livePath);
  manifestSha.set(i.rel, sha(i.livePath));   // refresh provenance
  written++;
}
manifest.version = bundleVersion;
manifest.files = [...manifestSha].map(([path, sha256]) => ({ path, sha256 }));
writeFileSync(MANIFEST, JSON.stringify(manifest, null, 2) + '\n');
console.log(`\napplied — ${written} file(s) written, manifest → ${bundleVersion}.`);
if (plan.conflict.length) console.log(`${plan.conflict.length} conflict(s) left for manual resolution.`);
process.exit(plan.conflict.length ? 1 : 0);
