"""Two scalar-limit changes, tested offline against current runtime and sealed data."""
from pathlib import Path
import ast, copy, difflib, hashlib, importlib.util, json, os, sys, tempfile
C=Path(__file__).resolve().parent
A=C.parent;W=A.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True
sys.path.insert(0,str(W))
import task
preflight=task.check('reader_compat',actor='codex-v394-app-builder');assert preflight['ready']
sys.path[:0]=[str(A),str(R)]
from prepare_science import save,write,sha
original_receipt=A/'DELIVERY_PREPARED.json';original_receipt_pin=sha(original_receipt.read_bytes())
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):
        raise RuntimeError('Offline reader compatibility only')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,int):return
        p=Path(os.fsdecode(path)).resolve()
        if p.name.lower() in ('.env','iald_stack_v7.py','iald_psion_state.json'):
            raise RuntimeError('Confidential source refused')
        writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not p.is_relative_to(C):raise RuntimeError('Write outside compat staging')
sys.addaudithook(guard)
stage=C/'staging';stage.mkdir(parents=True,exist_ok=True)
plan=[]
def ast_changes(a,b,path='root'):
    if type(a)!=type(b):return [(path,'type_changed')]
    if isinstance(a,ast.AST):
        changes=[]
        for field in a._fields:changes+=ast_changes(getattr(a,field),getattr(b,field),path+'.'+field)
        return changes
    if isinstance(a,list):
        if len(a)!=len(b):return [(path,'length_changed')]
        return [change for i,(x,y) in enumerate(zip(a,b)) for change in ast_changes(x,y,path+f'[{i}]')]
    return [] if a==b else [(path,[a,b])]
for name,old,new in [('iald_estado_publicado.py',b'else 10000000',b'else 32000000'),('iald_core_indexado.py',b'total > 10000000',b'total > 32000000')]:
    raw=(R/name).read_bytes();assert raw.count(old)==1
    changed=raw.replace(old,new);save(stage/name,changed)
    before=ast.parse(raw);after=ast.parse(changed);delta=ast_changes(before,after)
    assert len(delta)==1 and delta[0][1]==[10000000,32000000],delta
    if name=='iald_estado_publicado.py':assert b'64000000 if key == ' in changed
    patch=''.join(difflib.unified_diff(raw.decode().splitlines(True),changed.decode().splitlines(True),fromfile=name,tofile=name))
    save(C/'patches'/(name+'.patch'),patch.encode())
    plan.append({'runtime_path':str(R/name),'baseline_sha256':sha(raw),'baseline_bytes':len(raw),
        'staged_path':str(stage/name),'staged_sha256':sha(changed),'staged_bytes':len(changed),
        'ast_changes':delta,'all_other_ast_nodes_identical':True,'replacement_occurrences':1,
        'patch_path':str(C/'patches'/(name+'.patch'))})
