"""Install only the three reviewed iOS files, with byte backups and CAS checks."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import subprocess

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
WORK = Path(__file__).resolve().parent
STAGE = WORK / 'stage_v2'
GIT = r'C:\Program Files\Git\cmd\git.exe'
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def create(p, raw):
    with p.open('xb') as out:
        out.write(raw)
    assert p.read_bytes() == raw

assert not subprocess.check_output([GIT, '-C', str(ROOT), 'status', '--porcelain']).strip(), 'Dirty repository'
manifest = json.loads((WORK / 'manifest.json').read_text())
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
originals = {}
for relative, row in manifest.items():
    target = ROOT / relative
    originals[relative] = target.read_bytes()
    assert digest(originals[relative]) == row['before'], relative
    assert digest((STAGE / relative).read_bytes()) == row['after'], relative
for relative, raw in originals.items():
    p = ROOT / relative
    create(p.with_name(p.name + '.bak_' + stamp), raw)
for relative, row in manifest.items():
    p = ROOT / relative
    assert p.read_bytes() == originals[relative], relative
    temp = p.with_name(p.name + '.tmp_' + stamp)
    create(temp, (STAGE / relative).read_bytes())
    temp.replace(p)
    assert digest(p.read_bytes()) == row['after']
create(WORK / ('installed_' + stamp + '.json'), json.dumps({
    'at': datetime.now().astimezone().isoformat(), 'files': manifest,
    'ios': '4.1 (22)', 'web_changed': False, 'android_changed': False,
    'physical_launch_verification': 'pending'
}, indent=2).encode())
print('Installed three iOS files. Backups preserved. Build 22 awaits native compilation.')
