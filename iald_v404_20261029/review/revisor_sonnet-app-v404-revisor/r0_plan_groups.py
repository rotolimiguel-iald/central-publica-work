import json,collections
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029')
p=json.loads((W/'install_plan.json').read_bytes())
R=Path(r'C:\IALD\projetos_pyhton\IALD')
c=collections.Counter()
for r in p['files']:
    d=Path(r['destination']).relative_to(R).parts
    key='/'.join(d[:2]) if d[0]=='.iald_runtime' else d[0] if len(d)>1 else d[0]
    c[key]+=1
for k,v in sorted(c.items()):print(v,k)
for r in p['files']:
    d=Path(r['destination']).relative_to(R)
    if d.parts[0]=='.iald_runtime' or len(d.parts)==1:print(d,'<-',Path(r['source']).relative_to(W),'baseline_present',r['baseline'] is not None)
