"""Offline independent audit; all writes confined to validation, never deployment."""
from pathlib import Path
import ast, copy, hashlib, importlib.util, io, json, os, re, sqlite3, sys, types, unittest
from unittest.mock import patch
sys.dont_write_bytecode=True
V=Path(__file__).resolve().parent;W=V.parent;S=W/'science';ST=S/'memory_stage';APP=Path('C:/IALD/projetos_pyhton/IALD')
sys.path[:0]=[str(W/'integration'),str(W/'routing/patched'),str(S/'memory_build'),str(APP)]
sha=lambda b:hashlib.sha256(b).hexdigest()
pins={};tests=[];findings=[]
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):raise RuntimeError('External operation blocked by review')
    if event=='open':
        p,mode,flags=args
        if isinstance(p,int):return
        p=Path(os.fsdecode(p)).resolve()
        if p.name in ('.env','iald_stack_v7.py','iald_psion_state.json'):raise RuntimeError('Confidential input blocked')
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not p.is_relative_to(V):raise RuntimeError('Write outside validation: '+str(p))
    if event in ('os.mkdir','os.rmdir','os.remove','os.rename'):
        for p in args[:2] if event=='os.rename' else args[:1]:
            if isinstance(p,(str,bytes)) and not Path(os.fsdecode(p)).resolve().is_relative_to(V):raise RuntimeError('Mutation outside validation')
sys.addaudithook(guard)
def read(p):
    p=Path(p).resolve();raw=p.read_bytes();pin={'sha256':sha(raw),'bytes':len(raw)}
    if str(p) in pins:assert pins[str(p)]==pin,'Input drift '+str(p)
    pins[str(p)]=pin;return raw
def load(p):return json.loads(read(p))
def module(name,path):
    read(path);spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def save(name,value):
    p=V/name;assert not p.exists(),name;p.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')
def check(name,fn):
    print('CHECK '+name,flush=True)
    try:result=fn();tests.append({'name':name,'passed':True,'details':result})
    except Exception as e:tests.append({'name':name,'passed':False,'error':type(e).__name__+': '+str(e)})
planraw=read(W/'install_plan.json');plan= json.loads(planraw);plan_sha=sha(planraw)
for p in [W/'transaction.py',W/'prepare_plan.py',W/'prepare_integration.py',W/'test_integration.py',S/'compact_package.py',ST/'shared_provenance.json',ST/'shared_prefix.md',ST/'jev_control_v392.json',ST/'manifest_staged.json',ST/'manifest_install.json',S/'shared_count/native_count.json',S/'native_count.json']:
    read(p)
for p in (S/'memory_build').glob('*.py'):read(p)

def plan_check():
    assert len(plan['files'])==1257
    dests=set()
    for row in plan['files']:
        source=Path(row['source']).resolve();dest=Path(row['destination']).resolve()
        assert source.is_relative_to(W) and dest.is_relative_to(APP)
        assert str(dest).casefold() not in dests;dests.add(str(dest).casefold())
        assert sha(read(source))==row['sha256'],str(source)
        prior=sha(read(dest)) if dest.exists() else None
        assert prior==row['baseline'],str(dest)
    assert Path(plan['files'][-1]['destination'])==APP/'iald_nucleo_fixo.json'
    fc=load(V/'final_checks.json');mr=load(V/'routing_main_review.json')
    assert fc['passed'] and fc['plan_sha256']==plan_sha
    assert mr['status']=='PASS' and mr['independent_of_routing_author']
    for p,d in mr['files'].items():assert sha(read(p))==d
    return {'files':len(dests),'manifest_last':True,'routing_review':'main receipt validated; routing not independently audited here'}
check('plan_sources_baselines_destinations_and_main_routing_receipt',plan_check)

