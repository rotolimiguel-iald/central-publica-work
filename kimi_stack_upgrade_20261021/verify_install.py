"""Read-only checks of installed candidate pins and fresh-process local retrieval."""
from task import *
import time
BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
check('integration')
plan=json.loads((W/'integration/INSTALL_PLAN_R3.json').read_bytes())
items=[{'path':i['destination'],'expected':i['source']['sha256']} for i in plan['files_in_install_order']]
envelope=json.loads((W/'envelope/install_plan.json').read_bytes())['files'][0]
items.append({'path':envelope['destination'],'expected':envelope['sha256']})
for item in items:
    item['actual']=hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()
    assert item['actual']==item['expected'],item['path']
science=json.loads((W/'SCIENCE_BASELINE.json').read_bytes())
for item in science['files']:
    assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['current_sha256']
catalog=json.loads((BASE/'iald_orchestrator/layered_retrieval_catalog.json').read_bytes())
node=next(iter(catalog['entries']))
request={'operation':'retrieve_knowledge','query':node,'budget_bytes':48000,'mandatory_ids':[node]}
t=time.perf_counter()
p=subprocess.run([PY,'-B','-X','utf8',str(BASE/'transport_cli.py')],input=json.dumps(request).encode(),capture_output=True,timeout=30)
assert p.returncode==0,p.stderr.decode('utf8')
r=json.loads(p.stdout);assert r['ok'] and any(x['row']['id']==node for x in r['nodes']),r
assert len(p.stdout.rstrip(b'\r\n'))==r['budget']['serialized_bytes']
assert all(x['source']['status']=='VERIFIED_SHA256' for x in r['nodes'])
new('INSTALLED_VERIFICATION.json',{'status':'PASS','pins':items,'science_files_unchanged':len(science['files']),'fresh_process_cli_result':r,'cli_elapsed_seconds':time.perf_counter()-t,'provider_calls':0,'jobs_created':0,'app_restart':False,'scope':'Queue CLI and installed modules; no claim that already-running Python/MCP processes reloaded.'})
print('PASS: five installed files, five app science files unchanged, fresh CLI retrieval')
