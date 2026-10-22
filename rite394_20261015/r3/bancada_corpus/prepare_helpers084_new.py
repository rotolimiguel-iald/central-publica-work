from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_084_20260910'
PREV = ROOT / 'REEXAME_SUFICIENCIA_083_20260910'

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

sources = [PREV / 'capture_current083.py', PREV / 'finalize_delivery083.py']
before = [pin(p) for p in sources]
OUT.mkdir(exist_ok=False)
outputs = []
for p in sources:
    text = p.read_text(encoding='utf-8').replace('083', '084').replace('082', '083')
    if p.name.startswith('finalize'):
        text = text.replace('derivadas_Weyl_e_limite_do_detector', 'criterio_da_corrente_e_canal_Euler')
        text = text.replace("config['new_exact_arithmetic_controls'] == 10", "config['new_exact_arithmetic_controls'] == 0")
        text = text.replace("config['new_source_integrity_controls'] == 1", "config['new_source_integrity_controls'] == 0")
    outputs.append(emit(OUT / p.name.replace('083', '084'), text.encode('utf-8')))
assert [pin(p) for p in sources] == before
emit(OUT / 'PROVENIENCIA_HELPERS_084.json', (json.dumps({
    'created_utc': datetime.now(timezone.utc).isoformat(), 'sources_before': before,
    'sources_after': [pin(p) for p in sources], 'outputs': outputs,
    'all_sources_unchanged': True, 'scope': 'New exclusive helpers adapted from delivery083; zero mathematical execution.'
}, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(json.dumps(outputs, ensure_ascii=True))
