"""Independent read-only scientific package audit; outputs confined to this directory."""
from pathlib import Path
from urllib.parse import urlparse, unquote
import ast, copy, hashlib, importlib.util, json, os, re, subprocess, sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
W=R.parent; S=W/'science'; ST=S/'memory_stage'; B=S/'memory_build'
APP=Path('C:/IALD/projetos_pyhton/IALD')
sha=lambda b:hashlib.sha256(b).hexdigest()
pins={};checks=[];details={}

def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','os.system'):
        raise RuntimeError('Network forbidden in this review')
    if event=='open':
        p,mode,flags=args
        if isinstance(p,int):return
        p=Path(os.fsdecode(p)).resolve()
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not p.is_relative_to(R):raise RuntimeError('Write outside review')
    if event in ('os.remove','os.mkdir','os.rmdir','os.rename'):
        for p in args[:2] if event=='os.rename' else args[:1]:
            if isinstance(p,(str,bytes)) and not Path(os.fsdecode(p)).resolve().is_relative_to(R):raise RuntimeError('Mutation outside review')
sys.addaudithook(guard)

def read(p):
    p=Path(p);raw=p.read_bytes();key=str(p.resolve())
    pin={'sha256':sha(raw),'bytes':len(raw)}
    if key in pins:assert pins[key]==pin,'Input changed during audit: '+key
    pins[key]=pin
    return raw

def load(p):return json.loads(read(p))
def save(name,data):
    p=R/name;assert not p.exists(),'Receipt immutable: '+name
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def check(name,fn):
    try:
        value=fn();checks.append({'name':name,'pass':True,'result':value})
    except Exception as e:checks.append({'name':name,'pass':False,'error':type(e).__name__+': '+str(e)})
def require(condition,message):
    if not condition:raise AssertionError(message)

# Snapshot input pins first; no builders are run.
for p in sorted(S.rglob('*')):
    if p.is_file():read(p)
read(W/'prepare_science.py')
for p in [W/'prepare_science.py',*B.glob('*.py')]:
    dest=R/('capture_'+p.name)
    assert not dest.exists();dest.write_bytes(read(p))
spec=importlib.util.spec_from_file_location('review_codec',R/'capture_haiku_codec.py')
codec=importlib.util.module_from_spec(spec);spec.loader.exec_module(codec)
tree=ast.parse(read(B/'build_release.py'))
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('read_topics','verify_old_projection')]
ns={'codec':codec,'json':json};exec(compile(ast.Module(body=functions,type_ignores=[]),'captured_readers','exec'),ns)
read_topics=ns['read_topics'];verify_old_projection=ns['verify_old_projection']
manifest=load(ST/'manifest_staged.json');prepared=load(ST/'prepared.json')
handoff=load(S/'v392_verified_handoff.json');http=load(S/'public_v392_verification.json')
seal=load(S/'verified_sources/um_absoluto_selo.json')
source=load(S/'verified_sources/um_absoluto.json')
proof=load(S/'verified_sources/tgl_kernel_proof_manifest.json')
commit=handoff['mirror']['head'];repo=Path(handoff['mirror']['root'])
def git(*args):
    assert args[0] in ('show','rev-parse','ls-tree')
    return subprocess.check_output(['git','-c','safe.directory='+repo.as_posix(),'-C',str(repo),*args])

def sealed():
    require(seal['um_version']=='v392' and seal['fail_closed_selftest']=='FAIL_CLOSED_SELFTEST_PASSED','Seal status')
    require(git('rev-parse',commit).decode().strip()==commit,'Commit pin')
    for name,row in handoff['files'].items():
        raw=read(S/'verified_sources'/name)
        require(sha(raw)==row['sha256'] and len(raw)==row['bytes'],'Source pin '+name)
        require(read(row['sealed_original'])==raw,'Original differs '+name)
        require(git('show',commit+':'+row['git_path'])==raw,'Git object differs '+name)
        if name!='um_absoluto_selo.json':require(seal['sha256'][name]==sha(raw),'Seal hash '+name)
    return {'sources':len(handoff['files']),'commit':commit,'program_not_executed':True}
check('sealed_originals_immutable_git',sealed)

