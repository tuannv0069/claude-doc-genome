"""Local loader/config probes. Never persist raw prompt or configuration output."""
import argparse
import json
import os
import queue
import shutil
import subprocess
import threading
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, required=True, help='New directory for isolated fixtures and sanitized evidence')
args = parser.parse_args()
HERE = args.output.absolute()
if HERE.exists():
    parser.error('--output must be a new directory')
HERE.mkdir(parents=True)
FIXTURE = HERE / 'fixture'
PROBE_HOME = HERE / 'isolated-home'
CODEX = shutil.which('codex')
if not CODEX:
    parser.error('Codex CLI is required for this optional platform probe')
for directory in (FIXTURE, PROBE_HOME):
    directory.mkdir(exist_ok=True)
subprocess.run(['git', 'init', '--quiet', str(FIXTURE)], check=True)
ENV = dict(os.environ, CODEX_HOME=str(PROBE_HOME))
MARKERS = ['CAP_ROOT_9817', 'CAP_FALLBACK_9817', 'CAP_CHILD_9817',
           'capability-parent-skill', 'CAP_SKILL_BODY_9817']

def put(name, text):
    p = FIXTURE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

put('AGENTS.md', '# Fixture\nCAP_ROOT_9817\n')
put('nested/CUSTOM.md', '# Fallback\nCAP_FALLBACK_9817\n')
put('.agents/skills/capability-parent-skill/SKILL.md',
    '---\nname: capability-parent-skill\ndescription: Only for capability probes.\n---\n\nCAP_SKILL_BODY_9817\n')
put('.codex/config.toml', 'project_doc_fallback_filenames = ["CUSTOM.md"]\nproject_doc_max_bytes = 18001\n')
put('nested/.codex/config.toml', 'project_doc_max_bytes = 18002\n')
regular = FIXTURE / 'nested/AGENTS.md'
if regular.exists():
    regular.unlink()
results = []

def configure(trust):
    # The trust declaration is confined to a synthetic CODEX_HOME.
    key = json.dumps(str(FIXTURE))
    (PROBE_HOME / 'config.toml').write_text(
        f'project_doc_max_bytes = 18000\n[projects.{key}]\ntrust_level = "{trust}"\n', encoding='utf-8')

def prompt(name, cwd, options=()):
    run = subprocess.run([CODEX, *options, 'debug', 'prompt-input', 'Synthetic loader probe only.'],
        cwd=cwd, env=ENV, capture_output=True, encoding='utf-8', timeout=90)
    serial = json.dumps(json.loads(run.stdout), ensure_ascii=False) if run.returncode == 0 else ''
    item = {'case': name, 'exit_code': run.returncode,
            'markers': {m: m in serial for m in MARKERS}, 'stderr_present': bool(run.stderr.strip())}
    results.append(item)

class Server:
    def __init__(self, overrides=()):
        self.proc = subprocess.Popen([CODEX, *overrides, 'app-server', '--stdio'], cwd=FIXTURE,
            env=ENV, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, encoding='utf-8', bufsize=1)
        self.q = queue.Queue()
        def reader():
            for line in self.proc.stdout:
                try:
                    self.q.put(json.loads(line))
                except json.JSONDecodeError:
                    pass
        threading.Thread(target=reader, daemon=True).start()
        self.ident = 0
        self.call('initialize', {'clientInfo': {'name': 'genome_capability_probe', 'version': '1'},
            'capabilities': {'experimentalApi': True}})
        self.proc.stdin.write(json.dumps({'method': 'initialized'}) + '\n')
        self.proc.stdin.flush()
    def call(self, method, params):
        self.ident += 1
        self.proc.stdin.write(json.dumps({'id': self.ident, 'method': method, 'params': params}) + '\n')
        self.proc.stdin.flush()
        while True:
            event = self.q.get(timeout=45)
            if event.get('id') == self.ident:
                return event
    def close(self):
        self.proc.terminate()
        self.proc.wait(timeout=10)

def config(name, cwd, overrides=()):
    server = Server(overrides)
    try:
        result = server.call('config/read', {'cwd': str(cwd), 'includeLayers': True})
        data = result.get('result', {})
        cfg = data.get('config', {})
        layers = data.get('layers', [])
        results.append({'case': name, 'rpc_error': 'error' in result,
            'project_doc_max_bytes': cfg.get('project_doc_max_bytes'),
            'disabled_project_layers': sum(bool(x.get('disabledReason')) for x in layers),
            'project_marker_layer_values': [x.get('config', {}).get('project_doc_max_bytes') for x in layers
                if x.get('config', {}).get('project_doc_max_bytes') in (18000, 18001, 18002, 18003)]})
    finally:
        server.close()

configure('untrusted')
config('untrusted_nested_config', FIXTURE / 'nested')
prompt('untrusted_fallback_not_loaded', FIXTURE / 'nested')
configure('trusted')
config('trusted_root_config', FIXTURE)
config('trusted_nested_config', FIXTURE / 'nested')
config('cli_overrides_project_config', FIXTURE / 'nested', ['-c', 'project_doc_max_bytes=18003'])
prompt('trusted_nested_fallback_and_parent_skill', FIXTURE / 'nested')
put('nested/AGENTS.md', '# Child\nCAP_CHILD_9817\n')
prompt('regular_agents_precedes_fallback', FIXTURE / 'nested')
output = {'cli_version': subprocess.check_output([CODEX, '--version'], encoding='utf-8').strip(),
          'isolation': 'Synthetic CODEX_HOME and Git fixture. No credentials copied, no model call.',
          'desktop_ui_tested': False, 'results': results}
by_name = {item['case']: item for item in results}
output['checks'] = {
    'untrusted_project_config_is_disabled': by_name['untrusted_nested_config']['project_doc_max_bytes'] == 18000 and by_name['untrusted_nested_config']['disabled_project_layers'] == 2,
    'root_project_config_overrides_user': by_name['trusted_root_config']['project_doc_max_bytes'] == 18001,
    'nested_project_config_overrides_root': by_name['trusted_nested_config']['project_doc_max_bytes'] == 18002,
    'cli_overrides_nested_config': by_name['cli_overrides_project_config']['project_doc_max_bytes'] == 18003,
    'trusted_fallback_is_loaded': by_name['trusted_nested_fallback_and_parent_skill']['markers']['CAP_FALLBACK_9817'],
    'regular_agents_precedes_fallback': by_name['regular_agents_precedes_fallback']['markers']['CAP_CHILD_9817'] and not by_name['regular_agents_precedes_fallback']['markers']['CAP_FALLBACK_9817'],
    'root_skill_metadata_reaches_nested_cwd': by_name['trusted_nested_fallback_and_parent_skill']['markers']['capability-parent-skill'],
    'skill_body_not_in_initial_prompt': not by_name['trusted_nested_fallback_and_parent_skill']['markers']['CAP_SKILL_BODY_9817'],
    'explicit_untrusted_root_instructions_omitted_in_this_cli': not by_name['untrusted_fallback_not_loaded']['markers']['CAP_ROOT_9817'],
}
(HERE / 'capability-results.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
print(json.dumps(output, indent=2))
if not all(output['checks'].values()):
    raise SystemExit('A local capability expectation failed. Inspect sanitized evidence.')
