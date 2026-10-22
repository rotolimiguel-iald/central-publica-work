from pathlib import Path
from datetime import datetime
import hashlib
import os
import json
root=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
old=root/'REEXAME_SUFICIENCIA_075_20260910'
out=root/'REEXAME_SUFICIENCIA_076_20260910'
assert not out.exists()
out.mkdir()
created=[]
for source_name,target_name in [('capture_current075.py','capture_current076.py'),('finalize_delivery075.py','finalize_delivery076.py')]:
    raw=(old/source_name).read_bytes()
    content=raw.decode('utf-8').replace('075','__CURRENT__').replace('074','075').replace('__CURRENT__','076')
    content=content.replace('descida_natural_relativa_e_obrigacoes_restantes','modulos_BRST_correntes_e_transgressao_caracteristica')
    data=content.encode('utf-8')
    path=out/target_name
    temp=path.with_name(path.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes()==data
    temp.rename(path)
    assert path.read_bytes()==data and (old/source_name).read_bytes()==raw
    created.append({'path':path.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
print(json.dumps(created,ensure_ascii=True))

