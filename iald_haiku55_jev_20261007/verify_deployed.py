"""Read-only deployed runtime verification, without provider calls or web imports."""
from pathlib import Path
import sys,json,hashlib,urllib.request,urllib.error
w=Path(__file__).resolve().parent
r=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(r),str(w),r'C:\Users\rotol\AppData\Roaming\Python\Python314\site-packages']
from transaction import write_evidence,bench_snapshot
from claude_memory_package import load_package
from claude_profiles import HAIKU,LEGACY_HAIKU
from claude_server_selection import option_rows,selected_model
import iald_task_policy,iald_execution_guide
plan=json.loads((w/'plan.json').read_bytes())
fix_plan=json.loads((w/'memory_ceiling_fix_plan.json').read_bytes())
for item in plan['files']+fix_plan['files']:
    assert hashlib.sha256(Path(item['destination']).read_bytes()).hexdigest()==item['sha256'],item['destination']
p=load_package(r/'.iald_runtime/haiku55')
s=load_package(r/'.iald_runtime/haiku',expected_model=LEGACY_HAIKU.model)
owner=option_rows({'motor':'automatico'},'luiz',haiku_ready=True,sonnet_ready=True)
other=option_rows({'motor':'automatico'},'ordinary_fixture',haiku_ready=True,sonnet_ready=True)
assert [x['modelo'] for x in other]==[HAIKU.model]
assert len(owner)==2 and sum('haiku' in x['modelo'] for x in owner)==1
assert selected_model({'modelo_claude':LEGACY_HAIKU.model},'luiz',haiku_ready=True,sonnet_ready=True)==HAIKU.model
cap=iald_task_policy.capabilities()
assert 'api.model.images.request' not in json.dumps(cap)
assert 'operator_bench' not in iald_execution_guide.routing_guide('code',['mimo'])
http={}
for url in ['http://127.0.0.1:8082/login','https://demo.iald.ia.br/login','https://demo.iald.ia.br/app/index.html']:
    try:
        with urllib.request.urlopen(url,timeout=30) as res:
            http[url]={'status':res.status,'html': 'text/html' in res.headers.get('Content-Type','')}
            assert res.status==200 and http[url]['html']
    except urllib.error.HTTPError as e:
        if url.startswith('http://127.0.0.1') or e.code!=403:raise
        http[url]={'status':403,'browser_verification_required':True}
if any(x.get('browser_verification_required') for x in http.values()):
    assert json.loads((w/'validation/browser_verification.json').read_bytes())['status']=='PASS'
report={'status':'PASS','installed_files':len(plan['files'])+len(fix_plan['files']),'plan_sha256':hashlib.sha256((w/'plan.json').read_bytes()).hexdigest(),'haiku_model':HAIKU.model,'window':HAIKU.window,'permanent_tokens':p.measurement.permanent_tokens,'reserved_output':p.reserved_output_tokens,'reference_dynamic_tokens':p.available_dynamic_tokens,'shared_compact_loaded':bool(s.prefix),'owner_models':[x['modelo'] for x in owner],'ordinary_policy_models':[x['modelo'] for x in other],'public_budget':'PENDING_EXACT_VALUES_APPROVAL','http':http,'bench':bench_snapshot(),'memory_ceiling_fix_verified':True,'provider_calls':0,'client_files_changed':False,'private_atlas_loaded':False}
write_evidence(w/'validation/deployed_runtime.json',report)
print(json.dumps(report))
