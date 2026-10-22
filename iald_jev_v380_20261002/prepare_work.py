"""Snapshot only application code/config metadata; never credentials or accounts."""
from pathlib import Path
import hashlib
import json
import shutil

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
NAMES = ('iald_auto_router.py', 'iald_web_server.py', 'iald_task_bridge.py',
         'iald_task_policy.py', 'iald_operator_bench.py', 'iald_app_providers.py',
         'iald_research_routes.py', 'iald_bench_catalog.py', 'iald_public_fetch.py',
         'iald_nucleo_fixo.json', 'claude_memory_package.py', 'iald_native_memory.py')

def main():
    dest = WORK / 'baseline'
    dest.mkdir(exist_ok=True)
    rows = []
    for name in NAMES:
        raw = (ROOT / name).read_bytes()
        target = dest / name
        if target.exists() and target.read_bytes() != raw:
            raise RuntimeError('Baseline differs; investigate concurrent change: '+name)
        if not target.exists():
            with target.open('xb') as out:
                out.write(raw)
        rows.append(dict(name=name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    path = WORK / 'baseline.json'
    if not path.exists():
        with path.open('x', encoding='utf-8') as out:
            json.dump({'root': str(ROOT), 'files': rows}, out, indent=2)
    print(json.dumps({'files': len(rows), 'baseline':str(path)}))

if __name__ == '__main__':
    main()
