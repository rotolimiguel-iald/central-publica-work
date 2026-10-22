"""Offline final package validation and exact installation proposal; never deploys."""
from pathlib import Path
from types import SimpleNamespace
import ast,copy,json,os,sys
F=Path(__file__).resolve().parent;A=F.parent;W=A.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True;sys.path.insert(0,str(W));import task
preflight=task.check('app',actor='codex-v394-app-builder');assert preflight['ready']
sys.path[:0]=[str(F/'build'),str(R),str(A)]
from prepare_science import save,write,sha
def pin(path):
    p=Path(path);raw=p.read_bytes();return {'path':str(p),'sha256':sha(raw),'bytes':len(raw)}
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):raise RuntimeError('Offline validation only')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,int):return
        p=Path(os.fsdecode(path)).resolve()
        if p.name.lower() in ('.env','iald_stack_v7.py','iald_psion_state.json'):raise RuntimeError('Private source refused')
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not p.is_relative_to(F):raise RuntimeError('Write outside final')
sys.addaudithook(guard)
import haiku_codec as c,iald_kernel,iald_release_binding,iald_jev_control,iald_app_providers
import iald_core_indexado,iald_fontes_publicas,iald_app_memory
from claude_memory_package import load_package
from claude_context_snapshot import load_snapshot,verify_native_tools
from claude_profiles import HAIKU
from iald_motor_claude import converter_pedido
binding=json.loads((F/'PREPARED_BINDING.json').read_bytes());stage=F/'science/memory_stage';manifest=stage/'manifest_staged.json'
m=json.loads(manifest.read_bytes());release=iald_release_binding.load_release(manifest)
assert release.identity==binding['deployment'];tests=[]
def passed(name):tests.append({'name':name,'status':'PASS'})
catalog=iald_kernel.KernelCatalog(stage/'kernel',stage/'kernel_verification.json')
proof=json.loads(Path(m['published_evidence']['proof_manifest']['path']).read_bytes())
assert len(proof['formal_files_sha256'])==1423
for name,digest in proof['formal_files_sha256'].items():assert sha((stage/'kernel'/name).read_bytes())==digest
passed('all_1423_kernel_files_equal_sealed_formal_report')
assert iald_jev_control.load_contract(stage)['source_sha256']==release.identity['source_sha256'];passed('JEV_contract_new_release_source_binding')
for key in ('mother_instruction','operational_core'):
    assert Path(m[key]['path']).read_bytes()==Path(json.loads((R/'iald_nucleo_fixo.json').read_bytes())[key]['path']).read_bytes() if key=='mother_instruction' else Path(m[key]['path']).read_bytes()==(A/'science/memory_stage'/Path(m[key]['path']).name).read_bytes()
passed('v5_and_approved_core_bytes_preserved')
tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
for folder in ('haiku55','shared'):
    root=F/'packages'/folder
    package=load_package(root,canonical_manifest=manifest,source_sha=catalog.source_sha,expected_model=HAIKU.model)
    assert package.measurement.prefix_sha256==sha((root/'prefix.md').read_bytes())
    passed(folder+'_actual_current_package_loader_accepts_final_binding_and_budget')
    if folder=='haiku55':
        _,snapshot=load_snapshot(root,lambda path:load_package(path,canonical_manifest=manifest,source_sha=catalog.source_sha))
        cfg=SimpleNamespace(modelo=HAIKU.model,max_saida=16384,cache_ttl='5m',esforco_claude='medium')
        wire=converter_pedido(cfg,{'model':HAIKU.model,'max_completion_tokens':16384,
            'messages':[{'role':'system','content':package.prefix},{'role':'user','content':'.'}],
            'tools':tools},prefixo=package.prefix)
        verify_native_tools(wire,snapshot,trusted_tools=wire['tools']);passed('haiku_actual_snapshot_and_ACOM_tool_integrity_pass')
