"""Rebind new final data and public prefixes. No API, inference or production writes."""
from pathlib import Path
from types import SimpleNamespace
import ast,copy,hashlib,json,os,re,sys
F=Path(__file__).resolve().parent;A=F.parent;W=A.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True;sys.path.insert(0,str(W));import task
preflight=task.check('app',actor='codex-v394-app-builder');assert preflight['ready']
sys.path.insert(0,str(A));from prepare_science import save,write,sha
def pin(path):
    p=Path(path);raw=p.read_bytes();return {'path':str(p),'sha256':sha(raw),'bytes':len(raw)}
frozen=[pin(p) for p in A.rglob('*') if p.is_file() and not p.is_relative_to(F)]
write(F/'HISTORICAL_PINS.json',{'files':frozen})
runtime=[pin(p) for p in R.glob('*.py') if p.name not in ('iald_stack_v7.py','iald_psion_state.py')]
runtime.append(pin(R/'iald_nucleo_fixo.json'));write(F/'RUNTIME_BASELINE.json',{'files':runtime})
pub=json.loads((F/'PUBLICATION_VERIFIED.json').read_bytes());commit=pub['commit'];stage=F/'science/memory_stage'
B=F/'build';B.mkdir(exist_ok=True)
source=A.parent.parent/'iald_app_stack_20261014/science/memory_build'
# Audited codec/fit policies; only allow the two reviewed staged readers as pure loaders.
for name in ('haiku_codec.py','fit_transport.py','fit_memory.py'):
    raw=(source/name).read_bytes()
    if name=='haiku_codec.py':
        text=raw.decode();old="need(Path(module.__file__).resolve().parent == root, 'Document loader from unexpected directory')"
        assert text.count(old)==1
        text=text.replace(old,"need(Path(module.__file__).resolve().parent in (root, Path(__file__).resolve().parent), 'Document loader from unexpected directory')")
        raw=text.encode()
    save(B/name,raw)
compat=json.loads((A/'compat/INSTALL_PLAN_R1.json').read_bytes())
for row in compat['files']:
    assert sha(Path(row['runtime_path']).read_bytes())==row['baseline_sha256']
    raw=Path(row['staged_path']).read_bytes();assert sha(raw)==row['staged_sha256'];save(B/Path(row['runtime_path']).name,raw)
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):raise RuntimeError('Final preparation is offline')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,int):return
        p=Path(os.fsdecode(path)).resolve()
        if p.name.lower() in ('.env','iald_stack_v7.py','iald_psion_state.json'):raise RuntimeError('Private source refused')
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not p.is_relative_to(F):raise RuntimeError('Write outside final')
sys.addaudithook(guard)
sys.path[:0]=[str(B),str(R)]
import iald_core_indexado,iald_estado_publicado,iald_cluster,iald_release_binding,iald_memoria_canonica as cm
import iald_kernel,iald_native_memory,iald_jev_control,haiku_codec as c
from fit_transport import fit
from fit_memory import compact
assert Path(cm.__file__).resolve()==(R/'iald_memoria_canonica.py').resolve()
os.environ['TIKTOKEN_CACHE_DIR']=str(R/'.iald_runtime/tokenizer_cache')
m=json.loads((A/'engines/R2/manifest_pending_publication.json').read_bytes())
baseline=json.loads((R/'iald_nucleo_fixo.json').read_bytes())
paths_by_name={Path(rel).name:rel for rel in pub['sources']}
for entry in m['entries']:
    old=next(x for x in baseline['entries'] if x['id']==entry['id'])
    from urllib.parse import urlparse,unquote
    rel=unquote('/'.join(urlparse(old['url']).path.split('/')[4:]));row=pub['sources'][rel]
    entry.update(path=str(stage/'release'/rel),url=row['url'],public_sha256=row['sha256'])
for key in ('program','seal','result','proof_manifest'):
    entry=m['published_evidence'][key];rel=paths_by_name[Path(entry['path']).name]
    entry.update(path=str(stage/'release'/rel),url=pub['sources'][rel]['url'])
