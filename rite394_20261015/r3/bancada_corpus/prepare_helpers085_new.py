from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_085_20260910'
PREV = ROOT / 'REEXAME_SUFICIENCIA_084_20260910'

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

sources = [PREV / 'capture_current084.py', PREV / 'finalize_delivery084.py']
before = [pin(p) for p in sources]
OUT.mkdir(exist_ok=False)
outputs = []
for path in sources:
    source = path.read_text(encoding='utf-8').replace('084', '085').replace('083', '084')
    if path.name.startswith('finalize'):
        source = source.replace('criterio_da_corrente_e_canal_Euler', 'invariantes_nulos_e_corrente_natural')
    outputs.append(emit(OUT / path.name.replace('084', '085'), source.encode('utf-8')))
assert before == [pin(p) for p in sources]
emit(OUT / 'PROVENIENCIA_HELPERS_085.json', (json.dumps({
    'created_utc': datetime.now(timezone.utc).isoformat(), 'sources_before': before,
    'sources_after': [pin(p) for p in sources], 'outputs': outputs,
    'all_sources_unchanged': True, 'new_mathematical_executions': 0,
    'scope': 'Exclusive new helpers copied and adapted from084; source bytes preserved.'
}, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(json.dumps(outputs, ensure_ascii=True))
