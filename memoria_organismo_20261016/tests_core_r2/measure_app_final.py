"""Observed Binding + actual local JEV size functions, no provider/server import."""
from pathlib import Path
import ast
import json
import sys
import time
import types
import uuid

WORK=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(WORK/'staging/core_r2/lib'),str(WORK/'tests_core_r2/app_observed_final'),str(WORK)]
from mission_io import save,pin
from iald_memory import MemoryStore
import iald_app_memory as m

folder=WORK/'tests_core_r2/runs'/('app_'+uuid.uuid4().hex[:10]);folder.mkdir(parents=True)
m._SHARED_ROOT=folder/'store'
m.MemoryStore=lambda root:MemoryStore(root,snapshot_archive_dir=folder/'archive')
control_path=Path(r'C:\IALD\projetos_pyhton\IALD\iald_jev_control.py')
nodes=ast.parse(control_path.read_bytes()).body
selected=[]
for node in nodes:
    if isinstance(node,(ast.FunctionDef,ast.ClassDef)) and node.name in {'check_payload','ControlError'}:selected.append(node)
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'MODEL','MAX_STATE_BYTES','MAX_REQUEST_BYTES'} for t in node.targets):
        ast.literal_eval(node.value);selected.append(node)
control={'json':json};exec(compile(ast.Module(body=selected,type_ignores=[]),str(control_path),'exec'),control)
jev=types.SimpleNamespace(**control)
router_path=WORK/'tests_core_r2/app_observed_final/iald_auto_router.py'
nodes=ast.parse(router_path.read_bytes()).body
selected=[n for n in nodes if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in {'_fit_routing_payload','RoutingContextOverflow'}]
router={'json':json,'app_memory':m,'jev_control':jev}
exec(compile(ast.Module(body=selected,type_ignores=[]),str(router_path),'exec'),router)
start=time.perf_counter()
for n in range(1,11):
    b=m.begin(folder,'authenticated-fixture','conversation',[{'role':'user','content':'Continue a atividade '+str(n)}],'turn_'+str(n))
    with m.bound(b):
        if n==10:
            for k in range(5):
                with m.operation('fixture_tool',key='tool_'+str(k)) as op:
                    op.complete({'result':'local fixture tool '+str(k)},terminal=False)
        m.finish_result(b,{'answer':'Resposta candidata '+str(n)})
with m.bound(b):
    snap=b.snapshot();p=b.projection()
    body={'model':jev.MODEL,'state':{'source':{'coverage':'FIXTURE'},
        'canonical_memory':'Synthetic scientific retrieval. '*300,
        'contract_fixture':'Source-bound routing and capabilities placeholder. '*70,
        'request':'Continue a atividade 10','common_memory':m.routing_state()},
        'questions':{'executor':{'type':'choice','instructions':'Synthetic candidate selection fixture.','choices':['native']}}}
    before_bytes=len(json.dumps(body,ensure_ascii=True,allow_nan=False).encode('ascii'))
    admitted=router['_fit_routing_payload'](body)
    assert b.snapshot()==snap
    expected_commands=[r for r in snap['q']['records'] if r['kind']=='decision' and r['statute']=='INPUT']
    assert len(expected_commands)==10
    for r in expected_commands:assert r['text'] in body['state']['common_memory']['projection']
    assert len(p['activity']['active'])==10 and all(t['status']=='review_pending' for t in p['activity']['active'])
save(WORK/'tests_core_r2/APP_ROUTING_MEASUREMENT_FINAL_R1.json',{
    'status':'PASS_REAL_LOCAL_FUNCTIONS_SYNTHETIC_PAYLOAD','turns':10,'tools':5,'human_reviews':0,
    'required_chars':p['required_chars'],'before_fit_request_bytes':before_bytes,'admission':admitted,
    'remaining_state_bytes':jev.MAX_STATE_BYTES-admitted['state_bytes'],
    'required_commands_preserved':len(expected_commands),'active_criteria_preserved':len(p['activity']['active']),
    'indexed_records':len(p['indexed_record_ids']),'elapsed_seconds':time.perf_counter()-start,
    'state_unchanged_by_projection':True,'providers_called':0,
    'scope':'Real frozen Binding/operation/fit/check_payload functions on private store. Science/contract/capability content is synthetic; final A uses its actual contract.',
    'pins':[pin(WORK/'staging/core_r2/lib/iald_memory/activity.py'),pin(control_path),pin(router_path),pin(__file__),pin(WORK/'tests_core_r2/APP_OBSERVED_FINAL_R1.json')],
    'private_store':str(folder)})
print(json.dumps({'status':'PASS','required_chars':p['required_chars'],'before_bytes':before_bytes,
    'admission':admitted,'indexed':len(p['indexed_record_ids']),'seconds':time.perf_counter()-start}))
