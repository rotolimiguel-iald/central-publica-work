import ast, copy, hashlib, importlib.util, io, json, shutil, sys, unittest
from pathlib import Path
W=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
H=W/'host_followup/availability_R1'
SNAP=OUT/'snapshot/availability_R1'
SNAP.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p))
def save(p,d):
    raw=json.dumps(d,ensure_ascii=False,indent=2).encode();p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
    assert p.read_bytes()==raw
def deny(event,args):
    if event in ('socket.connect','socket.getaddrinfo'):raise RuntimeError('OFFLINE_REVIEW_NETWORK_DENIED')
sys.addaudithook(deny)
plan=json.loads((H/'INSTALL_PLAN.json').read_bytes());receipt=json.loads((H/'AVAILABILITY_DELIVERY_R1.json').read_bytes())
assert sha(H/'INSTALL_PLAN.json')==receipt['plan']['sha256']
sources={p:sha(p) for p in H.iterdir() if p.is_file()}
for row in plan['files']:
    src=Path(row['source']['path']);dst=Path(row['target'])
    assert sha(src)==row['source']['sha256']
    if row.get('baseline')=='ABSENT':assert not dst.exists()
    else:assert sha(dst)==row['baseline_sha256']
for row in receipt['actual_historical_evidence']:assert sha(row['path'])==row['sha256']
for name in ('iald_auto_router.py','iald_jev_connection_evidence.json','test_availability.py','test_capability_regression.py'):
    shutil.copyfile(H/name,SNAP/name)
for name in ('SCOPED_ACOM_INPUT.json','SCOPED_JOB_METADATA.json'):
    shutil.copyfile(H.parent/name,SNAP.parent/name)
def load(name):
    spec=importlib.util.spec_from_file_location(name,SNAP/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
a=load('test_availability');c=load('test_capability_regression')
log=io.StringIO();suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromModule(m) for m in (a,c))
r=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
save(OUT/'REPLAY.json',dict(passed=r.wasSuccessful(),tests=r.testsRun,log=log.getvalue(),provider_calls=0))
assert r.wasSuccessful() and r.testsRun==11
# Capture actual whole chooser outcome: local policy refusal remains failed,
# while received HTTP200 evidence is independently retained for availability.
f=c.Capability()
try:
    options=c.plans([c.ITEM],{'standard':{'fps':2.,'media_resolution':'default'},'detail':{'fps':2.,'media_resolution':'max'}})
    ns,wallet,captured,post=f.run_choice(options,dict(image=0,audio=1,video=0))
    try:ns['choose']('synthetic',['mimo'],post=post,validation_probe=True,multimodal=True,media_budget_options=options)
    except c.budget.BudgetRefusal:pass
    else:raise AssertionError('Expected refusal')
    rows=[json.loads(p.read_bytes()) for p in (ns['ROOT']/'.iald_runtime/app_routing').glob('*.json')]
    assert len(rows)==1
    row=rows[0];assert row['status']=='failed_or_uncertain' and row['error_type']=='BudgetRefusal'
    health=row['connection_health'];assert health['http_status']==200 and health['status']=='response_received'
    actual=post.return_value if False else None
    tree=ast.parse((SNAP/'iald_auto_router.py').read_bytes())
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('available','_verified_local_routing_refusal')]
    ns['report']=lambda:[row,copy.deepcopy(a.SELECTED)]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'actual health availability','exec'),ns)
    assert ns['available']() is True
    ns['report']=lambda:[row];assert ns['available']() is False
    ns['report']=lambda:[dict(row,error_type='HTTPError'),a.SELECTED];assert ns['available']() is False
    assert post.call_count==1 and wallet.routing_begin.call_count==1 and wallet.routing_end.call_count==1
finally:f.doCleanups()
baseline=Path(plan['files'][0]['target'])
def defs(p):return {getattr(n,'name',f'index{i}'):ast.dump(n,include_attributes=False) for i,n in enumerate(ast.parse(p.read_bytes()).body)}
old,new=defs(baseline),defs(SNAP/'iald_auto_router.py')
# Compare named functions and non-function module statements separately.
def functions(p):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_bytes()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
old,new=functions(baseline),functions(SNAP/'iald_auto_router.py')
changed=sorted(k for k in old if old[k]!=new.get(k));added=sorted(new.keys()-old.keys())
assert changed==['available','choose'] and added==['_verified_local_routing_refusal']
def rest(p):return ast.dump(ast.Module(body=[n for n in ast.parse(p.read_bytes()).body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))],type_ignores=[]),include_attributes=False)
assert rest(baseline)==rest(SNAP/'iald_auto_router.py')
for p,d in sources.items():assert sha(p)==d
for row in receipt['actual_historical_evidence']:assert sha(row['path'])==row['sha256']
save(OUT/'OWN_CONTROLS.json',dict(passed=True,controls=['actual whole chooser persists failed BudgetRefusal plus receive-only HTTP200 health','prior selected required after actual policy refusal','HTTPError with received health still blocks','one synthetic POST and one ledger lifecycle','only available/choose/new helper changed; other module statements exact','historical route bytes and frozen source bytes unchanged'],changed_functions=changed,new_functions=added,provider_calls=0,runtime_writes=False))
save(OUT/'SOURCE_PINS.json',dict(sources=[pin(p) for p in sources],historical_journals=receipt['actual_historical_evidence'],original_plan=pin(H/'INSTALL_PLAN.json'),receipt=pin(H/'AVAILABILITY_DELIVERY_R1.json')))
print(json.dumps(dict(passed=True,tests=r.testsRun,own_controls=6,findings=[])))
