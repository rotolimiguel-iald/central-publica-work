from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
PREV = ROOT / 'REEXAME_SUFICIENCIA_080_20260910'
OUT = ROOT / 'REEXAME_SUFICIENCIA_081_20260910'
OUT.mkdir(exist_ok=False)

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    temporary = path.with_name(path.name + '.tmp_new')
    with temporary.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == raw
    temporary.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

records = []
for filename in ['capture_current080.py', 'finalize_delivery080.py']:
    source = PREV / filename
    before = pin(source)
    raw = source.read_bytes()
    replacements = [(b'080', b'081'), (b'079', b'080')]
    if filename.startswith('finalize'):
        replacements += [
         (b"== 15 and config['new_lean_compilations'] == 0", b"== 13 and config['new_source_integrity_controls'] == 1 and config['new_lean_compilations'] == 0"),
         (b"    'new_lean_compilations': 0,", b"    'new_source_integrity_controls': config['new_source_integrity_controls'],\n    'new_lean_compilations': 0,"),
         (b'geracao_E4_e_reducao_da_imagem_delta', b'representantes_E5_imagem_nao_nula_e_independencia')]
    changes = []
    for old, new in replacements:
        count = raw.count(old)
        assert count > 0, old
        raw = raw.replace(old, new)
        changes.append({'old': old.decode(), 'new': new.decode(), 'count': count})
    ast.parse(raw)
    target = emit(OUT / filename.replace('080', '081'), raw)
    after = pin(source)
    assert before == after
    records.append({'source_before': before, 'source_after': after,
                    'target': target, 'replacements': changes})
record = {'created_utc': datetime.now(timezone.utc).isoformat(),
 'status': 'PREPARED_NOT_EXECUTED', 'copies': records, 'originals_preserved': True,
 'scope': 'New byte-derived helpers; stage081 separates13 algebraic checks from1 source-integrity check in the execution receipt.'}
print(json.dumps(emit(OUT / 'PROVENIENCIA_AUXILIARES_081.json',
 (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8')), ensure_ascii=True))