result_raw=Path(m['published_evidence']['result']['path']).read_bytes();result=json.loads(result_raw)
expanded=(F/'packages/haiku55/prefix.md').read_text(encoding='utf-8')
dictionary=json.loads(expanded.split('LITERAIS_COMPARTILHADOS\n',1)[1].split('\n',1)[0])
exposition=expanded.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
blocks=c.source_topics(expanded,result['core'])
def recover(value,topic,pointer):
    if isinstance(value,dict):
        if '@' in value:return c.restore(value,result,topic,pointer,{})
        if 'DETAILS_IN_SOURCE' in value:return c.resolve(result,value['DETAILS_IN_SOURCE'])
        return {k:recover(v,topic,c.child(pointer,k)) for k,v in value.items()}
    if isinstance(value,list):return [recover(v,topic,c.child(pointer,i)) for i,v in enumerate(value)]
    return value
for name,body in blocks.items():
    decoded=c.decode_literals(c.unpack_metadata(json.loads(body.splitlines()[1])),dictionary,exposition)
    pointer=c.child('/core',name);assert recover(decoded,pointer,pointer)==result['core'][name]
assert len(blocks)==422;passed('expanded_422_topic_original_subtrees_reconstructed_exactly')
corpus=iald_core_indexado.DocumentCorpus(manifest);docs=corpus._load()
assert len(docs)==8 and 'tgl_cluster_integral' not in docs
assert json.loads(docs['resultado_publicado_integral']['text'])==result;passed('only_8_authentic_sources_all_result_fields_retrievable')
pub=json.loads((F/'PUBLICATION_VERIFIED.json').read_bytes())
for row in m['entries']:
    matched=[r for r in pub['sources'].values() if r['url']==row['url']]
    assert len(matched)==1 and matched[0]['sha256']==row['public_sha256']
    assert row['url'].split('/')[5]==binding['commit']
assert m['active_cluster']['commit']==binding['commit'] and not m.get('staging_only')
passed('all_document_URLs_and_hashes_from_verified_real_public_commit')
assert (stage/'TGL_CLUSTER_v394_full.md').read_bytes()==(A/'engines/R2/data/TGL_CLUSTER_v394_full.md').read_bytes()
passed('full_cluster_local_companion_preserved_without_publication_dependency')
shared=(F/'packages/shared/prefix.md').read_text(encoding='utf-8');bounds={}
messages=[{'role':'system','content':shared},{'role':'user','content':'Explique o alcance documentado da v394.'}]
for provider in ('kimi','mimo','deepseek'):
    body={'messages':messages,'tools':[] if provider=='kimi' else tools}
    if provider!='kimi':body.update(model=iald_app_providers.MODELS[provider]['model'],stream=True,stream_options={'include_usage':True},thinking={'type':'enabled'})
    if provider=='deepseek':body['reasoning_effort']='max'
    reserve=iald_app_providers.MODELS[provider]['output'] if provider=='kimi' else iald_app_providers.output_budget(body,iald_app_providers.MODELS[provider]['output'])
    if provider!='kimi':body['max_tokens' if provider=='deepseek' else 'max_completion_tokens']=reserve
    used=iald_app_providers.check_window(body,reserve)
    bounds[provider]={'input_utf8_bytes_bound':used,'output_reserve_tokens':reserve,
        'remaining_bytes_bound':1048576-used-reserve-4096,'actual_conversation_and_activity_admission_required':True}
passed('Kimi_MiMo_DeepSeek_actual_serialized_byte_guards_accept_final_shared_synthetic_envelope')
counts={}
for folder in ('haiku55','shared','sonnet_public'):
    root=F/'packages'/folder;rc=json.loads((root/'native_count.json').read_bytes())
    assert rc['prefix_sha256']==sha((root/'prefix.md').read_bytes()) and rc['deployment']==release.identity
    assert rc['budget']['ready'] and rc['budget']['remaining_tokens']>=10000 and rc['private_atlas_included'] is False
    counts[folder]={'receipt':pin(root/'native_count.json'),'prefix':pin(root/'prefix.md'),'budget':rc['budget']}
