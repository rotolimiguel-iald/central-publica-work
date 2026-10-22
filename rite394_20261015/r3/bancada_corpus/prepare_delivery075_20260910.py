from pathlib import Path
from datetime import datetime
import hashlib
import os
import json

root = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
old = root / 'REEXAME_SUFICIENCIA_074_20260910'
out = root / 'REEXAME_SUFICIENCIA_075_20260910'
assert not out.exists()
out.mkdir()
created = []
for source_name, target_name in [
    ('capture_current074.py', 'capture_current075.py'),
    ('finalize_delivery074.py', 'finalize_delivery075.py')
]:
    original = (old / source_name).read_bytes()
    content = original.decode('utf-8').replace('074', '__CURRENT_DELIVERY__').replace('073', '074').replace('__CURRENT_DELIVERY__', '075')
    content = content.replace('translacao_natural_curvatura_e_completacao', 'descida_natural_relativa_e_obrigacoes_restantes')
    data = content.encode('utf-8')
    path = out / target_name
    temporary = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == data
    temporary.rename(path)
    assert path.read_bytes() == data and (old / source_name).read_bytes() == original
    created.append({'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
print(json.dumps(created, ensure_ascii=True))
