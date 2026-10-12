#!/usr/bin/env node
// Record a completed deployment. Every portable file must already match its
// bundle source. This command does not copy files or resolve local changes.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { bundleFiles, checkRenderedTargets, options, pathIdentity, readManifest, RETIRED_PATHS, safePath, sha, TEMPLATES } from './deployment-map.mjs';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
function main() {
  const args = options(process.argv.slice(2), ['--project', '--modules']);
  const project = resolve(args['--project'] || process.cwd());
  const wanted = bundleFiles(repo);
  const wantedIdentities = new Set([...wanted.keys()].map(pathIdentity));
  for (const key of RETIRED_PATHS) {
    if (!wanted.has(key) && existsSync(safePath(project, key))) {
      throw new Error(`Retired file still exists: ${key}. Review its migration before recording completion.`);
    }
  }
  const files = [];
  for (const [path, source] of wanted) {
    const target = safePath(project, path);
    if (!existsSync(target) || sha(target) !== sha(source)) {
      throw new Error(`Deployment is incomplete or locally changed: ${path}`);
    }
    files.push({ path, sha256: sha(target) });
  }
  const target = safePath(project, '.claude/init-manifest.json');
  const prior = existsSync(target) ? readManifest(project) : {};
  const modules = args['--modules']
    ? [...new Set(['core', ...args['--modules'].split(',').map((item) => item.trim()).filter(Boolean)])]
    : prior.modules || ['core'];
  checkRenderedTargets(project, modules);
  for (const file of prior.files || []) {
    if (!wantedIdentities.has(pathIdentity(file.path)) && existsSync(safePath(project, file.path))) {
      throw new Error(`Retired manifest entry still exists: ${file.path}. Use update or complete its manual migration first.`);
    }
  }
  const templates = TEMPLATES.map(([path]) => ({
    path, sha256: sha(safePath(repo, `skills/init-project/templates/${path}`)),
  }));
  const manifest = {
    ...prior,
    version: readFileSync(join(repo, 'skills/init-project/VERSION'), 'utf8').trim(),
    deployedAt: new Date().toISOString(),
    modules,
    files, templates,
  };
  mkdirSync(dirname(target), { recursive: true });
  writeFileSync(target, JSON.stringify(manifest, null, 2) + '\n');
  console.log(`Recorded ${files.length} portable files and ${templates.length} templates at version ${manifest.version}.`);
}
try { main(); }
catch (error) { console.error(`init-manifest: ${error.message}`); process.exitCode = 2; }
