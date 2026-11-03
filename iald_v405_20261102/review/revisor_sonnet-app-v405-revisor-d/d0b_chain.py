"""Reviewer probe (read-only): compare v404 installed hashes (deployment.json) with the v405 plan baselines."""
import json
from pathlib import Path
R=r'C:\IALD\projetos_pyhton\IALD'
V4=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');W=Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
d=json.loads((V4/'deployment.json').read_bytes())
print({k:(v if k not in('backups','files') else '...') for k,v in d.items()})
print('v404 files',len(d['files']))
print('v404 restart',json.dumps(json.loads((V4/'restart.json').read_bytes())))
print('v404 maintenance',json.dumps(json.loads((V4/'maintenance.json').read_bytes())))
p=json.loads((W/'install_plan.json').read_bytes())
for r in p['files']:
    if r['baseline'] is not None:
        v4=d['files'].get(r['destination'])
        print(r['destination'].replace(R,'R'),'| plan baseline',r['baseline'][:16],'| v404 registered',(v4 or 'NONE')[:16],'| equal',v4==r['baseline'])
dest={r['destination'] for r in p['files']}
print('v404 files re-written by v405 plan:',sorted(Path(x).name for x in d['files'] if x in dest))
