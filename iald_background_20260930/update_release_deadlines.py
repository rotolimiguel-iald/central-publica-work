"""Update only the admin TestFlight metadata, preserving other deadline entries."""
from pathlib import Path
from datetime import datetime
import json, os, hashlib

p = Path(r'C:\IALD\projetos_pyhton\IALD\iald_deadlines.json')
before = p.read_bytes()
data = json.loads(before)
stamp = datetime.now().astimezone()
original_other = {k:v for k,v in data['items'].items() if not k.startswith('testflight_')}
data['checked_at'] = stamp.isoformat()
for key, group in [('testflight_internal', 'IALD Equipe'), ('testflight_external', 'IALD Piloto')]:
    data['items'][key].update({
        'expires_at': None,
        'label': f'IALD 4.1 (26) — {group}',
        'source': f'App Store Connect {stamp.isoformat()}: Em testes; Expira em 90 dias; data/hora exatas não exibidas.',
        'build': '4.1 (26)',
        'status': 'Em testes',
    })
assert original_other == {k:v for k,v in data['items'].items() if not k.startswith('testflight_')}
after = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
suffix = stamp.strftime('%Y%m%d_%H%M%S_%f')
backup = p.with_name(p.name + '.bak_' + suffix)
backup.write_bytes(before)
assert backup.read_bytes() == before
temp = p.with_name(p.name + '.tmp_' + suffix)
temp.write_bytes(after)
assert temp.read_bytes() == after and len(after) >= len(before) - 100
assert p.read_bytes() == before, 'Concurrent change'
os.replace(temp, p)
assert p.read_bytes() == after
print(json.dumps({'build': '4.1 (26)', 'groups': 2, 'exact_expiry': None, 'other_entries_preserved': True, 'sha256': hashlib.sha256(after).hexdigest()}))
