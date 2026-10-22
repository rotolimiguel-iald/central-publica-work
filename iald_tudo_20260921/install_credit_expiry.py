"""Install only the administrative expiry reader and observed credit date."""
from datetime import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
STAGE = WORK / 'credit_expiry_20260922_162518_153886'

def create(path, data):
    with path.open('xb') as stream:
        stream.write(data)
    assert path.read_bytes() == data

def main():
    receipt = json.loads((STAGE / 'receipt.json').read_bytes())
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    pending = []
    for name, kind in [('iald_deadlines.py', 'module'), ('iald_deadlines.json', 'data')]:
        path = ROOT / name
        before, after = path.read_bytes(), (STAGE / name).read_bytes()
        assert hashlib.sha256(before).hexdigest() == receipt['old_' + kind + '_sha256'], 'Concurrent change'
        assert hashlib.sha256(after).hexdigest() == receipt['new_' + kind + '_sha256'], 'Stage changed'
        pending.append((path, before, after))
    rows = []
    for path, before, after in pending:
        backup = path.with_name(path.name + '.bak_' + stamp)
        create(backup, before)
        temp = path.with_name(path.name + '.tmp_' + stamp)
        create(temp, after)
        assert path.read_bytes() == before
        temp.replace(path)
        assert path.read_bytes() == after
        rows.append({'file': path.name, 'backup': str(backup), 'sha256': hashlib.sha256(after).hexdigest()})
    result = {'status': 'INSTALLED_ADMIN_ONLY_RESTART_PENDING', 'files': rows,
              'app_or_mobile_modified': False, 'exact_expiry_hour_invented': False,
              'expires_on': '2027-09-23', 'date_timezone': 'UTC', 'expires_at': None}
    out = WORK / ('credit_expiry_installed_' + stamp + '.json')
    create(out, json.dumps(result, ensure_ascii=False, indent=2).encode('utf8'))
    print(json.dumps({'receipt': str(out), 'status': result['status']}))

if __name__ == '__main__':
    main()
