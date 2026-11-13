"""Offline staging plan only; no deployment or provider call."""
from pathlib import Path
import json,hashlib,copy
S=Path(__file__).resolve().parent;W=S.parent.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');P=S/'release_final';T=R/'canonical_releases/v410_608b7108977e'
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,d):
 b=d if isinstance(d,bytes) else json.dumps(d,ensure_ascii=False,indent=2).encode()
 if p.exists(): assert p.read_bytes()==b;return
 with p.open('xb') as f:f.write(b)
 assert p.read_bytes()==b
rows=[]
def add(p,d):
 p=Path(p);d=Path(d);b=p.read_bytes();rows.append({'source':str(p),'destination':str(d),'sha256':sha(b),'baseline':sha(d.read_bytes()) if d.exists() else None});return rows[-1]
rel=json.loads((P/'release.json').read_bytes());ident={**rel['identity'],'manifest_sha256':sha((P/'release.json').read_bytes())}
for p in sorted(P.rglob('*')):
 if p.is_file():add(p,T/p.relative_to(P))
packages={}
for name in ('haiku55','sonnet'):
 f=S/'certificates_final'/name;m=f/'manifest.json';v=json.loads(m.read_bytes());assert v['deployment']==ident and v['budget']['ready']
 packages[name]={'path':str(T/'packages'/name),'manifest_sha256':sha(m.read_bytes())}
 for p in f.iterdir():
  if p.is_file():add(p,T/'packages'/name/p.name)
 for fn in ('prefix.md','manifest.json','native_count.json'):add(f/('manifest.json' if fn=='native_count.json' else fn),R/'.iald_runtime'/('haiku55' if name=='haiku55' else 'haiku')/fn)
add(P/'jev.json',T/'jev_control_v410.json')
b=(P/'documents/um_forma_canonica_integral.md').read_text(encoding='utf-8-sig')[:8000].encode();assert sha(b)==json.loads((P/'jev.json').read_bytes())['core_packet']['sha256'];write(S/'core_packet_v410_bound.txt',b);add(S/'core_packet_v410_bound.txt',R/'core_packet_v410_bound.txt')
up=json.loads((S/'CONTINUOUS_UPDATE_FILES.json').read_bytes())
for x in up['files']:
 assert sha(Path(x['source']).read_bytes())==x['sha256'];add(x['source'],x['destination'])
runtime=[]
for p in sorted((S/'runtime').glob('*.py')):runtime.append(add(p,R/p.name))
runtime.append(add(S/'continuous_update/continuous_update_hook.py',R/'iald_science_update_hook.py'))
source=json.loads(Path(json.loads((S/'descriptor_final.json').read_bytes())['source_manifest']).read_bytes());outer=copy.deepcopy(source);docs={d['id']:d['path'] for d in rel['documents']}
for e in outer['entries']:e['path']=str(T/docs[e['id']])
for name in ('program','seal','result','proof_manifest'):
 old=outer['published_evidence'][name];found=[x for x in rel['artifacts'] if x['sha256']==old['public_sha256']];assert found;old['path']=str(T/found[0]['path'])
for field,filename in [('mother_instruction','mother.txt'),('operational_core','operational_core.md'),('jev_control','jev.json')]:outer[field]['path']=str(T/filename);outer[field]['sha256']=sha((P/filename).read_bytes())
outer['operational_core'].update(current_release='v410',release_source_sha256=ident['source_sha256']);outer['kernel_bundle']=str(T/'kernel');outer['kernel_verification']=str(T/'kernel_verification.json');outer.pop('active_cluster',None)
# Source audit handles remain explicit historical provenance, never runtime file paths.
outer['source_artifacts_provenance']=outer.pop('source_artifacts',[])
outer['science_snapshot']={'path':str(T/'release.json'),'sha256':ident['manifest_sha256'],'packages':packages};outer['selected_science_identity']=ident
write(S/'manifest_install.json',outer);add(S/'manifest_install.json',R/'iald_nucleo_fixo.json')
assert len({x['destination'] for x in rows})==len(rows)
assert all(x['baseline'] is None for x in rows if Path(x['destination']).is_relative_to(T))
write(W/'RUNTIME_DELTA_R4.json',{'schema':'iald.reviewed-runtime-delta.v1','authorization':str(W/'AUTORIZACAO_ACERVO_VERSIONADO_R4.txt'),'files':runtime})
write(W/'install_plan.json',{'schema':'iald.app.versioned-retrieval-plan.v1','identity':ident,'files':rows,'runtime_python_changes':len(runtime),'corpus_scope':rel['coverage'],'provider_generation_calls':0})
print(json.dumps({'files':len(rows),'runtime':len(runtime),'plan_sha256':sha((W/'install_plan.json').read_bytes()),'delta_sha256':sha((W/'RUNTIME_DELTA_R4.json').read_bytes())}))