def load(path,label):
    spec=importlib.util.spec_from_file_location(label,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
old_pub=load(R/'iald_estado_publicado.py','compat_original_published')
new_pub=load(stage/'iald_estado_publicado.py','compat_candidate_published')
old_corpus=load(R/'iald_core_indexado.py','compat_original_corpus')
new_corpus=load(stage/'iald_core_indexado.py','compat_candidate_corpus')
from iald_kernel import KernelCatalog
catalog=KernelCatalog(A/'science/memory_stage/kernel')
m=json.loads((A/'science/memory_stage/manifest_staged.json').read_bytes())
baseline=json.loads((R/'iald_nucleo_fixo.json').read_bytes())
evidence=copy.deepcopy(m['published_evidence'])
# URLs below are syntax fixtures reused from the verified installed baseline.
# These tests assert no v394 publication, remote availability, or URL/content binding.
for key in ('program','seal','result','proof_manifest'):evidence[key]['url']=baseline['published_evidence'][key]['url']
result_path=Path(evidence['result']['path']);result_raw=result_path.read_bytes();assert len(result_raw)==12670682
for row in evidence['hypothesis_sources']:
    row['url']=next(x['url'] for x in baseline['published_evidence']['hypothesis_sources'] if x['id']==row['id'])
tests=[]
def expect_error(name,fn,fragment=None):
    try:fn()
    except ValueError as exc:
        assert fragment is None or fragment in str(exc),(name,type(exc).__name__)
        tests.append({'name':name,'status':'PASS_EXPECTED_REFUSAL','exception_type':type(exc).__name__})
    else:raise AssertionError('Expected refusal: '+name)
def passed(name):tests.append({'name':name,'status':'PASS'})
with tempfile.TemporaryDirectory(prefix='fixtures_',dir=C) as temp:
    fixture=Path(temp);cfg=fixture/'corpus.json'
    entry={'id':'sealed_result_fixture','path':str(result_path),'url':baseline['published_evidence']['result']['url'],
           'public_sha256':sha(result_raw),'role':'OFFLINE_SYNTAX_FIXTURE_NOT_V394_PUBLICATION'}
    def corpus(module,entries=None):
        cfg.write_bytes(json.dumps({'format':1,'entries':entries if entries is not None else [entry]}).encode())
        return module.DocumentCorpus(cfg)._load()
    expect_error('original_published_rejects_real_v394_12670682',lambda:old_pub.published_evidence(evidence,catalog),'acima do limite')
    expect_error('original_corpus_rejects_real_v394_12670682',lambda:corpus(old_corpus),'acima do limite')
    _,meta=new_pub.published_evidence(evidence,catalog);assert meta['published_evidence_checked'];passed('candidate_published_accepts_real_sealed_v394')
    docs=corpus(new_corpus);assert docs[entry['id']]['sha256']==sha(result_raw);passed('candidate_corpus_accepts_v394_valid_hash_url_fixture')
    scratch=fixture/'um_absoluto.json';sealfile=fixture/'um_absoluto_selo.json'
    def altered_evidence(raw,refresh_hash):
        scratch.write_bytes(raw);ev=copy.deepcopy(evidence);ev['result']['path']=str(scratch)
        if refresh_hash:
            seal=json.loads(Path(evidence['seal']['path']).read_bytes());seal['sha256'][scratch.name]=sha(raw)
            sealfile.write_bytes(json.dumps(seal).encode());ev['seal']['path']=str(sealfile)
        return ev
    oversized=result_raw+b' '*(32000001-len(result_raw))
    ev=altered_evidence(oversized,True)
    expect_error('candidate_published_rejects_32000001_bytes',lambda:new_pub.published_evidence(ev,catalog),'acima do limite')
    large_entry={**entry,'path':str(scratch),'public_sha256':sha(oversized)}
    expect_error('candidate_corpus_rejects_32000001_total',lambda:corpus(new_corpus,[large_entry]),'acima do limite')
    del oversized
    boundary=result_raw+b' '*(32000000-len(result_raw));ev=altered_evidence(boundary,True)
    assert new_pub.published_evidence(ev,catalog)[1]['published_evidence_checked'];passed('candidate_published_accepts_exact_32000000_valid_padded_json_fixture')
    large_entry={**entry,'path':str(scratch),'public_sha256':sha(boundary)}
    assert corpus(new_corpus,[large_entry])[entry['id']]['bytes']==32000000;passed('candidate_corpus_accepts_exact_32000000')
    tiny=fixture/'extra.txt';tiny.write_bytes(b'x')
    extra={**entry,'id':'extra_fixture','path':str(tiny),'public_sha256':sha(b'x')}
    expect_error('candidate_corpus_total_32000001_across_two_files',lambda:corpus(new_corpus,[large_entry,extra]),'acima do limite')
    del boundary
    bad=altered_evidence(result_raw+b' ',False)
    expect_error('candidate_published_rejects_tampered_hash',lambda:new_pub.published_evidence(bad,catalog),'corresponde ao selo')
    expect_error('candidate_corpus_rejects_tampered_hash',lambda:corpus(new_corpus,[{**entry,'public_sha256':'0'*64}]),'publicação verificada')
    expect_error('candidate_corpus_rejects_empty_url',lambda:corpus(new_corpus,[{**entry,'url':''}]),'publicação verificada')
    expect_error('candidate_corpus_rejects_unpinned_branch_url',lambda:corpus(new_corpus,[{**entry,'url':entry['url'].replace(entry['url'].split('/')[5],'main')}]),'publicação verificada')
    expect_error('candidate_corpus_rejects_relative_path',lambda:corpus(new_corpus,[{**entry,'path':'um_absoluto.json'}]),'Fonte de documento inválida')
    wrongext=fixture/'wrong.bin';wrongext.write_bytes(b'x')
    expect_error('candidate_corpus_rejects_wrong_extension',lambda:corpus(new_corpus,[{**entry,'path':str(wrongext)}]),'Fonte de documento inválida')
    expect_error('candidate_corpus_rejects_duplicate_id',lambda:corpus(new_corpus,[entry,entry]),'duplicado')
    empty=fixture/'empty.txt';empty.write_bytes(b'')
    expect_error('candidate_corpus_rejects_empty_file',lambda:corpus(new_corpus,[{**entry,'path':str(empty),'public_sha256':sha(b'')}]),'Acervo vazio')
    program=fixture/'oversize.py';program.write_bytes(b' '*(64000001));ev=copy.deepcopy(evidence);ev['program']['path']=str(program)
    expect_error('candidate_published_preserves_64000000_program_cap',lambda:new_pub.published_evidence(ev,catalog),'acima do limite')
    ev=copy.deepcopy(evidence);ev['program']['path']='um.py'
    expect_error('candidate_published_rejects_relative_program_path',lambda:new_pub.published_evidence(ev,catalog),'Caminho de evidência inválido')
    ev=copy.deepcopy(evidence);ev['unexpected']='extra'
    expect_error('candidate_published_rejects_unknown_config_key',lambda:new_pub.published_evidence(ev,catalog),'incompleta')
    ev=copy.deepcopy(evidence);del ev['proof_manifest']
    expect_error('candidate_published_rejects_missing_required_evidence',lambda:new_pub.published_evidence(ev,catalog),'incompleta')
assert all(sha(Path(row['runtime_path']).read_bytes())==row['baseline_sha256'] for row in plan)
assert sha(original_receipt.read_bytes())==original_receipt_pin
write(C/'TEST_RESULTS_R1.json',{'status':'PASS','test_count':len(tests),'tests':tests,
    'ast_guard_preservation':plan,'network_calls':0,'api_calls':0,'count_calls':0,
    'url_fixture_scope':'Existing v392 URL syntax and local hash only; not v394 publication or remote equality.',
    'empty_url_guard_location':'DocumentCorpus only. published_evidence never enforced URL syntax; AST parity preserves that existing scope.'})
write(C/'INSTALL_PLAN_R1.json',{'status':'STAGED_ONLY_REVIEW_REQUIRED','files':plan,'file_count':2,'installation_performed':False})
def pin(path):
    path=Path(path);raw=path.read_bytes();return {'path':str(path),'sha256':sha(raw),'bytes':len(raw)}
delivery={'status':'PREPARED_READER_COMPAT_REVIEW_REQUIRED','reference':str(task.REF),'task_id':'reader_compat',
    'actor':'codex-v394-app-builder','lease_id':preflight['lease_id'],'preflight_revision':preflight['receipt']['revision'],
    'changes':'Only JSON evidence maximum and corpus aggregate maximum: 10000000 -> 32000000 bytes. Program maximum remains 64000000.',
    'plan':pin(C/'INSTALL_PLAN_R1.json'),'tests':pin(C/'TEST_RESULTS_R1.json'),'test_script':pin(__file__),
    'staged_files':[pin(stage/row['runtime_path'].split('\\')[-1]) for row in plan],
    'test_count':len(tests),'only_two_ast_constants_changed':True,'all_other_guards_identical':True,
    'source_result':pin(result_path),'original_app_delivery':pin(original_receipt),
    'runtime_files_unchanged':True,'original_app_delivery_unchanged':True,
    'source_code_or_science_run':False,'reader_code_executed_in_isolation':True,
    'network_calls':0,'api_calls':0,'additional_token_counts':0,'private_sources_read':False,
    'production_installation':False,'independent_review_pending':True,'semantic_acceptance':False}
write(C/'DELIVERY_PREPARED_R1.json',delivery)
print(json.dumps({'status':delivery['status'],'tests_passed':len(tests),'staged_files':2,'runtime_changed':False}))