def compact_check():
    import haiku_codec as c
    from fit_transport import fit
    from fit_memory import compact
    cfg=load(ST/'manifest_staged.json');source=load(cfg['published_evidence']['result']['path'])
    prefix,receipt=c.build_fitted(ST/'manifest_staged.json',APP,S/'memory_build/baseline_v368/prefix.md',S/'memory_build/baseline_v368/canonical.json')
    assert receipt['topic_count']==411 and receipt['new_semantic_fields_verified'] and receipt['new_verdicts_exact']
    first=sha(prefix.encode());prefix,transport=fit(prefix,source);prefix,projection=compact(prefix,source,receipt['reused_identical_topics'])
    actual=read(ST/'shared_prefix.md');prov=load(ST/'shared_provenance.json')
    assert prefix.encode()==actual
    assert first==prov['receipt']['prefix_sha256'] and sha(actual)==prov['prefix_sha256']
    assert receipt['source_sha256']==cfg['active_cluster']['release_source_sha256']
    assert projection==prov['projection'] and transport==prov['transport']
    names=re.findall(r'(?m)^### ([^\r\n]+)',prefix.split(c.MARKER)[0]);names=[n for n in names if n in source['core']]
    assert len(names)==len(set(names))==411 and set(names)==set(source['core'])
    for field in ('mother_instruction','operational_core'):assert Path(cfg[field]['path']).read_text(encoding='utf-8-sig') in prefix
    assert '<ATLAS_CANONICO' not in prefix and not prov['private_atlas_included']
    for p,row in receipt['inputs'].items():
        if 'TGL_ATLAS' in p.upper():raise AssertionError('Private Atlas input')
        raw=read(p);assert sha(raw)==row['sha256']
    return {'reproduced_exactly':True,'topics':len(names),'bytes':len(actual),'new_topics':len(receipt['new_topics']),'private_atlas_read':False,'historical_details':'explicit source references, not all literal'}
check('shared_compact_reproduction_fidelity_and_input_privacy',compact_check)

def jev_check():
    import iald_jev_control as control
    cfg=load(ST/'manifest_install.json');contract=load(ST/'jev_control_v392.json')
    control.validate_contract(contract)
    result=load(ST/'release'/Path(load(ST/'manifest_staged.json')['published_evidence']['result']['path']).relative_to(ST/'release'))
    assert contract['core_record']==result['core']['iald_executive_runtime']
    assert contract['release']=='v392'
    for anchor in contract['anchors']:
        raw=read(ST/'kernel'/anchor['file']);assert sha(raw)==anchor['sha256'] and all(sym in raw.decode() for sym in anchor['symbols'])
    program=read(load(ST/'manifest_staged.json')['published_evidence']['program']['path'])
    f=next(n for n in ast.parse(program).body if isinstance(n,ast.FunctionDef) and n.name==contract['source']['symbol'])
    assert [f.lineno,f.end_lineno]==contract['source']['lines']
    mapping={str(Path(r['destination']).resolve()):Path(r['source']).resolve() for r in plan['files']}
    def mapped(root,path):
        p=Path(path);p=p if p.is_absolute() else root/p
        return mapping[str(p.resolve())]
    with patch.object(control,'_local_file',side_effect=mapped):
        assert control.load_contract(APP)==contract
    corrupt=copy.deepcopy(contract);corrupt['core_record']['status']='CONFIRMED'
    try:control.validate_contract(corrupt)
    except ValueError:pass
    else:raise AssertionError('Bad status accepted')
    return {'actual_loader_verified_with_plan_path_mapping':True,'source_lines':contract['source']['lines'],'anchors':len(contract['anchors'])}
check('JEV_validate_and_install_mapping_load_contract',jev_check)

def integration_check():
    m=module('main_integration_tests',W/'test_integration.py')
    stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(m.Integration))
    (V/'independent_integration_output.txt').write_text(stream.getvalue(),encoding='utf8')
    assert r.wasSuccessful(),stream.getvalue()
    return {'tests':r.testsRun,'live_network':False,'credentials':'mocked for dispatch tests'}
check('main_integration_tests_reexecuted_under_offline_write_guard',integration_check)

