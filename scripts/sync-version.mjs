#!/usr/bin/env node
// sync-version — single source of truth for the plugin version.
//
// Canonical version lives in skills/init-project/VERSION (the bundle version that
// `promote` bumps and `init` records in init-manifest.json). This script mirrors
// it into every other place a version string appears so they never drift:
//   - .claude-plugin/plugin.json            .version
//   - .claude-plugin/marketplace.json       .version
//   - .claude-plugin/marketplace.json       .plugins[*].version
//   - README.md                             shields.io version badge
//
// Usage:
//   node scripts/sync-version.mjs            # check (default): verify in sync, exit 1 on drift
//   node scripts/sync-version.mjs check
//   node scripts/sync-version.mjs sync       # write canonical VERSION into all mirrors
//   node scripts/sync-version.mjs set 1.4.0  # set canonical VERSION, then sync

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const VERSION_FILE = join(root, 'skills/init-project/VERSION');
const PLUGIN_JSON = join(root, '.claude-plugin/plugin.json');
const MARKETPLACE_JSON = join(root, '.claude-plugin/marketplace.json');
const README = join(root, 'README.md');

const SEMVER = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/;
const BADGE = /(\/badge\/version-).+?(-blue)/;

const VERSION_FIELD = /("version":\s*")[^"]*(")/g;

const readVersion = () => readFileSync(VERSION_FILE, 'utf8').trim();
const readJson = (p) => JSON.parse(readFileSync(p, 'utf8'));
// Surgical replace of every "version" field — preserves all other formatting (no JSON reflow).
const setJsonVersion = (p, v) => writeFileSync(p, readFileSync(p, 'utf8').replace(VERSION_FIELD, `$1${v}$2`));

function mirrors() {
  const plugin = readJson(PLUGIN_JSON);
  const market = readJson(MARKETPLACE_JSON);
  const readme = readFileSync(README, 'utf8');
  const badge = readme.match(BADGE);
  // BADGE has no capture for the version itself; re-extract for reporting.
  const badgeVer = readme.match(/\/badge\/version-(.+?)-blue/);
  const list = [
    { label: '.claude-plugin/plugin.json .version', actual: plugin.version },
    { label: '.claude-plugin/marketplace.json .version', actual: market.version },
  ];
  (market.plugins || []).forEach((p, i) =>
    list.push({ label: `.claude-plugin/marketplace.json .plugins[${i}].version (${p.name})`, actual: p.version }));
  list.push({ label: 'README.md version badge', actual: badge ? badgeVer[1] : '(not found)' });
  return list;
}

function doCheck() {
  const v = readVersion();
  const drift = mirrors().filter((t) => t.actual !== v);
  if (drift.length === 0) {
    console.log(`IN SYNC — all version fields = ${v}`);
    return 0;
  }
  console.error(`DRIFT — canonical (skills/init-project/VERSION) = ${v}`);
  for (const d of drift) console.error(`  ${d.label} = ${d.actual}`);
  console.error('Fix: node scripts/sync-version.mjs sync');
  return 1;
}

function doSync() {
  const v = readVersion();
  setJsonVersion(PLUGIN_JSON, v);
  setJsonVersion(MARKETPLACE_JSON, v);
  writeFileSync(README, readFileSync(README, 'utf8').replace(BADGE, `$1${v}$2`));
  console.log(`SYNCED — all version fields set to ${v}`);
  return 0;
}

function doSet(v) {
  if (!SEMVER.test(v)) {
    console.error(`Invalid semver: ${v}`);
    return 2;
  }
  writeFileSync(VERSION_FILE, v + '\n');
  console.log(`canonical VERSION → ${v}`);
  return doSync();
}

const [cmd, arg] = process.argv.slice(2);
let code;
switch (cmd) {
  case undefined:
  case 'check': code = doCheck(); break;
  case 'sync': code = doSync(); break;
  case 'set': code = arg ? doSet(arg) : (console.error('Usage: set <x.y.z>'), 2); break;
  default:
    console.error(`Unknown command: ${cmd}`);
    console.error('Usage: node scripts/sync-version.mjs [check|sync|set <x.y.z>]');
    code = 2;
}
process.exit(code);
