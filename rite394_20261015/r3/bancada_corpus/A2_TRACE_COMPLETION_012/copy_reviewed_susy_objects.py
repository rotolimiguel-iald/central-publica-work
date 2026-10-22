from pathlib import Path
import datetime, hashlib, json, os
root=Path(__file__).resolve().parent
review=root.parent/'REVISAO_A2_012/TRACE_COMPLETION_012/COMPATIBILIDADE_7'
d=json.loads((review/'AUDITORIA_FINAL_INDEPENDENTE.json').read_bytes())
assert all(d['gates'].values()) and not any(d['counts'].values())
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
rows=[]
for name in ['V354CoreProjectionLattice','V354ProjectionTraceSubadditivity','V354RegularSusy']:
    result=d['modules']['TGLExt.'+name]
    assert result['returncode']==0 and result['source_unchanged']
    for key in ['source','object']:
        assert pin(Path(result[key]['path']))==result[key]
    src=Path(result['object']['path']);target=root/'dev_build/TGLExt'/f'{name}.olean'
    assert not target.exists()
    b=src.read_bytes();target.write_bytes(b);assert target.read_bytes()==b
    rows.append({'source':pin(src),'copy':pin(target)})
p=root/'PROVENIENCIA_SUSY_PARA_AUDIT_TIPOS.json';assert not p.exists()
b=json.dumps({'timestamp':datetime.datetime.now().astimezone().isoformat(),'mode':'read-only copy of independently reviewed objects for exact-type audit; no new compilation of unchanged SUSY','objects':rows},ensure_ascii=False,indent=2).encode('utf8')
t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
print(p)