from urllib.parse import quote
formal_git={row['path']:row for row in pub['kernel_files_git_proof_and_staging_equal']}
for entry in m['published_evidence']['hypothesis_sources']:
    rel=formal_git[entry['catalog_path']]['git_path']
    entry['url']='https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+commit+'/'+quote(rel,safe='/')
for key in ('mother_instruction','operational_core','jev_control'):
    m[key]['path']=str(stage/Path(m[key]['path']).name)
projected=(A/'engines/R2/data/TGL_CLUSTER_v394_prompt.md').read_bytes()
full=(A/'engines/R2/data/TGL_CLUSTER_v394_full.md').read_bytes()
save(stage/'TGL_CLUSTER_v394_prompt.md',projected);save(stage/'TGL_CLUSTER_v394_full.md',full)
m['active_cluster'].update(path=str(stage/'TGL_CLUSTER_v394_prompt.md'),commit=commit,
    publication_pending=False,kernel_bundle=str(stage/'kernel'),kernel_verification=str(stage/'kernel_verification.json'))
m.pop('staging_only',None);m.pop('publication_pending',None)
assert {e['id'] for e in m['entries']}=={e['id'] for e in baseline['entries']}
assert all(e['url'] for e in m['entries'])
manifest=stage/'manifest_staged.json';write(manifest,m)
save(stage/'iald_nucleo_fixo.json',manifest.read_bytes())
identity=iald_release_binding.load_release(manifest).identity
control=iald_jev_control.load_contract(stage);assert control['release']=='v394'
catalog=iald_kernel.KernelCatalog(stage/'kernel',stage/'kernel_verification.json')
# New faithful base and new shared transport package are reconstructed from the final sources.
base,base_receipt=c.build(manifest,R)
save(F/'science/faithful_base/prefix.md',base.encode());write(F/'science/faithful_base/receipt.json',base_receipt)
previous=A/'science/memory_build/baseline_v368'
shared,shared_receipt=c.build_fitted(manifest,R,previous/'prefix.md',previous/'canonical.json')
result_raw=Path(m['published_evidence']['result']['path']).read_bytes();result=json.loads(result_raw)
shared,transport=fit(shared,result);shared,projection=compact(shared,result,shared_receipt['reused_identical_topics'])
save(F/'packages/shared/prefix.md',shared.encode())
write(F/'packages/shared/preparation.json',{'deployment':identity,'prefix_sha256':sha(shared.encode()),
    'bytes':len(shared.encode()),'receipt':shared_receipt,'transport':transport,'projection':projection,
    'private_atlas_included':False,'public_commit':commit})
expanded=base;selected=[n for n in result['core'] if n.endswith('_v394') or re.search('lagrang|hamilton|lindblad|dephas|bootstrap|breuer|horizon|master|three_locks|continuous_modular_zero|light_eigen|the_imported|price_of_the_gravity',n)]
deferred=[];resident=[]
for name in selected:
    value=copy.deepcopy(result['core'][name])
    for fields in ([('runtime','checks')] if name=='tempo_frequencia_v394' else [('formal_declarations',)] if name=='rede_fock_v394' else []):
        parent=value;ptr=c.child('/core',name)
        for k in fields[:-1]:parent=parent[k];ptr=c.child(ptr,k)
        key=fields[-1];ptr=c.child(ptr,key);whole=parent[key]
        deferred.append({'source_id':'resultado_publicado_integral','json_pointer':ptr,'source_sha256':sha(result_raw),
            'value_sha256':sha(c.dump(whole).encode()),'items':len(whole)})
        parent[key]={'DETAILS_IN_SOURCE':ptr}
    pattern=r'(?m)^### '+re.escape(name)+r'\nFonte: [^\n]+\n[^\n]+(?=\n)'
    replacement='### '+name+'\nFonte: resultado_publicado_integral '+c.child('/core',name)+'\n'+c.dump(value)
    expanded,count=re.subn(pattern,lambda _:replacement,expanded);assert count==1
    resident.append(name)
