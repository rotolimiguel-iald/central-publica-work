"""Keep the accepted staging evidence immutable; publish later notes alongside."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
import task
W = Path(__file__).resolve().parent
target = W / 'LICOES_v409.md'
get = task.call({'operation': 'get', 'reference': str(task.REF)})
pins = set()
def walk(item):
    if isinstance(item, dict):
        if item.get('path', item.get('ref')) == str(target) and 'sha256' in item:
            pins.add(item['sha256'])
        for value in item.values(): walk(value)
    elif isinstance(item, list):
        for value in item: walk(value)
walk(get)
assert len(pins) == 1
expected = next(iter(pins))
backups = [p for p in W.glob('LICOES_v409.md.bak_*') if hashlib.sha256(p.read_bytes()).hexdigest() == expected]
assert len(backups) == 1
before = target.read_bytes()
assert hashlib.sha256(before).hexdigest() != expected
stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
backup = target.with_name(target.name + '.bak_' + stamp)
with backup.open('xb') as f: f.write(before)
complement = W / 'LICOES_v409_COMPLEMENTO.md'
with complement.open('xb') as f: f.write(before)
assert complement.read_bytes() == backup.read_bytes() == before
raw = backups[0].read_bytes()
temp = W / ('lessons_restore_' + stamp + '.tmp')
with temp.open('xb') as f: f.write(raw)
assert temp.read_bytes() == raw and hashlib.sha256(raw).hexdigest() == expected
temp.replace(target)
assert hashlib.sha256(target.read_bytes()).hexdigest() == expected
project = task.project()
receipt = {'status': 'PINNED_ORIGINAL_RESTORED_ADDENDUM_PRESERVED', 'original_sha256': expected,
           'restored_from': str(backups[0]), 'current_bytes_backup': str(backup), 'addendum': str(complement),
           'addendum_sha256': hashlib.sha256(before).hexdigest(), 'mission_revision': project['receipt']['revision'],
           'reason': 'Post-deployment notes had changed a pinned staging artifact. No runtime changed. Restore accepted bytes and keep new notes alongside.'}
task.new('LESSONS_PIN_RECOVERY.json', receipt)
print(json.dumps(receipt))
