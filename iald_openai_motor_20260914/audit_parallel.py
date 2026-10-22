from pathlib import Path
import hashlib
import json
import difflib
import re
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
work = Path(__file__).parent
source = Path('C:/IALD/projetos_pyhton/IALD')
records = json.loads((work / 'source_manifest.json').read_bytes())
baseline = work / 'baseline'
incoming = work / 'incoming'
for name, record in records.items():
    path = source / name
    current = path.read_bytes()
    sha = hashlib.sha256(current).hexdigest()
    candidates = [path] + sorted(path.parent.glob(path.name + '.bak*'))
    previous = next((p for p in candidates if hashlib.sha256(p.read_bytes()).hexdigest() == record['sha256']), None)
    print(json.dumps({'path': name, 'changed': sha != record['sha256'], 'baseline_found': str(previous) if previous else None,
                      'current_bytes': len(current), 'current_sha256': sha}, ensure_ascii=False))
    for root, payload in [(incoming, current)] + ([(baseline, previous.read_bytes())] if previous else []):
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
    if sha != record['sha256'] and previous:
        diff = '\n'.join(difflib.unified_diff(previous.read_text(encoding='utf-8').splitlines(), current.decode('utf-8').splitlines(), fromfile='baseline/' + name, tofile='incoming/' + name, n=2))
        diff = re.sub(r'(?:sk-|AIza)[A-Za-z0-9_-]+', '[REDACTED]', diff)
        (work / (path.name + '.parallel.diff')).write_text(diff, encoding='utf-8')
        print('DIFF=' + str(work / (path.name + '.parallel.diff')))
