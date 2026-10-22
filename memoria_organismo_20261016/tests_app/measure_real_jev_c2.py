"""Actual choose construction/admission, frozen private snapshots, zero dispatch."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import socket
import sys
import types
from unittest import mock

WORK=Path(__file__).resolve().parents[1]
PROD=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(WORK/'staging/app'),str(WORK/'staging/core_r2/lib'),str(WORK/'staging/native'),str(PROD),str(WORK)]
import mission_io as io
import iald_app_memory as memory
import iald_auto_router as router
from iald_memory import MemoryStore
from iald_memory.activity import ActivityRuntime

source=WORK/'staging/app/iald_auto_router.py'
node=next(n for n in ast.parse(source.read_bytes()).body if isinstance(n,ast.FunctionDef) and n.name=='choose')
end=next(i for i,n in enumerate(node.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='admission' for t in n.targets))
node=copy.deepcopy(node);node.name='preview_actual_choose';node.decorator_list=[]
node.body=node.body[:end]+[ast.Return(value=ast.Call(func=ast.Name(id='_measure_fit',ctx=ast.Load()),args=[ast.Name(id='body',ctx=ast.Load())],keywords=[]))]
ast.fix_missing_locations(node)
def size(value):return len(json.dumps(value,ensure_ascii=True,allow_nan=False).encode('ascii'))
def measured(body):
    before={'state_bytes':size(body['state']),'request_bytes':size(body)}
    try:
        admission=router._fit_routing_payload(body);error=None
    except router.RoutingContextOverflow as exc:
        admission=None;error={'type':type(exc).__name__,'message':str(exc)}
    return {'before':before,'admission':admission,'error':error,'body':body,
        'after':{'state_bytes':size(body['state']),'request_bytes':size(body),
            'state_field_bytes':{k:size(v) for k,v in body['state'].items()},
            'question_bytes':{k:size(v) for k,v in body['questions'].items()}}}
namespace=dict(vars(router),_measure_fit=measured)
exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),namespace)

control=router.jev_control.load_contract(PROD)
scientific=router.memory_slice(PROD)
manifest=json.loads((PROD/'iald_nucleo_fixo.json').read_bytes())
core_pin=io.pin(WORK/'staging/core_r2/lib/iald_memory/activity.py')
assert core_pin['sha256']=='144838974cee8d9997927685809f792222e4c32c3b6b50c0d1f498de764f2947'
backend=types.SimpleNamespace(availability=lambda:{'status':'ready'},validate_prompt=lambda value:None)
profiles=[('ordinary','Continue a atividade', ['kimi','mimo','openai','deepseek','nativa']),
          ('haja_luz','Haja Luz',['kimi','mimo','openai','deepseek','nativa'])]
assert all(c in router.DESCRIPTIONS for _,_,cs in profiles for c in cs)
rows=[]
for count in (1,10,100):
    path=WORK/f'tests_core_r2/SNAPSHOT_pending_{count}.json'
    fixture=json.loads(path.read_bytes());snapshot=fixture['snapshot'];scope=snapshot['scope']
    store=MemoryStore(fixture['store_root'])
    with mock.patch.object(store,'get',return_value=copy.deepcopy(snapshot)):
        runtime=ActivityRuntime(store,snapshot['context_id'],scope,{'kind':'agent','id':'offline-jev-preview'})
    for profile,prompt,candidates in profiles:
        binding=memory.Binding(store,snapshot['context_id'],scope,'preview',prompt)
        object.__setattr__(binding,'_lifecycle',types.SimpleNamespace(runtime=runtime))
        with mock.patch.object(socket,'create_connection',side_effect=AssertionError('NETWORK FORBIDDEN')), \
            mock.patch.object(store,'get',return_value=copy.deepcopy(snapshot)), \
            memory.bound(binding), \
            mock.patch.object(router.jev_control,'load_contract',return_value=control), \
            mock.patch.object(router.wallet_runtime,'enabled',return_value=False):
            # Prefix globals are real modules/functions except these explicit boundaries.
            namespace['backend']=lambda:backend
            namespace['available']=lambda:True
            namespace['memory_slice']=lambda root:scientific
            namespace['observations']=lambda *a,**k:{'status':'no_samples','quality':'not_benchmarked'}
            result=namespace['preview_actual_choose'](prompt,candidates,root=PROD)
        body=result.pop('body')
        packet_path=WORK/f'tests_app/JEV_C2_PACKET_{profile}_{count}_R1.json'
        io.save(packet_path,body)
        common=body['state'].get('common_memory',{})
        decisions=[r for r in snapshot['q']['records'] if r.get('kind')=='decision' and r.get('statute')=='INPUT']
        projected=common.get('projection','')
        assert all(r['text'] in projected for r in decisions)
        rows.append(dict(turns=count,profile=profile,revision=snapshot['revision'],
            status='ADMITTED' if result['admission'] else 'REFUSED_REQUIRED_CONTEXT',
            commands_preserved=len(decisions),coverage=common.get('coverage'),
            snapshot=io.pin(path),packet=io.pin(packet_path),**result))
result={'status':'REAL_LOCAL_MEASUREMENT','source':io.pin(source),'core':core_pin,
    'contract_loader':io.pin(PROD/'iald_jev_control.py'),'science_manifest':io.pin(PROD/'iald_nucleo_fixo.json'),
    'scientific_source':scientific[1],'script':io.pin(__file__),'rows':rows,
    'scope':'Exact choose AST prefix through actual _fit_routing_payload, using installed source-bound contract/science and real capability/guide/intent/continuity functions. No post-admission code executes.',
    'fixtures':'Private frozen C2 snapshots; all five catalog candidates assume authorized capability availability, not a live account query. Availability, observed usage and wallet are fixtures; wallet omitted. No production account or metrics database read.',
    'state_mutations':0,'provider_calls':0,'production_writes':0}
io.save(WORK/'tests_app/JEV_REAL_C2_MEASUREMENT_R1.json',result)
print(json.dumps({'result':io.pin(WORK/'tests_app/JEV_REAL_C2_MEASUREMENT_R1.json'),
    'rows':[{k:r[k] for k in ('turns','profile','status','before','after')} for r in rows]},ensure_ascii=False))
