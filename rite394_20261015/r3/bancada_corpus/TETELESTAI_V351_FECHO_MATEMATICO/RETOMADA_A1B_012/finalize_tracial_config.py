from pathlib import Path
import json,hashlib,os
R=Path(__file__).resolve().parent
d=R/'revisao_consulta_rota_tracial_2'
old=json.loads((d/'CONSULTA_ROTA_TRACIAL_2.json').read_text(encoding='utf8'))
new=json.loads((d/'CONSULTA_ROTA_TRACIAL_2_V2.json').read_text(encoding='utf8'))
def normalized(v):
    if isinstance(v,dict):
        return {k:(str(Path(x)) if k=='path' and isinstance(x,str) else normalized(x)) for k,x in v.items()}
    if isinstance(v,list): return [normalized(x) for x in v]
    return v
adj=new.pop('path_serialization_correction')
assert normalized(old)==new
print(json.dumps(adj,ensure_ascii=False,indent=2))
p=R/'delivery_configs/tracial_extension_final.json'
assert not p.exists()
cfg=json.loads((R/'delivery_configs/tracial_extension.json').read_text(encoding='utf8'))
cfg['docs'][-1]='revisao_consulta_rota_tracial_2/CONSULTA_ROTA_TRACIAL_2_V2'
b=json.dumps(cfg,ensure_ascii=False,indent=2).encode()
t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
print('New configuration; mathematical content equality verified.')