assert counts['sonnet_public']['budget']['model']!=counts['haiku55']['budget']['model'];passed('model_specific_native_counts_final_bytes_not_transferred_between_models')
# Historical manifests must be rejected against the new projected identity.
for directory in (A/'science/haiku_expanded_count/package',A/'science/shared_count/package'):
    try:load_package(directory,canonical_manifest=manifest)
    except ValueError:pass
    else:raise AssertionError('Old package silently rebound')
passed('historical_packages_cannot_silently_rebind_to_final_identity')
target=Path(binding['target']);rows=[]
def plan_file(source,dest,purpose):
    source=Path(source);dest=Path(dest)
    assert dest.is_relative_to(R)
    baseline=pin(dest) if dest.is_file() else {'path':str(dest),'exists':False}
    rows.append({**pin(source),'destination':str(dest),'baseline':baseline,'purpose':purpose})
for root in (stage/'release',stage/'kernel'):
    for source in sorted(root.rglob('*')):
        if source.is_file():plan_file(source,target/source.relative_to(stage),'SCIENTIFIC_SOURCE_DATA_NEVER_EXECUTE' if source.name=='um.py' else 'SCIENTIFIC_DOCUMENT_OR_FORMAL_SOURCE_DATA')
for name in ('IALD_Kernel_v5.txt','IALD_TGL_MEMORY_CORE.md','TGL_CLUSTER_v394_prompt.md','TGL_CLUSTER_v394_full.md','kernel_verification.json','jev_control_v394.json'):
    plan_file(stage/name,target/name,'CANONICAL_DATA')
for folder,destname in [('haiku55','haiku55'),('shared','haiku')]:
    root=F/'packages'/folder;dest=R/'.iald_runtime'/destname
    pkg=json.loads((root/'manifest.json').read_bytes());pkg['measurement_receipt']=str(dest/'native_count.json')
    write(root/'manifest_install.json',pkg)
    for source,name in [(root/'prefix.md','prefix.md'),(root/'manifest_install.json','manifest.json'),(root/'native_count.json','native_count.json')]:plan_file(source,dest/name,'NATIVE_MEASURED_MEMORY_PACKAGE_DATA')
plan_file(stage/'manifest_install.json',R/'iald_nucleo_fixo.json','ACTIVE_MANIFEST_CANDIDATE_INSTALL_ONLY_AFTER_REVIEW_AND_QUIESCENCE')
compat=json.loads((A/'compat/INSTALL_PLAN_R1.json').read_bytes())
for row in compat['files']:
    assert sha(Path(row['runtime_path']).read_bytes())==row['baseline_sha256']
    plan_file(F/'build'/Path(row['runtime_path']).name,Path(row['runtime_path']),'ONLY_APPROVED_READER_LIMIT_10MB_TO_32MB')
runtime_python=[row for row in rows if Path(row['destination']).parent==R and Path(row['destination']).suffix=='.py']
assert {Path(row['destination']).name for row in runtime_python}=={'iald_estado_publicado.py','iald_core_indexado.py'}
write(F/'INSTALL_PLAN_FINAL.json',{'status':'PREPARED_NOT_INSTALLED_DISTINCT_REVIEW_REQUIRED','files':rows,
    'file_count':len(rows),'kernel_source_count':1423,'runtime_python_changes':2,
    'runtime_python_scope':'Exactly two reader caps from currently installed baseline. No web/router/ACOM/HajaLuz replacement.',
    'runtime_package_destinations':{'expanded_haiku':str(R/'.iald_runtime/haiku55'),'shared_connectors':str(R/'.iald_runtime/haiku')},
    'sonnet_measurement_is_evidence_only':'Sonnet continues through CanonicalMemory.prompt; its public counter is not installed as a Haiku package.',
    'deployment_identity':release.identity,'required_install_order':['Distinct review and accepted preparation gates verified by main.',
        'Fresh exact-baseline/CAS and idle/maintenance admission controlled by main; backup bytes before replacing existing targets.',
        'Install immutable canonical data and measured packages plus two reviewed readers; activate canonical manifest last.',
        'Main verifies new process imports, exact loaded identity, per-request activity/history admission and rollback before claiming deployed.'],
    'production_actions_performed':0,'queue_or_gate_actions_performed':0})
