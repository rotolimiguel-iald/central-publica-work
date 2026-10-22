from datetime import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent


def create(path, data):
    with path.open('xb') as handle: handle.write(data)
    assert path.read_bytes() == data


def install(target, data, expected):
    old = target.read_bytes() if target.exists() else None
    assert (hashlib.sha256(old).hexdigest() if old is not None else None) == expected, 'Concurrent modification: ' + str(target)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    backup = None
    if old is not None:
        backup = target.with_name(target.name + '.bak_' + stamp)
        create(backup, old)
    tmp = target.with_name(target.name + '.tmp_' + stamp)
    create(tmp, data)
    assert (target.read_bytes() if target.exists() else None) == old
    tmp.replace(target)
    assert target.read_bytes() == data
    return {'path': str(target), 'backup': str(backup) if backup else None, 'sha256': hashlib.sha256(data).hexdigest()}


if __name__ == '__main__':
    assert not (WORK / 'code_installed.json').exists()
    baseline = json.loads((WORK / 'prepared.json').read_bytes())['baseline']
    assert json.loads((WORK / 'verification.json').read_bytes())['all_sources_complete']
    rows = []
    for name in ['iald_hipoteses.py', 'iald_estado_publicado.py', 'iald_memoria_canonica.py']:
        data = (WORK / name).read_bytes()
        compile(data, str(ROOT / name), 'exec')
        rows.append(install(ROOT / name, data, baseline[name]))
    test = (WORK / 'test_hypothesis_sources.py').read_text(encoding='utf-8')
    test = 'import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n' + test
    rows.append(install(ROOT / 'tests/test_hypothesis_sources.py', test.encode(), None))
    create(WORK / 'code_installed.json', json.dumps({'at': datetime.now().astimezone().isoformat(),
           'status': 'CODE_INSTALLED_MANIFEST_AND_RESTART_PENDING', 'files': rows}, indent=2).encode())
    print('Code installed with byte backups; manifest and web process pending regression checks.')
