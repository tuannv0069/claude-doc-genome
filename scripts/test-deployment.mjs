#!/usr/bin/env node
// These fixtures exercise real CLI processes against temporary plugin and project
// trees. Every compared hash refers to the same file's bytes before or after a
// deployment step. The repository itself is never an update target.
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { copyFileSync, existsSync, linkSync, mkdirSync, mkdtempSync, readFileSync, renameSync, rmSync, symlinkSync, unlinkSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { GROUPS, TEMPLATES, sha } from './deployment-map.mjs';
const scripts = dirname(fileURLToPath(import.meta.url));
const put = (path, text) => { mkdirSync(dirname(path), { recursive: true }); writeFileSync(path, text); };

function fixture(run) {
  const base = mkdtempSync(join(tmpdir(), 'genome-deployment-'));
  const repo = join(base, 'plugin'), project = join(base, 'project');
  mkdirSync(project); mkdirSync(join(repo, 'scripts'), { recursive: true });
  for (const file of ['deployment-map.mjs', 'update.mjs', 'init-manifest.mjs', 'doc-lint.mjs', 'sync-version.mjs']) {
    copyFileSync(join(scripts, file), join(repo, 'scripts', file));
  }
  const entries = GROUPS.map(([group, target]) => {
    const name = group === 'skills' ? 'sample/SKILL.md' : group === 'tooling' ? 'sample.py' : 'sample.md';
    const source = join(repo, 'skills/init-project/portable', group, name);
    const live = `${target}/${name}`;
    put(source, `Initial ${group} content.\n`); put(join(project, live), readFileSync(source));
    return { group, source, live };
  });
  put(join(repo, 'skills/init-project/VERSION'), '1.0.0\n');
  for (const [path] of TEMPLATES) put(join(repo, 'skills/init-project/templates', path), `Template ${path}\n`);
  for (const path of ['CLAUDE.md', '.agent-workspace/guide/index.md',
    '.agent-workspace/guide/roles/index.md', '.agent-workspace/lessons/index.md',
    '.agent-workspace/decisions/index.md']) {
    put(join(project, path), '---\nscope: project\n---\n\nProject-owned index.\n');
  }
  const manifestPath = join(project, '.claude/init-manifest.json');
  const cli = (file, ...args) => spawnSync(process.execPath, [join(repo, 'scripts', file), ...args], { cwd: project, encoding: 'utf8' });
  const init = cli('init-manifest.mjs');
  assert.equal(init.status, 0, init.stderr);
  const state = {
    base, repo, project, entries, cli, manifestPath,
    manifest: () => JSON.parse(readFileSync(manifestPath, 'utf8')),
    save: (manifest) => put(manifestPath, JSON.stringify(manifest)),
    bump: () => put(join(repo, 'skills/init-project/VERSION'), '2.0.0\n'),
  };
  try { run(state); }
  finally {
    // The only recursive delete target is the direct mkdtemp child created here.
    assert.equal(dirname(resolve(base)), resolve(tmpdir()));
    assert.ok(base.includes('genome-deployment-'));
    rmSync(base, { recursive: true, force: true });
  }
}

test('manifest records all six groups and seven templates', () => fixture((f) => {
  assert.equal(f.manifest().files.length, 6); assert.equal(f.manifest().templates.length, 7);
  assert.ok(f.manifest().files.some((item) => item.path.includes('/roles/')));
  assert.ok(f.manifest().files.some((item) => item.path.includes('/tooling/')));
}));

test('dry run is read only; apply updates clean files and adds missing files', () => fixture((f) => {
  f.bump(); put(f.entries[0].source, 'New rule.\n');
  unlinkSync(join(f.project, f.entries[1].live));
  const before = readFileSync(f.manifestPath, 'utf8');
  let out = f.cli('update.mjs'); assert.equal(out.status, 0, out.stderr);
  assert.equal(readFileSync(f.manifestPath, 'utf8'), before);
  assert.equal(existsSync(join(f.project, f.entries[1].live)), false);
  out = f.cli('update.mjs', '--apply'); assert.equal(out.status, 0, out.stderr);
  assert.equal(sha(join(f.project, f.entries[0].live)), sha(f.entries[0].source));
  assert.ok(existsSync(join(f.project, f.entries[1].live)));
  assert.equal(f.manifest().version, '2.0.0');
}));

test('local conflicts survive while independent clean files update; version stays old', () => fixture((f) => {
  f.bump(); put(f.entries[0].source, 'Bundle change.');
  put(join(f.project, f.entries[0].live), 'Local change.');
  put(f.entries[2].source, 'New role.');
  const out = f.cli('update.mjs', '--apply'); assert.equal(out.status, 1, out.stderr);
  assert.equal(readFileSync(join(f.project, f.entries[0].live), 'utf8'), 'Local change.');
  assert.equal(readFileSync(join(f.project, f.entries[2].live), 'utf8'), 'New role.');
  assert.equal(f.manifest().version, '1.0.0');
}));

test('retired manifest-owned files are removed only when their bytes match', () => fixture((f) => {
  f.bump(); const clean = '.claude/rules/conversational-output.md';
  const edited = '.claude/rules/rule-writing-standards.md';
  const manifest = f.manifest();
  for (const path of [clean, edited]) {
    put(join(f.project, path), 'Retired original.');
    manifest.files.push({ path, sha256: sha(join(f.project, path)) });
  }
  f.save(manifest); put(join(f.project, edited), 'User changes.');
  const out = f.cli('update.mjs', '--apply'); assert.equal(out.status, 1, out.stderr);
  assert.equal(existsSync(join(f.project, clean)), false);
  assert.equal(readFileSync(join(f.project, edited), 'utf8'), 'User changes.');
  assert.ok(!f.manifest().files.some((item) => item.path === clean));
  assert.equal(f.manifest().version, '1.0.0');
}));

test('unowned retired files and unknown old manifest targets are never deleted', () => fixture((f) => {
  const retired = '.claude/skills/document-writer/SKILL.md';
  const customer = 'docs/customer.md';
  put(join(f.project, retired), 'User-owned writer.'); put(join(f.project, customer), 'Customer content.');
  const manifest = f.manifest(); manifest.files.push({ path: customer, sha256: sha(join(f.project, customer)) }); f.save(manifest);
  const out = f.cli('update.mjs', '--apply'); assert.equal(out.status, 1, out.stderr);
  assert.equal(readFileSync(join(f.project, retired), 'utf8'), 'User-owned writer.');
  assert.equal(readFileSync(join(f.project, customer), 'utf8'), 'Customer content.');
}));

test('template migration is explicit, read-only in dry run, and preserves project content', () => fixture((f) => {
  f.bump(); put(join(f.repo, 'skills/init-project/templates/roles/index.md.tpl'), 'New role template.');
  const router = join(f.project, '.agent-workspace/guide/roles/index.md'); put(router, 'Project-owned router.');
  let out = f.cli('update.mjs', '--apply'); assert.equal(out.status, 1, out.stderr);
  assert.equal(f.manifest().version, '1.0.0');
  const before = readFileSync(f.manifestPath, 'utf8');
  out = f.cli('update.mjs', '--acknowledge-templates'); assert.equal(out.status, 0, out.stderr);
  assert.equal(readFileSync(f.manifestPath, 'utf8'), before);
  out = f.cli('update.mjs', '--apply', '--acknowledge-templates'); assert.equal(out.status, 0, out.stderr);
  assert.equal(f.manifest().version, '2.0.0');
  assert.equal(readFileSync(router, 'utf8'), 'Project-owned router.');
}));

test('unsafe manifest paths fail before any safe change is applied', () => fixture((f) => {
  put(f.entries[0].source, 'Do not apply yet.');
  for (const path of ['../outside.md', '/absolute.md', 'C:/outside.md', '.claude\\rules\\bad.md']) {
    const manifest = f.manifest(); manifest.files = manifest.files.filter((item) => !item.invalid);
    manifest.files.push({ path, sha256: '0'.repeat(64), invalid: true }); f.save(manifest);
    const out = f.cli('update.mjs', '--apply'); assert.equal(out.status, 2, out.stderr);
    assert.equal(readFileSync(join(f.project, f.entries[0].live), 'utf8'), 'Initial rules content.\n');
  }
}));

test('a linked deployment directory cannot redirect writes outside the project', () => fixture((f) => {
  const rules = join(f.project, '.claude/rules');
  renameSync(rules, `${rules}-saved`);
  const external = join(f.base, 'external'); mkdirSync(external); put(join(external, 'sample.md'), 'External original.');
  symlinkSync(external, rules, process.platform === 'win32' ? 'junction' : 'dir');
  const out = f.cli('update.mjs', '--apply'); assert.equal(out.status, 2, out.stderr);
  assert.equal(readFileSync(join(external, 'sample.md'), 'utf8'), 'External original.');
}));

test('init does not record missing files or silently bless local edits', () => fixture((f) => {
  const before = readFileSync(f.manifestPath, 'utf8');
  put(join(f.project, f.entries[3].live), 'Locally modified tooling.');
  const out = f.cli('init-manifest.mjs'); assert.equal(out.status, 2, out.stderr);
  assert.equal(readFileSync(f.manifestPath, 'utf8'), before);
}));

test('doc lint permits long prose without a line budget and still finds dead links', () => fixture((f) => {
  put(join(f.project, 'CLAUDE.md'), Array(220).fill('A complete explanation can use its own paragraph.').join('\n') + '\n');
  for (const path of ['.claude/rules/sample.md', '.agent-workspace/guide/general/sample.md', '.agent-workspace/guide/roles/sample.md']) {
    put(join(f.project, path), '---\nscope: portable\n---\n\n## §1 Meaning\n\nRead the source before drawing a conclusion.\n');
  }
  put(join(f.project, '.agent-workspace/guide/index.md'), '---\nscope: project\n---\n\n| file | purpose |\n|---|---|\n| `general/sample.md` | Explanation |\n');
  let out = f.cli('doc-lint.mjs'); assert.equal(out.status, 0, out.stdout + out.stderr);
  put(join(f.project, 'CLAUDE.md'), 'Read `missing.md`.\n');
  out = f.cli('doc-lint.mjs'); assert.equal(out.status, 1, out.stdout + out.stderr);
  assert.match(out.stdout, /dead trigger/);
}));

test('init refuses unrecorded retired files even without an existing manifest', () => fixture((f) => {
  unlinkSync(f.manifestPath);
  const path = join(f.project, '.claude/rules/conversational-output.md'); put(path, 'Unrecorded old instructions.');
  const out = f.cli('init-manifest.mjs'); assert.equal(out.status, 2, out.stderr);
  assert.equal(existsSync(f.manifestPath), false);
  assert.equal(readFileSync(path, 'utf8'), 'Unrecorded old instructions.');
}));

test('an incomplete bundle cannot retire the missing group from the project', () => fixture((f) => {
  const entry = f.entries.find((item) => item.group === 'tooling'); unlinkSync(entry.source);
  const before = readFileSync(f.manifestPath, 'utf8');
  const out = f.cli('update.mjs', '--apply'); assert.equal(out.status, 2, out.stderr);
  assert.equal(readFileSync(f.manifestPath, 'utf8'), before);
  assert.ok(existsSync(join(f.project, entry.live)));
}));

test('a portable file cannot replace a rendered project router', () => fixture((f) => {
  put(join(f.repo, 'skills/init-project/portable/roles/index.md'), 'Wrongly packaged router.');
  const router = join(f.project, '.agent-workspace/guide/roles/index.md'); put(router, 'Project router.');
  const out = f.cli('update.mjs', '--apply'); assert.equal(out.status, 2, out.stderr);
  assert.equal(readFileSync(router, 'utf8'), 'Project router.');
}));

test('case aliases in Windows manifests cannot claim one file twice', { skip: process.platform !== 'win32' }, () => fixture((f) => {
  const manifest = f.manifest();
  manifest.files.push({ ...manifest.files[0], path: manifest.files[0].path.toUpperCase() }); f.save(manifest);
  const out = f.cli('update.mjs', '--apply'); assert.equal(out.status, 2, out.stderr);
  assert.match(out.stderr, /duplicate/);
}));

test('hard-linked managed files and manifests cannot redirect writes outside the project', () => fixture((f) => {
  for (const target of [join(f.project, f.entries[0].live), f.manifestPath]) {
    const external = join(f.base, 'external-' + (target === f.manifestPath ? 'manifest' : 'rule'));
    copyFileSync(target, external);
    const before = readFileSync(external, 'utf8');
    unlinkSync(target); linkSync(external, target);
    put(f.entries[0].source, 'New bundle bytes.');
    for (const script of ['update.mjs', 'init-manifest.mjs']) {
      const out = f.cli(script, ...(script === 'update.mjs' ? ['--apply'] : []));
      assert.equal(out.status, 2, out.stdout + out.stderr);
      assert.equal(readFileSync(external, 'utf8'), before);
    }
    unlinkSync(target); copyFileSync(external, target);
    put(f.entries[0].source, 'Initial rules content.\n');
  }
}));

test('init preserves valid Windows path identity and prior module selection', { skip: process.platform !== 'win32' }, () => fixture((f) => {
  const manifest = f.manifest(); manifest.files[0].path = manifest.files[0].path.toUpperCase();
  manifest.modules = ['core', 'runtime']; f.save(manifest);
  const out = f.cli('init-manifest.mjs'); assert.equal(out.status, 0, out.stderr);
  assert.deepEqual(f.manifest().modules, ['core', 'runtime']);
}));

test('missing rendered core targets prevent a completed deployment record', () => fixture((f) => {
  const before = readFileSync(f.manifestPath, 'utf8');
  unlinkSync(join(f.project, 'CLAUDE.md'));
  for (const script of ['init-manifest.mjs', 'update.mjs']) {
    const out = f.cli(script, ...(script === 'update.mjs' ? ['--apply'] : []));
    assert.equal(out.status, 2, out.stdout + out.stderr);
    assert.match(out.stderr, /Required rendered target/);
    assert.equal(readFileSync(f.manifestPath, 'utf8'), before);
  }
}));

test('an enabled wiki needs its router while the optional docs index may be absent', () => fixture((f) => {
  const before = readFileSync(f.manifestPath, 'utf8');
  let out = f.cli('init-manifest.mjs', '--modules', 'core,wiki');
  assert.equal(out.status, 2, out.stderr);
  assert.equal(readFileSync(f.manifestPath, 'utf8'), before);
  put(join(f.project, '.agent-workspace/wiki/index.md'), 'A project wiki router.');
  out = f.cli('init-manifest.mjs', '--modules', 'core,wiki');
  assert.equal(out.status, 0, out.stderr);
  assert.equal(existsSync(join(f.project, 'docs/index.md')), false);
}));
