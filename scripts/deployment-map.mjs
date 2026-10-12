// Shared deployment paths and safety checks for the manifest writer and updater.
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readFileSync, readdirSync, realpathSync } from 'node:fs';
import { isAbsolute, join, relative, resolve, sep } from 'node:path';

export const GROUPS = [
  ['rules', '.claude/rules'], ['guide', '.agent-workspace/guide/general'],
  ['roles', '.agent-workspace/guide/roles'], ['tooling', '.agent-workspace/tooling'],
  ['skills', '.claude/skills'], ['agents', '.claude/agents'],
];
export const TEMPLATES = [
  ['CLAUDE.md.tpl', 'CLAUDE.md'],
  ['guide/index.md.tpl', '.agent-workspace/guide/index.md'],
  ['docs/index.md.tpl', 'docs/index.md'],
  ['lessons/index.md.tpl', '.agent-workspace/lessons/index.md'],
  ['roles/index.md.tpl', '.agent-workspace/guide/roles/index.md'],
  ['decisions/index.md.tpl', '.agent-workspace/decisions/index.md'],
  ['wiki/index.md.tpl', '.agent-workspace/wiki/index.md'],
];
// Unrecorded retired files are reported for review and never deleted automatically.
export const RETIRED_PATHS = [
  '.claude/rules/rule-writing-standards.md', '.claude/rules/conversational-output.md',
  '.claude/skills/document-writer/SKILL.md', '.claude/skills/document-writer/README.md',
];
export const sha = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');
export const pathIdentity = (path) => process.platform === 'win32' ? path.toLowerCase() : path;

export function checkRenderedTargets(project, modules = []) {
  const required = ['CLAUDE.md', '.agent-workspace/guide/index.md',
    '.agent-workspace/guide/roles/index.md', '.agent-workspace/lessons/index.md',
    '.agent-workspace/decisions/index.md'];
  if (modules.includes('wiki')) required.push('.agent-workspace/wiki/index.md');
  for (const key of required) {
    const target = safePath(project, key);
    if (!existsSync(target) || !lstatSync(target).isFile()) {
      throw new Error(`Required rendered target is missing: ${key}. Complete its template migration first.`);
    }
  }
}

export function safePath(root, key) {
  if (typeof key !== 'string' || !key || key.includes('\\') || key.includes(':') ||
      isAbsolute(key) || key.split('/').some((part) => !part || part === '.' || part === '..' ||
        /[. ]$/.test(part) || /^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(part))) {
    throw new Error(`Unsafe deployment path: ${JSON.stringify(key)}`);
  }
  const base = realpathSync(root);
  const target = resolve(base, key);
  if (!relative(base, target) || relative(base, target).startsWith(`..${sep}`)) {
    throw new Error(`Deployment path escapes the project: ${key}`);
  }
  let current = base;
  for (const part of key.split('/')) {
    current = join(current, part);
    try {
      const stat = lstatSync(current);
      if (stat.isSymbolicLink()) throw new Error(`Deployment path contains a link: ${key}`);
      if (stat.isFile() && stat.nlink > 1) throw new Error(`Deployment path contains a hard-linked file: ${key}`);
      if (current !== target && !stat.isDirectory()) throw new Error(`Parent is not a directory: ${key}`);
    } catch (error) {
      if (error.code === 'ENOENT') break;
      throw error;
    }
  }
  return target;
}

export function filesUnder(root, folder) {
  if (!existsSync(safePath(root, folder))) return [];
  const result = [];
  function visit(key) {
    const path = safePath(root, key);
    const stat = lstatSync(path);
    if (stat.isDirectory()) {
      for (const name of readdirSync(path).sort()) visit(`${key}/${name}`);
    } else if (stat.isFile()) result.push(key);
    else throw new Error(`Unsupported deployment file: ${key}`);
  }
  visit(folder);
  return result;
}

export function bundleFiles(repo) {
  const result = new Map();
  for (const group of ['rules', 'guide', 'roles', 'tooling']) {
    if (!filesUnder(repo, `skills/init-project/portable/${group}`).length) {
      throw new Error(`Required bundle group is missing or empty: ${group}`);
    }
  }
  const seen = new Set();
  for (const [group, live] of GROUPS) {
    const folder = `skills/init-project/portable/${group}`;
    for (const path of filesUnder(repo, folder)) {
      const key = `${live}/${path.slice(folder.length + 1)}`;
      if (TEMPLATES.some(([, rendered]) => pathIdentity(rendered) === pathIdentity(key))) {
        throw new Error(`Portable file would overwrite a rendered template: ${key}`);
      }
      if (seen.has(pathIdentity(key))) throw new Error(`Bundle paths alias the same file: ${key}`);
      seen.add(pathIdentity(key));
      result.set(key, safePath(repo, path));
    }
  }
  return result;
}

export function ownedPath(key) {
  return !TEMPLATES.some(([, live]) => pathIdentity(live) === pathIdentity(key)) &&
    GROUPS.some(([, live]) => pathIdentity(key).startsWith(`${pathIdentity(live)}/`));
}

export function readManifest(project) {
  const path = safePath(project, '.claude/init-manifest.json');
  if (!existsSync(path)) throw new Error(`Manifest not found: ${path}`);
  const manifest = JSON.parse(readFileSync(path, 'utf8'));
  if (!Array.isArray(manifest.files)) throw new Error('Manifest files must be an array.');
  const seen = new Set();
  for (const file of manifest.files) {
    safePath(project, file.path);
    if (!/^[a-f0-9]{64}$/i.test(file.sha256 || '') || seen.has(pathIdentity(file.path))) {
      throw new Error(`Invalid or duplicate manifest entry: ${file.path}`);
    }
    seen.add(pathIdentity(file.path));
  }
  return manifest;
}

export function options(argv, allow = []) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    const flag = argv[i];
    if (!allow.includes(flag)) throw new Error(`Unknown option: ${flag}`);
    if (flag === '--project' || flag === '--modules') {
      const value = argv[++i];
      if (!value || value.startsWith('--')) throw new Error(`${flag} requires a value.`);
      result[flag] = value;
    } else result[flag] = true;
  }
  return result;
}
