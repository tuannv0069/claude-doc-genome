#!/usr/bin/env node
// Run the tests of the bundle's genome tools inside a temporary project layout.
// The tools resolve their data from `.agent-workspace/tooling/genome/` beside a
// project root, so they cannot run from the bundle directory itself. The routing
// test needs a fully rendered project and is left to the deployment fixtures; every
// other test file runs here.
import { cpSync, mkdirSync, mkdtempSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const repo = join(dirname(fileURLToPath(import.meta.url)), '..');
const genome = join(repo, 'skills/init-project/portable/tooling/genome');
const SKIPPED = new Set(['test_trigger_kinds.py']);

const project = mkdtempSync(join(tmpdir(), 'genome-tools-'));
try {
  const tooling = join(project, '.agent-workspace/tooling');
  mkdirSync(tooling, { recursive: true });
  cpSync(genome, join(tooling, 'genome'), { recursive: true, filter: (src) => !src.includes('__pycache__') });
  writeFileSync(join(project, 'CLAUDE.md'), '# Temporary project\n');
  const tests = readdirSync(join(genome, 'tests')).filter((n) => /^test_.*\.py$/.test(n) && !SKIPPED.has(n));
  const run = spawnSync('python', [join(tooling, 'genome/run_tests.py'), ...tests], { cwd: project, encoding: 'utf8' });
  process.stdout.write(run.stdout ?? '');
  process.stderr.write(run.stderr ?? '');
  process.exitCode = run.status ?? 1;
} finally {
  rmSync(project, { recursive: true, force: true });
}
