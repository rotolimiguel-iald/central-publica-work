from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_082_20260910'
OUT.mkdir(exist_ok=False)

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    temp = path.with_name(path.name + '.tmp_new')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

records = []
for old_name, new_name in [('capture_current081.py', 'capture_current082.py'),
                           ('finalize_delivery081_algebraic.py', 'finalize_delivery082.py')]:
    source = ROOT / 'REEXAME_SUFICIENCIA_081_20260910' / old_name
    before = pin(source)
    raw = source.read_bytes()
    changes = []
    for old, new in [(b'081', b'082'), (b'080', b'081')]:
        count = raw.count(old)
        assert count > 0
        raw = raw.replace(old, new)
        changes.append({'old': old.decode(), 'new': new.decode(), 'count': count})
    if old_name.startswith('finalize'):
        for old, new in [
            (b"config['new_exact_arithmetic_controls'] == 13", b"config['new_exact_arithmetic_controls'] == 18"),
            (b'ENTREGA_082_ESPONTANEA_representantes_E5_imagem_nao_nula_e_independencia.md',
             b'ENTREGA_082_ESPONTANEA_setor_sem_derivadas_e_diferencial_CE.md')]:
            count = raw.count(old)
            assert count == 1
            raw = raw.replace(old, new)
            changes.append({'old': old.decode(), 'new': new.decode(), 'count': count})
    ast.parse(raw)
    target = emit(OUT / new_name, raw)
    after = pin(source)
    assert before == after
    records.append({'source_before': before, 'source_after': after, 'target': target,
                    'changes': changes, 'status': 'PREPARED_NOT_EXECUTED'})

result = {'created_utc': datetime.now(timezone.utc).isoformat(), 'records': records,
          'scope': 'New helpers only: stage references and expected control count adapted; canonical originals only read by capture/finalizer. No mathematical execution.'}
manifest = emit(OUT / 'PROVENIENCIA_AUXILIARES_082.json',
                (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'helpers': records, 'provenance': manifest}, ensure_ascii=True))
