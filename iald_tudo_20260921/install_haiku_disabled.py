"""Install the reviewed integration behind a disabled feature switch, with CAS backups."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import re

work = Path(__file__).resolve().parent
root = Path(r'C:\IALD\projetos_pyhton\IALD').resolve()
plan_path = work / 'haiku_install_plan_20260922_155240_218040.json'
plan = json.loads(plan_path.read_bytes())
assert plan['feature_activation'] is False and plan['public_spend_activation'] is False
review = json.loads((work / 'adversarial_memory_review/integration_154903_recheck_20260922_185208_137137.json').read_bytes())
assert review['remaining_reproduced_findings'] == []
for path, digest in review['pins'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, 'Review drift'
# Check only this non-secret switch; never print or write any credential.
env_bytes = (root / '.env').read_bytes()
matches = re.findall(rb'^\s*IALD_HAIKU_ATIVO\s*=\s*([^\r\n]*)', env_bytes, flags=re.M)
assert all(value.strip().strip(b'\"\'') in (b'', b'0') for value in matches), 'Haiku is already enabled'
assert os.environ.get('IALD_HAIKU_ATIVO', '0') == '0', 'Process feature switch is enabled'
del env_bytes, matches
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
pending = []
for row in plan['files']:
    target = (root / row['relative']).resolve()
    assert target.is_relative_to(root), 'Outside application root'
    before = target.read_bytes() if target.exists() else None
    digest = hashlib.sha256(before).hexdigest() if before is not None else None
    assert digest == row['old_sha256'], 'Production changed: ' + row['relative']
    new = Path(row['source']).read_bytes()
    assert len(new) == row['bytes'] and hashlib.sha256(new).hexdigest() == row['new_sha256']
    pending.append((target, before, new, row))
written = []
try:
    for target, before, new, row in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        backup = None
        if before is not None:
            backup = target.with_name(target.name + '.bak_' + stamp)
            with backup.open('xb') as handle: handle.write(before)
            assert backup.read_bytes() == before
        temp = target.with_name(target.name + '.tmp_' + stamp)
        with temp.open('xb') as handle: handle.write(new)
        assert temp.read_bytes() == new
        assert (target.read_bytes() if target.exists() else None) == before, 'Concurrent edit'
        temp.replace(target)
        assert target.read_bytes() == new
        written.append({'relative': row['relative'], 'sha256': row['new_sha256'],
                        'backup': str(backup) if backup else None})
except Exception:
    # Restore existing files only if nobody has changed them since this write.
    for item in reversed(written):
        if not item['backup']: continue
        target = root / item['relative']
        assert hashlib.sha256(target.read_bytes()).hexdigest() == item['sha256'], 'Rollback conflict'
        restore = target.with_name(target.name + '.restore_' + stamp)
        original = Path(item['backup']).read_bytes()
        with restore.open('xb') as handle: handle.write(original)
        assert restore.read_bytes() == original
        restore.replace(target)
    raise
receipt = work / ('haiku_installed_disabled_' + stamp + '.json')
with receipt.open('x', encoding='utf8') as handle:
    json.dump({'status': 'INSTALLED_DISABLED_RESTART_PENDING', 'plan': str(plan_path),
        'activation': False, 'public_budget_configured_by_this_operation': False,
        'paid_requests': 0, 'files': written}, handle, indent=2)
print(json.dumps({'receipt': str(receipt), 'files': len(written), 'activation': False}))
