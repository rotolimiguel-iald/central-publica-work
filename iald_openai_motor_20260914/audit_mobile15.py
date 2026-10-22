from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
WORK = Path(__file__).parent
files = sorted(set(filter(None, subprocess.check_output(
    ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT).decode().split('\0'))))
bad = []
manifest = {}
patterns = [rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', rb'\bAIza[0-9A-Za-z_-]{30,}',
            rb'\bgh[pousr]_[0-9A-Za-z]{20,}', rb'\bgithub_pat_[0-9A-Za-z_]{30,}', rb'\bsk-(?:proj-|svcacct-)?[0-9A-Za-z_-]{20,}']
for name in files:
    path = ROOT / name
    if not path.is_file():
        raise RuntimeError('Missing tracked file: ' + name)
    if re.search(r'(^|/)(node_modules|_backups_[^/]+)(/|$)|(^|/)(\.env[^/]*|keystore.properties|local.properties|HANDOFF[^/]*|iald_stack_v7.py|iald_psion_state.json)$|\.(jks|keystore|p12|p8|mobileprovision)$|\.bak_', name, re.I):
        bad.append(name + ': excluded path')
        continue
    data = path.read_bytes()
    if any(re.search(pattern, data) for pattern in patterns):
        bad.append(name + ': credential pattern (value withheld)')
    manifest[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
if bad:
    raise RuntimeError('\n'.join(bad))
js = (ROOT / 'www/iald.js').read_bytes()
assert b'/api/motor/consentimento' in js
for directory in ['ios/App/App/public', 'android/app/src/main/assets/public']:
    for name in ['iald.js', 'iald.css', 'index.html', 'kernel_prompt.js', 'kernel_prompt_loja.js']:
        assert (ROOT / directory / name).read_bytes() == (ROOT / 'www' / name).read_bytes(), directory + '/' + name
report = {'created_at': datetime.now().astimezone().isoformat(), 'status': 'PASS', 'files': manifest,
          'count': len(manifest), 'bytes': sum(x['bytes'] for x in manifest.values()),
          'consent_present': True, 'native_assets_match_www': True}
target = WORK / 'mobile15_audit.json'
if target.exists():
    target.with_name(target.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S')).write_bytes(target.read_bytes())
temporary = target.with_suffix('.tmp')
temporary.write_bytes(json.dumps(report, indent=2).encode())
assert json.loads(temporary.read_bytes())['status'] == 'PASS'
temporary.replace(target)
print(json.dumps({key: report[key] for key in ['status', 'count', 'bytes', 'consent_present', 'native_assets_match_www']}))
