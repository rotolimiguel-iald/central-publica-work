"""Data-only projected cluster; real current CanonicalMemory, no provider calls."""
from pathlib import Path
import copy, hashlib, importlib.util, json, math, os, re, sys
from types import SimpleNamespace
E=Path(__file__).resolve().parent;A=E.parent;W=A.parent
R=Path(r'C:\IALD\projetos_pyhton\IALD');S=A/'science';OLD=S/'memory_stage'
sys.dont_write_bytecode=True
sys.path.insert(0,str(W));import task
preflight=task.check('all_engines_admission',actor='codex-v394-app-builder');assert preflight['ready']
# Only the reviewed 32 MB reader candidates precede CURRENT runtime modules.
# Never import the earlier staging CanonicalMemory or its relaxed admission guard.
sys.path[:0]=[str(A/'compat/staging'),str(R),str(A)]
from prepare_science import save,write,sha
def pin(path):
    path=Path(path);raw=path.read_bytes();return {'path':str(path),'sha256':sha(raw),'bytes':len(raw)}
frozen_paths=[A/'DELIVERY_PREPARED.json',A/'PACKAGE_SELECTION.json',
    S/'haiku_expanded_count/package/prefix.md',S/'haiku_expanded_count/package/manifest.json',
    S/'haiku_expanded_count/native_count.json',S/'shared_count/package/prefix.md',
    S/'shared_count/package/manifest.json',S/'shared_count/native_count.json']
frozen=[pin(p) for p in frozen_paths]
runtime={str(p):sha(p.read_bytes()) for p in R.glob('*.py') if p.name not in ('iald_stack_v7.py','iald_psion_state.py')}
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):
        raise RuntimeError('Offline engines admission only')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,int):return
        p=Path(os.fsdecode(path)).resolve()
        if p.name.lower() in ('.env','iald_stack_v7.py','iald_psion_state.json'):
            raise RuntimeError('Confidential source refused')
        writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not p.is_relative_to(E):raise RuntimeError('Write outside engines staging')
sys.addaudithook(guard)
import iald_cluster,iald_memoria_canonica as cm,iald_release_binding,iald_native_memory
import iald_estado_publicado,iald_core_indexado,iald_kernel,iald_fontes_publicas,iald_app_memory
assert Path(cm.__file__).resolve()==(R/'iald_memoria_canonica.py').resolve()
assert Path(iald_cluster.__file__).resolve()==(R/'iald_cluster.py').resolve()
assert Path(iald_estado_publicado.__file__).resolve().parent==(A/'compat/staging').resolve()
sys.path.append(str(S/'memory_build'))
import haiku_codec as codec
# Initialize the existing cached tokenizer through its checked offline loader.
codec.offline_tokens('offline',R/'.iald_runtime/tokenizer_cache')
os.environ['TIKTOKEN_CACHE_DIR']=str(R/'.iald_runtime/tokenizer_cache')
manifest=json.loads((OLD/'manifest_staged.json').read_bytes());baseline=json.loads((R/'iald_nucleo_fixo.json').read_bytes())
result_raw=Path(manifest['published_evidence']['result']['path']).read_bytes();result=json.loads(result_raw)
shared=(OLD/'shared_prefix.md').read_text(encoding='utf-8')
topic_end=shared.index('\n'+codec.MARKER)
matches=[x for x in re.finditer(r'(?m)^### ([^\n]+)\n',shared[:topic_end]) if x.group(1) in result['core']]
capsules={};original_capsules={};added_anchors={}
for i,match in enumerate(matches):
    name=match.group(1);assert name not in capsules
    stop=matches[i+1].start() if i+1<len(matches) else topic_end
    body=shared[match.end():stop].strip()
    original_capsules[name]=body
    added_anchors[name]='/core/'+name not in body
    if added_anchors[name]:body='Fonte: resultado_publicado_integral '+codec.child('/core',name)+'\n'+body
    capsules[name]=body