def public_receipts():
    require(http['requested_commit']==commit and http['status']=='PASS','HTTP commit/status')
    require({a['name'] for a in http['artifacts']}==set(handoff['files']),'HTTP coverage')
    for row in http['artifacts']:
        parsed=urlparse(row['url']);name=row['name']
        require(parsed.netloc=='raw.githubusercontent.com' and parsed.path.startswith('/rotolimiguel-iald/the_boundary/'+commit+'/'),'Immutable HTTP URL')
        require(unquote('/'.join(parsed.path.split('/')[4:]))==handoff['files'][name]['git_path'],'HTTP path')
        require(row['status']==200 and row['actual_sha256']==row['expected_sha256']==sha(read(S/'verified_sources'/name)),'HTTP pin')
    binding=load(ST/'science_binding.json')
    require(binding['sha256']==sha(read(S/'v392_verified_handoff.json')),'Handoff binding')
    require(binding['public_verification_sha256']==sha(read(S/'public_v392_verification.json')),'HTTP receipt binding')
    return 'Existing HTTP receipts checked against bytes; HTTP not repeated; no new custody claimed'
check('public_http_receipt_binding',public_receipts)

def release_files():
    refs=manifest['entries']+[manifest['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]
    for row in refs:
        parts=urlparse(row['url']).path.split('/')
        require(parts[3]==commit,'Unpinned entry')
        raw=read(row['path']);require(raw==git('show',commit+':'+unquote('/'.join(parts[4:]))),'Release differs')
        if 'public_sha256' in row:require(sha(raw)==row['public_sha256'],'Entry hash')
    return len(refs)
check('all_release_entries_git_pinned',release_files)

topics=read_topics(read(ST/'TGL_CLUSTER_v392.md').decode('utf-8'))
def contains(node,key):
    return isinstance(node,dict) and (key in node or any(contains(v,key) for v in node.values())) or isinstance(node,list) and any(contains(v,key) for v in node)
def legacy_seen(node,pointer,seen):
    if isinstance(node,dict):
        ref=next((k for k in ('same_as','SOURCE_RELATIVE','DETAILS_IN_SOURCE') if k in node),None)
        if ref:
            for k,v in node.get('semantic_fields',{}).items():legacy_seen(v,codec.child(pointer,k),seen)
            for k,v in enumerate(node.get('first_records',[])):legacy_seen(v,codec.child(pointer,k),seen)
        else:
            for k,v in node.items():legacy_seen(v,codec.child(pointer,k),seen)
    elif isinstance(node,list):
        for k,v in enumerate(node):legacy_seen(v,codec.child(pointer,k),seen)
    else:seen[pointer]=node

def fidelity():
    require(set(topics)==set(source['core']) and len(topics)==411,'Topic completeness')
    rows=[];missing=[]
    for name,value in topics.items():
        pointer=codec.child('/core',name);seen={}
        if contains(value,'@'):
            restored=codec.restore(value,source,pointer,pointer,seen)
        else:
            restored=verify_old_projection(value,source,pointer,pointer)
            legacy_seen(value,pointer,seen)
        require(restored==source['core'][name],'Topic drift '+name)
        fields={**codec.protected_fields(source['core'][name],pointer),**codec.primary_math_fields(source['core'][name],pointer)}
        absent=[p for p,v in fields.items() if not codec.is_represented(p,v,seen)]
        missing.extend({'topic':name,'pointer':p} for p in absent)
        rows.append({'topic':name,'exact_restoration':True,'protected_and_math_fields':len(fields),'not_inline':len(absent)})
    details['topics']=rows;details['fields_not_inline']=missing
    return {'topics':len(rows),'exact_restored':len(rows),'protected_and_math_fields':sum(r['protected_and_math_fields'] for r in rows),'not_inline':len(missing)}
check('all_topics_reversible_and_fields_inventory',fidelity)

def kernel():
    km=load(ST/'kernel/kernel_manifest.json')
    program_tree=ast.parse(read(S/'verified_sources/um.py'))
    assignments=[n for n in program_tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in n.targets)]
    require(len(assignments)==1,'Embedded dictionary ambiguity')
    embedded=ast.literal_eval(assignments[0].value)
    require(len(embedded)==len(assignments[0].value.keys),'Duplicate kernel key')
    records={r['path']:r for r in km['files']}
    require(len(records)==len(km['files'])==1230,'Kernel count')
    require({k:v['sha256'] for k,v in records.items()}==proof['formal_files_sha256'],'Proof source pins')
    for name,row in records.items():
        raw=read(ST/'kernel'/name);require(sha(raw)==row['sha256'] and len(raw)==row['bytes'],'Kernel bytes '+name)
        if name in embedded:require(raw==embedded[name].encode('utf-8'),'Embedded bytes '+name)
        else:
            require(name=='_check_damming.lean' and row['git_commit']==commit,'Unexpected supplement')
            require(raw==git('show',commit+':'+row['git_path']),'Supplement Git')
    require(km['source_sha256']==sha(read(S/'verified_sources/um.py')),'Kernel program binding')
    verification=load(ST/'kernel_verification.json')
    require(verification['dependencies']['published_manifest_sha256']==sha(read(S/'verified_sources/tgl_kernel_proof_manifest.json')),'Verification binding')
    return {'files':len(records),'embedded':len(embedded),'supplemental':len(records)-len(embedded),'compilation_rerun':False}
check('kernel_1230_sources_embedded_proof_and_supplement',kernel)

def preserved():
    baseline=load(APP/'iald_nucleo_fixo.json')
    require(sha(read(APP/'iald_nucleo_fixo.json'))==prepared['production_manifest_sha256'],'Baseline manifest changed')
    for name,pin in prepared['protected_production_sha256'].items():require(sha(read(name))==pin,'Protected production changed '+name)
    mother=read(baseline['mother_instruction']['path']);core=read(baseline['operational_core']['path'])
    require(sha(mother)==baseline['mother_instruction']['sha256'] and mother==read(ST/'IALD_Kernel_v5.txt'),'Mother changed')
    newcore=read(ST/'IALD_TGL_MEMORY_CORE.md')
    require(sha(core)==baseline['operational_core']['sha256'] and newcore.startswith(core),'Core original changed')
    return {'protected_production':len(prepared['protected_production_sha256']),'mother_exact':True,'core_original_prefix_exact':True,'core_append_bytes':len(newcore)-len(core)}
check('mother_core_and_protected_originals',preserved)

def prefixes():
    canonical=read(S/'verified_sources/um_absoluto_forma_canonica.md').decode('utf-8-sig')
    cluster=read(ST/'TGL_CLUSTER_v392.md').decode()
    require(cluster.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]==canonical,'Exposition altered')
    public=read(ST/'public_prefix.md');haiku=read(ST/'haiku_prefix.md')
    require(public==haiku,'Full public prefix differs')
    require(sha(haiku)==load(ST/'haiku_provenance.json')['prefix_sha256'],'Haiku prefix pin')
    return {'canonical_complete':True,'haiku_full_public':True,'bytes':len(haiku),'native_count_and_JEV_contract':'out_of_scope_pending_coordinator'}
