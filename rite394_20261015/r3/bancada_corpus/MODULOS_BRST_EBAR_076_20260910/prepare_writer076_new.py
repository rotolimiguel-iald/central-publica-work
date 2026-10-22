from pathlib import Path
import datetime
import hashlib
import json
import os

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt')
OUT = Path(__file__).resolve().parent
assert OUT == ROOT / 'MODULOS_BRST_EBAR_076_20260910'
SOURCE = ROOT / 'MODULOS_BRST_EBAR_075_20260910/write_modules_new.py'

def pin(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'mtime_ns': path.stat().st_mtime_ns}

def write_new(name, data):
    path = OUT / name
    assert not path.exists(), str(path)
    temp = OUT / (name + '.tmp_new')
    with temp.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == data and data
    temp.rename(path)
    assert path.read_bytes() == data
    return pin(path)

before = pin(SOURCE)
raw = SOURCE.read_bytes()
replacements = [
    (b'MODULOS_BRST_EBAR_075_20260910', b'MODULOS_BRST_EBAR_076_20260910'),
    (b'MANIFESTO_MODULOS_EBAR_075.json', b'MANIFESTO_MODULOS_EBAR_076.json'),
]
counts = []
for old, new in replacements:
    counts.append({'from': old.decode(), 'to': new.decode(), 'count': raw.count(old)})
    assert raw.count(old) == 1
    raw = raw.replace(old, new)
target = write_new('write_modules_new.py', raw)
after = pin(SOURCE)
assert before == after
report = {'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'reason': 'Parent assigned this unreleased investigation to arc076 before the source writer was executed',
          'source_writer_before': before, 'source_writer_after': after, 'source_unchanged': True,
          'source_writer_was_executed_by_this_helper': False, 'replacements': counts,
          'new_writer': target, 'helper': pin(Path(__file__))}
provenance = write_new('PROVENIENCIA_CRIADOR_076.json', (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'new_writer': target, 'provenance': provenance, 'source_unchanged': True}, ensure_ascii=False))