assert len(capsules)==422
heading=shared.index('DICIONÁRIO DE INDICADORES LITERAIS\n')
legend_end=shared.index('\n',heading+len('DICIONÁRIO DE INDICADORES LITERAIS\n'))
legend=shared[:legend_end].replace('### nome →','Tópico nome →')
expo=shared.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
full=(OLD/'TGL_CLUSTER_v394.md').read_bytes()
data=E/'data';save(data/'TGL_CLUSTER_v394_full.md',full)
header=('# Cluster TGL v394 — projeção de prompt recuperável\n'
    'Fonte integral: resultado_publicado_integral; SHA256 '+sha(result_raw)+'.\n'
    'Cluster integral irmão: tgl_cluster_integral; SHA256 '+sha(full)+'.\n'
    '422 tópicos representados. Cápsulas e referências preservadas literalmente do pacote compartilhado verificado. '
    'Detalhes referenciados NÃO estão carregados; não substituir síntese por valor original. '
    'Estatutos, hipóteses, negativos e fórmulas seguem os campos indicados. Nenhum programa ou Lean executado.\n')
projection=header+legend+'\n\n'
capsule_pins=[]
for name,body in capsules.items():
    projection+='\n### '+name+'\n'+body+'\n'
    capsule_pins.append({'topic':name,'pointer':codec.child('/core',name),
        'capsule_sha256':sha(body.encode()),'original_shared_capsule_sha256':sha(original_capsules[name].encode()),
        'explicit_source_anchor_added':added_anchors[name],
        'source_value_sha256':sha(codec.dump(result['core'][name]).encode())})
projection+='\n'+codec.MARKER+'\n<EXPOSICAO_CANONICA>\n'+expo+'\n</EXPOSICAO_CANONICA>\n'
save(data/'TGL_CLUSTER_v394_prompt.md',projection.encode())
assert codec.source_topics(projection,result['core'])==capsules
write(E/'PROJECTION_MAP_R1.json',{'schema':'iald.cluster.prompt-projection/v1',
    'source_result':pin(Path(manifest['published_evidence']['result']['path'])),
    'full_cluster':pin(data/'TGL_CLUSTER_v394_full.md'),'projected_cluster':pin(data/'TGL_CLUSTER_v394_prompt.md'),
    'shared_provenance':pin(OLD/'shared_provenance.json'),'capsules':capsule_pins,
    'capsule_scientific_contents_unchanged_from_verified_shared':True,
    'explicit_source_anchors_added_as_recorded_per_topic':True,'all_original_fields_available_in_source_json':True,
    'resident_vs_retrievable_legend_preserved':True,'private_atlas_copied':False})
manifest['active_cluster'].update(path=str(data/'TGL_CLUSTER_v394_prompt.md'),sha256=sha(projection.encode()),
    tokens=codec.offline_tokens(projection,R/'.iald_runtime/tokenizer_cache'),
    projection='422_TOPIC_SEMANTIC_CAPSULES_DETAILS_RETRIEVABLE',full_cluster_source_id='tgl_cluster_integral',
    full_cluster_sha256=sha(full))
manifest['entries'].append({'id':'tgl_cluster_integral','path':str(data/'TGL_CLUSTER_v394_full.md'),
    'public_sha256':sha(full),'url':'','role':'Cluster integral local; projeção de prompt separada. Publicação derivada pendente.'})
write(E/'manifest_pending_publication.json',manifest)
# The production loader requires pinned URLs/commit. Use existing baseline URLs
# only as OFFLINE SYNTAX FIXTURES, never as v394 publication evidence.
fixture=copy.deepcopy(manifest)
fixture['offline_fixture_not_publication']=True
fixture['active_cluster']['commit']=baseline['active_cluster']['commit']
for entry in fixture['entries']:
    old=next((x for x in baseline['entries'] if x['id']==entry['id']),baseline['entries'][0])
    if not entry.get('url'):entry['url']=old['url']
