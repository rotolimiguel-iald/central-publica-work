"""Prepare a reviewed client delta from shipped mobile20; do not deploy or publish."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
from integrate_haiku_context import patch_client

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
MOBILE = ROOT / 'iald-app'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def create(path, raw):
    with path.open('xb') as stream:
        stream.write(raw)
    assert path.read_bytes() == raw

def main():
    original = (MOBILE / 'www/iald.js').read_bytes()
    source = original.decode('utf8')
    for old, new in [
        ('const atual = S.motor && S.motor.motor;', 'const atual = S.motor && (S.motor.motor_selecao || S.motor.motor);'),
        ('|| m.motor === motor ||', '|| (m.motor_selecao || m.motor) === motor ||'),
    ]:
        assert source.count(old) == 1
        source = source.replace(old, new, 1)
    source = patch_client(source)
    for removed in ['/api/alertas', 'renderDeadlines', 'verificarAlertas', 'operational_deadlines.js']:
        assert removed not in source
    stage = WORK / ('mobile_haiku_client_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    stage.mkdir()
    create(stage / 'iald.js', source.encode('utf8'))
    test = (WORK / 'test_haiku_client_context.cjs').read_text(encoding='utf8')
    old = "path.join(__dirname,\n  'claude_routes_stage_20260922_154903_859968', 'iald.js')"
    assert test.count(old) == 1
    create(stage / 'test_haiku_client_context.cjs', test.replace(old, "path.join(__dirname, 'iald.js')").encode('utf8'))
    for name in ['index.html', 'iald.css']:
        create(stage / name, (MOBILE / 'www' / name).read_bytes())
    node = r'C:\Program Files\nodejs\node.exe'
    subprocess.run([node, '--check', str(stage / 'iald.js')], check=True)
    test_run = subprocess.run([node, str(stage / 'test_haiku_client_context.cjs')], capture_output=True, text=True)
    assert test_run.returncode == 0, test_run.stdout + test_run.stderr
    assert (MOBILE / 'www/iald.js').read_bytes() == original
    result = {'status': 'PREPARED_NOT_DEPLOYED', 'mobile_base_sha256': sha(original),
              'prepared_js_sha256': sha(source.encode('utf8')), 'node_syntax_check': 'PASS',
              'behavioral_tests_output': test_run.stdout.strip(),
              'includes': ['distinct Haiku/Sonnet selection', 'native context marker',
                           'full history preserved for Haiku', 'stale response protection'],
              'operational_alerts': 'remain absent', 'production_files_changed': 0,
              'next_gate': 'Reconcile completed Selo client, then audit/sync/build21 iOS and20 Android.'}
    create(stage / 'receipt.json', json.dumps(result, ensure_ascii=False, indent=2).encode('utf8'))
    print(json.dumps({'stage': str(stage), 'status': result['status'], 'tests': result['behavioral_tests_output']}))

if __name__ == '__main__':
    main()
