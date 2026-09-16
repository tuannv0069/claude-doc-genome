#!/usr/bin/env node
// Check the documentation network defined by doc-system-mechanics.md section 5.
// The command checks metadata, unfilled template slots, root references, guide
// routing, section references, and the retired directory layout. It does not
// prescribe sentence wording, document length, or a presentation style.
//
// The corpus consists of the live rule, guide, and lesson trees, the root
// instruction file, and the init skill. Examples and fenced code are excluded
// where their paths are illustrative. A successful result applies to this
// corpus, not to every Markdown file in the repository.
//
// Run node scripts/doc-lint.mjs, optionally with --quiet. The command does not
// write files. It returns 0 when the checks pass and 1 when it reports findings.

import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, basename, dirname, sep } from 'node:path';

const quiet = process.argv.includes('--quiet');
const CLAUDE_MD = 'CLAUDE.md';
const RULES_DIR = '.claude/rules';
const GUIDE_DIR = '.agent-workspace/guide';
const LESSONS_DIR = '.agent-workspace/lessons';
const ROUTER = `${GUIDE_DIR}/index.md`;

const posix = (p) => p.split(sep).join('/');
const walk = (d) => !existsSync(d) ? [] :
  readdirSync(d, { recursive: true }).map((e) => posix(join(d, e.toString())))
    .filter((p) => statSync(p).isFile() && p.endsWith('.md'));

const findings = [];
const add = (check, file, msg) => findings.push({ check, file, msg });

// ---- corpus -------------------------------------------------------------
const liveFiles = [...walk(RULES_DIR), ...walk(GUIDE_DIR), ...walk(LESSONS_DIR)];
const mdFiles = [CLAUDE_MD, ...liveFiles, 'skills/init-project/SKILL.md'].filter(existsSync);
const text = new Map(mdFiles.map((p) => [p, readFileSync(p, 'utf8')]));

const byBase = new Map();
for (const p of mdFiles) if (!byBase.has(basename(p))) byBase.set(basename(p), p);

// A §ID is DEFINED where it opens a heading, a list item, or a table cell.
// (Surveyed against the corpus: 85 definitions, no other form.)
const defines = (body, id) =>
  new RegExp(`^(?:#{1,6}|[-*]|\\|) *§${id.replace(/\./g, '\\.')}(?![0-9.])`, 'm').test(body);

// Illustrative context: a path inside a worked example is a name, not a link.
function isExampleLine(line) {
  return /^\s*[✅❌]/.test(line) || /^\s*(?:input|output):/.test(line);
}
function nonExampleLines(body) {
  const out = [];
  let fenced = false;
  for (const line of body.split('\n')) {
    if (/^\s*```/.test(line)) { fenced = !fenced; continue; }
    if (fenced || isExampleLine(line)) continue;
    out.push(line);
  }
  return out;
}

const isPlaceholder = (s) => /[<>{}*]/.test(s);

// Resolve a cited path against the repo root, then every ancestor of the citing file.
function resolveFrom(citing, target) {
  if (existsSync(target)) return posix(target);
  let dir = dirname(citing);
  while (dir && dir !== '.' && dir !== sep) {
    const p = posix(join(dir, target));
    if (existsSync(p)) return p;
    dir = dirname(dir);
  }
  return null;
}

// ---- L1 scope: frontmatter ---------------------------------------------
for (const p of liveFiles) {
  const frontmatter = text.get(p).match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!frontmatter || !/^scope:\s*(?:portable|project)\s*$/m.test(frontmatter[1])) {
    add('L1', p, 'missing `scope:` frontmatter');
  }
}

// ---- L4 unrendered slots ------------------------------------------------
for (const [p, body] of text) {
  const m = body.match(/\{\{[A-Z][A-Z_]*\}\}/g);
  if (m) add('L4', p, `unrendered slot(s): ${[...new Set(m)].join(', ')}`);
}

// ---- L5 trigger -> file (CLAUDE.md is pure directive surface) -----------
if (text.has(CLAUDE_MD)) {
  const seen = new Set();
  for (const line of nonExampleLines(text.get(CLAUDE_MD))) {
    for (const m of line.matchAll(/`([A-Za-z0-9._/-]+\.md)`/g)) {
      const t = m[1];
      if (isPlaceholder(t) || seen.has(t)) continue;
      seen.add(t);
      // a bare basename is resolvable by the reader when the surrounding line
      // names its directory ("always-loaded (`.claude/rules/`): `file-reading.md`")
      if (!resolveFrom(CLAUDE_MD, t) && !byBase.has(basename(t))) {
        add('L5', CLAUDE_MD, `dead trigger target: ${t}`);
      }
    }
  }
}

// ---- L6 file <-> router (both directions) -------------------------------
if (existsSync(ROUTER)) {
  const router = text.get(ROUTER);
  for (const p of walk(`${GUIDE_DIR}/general`)) {
    if (!router.includes(basename(p))) add('L6', p, 'orphan — no entry in guide/index.md');
  }
  const seen = new Set();
  for (const line of router.split('\n')) {
    const m = line.match(/^\| *`([A-Za-z0-9._/-]+\.md)` *\|/);
    if (!m || isPlaceholder(m[1]) || seen.has(m[1])) continue;
    seen.add(m[1]);
    if (!resolveFrom(ROUTER, m[1])) add('L6', ROUTER, `router entry points at a missing file: ${m[1]}`);
  }
}

// ---- L7 pointer rot -----------------------------------------------------
for (const [p, body] of text) {
  const seen = new Set();
  for (const line of nonExampleLines(body)) {
    for (const m of line.matchAll(/([A-Za-z0-9._/-]+\.md)`? *§(\d+(?:\.\d+)*)/g)) {
      const [, ref, id] = m;
      const key = `${ref}#${id}`;
      if (isPlaceholder(ref) || seen.has(key)) continue;
      seen.add(key);
      const target = resolveFrom(p, ref) ?? byBase.get(basename(ref));
      if (!target) { add('L7', p, `pointer to unknown file: ${ref} §${id}`); continue; }
      if (!defines(text.get(target) ?? readFileSync(target, 'utf8'), id)) {
        add('L7', p, `dead §ID: ${basename(ref)} §${id} not defined in ${target}`);
      }
    }
  }
}

// ---- L8 pre-v2 layout ---------------------------------------------------
for (const [p, body] of text) {
  if (body.includes('docs/agent-guide')) add('L8', p, 'references the pre-v2 `docs/agent-guide/` layout');
}

// ---- report -------------------------------------------------------------
if (!findings.length) {
  console.log(`doc-lint: clean — ${mdFiles.length} files, metadata and documentation links are valid.`);
  process.exit(0);
}
const byCheck = new Map();
for (const f of findings) {
  if (!byCheck.has(f.check)) byCheck.set(f.check, []);
  byCheck.get(f.check).push(f);
}
console.log(`\ndoc-lint: ${findings.length} finding(s) across ${mdFiles.length} files\n`);
for (const check of [...byCheck.keys()].sort()) {
  console.log(`${check}:`);
  for (const f of byCheck.get(check)) console.log(`  ${f.file}: ${f.msg}`);
}
process.exit(1);
