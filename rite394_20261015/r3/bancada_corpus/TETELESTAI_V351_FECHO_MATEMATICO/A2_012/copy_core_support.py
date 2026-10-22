from pathlib import Path
import hashlib,json,os
R=Path(__file__).resolve().parent
K=R.parent/'RETOMADA_A1B_012/k'
rows=[]
for name in ('TransportData','CoreSupport'):
    p=K/'TGL'/(name+'.lean'); b=p.read_bytes()
    q=R/'src/TGL'/p.name;assert not q.exists()
    q.parent.mkdir(parents=True,exist_ok=True)
    t=q.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,q)
    rows.append(dict(source=str(p),copy=str(q),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
p=R/'PROVENIENCIA_CORE_SUPPORT.json';assert not p.exists()
b=json.dumps(rows,indent=2).encode();t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
print(json.dumps(rows))
