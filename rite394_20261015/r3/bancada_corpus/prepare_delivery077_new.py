from pathlib import Path
from datetime import datetime
import os,hashlib,json
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt')
OUT=ROOT/'REEXAME_SUFICIENCIA_077_20260910'
OUT.mkdir(exist_ok=False)
def new(p,s):
    assert not p.exists();b=s.encode();q=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with q.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert q.read_bytes()==b;q.rename(p);assert p.read_bytes()==b
    return {'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
previous=ROOT/'REEXAME_SUFICIENCIA_076_20260910'
cap=(previous/'capture_current076.py').read_text(encoding='utf-8-sig').replace('076','077').replace('075','076')
fin=(previous/'finalize_delivery076.py').read_text(encoding='utf-8-sig').replace('076','077').replace('075','076')
fin=fin.replace('ENTREGA_077_ESPONTANEA_modulos_BRST_correntes_e_transgressao_caracteristica.md','ENTREGA_077_ESPONTANEA_truncagens_BRST_e_levantamento_Pontryagin_C5.md')
fin=fin.replace("check('no_new_cas_or_lean_claim', config['new_cas_controls'] == 0", "check('exact_ce_controls_and_no_lean', config['new_cas_controls'] == 420")
fin=fin.replace("'new_exact_symbolic_controls': 0", "'new_exact_symbolic_controls': config['new_cas_controls']")
fin=fin.replace("'new_cas_controls': 0", "'new_cas_controls': config['new_cas_controls']")
assert "config['new_cas_controls'] == 420" in fin
print(json.dumps([new(OUT/'capture_current077.py',cap),new(OUT/'finalize_delivery077.py',fin)]))

