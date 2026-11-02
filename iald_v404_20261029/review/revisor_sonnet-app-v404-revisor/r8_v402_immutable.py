import json,hashlib
from pathlib import Path
V2=Path(r'C:\IALD\Central de Patentes\work\iald_v402_20261027')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
last=(V2/'receipts/v402-verify-accept.json').stat().st_mtime
newer=[str(p.relative_to(V2)) for p in V2.rglob('*') if p.is_file() and p.stat().st_mtime>last+1]
print('v402 files newer than last accept receipt:',newer[:10],len(newer))
bad=[];n=0
for f in V2.glob('receipts/*-accept.json'):
    d=json.loads(f.read_bytes())
    t=d.get('task',{})
    for e in t.get('evidence',[])+t.get('review_evidence',[]):
        n+=1
        if sha(e['path'])!=e['sha256']:bad.append((f.name,e['path']))
print('v402 pinned evidence checked',n,'mismatch',bad)
# production still v402?
R=Path(r'C:\IALD\projetos_pyhton\IALD')
m=json.loads((R/'iald_nucleo_fixo.json').read_bytes())
print('production active release:',m['active_cluster']['release'],'sha(iald_nucleo_fixo.json)',sha(R/'iald_nucleo_fixo.json')[:16])
