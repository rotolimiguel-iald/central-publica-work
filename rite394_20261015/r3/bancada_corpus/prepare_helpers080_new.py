from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import ast

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
PREV = ROOT / 'REEXAME_SUFICIENCIA_079_20260910'
OUT = ROOT / 'REEXAME_SUFICIENCIA_080_20260910'
OUT.mkdir(exist_ok=False)

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
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
for filename in ['capture_current079.py', 'finalize_delivery079.py']:
    source = PREV / filename
    before = pin(source)
    raw = source.read_bytes()
    replacements = [(b'079', b'080'), (b'078', b'079')]
    if filename.startswith('finalize'):
        replacements += [
            (b'new_cas_controls', b'new_exact_arithmetic_controls'),
            (b'new_exact_symbolic_controls', b'new_exact_integer_controls'),
            (b'exact_tensor_controls_and_no_lean', b'exact_integer_controls_and_no_lean'),
            (b'== 12 and', b'== 15 and'),
            (b'liberdade_de_correcao_e_funcional_impar', b'geracao_E4_e_reducao_da_imagem_delta')]
    changes = []
    for old, new in replacements:
        count = raw.count(old)
        assert count > 0, old
        raw = raw.replace(old, new)
        changes.append({'old': old.decode(), 'new': new.decode(), 'count': count})
    ast.parse(raw)
    dest = OUT / filename.replace('079', '080')
    target = emit(dest, raw)
    after = pin(source)
    assert before == after
    records.append({'source_before': before, 'source_after': after,
                    'target': target, 'replacements': changes})
record = {'created_utc': datetime.now(timezone.utc).isoformat(),
          'status': 'PREPARED_NOT_EXECUTED', 'copies': records,
          'scope': 'New byte-derived helpers only. The old failed finalizer source is reusable code, not a successful run; stage080 inputs will be independently verified.',
          'originals_preserved': True}
print(json.dumps(emit(OUT / 'PROVENIENCIA_AUXILIARES_080.json',
      (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8')), ensure_ascii=True))
