#!/usr/bin/env node
// Update a Claude Code deployment using its recorded file hashes. The default
// invocation prints a plan. Only --apply writes files or changes the manifest.
// After manually merging and verifying rendered templates, the caller may add
// --acknowledge-templates to record that review. It never rewrites a template.
import { copyFileSync, existsSync, lstatSync, mkdirSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { bundleFiles, checkRenderedTargets, options, ownedPath, pathIdentity, readManifest, RETIRED_PATHS, safePath, sha, TEMPLATES } from './deployment-map.mjs';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
function main() {
  const args = options(process.argv.slice(2), ['--project', '--apply', '--acknowledge-templates']);
  const project = resolve(args['--project'] || process.cwd());
  const manifest = readManifest(project);
  checkRenderedTargets(project, manifest.modules || ['core']);
  const wanted = bundleFiles(repo);
  const canonical = new Map([...wanted.keys()].map((key) => [pathIdentity(key), key]));
  const recorded = new Map(manifest.files.map((file) => [canonical.get(pathIdentity(file.path)) || file.path, file.sha256]));
  const version = readFileSync(join(repo, 'skills/init-project/VERSION'), 'utf8').trim();
  const plan = { add: [], update: [], remove: [], conflict: [], current: [], forget: [] };
  for (const [key, source] of wanted) {
    const target = safePath(project, key);
    if (!existsSync(target)) { plan.add.push({ key, source }); continue; }
    if (!lstatSync(target).isFile()) throw new Error(`Target is not a file: ${key}`);
    const liveHash = sha(target);
    if (liveHash === sha(source)) plan.current.push({ key, hash: liveHash });
    else if (liveHash === recorded.get(key)) plan.update.push({ key, source, expected: liveHash });
    else plan.conflict.push({ key, reason: 'The file differs from the bundle and its recorded baseline.' });
  }
  for (const [key, hash] of recorded) {
    if (wanted.has(key)) continue;
    const target = safePath(project, key);
    if (!existsSync(target)) { plan.forget.push({ key }); continue; }
    if (!ownedPath(key)) {
      plan.conflict.push({ key, reason: 'The old manifest records a path outside the current deployment. Migrate it manually.' });
    } else if (lstatSync(target).isFile() && sha(target) === hash) {
      plan.remove.push({ key, expected: hash });
    } else plan.conflict.push({ key, reason: 'A retired file has local changes. It will remain in place.' });
  }
  for (const key of RETIRED_PATHS) {
    if (![...recorded.keys()].some((path) => pathIdentity(path) === pathIdentity(key)) &&
        !wanted.has(key) && existsSync(safePath(project, key))) {
      plan.conflict.push({ key, reason: 'This retired file has no recorded ownership hash. Review it manually.' });
    }
  }
  const oldTemplates = new Map((manifest.templates || []).map((item) => [item.path, item.sha256]));
  const templates = TEMPLATES.map(([key, live]) => {
    const source = safePath(repo, `skills/init-project/templates/${key}`);
    if (!existsSync(source)) throw new Error(`Bundle template is missing: ${key}`);
    return { path: key, sha256: sha(source), live };
  });
  const drift = templates.filter((item) => oldTemplates.get(item.path) !== item.sha256);
  console.log(`Update plan: project ${manifest.version || '(unknown)'}; bundle ${version}.`);
  for (const kind of ['add', 'update', 'remove', 'conflict']) {
    console.log(`${kind}: ${plan[kind].length}`);
    for (const item of plan[kind]) console.log(`  ${item.key}${item.reason ? `: ${item.reason}` : ''}`);
  }
  for (const item of drift) console.log(`TEMPLATE REVIEW: ${item.path} affects ${item.live}. Merge and verify it manually.`);
  const pendingTemplates = drift.length > 0 && !args['--acknowledge-templates'];
  const unresolved = plan.conflict.length > 0 || pendingTemplates;
  if (!args['--apply']) {
    console.log('Dry run. No project file or manifest was changed.');
    return unresolved ? 1 : 0;
  }
  // Validate the complete plan before writing, and check paths again before use.
  for (const item of [...plan.add, ...plan.update]) {
    const target = safePath(project, item.key);
    if (item.expected ? !existsSync(target) || sha(target) !== item.expected : existsSync(target)) {
      throw new Error(`File changed after planning: ${item.key}. Run the plan again.`);
    }
    mkdirSync(dirname(target), { recursive: true });
    copyFileSync(item.source, target);
    recorded.set(item.key, sha(target));
  }
  for (const item of plan.remove) {
    const target = safePath(project, item.key);
    if (!existsSync(target) || sha(target) !== item.expected) {
      throw new Error(`Retired file changed after planning: ${item.key}. Run the plan again.`);
    }
    unlinkSync(target);
  }
  for (const item of [...plan.remove, ...plan.forget]) recorded.delete(item.key);
  for (const item of plan.current) recorded.set(item.key, item.hash);
  manifest.files = [...recorded].map(([path, sha256]) => ({ path, sha256 }));
  if (args['--acknowledge-templates']) {
    manifest.templates = templates.map(({ path, sha256 }) => ({ path, sha256 }));
  }
  if (!unresolved) manifest.version = version;
  writeFileSync(safePath(project, '.claude/init-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
  console.log(unresolved ? 'Safe changes were applied. The recorded version stays unchanged until migration is complete.' : `Migration is complete at version ${version}.`);
  return unresolved ? 1 : 0;
}
try { process.exitCode = main(); }
catch (error) { console.error(`update: ${error.message}`); process.exitCode = 2; }