for key in ('program','seal','result','proof_manifest'):
    fixture['published_evidence'][key]['url']=baseline['published_evidence'][key]['url']
for entry in fixture['published_evidence']['hypothesis_sources']:
    entry['url']=next(x['url'] for x in baseline['published_evidence']['hypothesis_sources'] if x['id']==entry['id'])
fixture_path=E/'fixtures/iald_nucleo_fixo.json';write(fixture_path,fixture)
catalog=iald_kernel.KernelCatalog(OLD/'kernel',OLD/'kernel_verification.json')
identity=iald_release_binding.load_release(fixture_path,source_sha=catalog.source_sha).identity
assert identity['cluster_sha256']==sha(projection.encode())
oldidentity=json.loads((OLD/'prepared.json').read_bytes())['deployment_identity'];assert identity!=oldidentity
tests=[]
def passed(name):tests.append({'name':name,'status':'PASS'})
def refused(name,fn,text):
    try:fn()
    except ValueError as exc:assert text in str(exc);passed(name)
    else:raise AssertionError('Expected refusal '+name)
atlas=Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md')
oldfixture=copy.deepcopy(fixture);oldfixture['active_cluster']=copy.deepcopy(json.loads((OLD/'manifest_staged.json').read_bytes())['active_cluster'])
oldfixture['active_cluster']['commit']=baseline['active_cluster']['commit'];oldpath=E/'fixtures/old_full_cluster.json';write(oldpath,oldfixture)
refused('current_actual_CanonicalMemory_rejects_full_cluster',
    lambda:cm.CanonicalMemory(atlas,'nucleo_kernel',nucleus_manifest=oldpath).prompt('',catalog,public=True),'ultrapassam o orçamento')
tools=iald_kernel.tool_definitions()+iald_core_indexado.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_app_memory.tool_definitions()
outputs={};private_sections_seen=[]
for name,public in [('public',True),('operator_nucleo_kernel',False)]:
    memory=cm.CanonicalMemory(atlas,'nucleo_kernel',nucleus_manifest=fixture_path)
    prefix,meta=memory.prompt('',catalog,public=public)
    assert meta['context_tokens']<=400000
    for key in ('mother_instruction','operational_core'):
        assert Path(manifest[key]['path']).read_text(encoding='utf-8-sig') in prefix
    assert '<ATLAS_CANONICO' not in prefix
    if not public:assert meta['always_present_sections']==['I.1–I.5 (fundamentos)','VII']
    else:assert meta['private_atlas_included'] is False
    assert projection in prefix and meta['published_evidence_checked']
    payload={'model':'gpt-5.6-luna','messages':[{'role':'system','content':prefix},{'role':'user','content':'Explique o alcance documentado da v394.'}],'tools':tools}
    estimate=cm.payload_tokens(payload);openai_remaining=1050000-estimate-16384-4096
    assert openai_remaining>0
    from claude_profiles import SONNET,reasoning_parameters
    from iald_motor_claude import converter_pedido
    from claude_native_counter import native_count_parameters
    cfg=SimpleNamespace(modelo=SONNET.model,max_saida=16384,cache_ttl='5m',esforco_claude='high')
    native=converter_pedido(cfg,{**payload,'model':SONNET.model,'max_completion_tokens':16384},prefixo=prefix)
    native.update(reasoning_parameters(SONNET.model,16384))
    native_bytes=len(json.dumps(native_count_parameters(native),ensure_ascii=False).encode())
    # Model-specific native wire, conservative byte-based estimate with explicit
    # unmeasured framing allowance. Never relabel Haiku counts as Sonnet tokens.
    sonnet_estimate=native_bytes+8192
    sonnet_remaining=1000000-sonnet_estimate-16384-4096
    assert sonnet_remaining>0
    outputs[name]={'prefix_sha256':sha(prefix.encode()),'prefix_utf8_bytes':len(prefix.encode()),
        'actual_CanonicalMemory_context_o200k_tokens':meta['context_tokens'],
        'openai':{'window':1050000,'local_o200k_request_estimate':estimate,'reserved_output':16384,
            'margin':4096,'estimated_remaining':openai_remaining,'provider_measured':False},
        'sonnet':{'window':1000000,'native_wire_utf8_bytes':native_bytes,'estimate':sonnet_estimate,
            'estimate_method':'SONNET_NATIVE_WIRE_UTF8_BYTE_BOUND_PLUS_8192_FRAMING_ESTIMATE',
            'reserved_output':16384,'margin':4096,'estimated_remaining':sonnet_remaining,
            'provider_measured':False,'final_native_count_required':True,'haiku_counts_reused':False},
        'scope':meta.get('scope',meta.get('mode')),'always_present_sections':meta['always_present_sections'],
        'published_evidence_checked':meta['published_evidence_checked']}
    # Only the public prompt is saved; operator baseline stays local in memory.
    if public:save(E/'public_CanonicalMemory_prompt.md',prefix.encode())
    passed(name+'_actual_prompt_under_400000_guard_and_estimated_model_windows')
