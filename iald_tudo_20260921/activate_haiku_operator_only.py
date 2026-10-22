"""Enable operator-only model choice; no account, quota, credential or spend changes."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from dotenv import dotenv_values
import iald_motores
from claude_memory_package import load_package
from claude_route_bridge import RouteBridge

def protected_file(path, data):
    with path.open('xb'):
        pass
    owner = subprocess.run(['whoami'], capture_output=True, text=True, check=True).stdout.strip()
    result = subprocess.run(['icacls', str(path), '/inheritance:r', '/grant:r', owner + ':F', '*S-1-5-18:F'], capture_output=True)
    if result.returncode:
        raise ValueError('Could not protect configuration file')
    with path.open('wb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert path.read_bytes() == data

def main():
    env = ROOT / '.env'
    before = env.read_bytes()
    settings = dotenv_values(env)
    assert settings.get('IALD_HAIKU_ATIVO', '0') in ('', '0', None), 'Switch changed; review needed'
    for name in ('IALD_HAIKU_PUBLICO_USD_DIA', 'IALD_HAIKU_GRUPO_USD_DIA'):
        assert settings.get(name) in (None, '', '0') and not os.environ.get(name), 'Public policy configured; review needed'
    reader = lambda name: settings.get(name) or ''
    base = iald_motores.carregar_config_claude(reader, iald_motores.carregar_config(reader))
    assert base.cota_global_usd == 15 and base.cache_ttl == '5m'
    package = load_package(ROOT / '.iald_runtime/haiku')
    measured = json.loads((WORK / 'installed_haiku_runtime_count_20260922_191637_790423.json').read_bytes())
    assert measured['prefix_sha256'] == package.measurement.prefix_sha256 and measured['budget']['ready']
    users_raw = (ROOT / 'iald_users.json').read_bytes()
    user = json.loads(users_raw).get('luiz')
    assert isinstance(user, dict) and user.get('admin') and iald_motores.consentiu(user, iald_motores.CLAUDE)
    bridge = RouteBridge(motors=iald_motores, base_config=base, package_loader=lambda: package,
                         enabled=True, public_daily_usd=None, public_group_daily_usd=None)
    operator_options = [r['id'] for r in bridge.options(user, 'luiz')]
    assert 'claude-haiku' in operator_options and 'claude-sonnet' in operator_options
    assert not bridge.policy_flags('public_budget_probe')['haiku_ready']
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    matches = list(re.finditer(rb'(?m)^[ \t]*IALD_HAIKU_ATIVO[ \t]*=[^\r\n]*', before))
    assert len(matches) <= 1
    if matches:
        match = matches[0]
        after = before[:match.start()] + b'IALD_HAIKU_ATIVO=1' + before[match.end():]
    else:
        newline = b'\r\n' if b'\r\n' in before else b'\n'
        after = before + (b'' if before.endswith(b'\n') else newline) + b'IALD_HAIKU_ATIVO=1' + newline
    backup = env.with_name('.env.bak_' + stamp)
    temp = env.with_name('.env.tmp_' + stamp)
    protected_file(backup, before)
    protected_file(temp, after)
    assert env.read_bytes() == before and (ROOT / 'iald_users.json').read_bytes() == users_raw
    temp.replace(env)
    assert env.read_bytes() == after
    result = {'status': 'OPERATOR_ONLY_FLAG_UPDATED_RESTART_PENDING',
              'checked_at': datetime.now().astimezone().isoformat(),
              'setting_changed': 'IALD_HAIKU_ATIVO=1', 'operator_options_checked': operator_options,
              'public_haiku_available': False, 'account_selection_modified': False,
              'global_daily_usd': 15, 'credentials_changed': False, 'paid_requests': 0,
              'backup_protected': str(backup), 'prefix_sha256': package.measurement.prefix_sha256}
    path = WORK / ('haiku_operator_activation_' + stamp + '.json')
    with path.open('xb') as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2).encode('utf8'))
    print(json.dumps({'receipt': str(path), 'status': result['status']}))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status': 'STOPPED', 'exception_type': type(exc).__name__}))
        raise SystemExit(1)
