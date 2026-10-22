from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_083_20260910'
OUT.mkdir(exist_ok=False)
def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    tmp = path.with_name(path.name + '.tmp_new')
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

records = []
for old_name, new_name in [('capture_current082.py', 'capture_current083.py'),
                           ('finalize_delivery082.py', 'finalize_delivery083.py')]:
    source = ROOT / 'REEXAME_SUFICIENCIA_082_20260910' / old_name
    before = pin(source)
    raw = source.read_bytes()
    changes = []
    for old, new in [(b'082', b'083'), (b'081', b'082')]:
        count = raw.count(old)
        assert count > 0
        raw = raw.replace(old, new)
        changes.append({'old': old.decode(), 'new': new.decode(), 'count': count})
    if old_name.startswith('finalize'):
        for old, new in [
            (b"config['new_exact_arithmetic_controls'] == 18", b"config['new_exact_arithmetic_controls'] == 10"),
            (b'ENTREGA_083_ESPONTANEA_setor_sem_derivadas_e_diferencial_CE.md',
             b'ENTREGA_083_ESPONTANEA_derivadas_We yl_e_limite_do_detector.md'.replace(b'We yl', b'Weyl'))]:
            count = raw.count(old)
            assert count == 1
            raw = raw.replace(old, new)
            changes.append({'old': old.decode(), 'new': new.decode(), 'count': count})
    ast.parse(raw)
    target = emit(OUT / new_name, raw)
    after = pin(source)
    assert before == after
    records.append({'source_before': before, 'source_after': after,
                    'target': target, 'changes': changes, 'status': 'PREPARED_NOT_EXECUTED'})
manifest = emit(OUT / 'PROVENIENCIA_AUXILIARES_083.json',
    (json.dumps({'created_utc': datetime.now(timezone.utc).isoformat(), 'records': records,
     'scope': 'New stage helpers only. Expected algebraic count is ten; one combined integrity guard in the mathematical script covers sources and its own bytes. No mathematical execution by these helpers.'},
     ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'records': records, 'provenance': manifest}, ensure_ascii=True))
