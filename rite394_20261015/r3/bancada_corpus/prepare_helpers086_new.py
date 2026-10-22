from pathlib import Path
from datetime import datetime
import hashlib, json, os

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
PREV=ROOT/'REEXAME_SUFICIENCIA_085_20260910'
OUT=ROOT/'REEXAME_SUFICIENCIA_086_20260910'
assert OUT.is_dir()
pins=[]
def pin(p):
    b=p.read_bytes()
    return {'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def new(p,b):
    assert p.resolve().is_relative_to(ROOT) and not p.exists() and b
    tmp=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==b
    tmp.rename(p)
    assert p.read_bytes()==b
for stem in ('capture_current','finalize_delivery'):
    source=PREV/(stem+'085.py')
    pins.append(pin(source))
    text=source.read_bytes().decode('utf-8').replace('085','086').replace('084','085')
    if stem=='finalize_delivery':
        old='ENTREGA_086_ESPONTANEA_invariantes_nulos_e_corrente_natural.md'
        assert old in text
        text=text.replace(old,'ENTREGA_086_ESPONTANEA_divergencia_injetiva_e_lider_cubico.md')
    new(OUT/(stem+'086.py'),text.encode('utf-8'))
for p in pins:
    assert p==pin(Path(p['path']))
new(OUT/'PROVENIENCIA_HELPERS_086.json',(json.dumps({'source_pins':pins,'source_pins_unchanged':True,'adaptation':'new copies 085->086 and predecessor084->085; new tunnel name','outputs':[pin(OUT/'capture_current086.py'),pin(OUT/'finalize_delivery086.py')]},ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'outputs':[pin(OUT/'capture_current086.py'),pin(OUT/'finalize_delivery086.py')]},ensure_ascii=True))