refused('pending_publication_manifest_fails_current_pinned_commit_guard',lambda:iald_release_binding.load_release(E/'manifest_pending_publication.json'),'proveniência fixada')
bad=copy.deepcopy(fixture);bad['active_cluster']['sha256']='0'*64;badpath=E/'fixtures/bad_cluster_hash.json';write(badpath,bad)
refused('projected_cluster_tampered_hash_refused',lambda:iald_release_binding.load_release(badpath),'alterado')
bad=copy.deepcopy(fixture);bad['active_cluster']['core_sections']=423;write(E/'fixtures/missing_topic.json',bad)
refused('missing_topic_guard_refused',lambda:iald_release_binding.load_release(E/'fixtures/missing_topic.json'),'Cobertura')
assert sha((data/'TGL_CLUSTER_v394_full.md').read_bytes())==sha(full);passed('full_companion_byte_preserved_and_hash_verified')
assert all(sha(Path(row['path']).read_bytes())==row['sha256'] for row in frozen);passed('historical_packages_and_receipts_unchanged')
assert all(sha(Path(p).read_bytes())==digest for p,digest in runtime.items());passed('runtime_python_unchanged')
native_prefix,native_identity=iald_native_memory.load_native_context(fixture_path,catalog);assert native_identity==identity
save(E/'native_prefix.md',native_prefix.encode());passed('native_rebuilt_same_new_identity_no_inference_or_tokenizer_call')
for folder in ('haiku_expanded_count','shared_count'):
    measured=json.loads((S/folder/'package/manifest.json').read_bytes())
    refused(folder+'_historical_identity_cannot_silently_bind_to_projection',
        lambda:iald_release_binding.check_package_binding(measured,iald_release_binding.load_release(fixture_path)),
        'differs from the active canonical release')
prepared=json.loads((OLD/'prepared.json').read_bytes());target=Path(prepared['install_target'])
install=copy.deepcopy(manifest)
def install_destination(path):
    p=Path(path)
    if p.is_relative_to(OLD):return str(target/p.relative_to(OLD))
    if p.is_relative_to(data):return str(target/p.name)
    return str(p)