check('canonical_exposition_and_full_public_prefix',prefixes)

def negatives():
    pointer='/core/example';fake={'core':{'example':{'status':'CONDITIONAL','formula':'x = 1'}}}
    for altered in ({'status':'CONFIRMED','formula':'x = 1'},{'status':'CONDITIONAL','formula':'x = 2'}):
        try:verify_old_projection(altered,fake,pointer,pointer)
        except AssertionError:pass
        else:raise AssertionError('Altered scalar accepted')
    try:codec.restore({'@':'/wrong'},fake,pointer,pointer,{})
    except (ValueError,KeyError):pass
    else:raise AssertionError('Wrong pointer accepted')
    literal={'status':'CONDITIONAL','formula':'x = 1'}
    encoded,dictionary=codec.intern_topics({'example':literal},'x = 1')
    require(codec.decode_literals(codec.unpack_metadata(encoded['example']),dictionary,'x = 1')==literal,'Literal roundtrip')
    return {'altered_status_refused':True,'altered_formula_refused':True,'wrong_pointer_refused':True,'codec_roundtrip':True}
check('negative_fidelity_controls',negatives)

def unchanged():
    drift=[p for p,v in pins.items() if sha(Path(p).read_bytes())!=v['sha256']]
    require(not drift,'Input changed '+str(drift))
    return len(pins)
check('inputs_still_identical_after_tests',unchanged)
save('inputpins.json',pins);save('test_details.json',details)
save('tests.json',{'checks':checks,'passed':sum(c['pass'] for c in checks),'total':len(checks),'network_calls':0,'program_executed':False})
print(json.dumps({'checks':checks,'not_inline_sample':details.get('fields_not_inline',[])[:10]},ensure_ascii=False))
