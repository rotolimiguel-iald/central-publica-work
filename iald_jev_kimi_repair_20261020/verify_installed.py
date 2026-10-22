from pathlib import Path
from types import SimpleNamespace
import sys,json,hashlib,sqlite3
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0,str(R))
import iald_jev_control as control,iald_auto_router as router,iald_app_memory as memory
from claude_memory_package import load_package
from iald_memory.activity import ActivityRuntime
plan=json.loads((W/'install_plan.json').read_bytes());checks={}
for item in plan['files']:
 checks['installed_'+Path(item['destination']).name]=hashlib.sha256(Path(item['destination']).read_bytes()).hexdigest()==item['sha256']
contract=control.load_contract(R);text,source=router.memory_slice(R,contract)
checks['v2_loaded']=contract['schema']=='iald.jev-control.v2'
checks['packet_loaded_and_verified']=source['packet_sha256']==contract['core_packet']['sha256'] and len(text)==8000
before=json.loads((W/'BASELINE_R1.json').read_bytes());kernel=next(x for x in before['files'] if x['path'].endswith('IALD_Kernel_v5.txt'))
checks['kernel_unchanged']=hashlib.sha256(Path(kernel['path']).read_bytes()).hexdigest()==kernel['sha256']
manifest_before=json.loads((W/'stage_kimi/baseline_R2/iald_nucleo_fixo.json').read_bytes())
manifest_after=json.loads((R/'iald_nucleo_fixo.json').read_bytes())
manifest_before.pop('jev_control');manifest_after.pop('jev_control')
checks['scientific_bindings_unchanged']=manifest_before==manifest_after
package_counts={}
for name in ('haiku55','haiku'):
 package=load_package(R/'.iald_runtime'/name,canonical_manifest=R/'iald_nucleo_fixo.json')
 package_counts[name]=package.measurement.permanent_tokens
 checks['package_binding_'+name]=bool(package.prefix)
v=json.loads((W/'affected_context.json').read_bytes())
b=memory.Binding(memory.MemoryStore(memory._SHARED_ROOT),v['context_id'],v['scope'],'readonly_diagnostic','Haja luz')
runtime=ActivityRuntime(b.store,b.context_id,b.scope,{'id':'readonly.verification','kind':'agent'})
object.__setattr__(b,'_lifecycle',SimpleNamespace(runtime=runtime))
projection=b.projection();checks['affected_context_projects']=not projection.get('overflow') or projection['required_chars']<=projection['actual_chars']
dbpath=R/'.iald_runtime/chat_jobs/jobs.sqlite3'
with sqlite3.connect(dbpath.as_uri()+'?mode=ro',uri=True) as db:
 for old in before['jobs']:
  row=db.execute('select status,seq,error from jobs where id=?',(old['id'],)).fetchone()
  checks['old_job_preserved_'+old['id']]=tuple(row)==(old['status'],old['seq'],old['error'])
assert all(checks.values()),checks
result={'status':'PASS','checks':checks,'release':contract['release'],'packet':source,'package_counts':package_counts,'affected_projection_chars':projection['actual_chars'],'required_chars':projection['required_chars'],'provider_calls':0,'original_requests_replayed':False}
with (W/'installed_verification.json').open('x',encoding='utf-8') as out:json.dump(result,out,ensure_ascii=False,indent=2)
print(json.dumps({'status':'PASS','checks':len(checks),'release':contract['release'],'affected_projection_chars':projection['actual_chars']}))