for file in F.rglob('*.py'):ast.parse(file.read_bytes())
passed('all_final_helpers_parse_and_plan_has_only_two_authorized_runtime_readers')
historical=json.loads((F/'HISTORICAL_PINS.json').read_bytes())['files'];runtime=json.loads((F/'RUNTIME_BASELINE.json').read_bytes())['files']
assert all(sha(Path(row['path']).read_bytes())==row['sha256'] for row in historical+runtime)
assert sha((F/'PUBLICATION_VERIFIED.json').read_bytes())==json.loads((F/'NATIVE_COUNTS_COMPLETE.json').read_bytes())['publication_receipt_sha256']
passed('all_historical_pins_runtime_and_ACOM_checkpoint_publication_receipt_preserved')
write(F/'FINAL_TEST_RESULTS.json',{'status':'PASS_OFFLINE_FINAL_PREPARATION','tests':tests,'test_count':len(tests),
    'native_counts':counts,'shared_connector_bounds':bounds,'deployment_identity':release.identity,
    'operator_admission':'Local only; no operator prompt written or sent remotely.',
    'network_calls':0,'production_changes':0,'science_executed_or_imported':False})
delivery={'schema':'iald.app.final-public-candidate/v1','status':'FINAL_PUBLIC_PREPARED_DISTINCT_REVIEW_REQUIRED_NOT_DEPLOYED',
    'reference':str(task.REF),'task_id':'app','actor':'codex-v394-app-builder','lease_id':preflight['lease_id'],
    'commit':binding['commit'],'deployment_identity':release.identity,'publication':pin(F/'PUBLICATION_VERIFIED.json'),
    'prepared_binding':pin(F/'PREPARED_BINDING.json'),'install_plan':pin(F/'INSTALL_PLAN_FINAL.json'),
    'tests':pin(F/'FINAL_TEST_RESULTS.json'),'native_counts_complete':pin(F/'NATIVE_COUNTS_COMPLETE.json'),
    'historical_pins':pin(F/'HISTORICAL_PINS.json'),'runtime_baseline':pin(F/'RUNTIME_BASELINE.json'),
    'counts':counts,'public_and_operator_local_admission':binding['actual_prompts'],'shared_connector_bounds':bounds,
    'core_topics':422,'formal_sources':1423,'reported_flags':9332,'reported_declarations':29026,'counts_are_distinct':True,
    'full_cluster_local_only_no_extra_publication':True,'only_original_8_public_corpus_entries':True,
    'two_reader_caps_only':True,'ACOM_HajaLuz_16_17Oct_preserved':True,
    'notes':['The approved operational core and local full cluster retain historical staging wording; the final manifest, measured prefix headers and explicit public binding identify the actual commit. No historical text was silently overwritten.',
        'Native counts cover exact public final prefixes plus synthetic tool envelopes. Real history, activity projections and tool results require per-request admission.',
        'Sonnet public count is model-specific; operator context remains offline-estimated and never egressed.'],
    'remaining':['Distinct real review and acceptance of this final candidate.',
        'Main controls deployment gate, exact-baseline/CAS, backups, maintenance, activation and live regression; this agent did none.',
        'Physical client availability and actual runtime v394 loading are not asserted.'],
    'test_count':len(tests),'provider_count_requests':6,'provider_generation_calls':0,
    'runtime_files_modified':0,'installed_files':0,'queue_actions':0,'gate_changes':0,'semantic_acceptance':False}
write(F/'DELIVERY_PREPARED_FINAL.json',delivery)
print(json.dumps({'status':delivery['status'],'tests_passed':len(tests),'planned_files':len(rows),'runtime_python_candidates':2,'historical_pins_verified':len(historical)}))
