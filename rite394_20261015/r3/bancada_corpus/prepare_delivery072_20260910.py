from pathlib import Path
from datetime import datetime
import hashlib
import json
import os

root = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
prior = root / 'REEXAME_SUFICIENCIA_071_20260910'
out = root / 'REEXAME_SUFICIENCIA_072_20260910'
assert not out.exists()
out.mkdir()


def new(name, content):
    path = out / name
    assert not path.exists()
    raw = content.encode('utf-8')
    temp = out / (name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


capture = (prior / 'capture_current071.py').read_text(encoding='utf-8-sig')
capture = capture.replace('REEXAME_SUFICIENCIA_070_20260909/ESTADO_CANONICO_070.json',
                          'REEXAME_SUFICIENCIA_071_20260910/ESTADO_CANONICO_071.json')
capture = capture.replace('comparison_with_delivery070', 'comparison_with_delivery071')
capture = capture.replace("OUT / 'ESTADO_CANONICO_071.json'", "OUT / 'ESTADO_CANONICO_072.json'")
capture_pin = new('capture_current072.py', capture)
finalizer = (prior / 'finalize_delivery071.py').read_text(encoding='utf-8-sig')
finalizer = finalizer.replace('071', '072')
finalizer = finalizer.replace('REEXAME_SUFICIENCIA_070_20260909/MANIFESTO_ENTREGA_070.json',
                              'REEXAME_SUFICIENCIA_071_20260910/MANIFESTO_ENTREGA_071.json')
finalizer = finalizer.replace('comparison_with_delivery070', 'comparison_with_delivery071')
finalizer = finalizer.replace('canonical_unchanged_from070', 'canonical_unchanged_from071')
finalizer = finalizer.replace('ENTREGA_072_ESPONTANEA_primitivas_suaves_e_covariancia.md',
                              'ENTREGA_072_ESPONTANEA_fundos_contratermos_e_positividade_formal.md')
finalizer_pin = new('finalize_delivery072.py', finalizer)
print(json.dumps({'directory': out.as_posix(), 'capture': capture_pin, 'finalizer': finalizer_pin}, ensure_ascii=True))