program=Path(m['published_evidence']['program']['path']).read_bytes();lines=program.decode('utf-8-sig').splitlines(keepends=True)
node=next(x for x in ast.parse(program).body if isinstance(x,ast.FunctionDef) and x.name=='prove_the_bootstrap')
chunk=''.join(lines[node.lineno-1:node.end_lineno])
expanded+='\n<BOOTSTRAP_SOURCE_DOCUMENTARY_NOT_EXECUTED>\n'+c.dump({'source_sha256':sha(program),'symbol':node.name,
    'lines':[node.lineno,node.end_lineno],'chunk_sha256':sha(chunk.encode()),'statute':'SOURCE_DEFINITION_NOT_NEW_EXECUTION'})+'\n```python\n'+chunk+'```\n</BOOTSTRAP_SOURCE_DOCUMENTARY_NOT_EXECUTED>\n'
save(F/'packages/haiku55/prefix.md',expanded.encode())
write(F/'packages/haiku55/preparation.json',{'deployment':identity,'prefix_sha256':sha(expanded.encode()),'bytes':len(expanded.encode()),
    'base_receipt':pin(F/'science/faithful_base/receipt.json'),'resident_whole_topics':resident,'deferred_whole_fields':deferred,
    'all_422_topics_retrievable':True,'private_atlas_included':False,'public_commit':commit})
atlas=Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md');prompts={}
import iald_fontes_publicas,iald_app_memory
tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
for name,public in [('public',True),('operator_local',False)]:
    prefix,metadata=cm.CanonicalMemory(atlas,'nucleo_kernel',nucleus_manifest=manifest).prompt('',catalog,public=public)
    assert metadata['context_tokens']<400000
    payload={'model':'gpt-5.6-luna','messages':[{'role':'system','content':prefix},{'role':'user','content':'Explique o alcance documentado da v394.'}],'tools':tools}
    estimate=cm.payload_tokens(payload);assert estimate+16384+4096<1050000
    prompts[name]={'prefix_sha256':sha(prefix.encode()),'bytes':len(prefix.encode()),'o200k_tokens':metadata['context_tokens'],
        'openai_request_estimate':estimate,'openai_estimated_remaining':1050000-estimate-16384-4096,
        'always_present_sections':metadata['always_present_sections'],'provider_counted':False}
    if public:save(F/'packages/sonnet_public/prefix.md',prefix.encode())
    else:assert metadata['always_present_sections']==['I.1–I.5 (fundamentos)','VII']
native,native_identity=iald_native_memory.load_native_context(manifest,catalog);assert native_identity==identity
save(F/'native_prefix.md',native.encode())
target=R/'canonical_releases'/('v394_'+commit[:12]);install=copy.deepcopy(m)
def destination(path):return str(target/Path(path).relative_to(stage))
for row in install['entries']+[install['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]:row['path']=destination(row['path'])
for key in ('mother_instruction','operational_core','jev_control'):install[key]['path']=destination(install[key]['path'])
for key in ('path','kernel_bundle','kernel_verification'):install['active_cluster'][key]=destination(install['active_cluster'][key])
write(stage/'manifest_install.json',install)
assert all(sha(Path(row['path']).read_bytes())==row['sha256'] for row in frozen+runtime)
write(F/'PREPARED_BINDING.json',{'status':'FINAL_PUBLIC_BINDING_PREPARED_NATIVE_COUNTS_REQUIRED','commit':commit,
    'deployment':identity,'manifest':pin(manifest),'install_manifest':pin(stage/'manifest_install.json'),
    'target':str(target),'public_source_ids':[x['id'] for x in m['entries']],
    'kernel_sources':1423,'core_v5_bytes_preserved':True,'runtime_unmodified':True,
    'historical_artifacts_unchanged':len(frozen),'actual_prompts':prompts,
    'public_only_count_targets':['packages/haiku55','packages/shared','packages/sonnet_public'],
    'operator_egress_forbidden':True,'production_changes':0,'provider_generation_calls':0})
print(json.dumps({'status':'FINAL_BINDING_PREPARED','commit':commit,'deployment':identity,
    'haiku_expanded_bytes':len(expanded.encode()),'shared_bytes':len(shared.encode()),'actual_prompts':prompts}))
