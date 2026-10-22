from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
PREV = ROOT / 'REEXAME_SUFICIENCIA_086_20260910'
OUT = ROOT / 'REEXAME_SUFICIENCIA_087_20260910'
assert not OUT.exists()
OUT.mkdir()
pins = []

def new(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    temp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw

for name in ('capture_current086.py', 'finalize_delivery086.py'):
    p = PREV / name
    raw = p.read_bytes()
    pins.append({'path': p.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
    source = re.sub('085|086', lambda m: {'085':'086', '086':'087'}[m.group()], raw.decode('utf-8-sig'))
    if name.startswith('finalize'):
        source = source.replace('divergencia_injetiva_e_lider_cubico', 'ce_linear_quadratico_e_classe_par_brst')
        source = source.replace('Path(link).is_file(), link)', "Path(re.sub(r':\\d+$', '', link)).is_file(), link)")
    compile(source, name.replace('086','087'), 'exec')
    new(OUT / name.replace('086','087'), source.encode('utf-8'))

for pin in pins:
    raw = Path(pin['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == pin['sha256'] and len(raw) == pin['bytes']
new(OUT / 'PROVENIENCIA_HELPERS_087.json', (json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(), 'source_pins':pins, 'originals_written':False, 'new_only':True, 'link_line_suffix_supported':True}, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(OUT.as_posix())
