from pathlib import Path
from datetime import datetime
import os
import hashlib
import json

root = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
previous = root / 'REEXAME_SUFICIENCIA_072_20260910'
out = root / 'REEXAME_SUFICIENCIA_073_20260910'
out.mkdir(exist_ok=False)
written = []
for source, destination in [('capture_current072.py', 'capture_current073.py'),
                            ('finalize_delivery072.py', 'finalize_delivery073.py')]:
    raw = (previous / source).read_bytes()
    text = raw.decode('utf-8').replace('071', '__PREVIOUS__').replace('072', '073').replace('__PREVIOUS__', '072')
    text = text.replace('_fundos_contratermos_e_positividade_formal.md', '_polarizacao_BRST_dominio_Wick_e_cohomologia.md')
    data = text.encode('utf-8')
    target = out / destination
    assert target.resolve().is_relative_to(root) and not target.exists()
    tmp = target.with_name(target.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == data
    tmp.rename(target)
    assert target.read_bytes() == data and (previous / source).read_bytes() == raw
    written.append({'path': target.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
print(json.dumps(written, ensure_ascii=True))
