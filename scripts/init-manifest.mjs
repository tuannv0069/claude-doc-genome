#!/usr/bin/env node
// init-manifest — write `.claude/init-manifest.json` for a project that has just
// had the bundle copied into it (SKILL.md workflow step 6).
//
// The manifest is not decoration: `update.mjs` reads `files[].sha256` to tell a
// clean UPDATE from a local edit it must not clobber. A hand-written sha is a
// silent CONFLICT or a silent overwrite later, so this is computed, never typed.
//
// Usage: node scripts/init-manifest.mjs [--project <path>] [--modules a,b]
// Exit:  0 = written · 2 = a bundle file has no live counterpart (copy step incomplete)

import { readFileSync, writeFileSync, readdirSync, statSync, existsSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, relative, dirname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const BUNDLE = join(repoRoot, 'skills/init-project/portable');
const TEMPLATE_BASE = join(repoRoot, 'skills/init-project/templates');
const VERSION_FILE = join(repoRoot, 'skills/init-project/VERSION');

// MUST stay identical to GROUPS / TEMPLATES in scripts/update.mjs — update.mjs
// reads what this writes, and a divergence shows up as a phantom CONFLICT.
const GROUPS = [
  ['rules', '.claude/rules'],
  ['guide', '.agent-workspace/guide/general'],
  ['skills', '.claude/skills'],
  ['agents', '.claude/agents'],
];
const TEMPLATES = ['CLAUDE.md.tpl', 'guide/index.md.tpl', 'docs/index.md.tpl', 'lessons/index.md.tpl'];

const argv = process.argv.slice(2);
const arg = (flag) => { const i = argv.indexOf(flag); return i >= 0 ? argv[i + 1] : undefined; };
const PROJECT = arg('--project') ?? process.cwd();
const modules = (arg('--modules') ?? 'core').split(',').map((s) => s.trim()).filter(Boolean);

const sha = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');
const posix = (p) => p.split(sep).join('/');
const walk = (d) => !existsSync(d) ? [] :
  readdirSync(d, { recursive: true }).map((e) => join(d, e.toString())).filter((p) => statSync(p).isFile());

const files = [];
const missing = [];
for (const [group, liveDir] of GROUPS) {
  const bundleDir = join(BUNDLE, group);
  for (const bundleFile of walk(bundleDir)) {
    const rel = relative(bundleDir, bundleFile);
    const livePath = join(PROJECT, liveDir, rel);
    const key = posix(join(liveDir, rel));
    if (!existsSync(livePath)) { missing.push(key); continue; }
    files.push({ path: key, sha256: sha(livePath) });
  }
}

if (missing.length) {
  console.error(`init-manifest: ${missing.length} bundle file(s) have no live counterpart — the copy step (SKILL.md step 3) is incomplete:`);
  missing.forEach((m) => console.error(`  ${m}`));
  process.exit(2);
}

const manifestPath = join(PROJECT, '.claude/init-manifest.json');
const prior = existsSync(manifestPath) ? JSON.parse(readFileSync(manifestPath, 'utf8')) : {};

const manifest = {
  ...prior,
  version: readFileSync(VERSION_FILE, 'utf8').trim(),
  deployedAt: new Date().toISOString(),
  modules,
  files,
  // Recorded even for a template deliberately not rendered — `update` then WARNs
  // on a real template change instead of on every run.
  templates: TEMPLATES.filter((t) => existsSync(join(TEMPLATE_BASE, t)))
    .map((t) => ({ path: t, sha256: sha(join(TEMPLATE_BASE, t)) })),
};

mkdirSync(dirname(manifestPath), { recursive: true });
writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
console.log(`init-manifest: ${files.length} files, ${manifest.templates.length} templates, v${manifest.version} → ${posix(relative(PROJECT, manifestPath))}`);
