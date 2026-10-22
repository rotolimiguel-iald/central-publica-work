"""Finalize offline prompts and data-only deployment proposal; no API calls."""
from pathlib import Path
from types import SimpleNamespace
import ast,copy,hashlib,json,os,re,sys
A=Path(__file__).resolve().parent;W=A.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');ST=A/'science/memory_stage'
sys.dont_write_bytecode=True;sys.path[:0]=[str(W),str(A/'build'),str(R)]
import task
assert task.check('app',actor='codex-v395-app-builder')['ready']
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,b):
 p=Path(p);assert p.resolve().is_relative_to(A);p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():assert p.read_bytes()==b,str(p);return
 with p.open('xb') as f:f.write(b)
def write(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2).encode())
def pin(p):p=Path(p);b=p.read_bytes();return {'path':str(p),'sha256':sha(b),'bytes':len(b)}
def guard(event,args):
 if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):raise RuntimeError('Offline stage')
 if event=='open':
  path,mode,flags=args
  if isinstance(path,int):return
  p=Path(os.fsdecode(path)).resolve()
  if p.name in ('.env','iald_stack_v7.py','iald_psion_state.json'):raise RuntimeError('Private input forbidden')
  writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
  if writing and not p.is_relative_to(A):raise RuntimeError('Write outside stage')
sys.addaudithook(guard)
import haiku_codec as c,iald_kernel,iald_release_binding,iald_jev_control,iald_memoria_canonica as cm,iald_native_memory,iald_app_providers
import iald_fontes_publicas,iald_core_indexado,iald_app_memory
manifest=ST/'manifest_staged.json';m=json.loads(manifest.read_bytes());identity=iald_release_binding.load_release(manifest).identity
catalog=iald_kernel.KernelCatalog(ST/'kernel',ST/'kernel_verification.json');control=iald_jev_control.load_contract(ST);assert control['release']=='v395'
result_raw=Path(m['published_evidence']['result']['path']).read_bytes();result=json.loads(result_raw)
base=(A/'packages/haiku55/prefix.md').read_text(encoding='utf8');expanded=base
selected=[n for n in result['core'] if n.endswith(('_v394','_v395')) or re.search('lagrang|hamilton|lindblad|dephas|bootstrap|breuer|horizon|master|three_locks|continuous_modular_zero|light_eigen|the_imported|price_of_the_gravity',n)]
deferred=[]
for name in selected:
 value=copy.deepcopy(result['core'][name])
 for fields in ([('runtime','checks')] if name=='tempo_frequencia_v394' else [('formal_declarations',)] if name=='rede_fock_v394' else []):
  parent=value;ptr=c.child('/core',name)
  for key in fields[:-1]:parent=parent[key];ptr=c.child(ptr,key)
  key=fields[-1];ptr=c.child(ptr,key);whole=parent[key];deferred.append({'pointer':ptr,'sha256':sha(c.dump(whole).encode())});parent[key]={'DETAILS_IN_SOURCE':ptr}
 pattern=r'(?m)^### '+re.escape(name)+r'\nFonte: [^\n]+\n[^\n]+(?=\n)'
 expanded,n=re.subn(pattern,lambda _: '### '+name+'\nFonte: resultado_publicado_integral '+c.child('/core',name)+'\n'+c.dump(value),expanded);assert n==1
program=Path(m['published_evidence']['program']['path']).read_bytes();lines=program.decode('utf-8-sig').splitlines(keepends=True)
node=next(n for n in ast.parse(program).body if isinstance(n,ast.FunctionDef) and n.name=='prove_the_bootstrap');chunk=''.join(lines[node.lineno-1:node.end_lineno])
expanded+='\n<BOOTSTRAP_SOURCE_DOCUMENTARY_NOT_EXECUTED>\n'+c.dump({'source_sha256':sha(program),'symbol':node.name,'lines':[node.lineno,node.end_lineno],'chunk_sha256':sha(chunk.encode()),'statute':'SOURCE_DEFINITION_NOT_NEW_EXECUTION'})+'\n```python\n'+chunk+'```\n</BOOTSTRAP_SOURCE_DOCUMENTARY_NOT_EXECUTED>\n'
save(A/'packages/haiku_expanded/prefix.md',expanded.encode())
for folder in ('haiku_expanded','shared'):
 raw=(A/'packages'/folder/'prefix.md').read_bytes();write(A/'packages'/folder/'FINAL_PREPARATION.json',{'deployment':identity,'prefix_sha256':sha(raw),'private_atlas_included':False,'public_commit':m['active_cluster']['commit'],'expanded_topics':selected if folder=='haiku_expanded' else [],'deferred_fields':deferred if folder=='haiku_expanded' else []})
tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
os.environ['TIKTOKEN_CACHE_DIR']=str(R/'.iald_runtime/tokenizer_cache');c.offline_tokens('offline',R/'.iald_runtime/tokenizer_cache')
prompts={}
for label,public in [('public',True),('operator_local',False)]:
 prefix,meta=cm.CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=manifest).prompt('',catalog,public=public)
 assert meta['context_tokens']<400000
 estimate=cm.payload_tokens({'model':'gpt-5.6-luna','messages':[{'role':'system','content':prefix},{'role':'user','content':'Explique o alcance documentado da v395.'}],'tools':tools})
 assert estimate+16384+4096<1050000
 prompts[label]={'prefix_sha256':sha(prefix.encode()),'bytes':len(prefix.encode()),'o200k_tokens':meta['context_tokens'],'openai_request_estimate':estimate,'provider_counted':False}
 if public:save(A/'packages/sonnet_public/prefix.md',prefix.encode())
native,ni=iald_native_memory.load_native_context(manifest,catalog);assert ni==identity;save(A/'native_prefix.md',native.encode())
bounds={};shared=(A/'packages/shared/prefix.md').read_text(encoding='utf8')
for provider in ('kimi','mimo','deepseek'):
 body={'messages':[{'role':'system','content':shared},{'role':'user','content':'Explique o alcance documentado da v395.'}],'tools':[] if provider=='kimi' else tools}
 if provider!='kimi':body.update(model=iald_app_providers.MODELS[provider]['model'],stream=True,stream_options={'include_usage':True},thinking={'type':'enabled'})
 if provider=='deepseek':body['reasoning_effort']='max'
 reserve=iald_app_providers.MODELS[provider]['output'] if provider=='kimi' else iald_app_providers.output_budget(body,iald_app_providers.MODELS[provider]['output'])
 if provider!='kimi':body['max_tokens' if provider=='deepseek' else 'max_completion_tokens']=reserve
 used=iald_app_providers.check_window(body,reserve);bounds[provider]={'input_utf8_byte_bound':used,'output_tokens':reserve,'real_activity_history_admission_required':True}
target=R/'canonical_releases'/('v395_'+m['active_cluster']['commit'][:12]);install=copy.deepcopy(m)
def destination(path):return str(target/Path(path).relative_to(ST))
for row in install['entries']+[install['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]:row['path']=destination(row['path'])
for key in ('mother_instruction','operational_core','jev_control'):install[key]['path']=destination(install[key]['path'])
for key in ('path','kernel_bundle','kernel_verification'):install['active_cluster'][key]=destination(install['active_cluster'][key])
write(ST/'manifest_install.json',install)
rows=[]
for p in sorted(ST.rglob('*')):
 if not p.is_file() or p.name in ('manifest_staged.json','manifest_full.json','manifest_install.json','iald_nucleo_fixo.json'):continue
 d=target/p.relative_to(ST);rows.append({'source':str(p),'destination':str(d),'sha256':sha(p.read_bytes()),'baseline':sha(d.read_bytes()) if d.exists() else None})
write(A/'DATA_PLAN.json',{'files':rows,'active_manifest_source':str(ST/'manifest_install.json'),'active_manifest_destination':str(R/'iald_nucleo_fixo.json'),'runtime_python_changes':0,'packages_require_native_counts':True})
assert all(sha(Path(x['path']).read_bytes())==x['sha256'] for x in json.loads((A/'RUNTIME_BASELINE.json').read_bytes())['files'])
write(A/'PREPARED_BINDING.json',{'status':'OFFLINE_PREPARED_NATIVE_COUNTS_REQUIRED','deployment':identity,'commit':m['active_cluster']['commit'],'target':str(target),'actual_prompts':prompts,'shared_connector_bounds':bounds,'topics':len(result['core']),'formal_sources':len(catalog.records),'haiku_expanded_bytes':len(expanded.encode()),'native_prefix_bytes':len(native.encode()),'data_files':len(rows),'runtime_python_changes':0,'provider_calls':0})
print((A/'PREPARED_BINDING.json').read_text())