def budget_check():
    import iald_app_providers as p
    for maximum in (131072,393216):
        for n in (0,1,500000,661952,700000,1020000,1048576):
            body={'messages':[{'role':'system','content':'x'*n}]};before=copy.deepcopy(body)
            try:
                reserve=p.output_budget(body,maximum)
                assert 16384<=reserve<=maximum
                p.check_window(dict(body,max_tokens=reserve),reserve)
            except ValueError:
                assert p.WINDOW-len(json.dumps(body,ensure_ascii=False).encode())-4096-128<16384
            assert body==before
    assert p.MODELS['deepseek']['output']==393216
    return {'maximum':393216,'minimum':16384,'boundary_cases':14,'input_unchanged':True}
check('adaptive_output_boundaries_and_no_input_truncation',budget_check)

def tx_check():
    tx=module('review_transaction',W/'transaction.py')
    fixture=V/'transaction_fixture';root=fixture/'runtime';work=fixture/'work'
    root.mkdir(parents=True);(work/'validation').mkdir(parents=True)
    (root/'.iald_runtime/chat_jobs').mkdir(parents=True)
    dbpath=root/'.iald_runtime/chat_jobs/jobs.sqlite3'
    db=sqlite3.connect(dbpath);db.execute('CREATE TABLE jobs (status TEXT)');db.commit();db.close()
    for name in ('a.txt','b.txt'):(root/name).write_bytes(b'old');(work/name).write_bytes(b'new')
    sample={'files':[{'source':str(work/n),'destination':str(root/n),'sha256':sha(b'new'),'baseline':sha(b'old')} for n in ('a.txt','b.txt')]}
    p=work/'plan.json';p.write_text(json.dumps(sample));pin=sha(p.read_bytes())
    (work/'validation/final_checks.json').write_text(json.dumps({'passed':True,'plan_sha256':pin}))
    # Synthetic review receipt is confined to the fixture, never the real gate.
    (work/'validation/review_final.json').write_text(json.dumps({'status':'PASS','plan_sha256':pin}))
    atomic=tx.atomic;count=[0]
    def concurrent_task(path,raw):
        atomic(path,raw)
        if Path(path)==root/'a.txt':
            db=sqlite3.connect(dbpath);db.execute("INSERT INTO jobs VALUES ('running')");db.commit();db.close();count[0]+=1
    with patch.object(tx,'ROOT',root),patch.object(tx,'WORK',work),patch.object(tx,'atomic',side_effect=concurrent_task):
        receipt=tx.apply_plan(p)
    db=sqlite3.connect(dbpath);active=db.execute("SELECT COUNT(*) FROM jobs WHERE status='running'").fetchone()[0];db.close()
    evidence={'new_task_after_first_write':count[0],'active_jobs_at_success':active,'deployment_status':receipt['status'],'second_file_installed':(root/'b.txt').read_bytes()==b'new'}
    save('transaction_race_reproduction.json',evidence)
    if active and receipt['status']=='INSTALLED_RESTART_REQUIRED':
        findings.append({'id':'TX-01','severity':'MEDIO','file':str(W/'transaction.py'),'line':115,
            'title':'Ociosidade sem bloqueio de admissao durante a troca',
            'evidence':str(V/'transaction_race_reproduction.json'),
            'impact':'Nova tarefa pode iniciar entre quiet() e a ultima escrita; troca in-place dos dois pacotes permite mistura de versoes/falha no meio de trabalho e restart posterior pode ser recusado.',
            'required_fix':'Adquirir e manter exclusao de admissao/instalacao durante preflight, troca e restart; ou parar o servico de modo controlado antes da troca. Repetir quiet() sozinho nao fecha a corrida.'})
        raise AssertionError('Transaction reported success with a new running task')
    return evidence
check('transaction_concurrent_admission_negative_control',tx_check)
drift=[p for p,v in pins.items() if sha(Path(p).read_bytes())!=v['sha256']]
tests.append({'name':'inputs_stable_at_end','passed':not drift,'details':drift})
save('independent_final_inputpins.json',pins)
save('independent_final_tests.json',{'tests':tests,'findings':findings,'plan_sha256':plan_sha,'provider_calls':0,'installation_performed':False})
print(json.dumps({'tests':tests,'findings':findings,'plan_sha256':plan_sha},ensure_ascii=False))
