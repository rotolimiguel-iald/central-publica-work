import json,re,hashlib
from pathlib import Path
W4=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');W2=Path(r'C:\IALD\Central de Patentes\work\iald_v402_20261027')
R=Path(r'C:\IALD\projetos_pyhton\IALD')
p4=json.loads((W4/'install_plan.json').read_bytes());p2=json.loads((W2/'install_plan.json').read_bytes())
def norm(plan,v):
    out={}
    for r in plan['files']:
        d=str(Path(r['destination']).relative_to(R));d=re.sub(r'v%s_[0-9a-f]{12}'%v,'vXXX_commit',d);d=d.replace('v%s'%v,'vXXX')
        out[d]=r
    return out
n4=norm(p4,'404');n2=norm(p2,'402')
print('count v404',len(n4),'v402',len(n2))
print('only v404:',sorted(set(n4)-set(n2))[:20])
print('only v402:',sorted(set(n2)-set(n4))[:20])
print('dest in v404 root-level:',[k for k in n4 if '\\' not in k])
print('dest in v402 root-level:',[k for k in n2 if '\\' not in k])
# destination not outside R, all unique, last = active manifest
print('last v404:',p4['files'][-1]['destination'],'last v402:',p2['files'][-1]['destination'])
print('dups v404:',len(p4['files'])-len(set(r['destination'] for r in p4['files'])))
# source set = build files? compare with DATA_PLAN + packages
src={str(Path(r['source']).relative_to(W4)) for r in p4['files']}
print('sources outside W4:',[s for s in (r['source'] for r in p4['files']) if not Path(s).resolve().is_relative_to(W4)][:3])
# every source under app/science/memory_stage (except manifests), plus 6 package files, plus active manifest
st=W4/'app'/'science'/'memory_stage'
files_st={str(p.relative_to(W4)) for p in st.rglob('*') if p.is_file()}
files_in_plan_st={s for s in src if s.startswith('app\\science\\memory_stage')}
print('stage files',len(files_st),'plan stage sources',len(files_in_plan_st),'stage-not-in-plan',sorted(files_st-files_in_plan_st))
print('plan-not-in-stage',sorted(files_in_plan_st-files_st)[:5])
print('package sources',sorted(s for s in src if s.startswith('app\\packages')))
