from pathlib import Path
from datetime import datetime
import hashlib, json, os

W = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD\app')
baseline = json.loads((W / 'baseline.json').read_bytes())
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
changes = []
for name, expected in baseline.items():
    source = R / name
    old = source.read_bytes()
    new = (W / 'stage' / name).read_bytes()
    assert hashlib.sha256(old).hexdigest() == expected, 'Source changed: ' + name
    assert len(new) >= len(old) * .99 and new != old
    changes.append((source, old, new))
report = []
for source, old, new in changes:
    backup = source.with_name(source.name + '.bak_' + stamp)
    with backup.open('xb') as f: f.write(old)
    assert backup.read_bytes() == old
    temp = source.with_name(source.name + '.tmp_edit_' + str(os.getpid()))
    with temp.open('xb') as f:
        f.write(new); f.flush(); os.fsync(f.fileno())
    assert temp.read_bytes() == new and source.read_bytes() == old
    os.replace(temp, source)
    assert source.read_bytes() == new
    report.append(dict(path=str(source), backup=str(backup), sha256=hashlib.sha256(new).hexdigest()))
(W / 'web_deployment.json').write_bytes(json.dumps(report, indent=2).encode())
print(json.dumps({'installed_files': len(report), 'restart_required': False}))