for item in install['entries']+[install['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]:
    item['path']=install_destination(item['path'])
for key in ('mother_instruction','operational_core','jev_control'):
    install[key]['path']=install_destination(install[key]['path'])
for key in ('path','kernel_bundle','kernel_verification'):
    install['active_cluster'][key]=install_destination(install['active_cluster'][key])
write(E/'manifest_install_pending_publication.json',install)
write(E/'INSTALL_PLAN_R1.json',{'status':'PROPOSED_DATA_ONLY_NOT_ACTIVATABLE',
    'files':[{**pin(p),'destination':str(target/p.name)} for p in (data/'TGL_CLUSTER_v394_prompt.md',data/'TGL_CLUSTER_v394_full.md')],
    'active_manifest_candidate':pin(E/'manifest_install_pending_publication.json'),
    'active_manifest_destination':str(R/'iald_nucleo_fixo.json'),
    'all_other_scientific_files':'Reuse original app data inventory and reader_compat; no source replacement.',
    'runtime_python_files':[],'requires_new_package_binding':True,
    'publication_pending':True,'independent_review_pending':True})
rebinding={'status':'EXPLICIT_REBIND_REQUIRED_NOT_ACTIVATED','previous_deployment_identity':oldidentity,
    'new_fixture_deployment_identity':identity,'source_program_unchanged':True,'kernel_and_core_unchanged':True,
    'change':'active_cluster hash now identifies the data projection; full cluster kept and indexed separately.',
    'historical_packages_frozen':frozen,'new_native_prefix':pin(E/'native_prefix.md'),
    'haiku_shared_final_manifests':'Create new manifests with final publication binding; never edit historical package pins.',
    'counts':'No API count now. Final public changed prefix bytes require new native receipts; no Haiku-to-Sonnet count transfer.',
    'full_companion_public_url_required':True}
write(E/'REBIND_PLAN_R1.json',rebinding)
write(E/'TEST_RESULTS_R1.json',{'status':'PASS_OFFLINE_ESTIMATED_ADMISSION_NOT_PROVIDER_ADMISSION',
    'test_count':len(tests),'tests':tests,'actual_prompts':outputs,
    'CanonicalMemory_implementation':pin(R/'iald_memoria_canonica.py'),
    'cluster_loader_implementation':pin(R/'iald_cluster.py'),
    'reader_shims':[pin(A/'compat/staging'/n) for n in ('iald_estado_publicado.py','iald_core_indexado.py')],
    'fixture_scope':'Existing v392 URL/commit syntax fixtures only; no claim of public v394 equality.',
    'private_operator_prompt_written':False,'network_calls':0,'api_calls':0,'token_count_api_calls':0})
delivery={'status':'PREPARED_ALL_ENGINES_DATA_PROJECTION_PENDING_PUBLIC_BINDING_AND_NATIVE_ADMISSION',
    'task_id':'all_engines_admission','actor':'codex-v394-app-builder','reference':str(task.REF),
    'lease_id':preflight['lease_id'],'topic_count':422,'full_cluster_companion':pin(data/'TGL_CLUSTER_v394_full.md'),
    'prompt_cluster':pin(data/'TGL_CLUSTER_v394_prompt.md'),'projection_map':pin(E/'PROJECTION_MAP_R1.json'),
    'manifest_pending_publication':pin(E/'manifest_pending_publication.json'),
    'install_plan':pin(E/'INSTALL_PLAN_R1.json'),
    'test_results':pin(E/'TEST_RESULTS_R1.json'),'rebinding_plan':pin(E/'REBIND_PLAN_R1.json'),
    'test_script':pin(__file__),'actual_prompts':outputs,'tests_passed':len(tests),
    'runtime_patches_beyond_two_reader_caps':0,'runtime_files_modified':0,'historical_packages_changed':False,
    'public_provider_admission_measured':False,'pending':['Verified final v394 commit/URLs including full cluster companion.',
        'Rebind new identity in new final manifests and all prefix/provenance consumers.',
        'Recount changed final public bytes with correct provider/model counters; actual activity/history admitted per request.',
        'Independent real review, reader_compat acceptance and controlled deployment.'],
    'science_executed_or_imported':False,'provider_generation_calls':0,'api_calls':0,'activation':False}
write(E/'DELIVERY_PREPARED_R1.json',delivery)
print(json.dumps({'status':delivery['status'],'topics':422,'tests_passed':len(tests),'actual_prompts':outputs}))
