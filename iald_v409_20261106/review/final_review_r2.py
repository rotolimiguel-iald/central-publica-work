"""Independent offline review of submitted plan and existing native counts."""
from pathlib import Path
from types import SimpleNamespace
import ast,hashlib,json,os,re,sys
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent.parent;A=W/'app';ST=A/'science/memory_stage'
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(W),str(A/'build'),str(R)]
os.environ['TIKTOKEN_CACHE_DIR']=str(R/'.iald_runtime/tokenizer_cache')
read=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
pin=lambda p:{'path':str(p),'sha256':sha(Path(p).read_bytes())}
def checkpin(e):assert sha(Path(e['path']).read_bytes())==e['sha256'],e['path']
attempts=[]
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','socket.sendto','subprocess.Popen','os.system','os.startfile'):
        attempts.append(event);raise RuntimeError('Offline review blocked external IO')
    if event=='exec' and Path(args[0].co_filename).name.casefold()=='um.py':raise RuntimeError('Scientific execution forbidden')
    if event=='open' and not isinstance(args[0],int):
        p=Path(os.fsdecode(args[0])).resolve();mode=args[1];flags=args[2]
        if p.name.casefold() in ('.env','iald_stack_v7.py','iald_psion_state.json'):raise RuntimeError('Secret read forbidden')
        writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not (p.is_relative_to(W/'review') or (p.parent==W/'validation' and p.name.startswith('review'))):raise RuntimeError('Review write outside scope')
sys.addaudithook(guard)
h=read(A/'BUILDER_HANDOFF_R2.json')
assert h['status']=='PREPARED_R2_READY_FOR_DISTINCT_REVIEW_NOT_INSTALLED'
for e in h['evidence']+[h[k] for k in ('plan','data_plan','checks','measurements','pruning_review')]:checkpin(e)
controls=read(W/'review/CONTROLS_R1.json')
for name,expected in controls['pins'].items():assert sha((W/name).read_bytes())==expected,name
for baseline in (W/'PRESERVATION_BASELINE.json',A/'RUNTIME_BASELINE.json'):
    for row in read(baseline)['files']:checkpin(row)
ast.parse((W/'refresh_tower.py').read_bytes())

import transaction
plan=read(W/'install_plan.json');rows=plan['files'];transaction.check_science_destinations(rows)
assert len(rows)==1788 and len({r['destination'] for r in rows})==1788
bydest={r['destination']:r for r in rows}
for row in rows:
    src=Path(row['source']);dest=Path(row['destination'])
    assert src.resolve()==src and src.is_relative_to(A)
    assert '.bak' not in src.name
    assert sha(src.read_bytes())==row['sha256']
    assert (sha(dest.read_bytes()) if dest.exists() else None)==row['baseline']
    assert not (dest.parent==R and dest.suffix=='.py')
checks=read(W/'validation/final_checks.json')
assert checks['passed'] and checks['plan_sha256']==sha((W/'install_plan.json').read_bytes())
binding=read(A/'PREPARED_BINDING.json');m=read(ST/'manifest_staged.json');installed=read(ST/'manifest_install.json');old=read(R/'iald_nucleo_fixo.json')
assert plan['deployment_identity']==binding['deployment']
def verify_paths(obj):
    if isinstance(obj,list):
        for x in obj:verify_paths(x)
    if isinstance(obj,dict):
        if 'path' in obj and str(obj['path']).startswith(str(R)):
            row=bydest[str(obj['path'])]
            for field in ('sha256','public_sha256'):
                if field in obj:assert obj[field]==row['sha256']
        for x in obj.values():verify_paths(x)
verify_paths(installed)
assert Path(m['mother_instruction']['path']).read_bytes()==Path(old['mother_instruction']['path']).read_bytes()
assert Path(m['operational_core']['path']).read_bytes().startswith(Path(old['operational_core']['path']).read_bytes())
oldc=read(old['jev_control']['path']);newc=read(m['jev_control']['path'])
for key in ('schema','stopping_criterion','memory_admission','decision_metric','holographic_state','switching'):assert oldc[key]==newc[key]
assert newc['release']=='v409'
proof=read(m['published_evidence']['proof_manifest']['path'])
for name,p in proof['formal_files_sha256'].items():assert sha((ST/'kernel'/name).read_bytes())==p

# Reuse the independent decoder definition, without running the old review.
tree=ast.parse((W/'review/sources_p2_r1.py').read_text(encoding='utf-8'))
decoder=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='decode')
scope={'aliases':{'@F':'@SOURCE_FIELDS','@I':'@SOURCE_ITEMS','@L':'@TGL_LITERAL','@Y':'@SUMMARY','@X':'@EXPOSITION'}}
exec(compile(ast.Module(body=[decoder],type_ignores=[]),'<independent_decoder>','exec'),scope)
document=Path(m['published_evidence']['result']['path']).read_bytes().decode();result=json.loads(document);core=result['core']
history=read(A/'D53_HISTORY.json');assert sha(document.encode())==history['source_text_sha256']
resident={n for n in core if n.endswith(('_v408','_v409'))}|{'the_iald_index'}
assert resident==set(history['resident'])
high=read(A/'KERNEL_HIGHLIGHTS.json')
prior=read(W/'review/P2_R1.json')
checkpin(next(e for e in prior['evidence'] if e['path'].endswith('KERNEL_HIGHLIGHTS.json')))
for folder in ('shared','sonnet_public'):
    raw=(A/'packages'/folder/'prefix.md').read_bytes();text=raw.decode()
    receipt=read(A/('D53_'+folder+'_VERIFIED.json'));assert receipt['prefix_sha256']==sha(raw)
    scope['literals']=json.loads(text.split('DICIONÁRIO DE LITERAIS\n',1)[1].split('\n',1)[0])
    scope['flags']=json.loads(text.split('DICIONÁRIO DE INDICADORES LITERAIS\n',1)[1].split('\n',1)[0])
    scope['exposition']=text.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    head=text.split('## Exposição canônica integral: fórmulas e derivações',1)[0]
    headings=[x for x in re.finditer(r'(?m)^### ([^\n]+)\n',head) if x[1] in core]
    assert len(headings)==len(core)==483
    for i,match in enumerate(headings):
        name=match[1]
        if name not in resident and name not in history['spans']:continue
        block=head[match.end():headings[i+1].start() if i+1<len(headings) else len(head)]
        v=scope['decode'](json.loads(next(line for line in block.splitlines() if line.startswith('{'))))
        if name in resident:assert v==core[name],name
        else:
            start,size=v.pop('@H');assert [start,size]==history['spans'][name]
            actual=json.loads(document[start:start+size]);assert actual==core[name]
            assert all(actual[k]==x for k,x in v.items())
    assert high['scope'] in text and all(a['statement'] in text for a in high['anchors'])
    assert '<ATLAS_CANONICO' not in text
assert sha((A/'packages/shared/prefix.md').read_bytes())==read(W/'capacity_experiments/PRUNING_REPORT.json')['candidate_sha256']

import haiku_codec as codec
full=(ST/'TGL_CLUSTER_v409_full.md').read_text(encoding='utf8')
dictionary=json.loads(full.split('DICIONÁRIO DO CLUSTER\n',1)[1].split('\n',1)[0]);expo=full.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
blocks=codec.source_topics(full,core);assert len(blocks)==483
for name,body in blocks.items():
    ptr=codec.child('/core',name)
    value=codec.decode_literals(codec.unpack_metadata(json.loads(body.splitlines()[1])),dictionary,expo)
    assert codec.restore(value,result,ptr,ptr,{})==core[name]

# Reconstruct all six fingerprints locally. Never call the count endpoint.
from claude_profiles import HAIKU,SONNET,reasoning_parameters,context_budget
from claude_native_counter import native_count_parameters
from iald_motor_claude import converter_pedido
import iald_kernel,iald_fontes_publicas,iald_core_indexado,iald_app_memory
from claude_memory_package import load_package
from claude_context_snapshot import load_snapshot,verify_native_tools
tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
preflight=read(A/'COUNT_PREFLIGHT.json');assert preflight['endpoint']=='https://api.anthropic.com/v1/messages/count_tokens'
countrows=[]
for folder,profile in (('haiku_expanded',HAIKU),('shared',HAIKU),('sonnet_public',SONNET)):
    root=A/'packages'/folder;raw=(root/'prefix.md').read_bytes();prefix=raw.decode();receipt=read(root/'native_count.json')
    assert receipt['prefix_sha256']==sha(raw) and receipt['deployment']==binding['deployment']
    assert receipt['model']==profile.model and receipt['public_commit']==binding['commit']
    assert receipt['private_atlas_included'] is False and receipt['operator_context_sent'] is False
    assert sha(raw)!=binding['actual_prompts']['operator_local']['prefix_sha256'] and '<ATLAS_CANONICO' not in prefix
    cfg=SimpleNamespace(modelo=profile.model,max_saida=16384,cache_ttl='5m',esforco_claude='medium' if profile is HAIKU else 'high')
    wire=converter_pedido(cfg,{'model':profile.model,'max_completion_tokens':16384,'messages':[{'role':'system','content':prefix},{'role':'user','content':'Explique o alcance documentado da v409.'}],'tools':tools},prefixo=prefix)
    wire.update(reasoning_parameters(profile.model,16384))
    minimal={'model':profile.model,'system':wire['system'],'messages':[{'role':'user','content':'.'}],**reasoning_parameters(profile.model,16384)}
    values={}
    for phase,request in (('permanent',minimal),('whole_request',wire)):
        fingerprint=sha(json.dumps(native_count_parameters(request),sort_keys=True,ensure_ascii=False).encode())
        row={'package':folder,'phase':phase,'model':profile.model,'prefix_sha256':sha(raw),'request_sha256':fingerprint}
        assert row==preflight['requests'][len(countrows)];countrows.append(row)
        intent=read(root/(phase+'_count_intent.json'));returned=read(root/(phase+'_count_result.json'))
        assert intent['request_sha256']==fingerprint and intent['prefix_sha256']==sha(raw) and intent['generation'] is False and intent['max_retries']==0
        assert returned['intent_sha256']==sha((root/(phase+'_count_intent.json')).read_bytes())
        assert returned['status']=='COUNT_RETURNED' and type(returned['input_tokens']) is int
        values[phase]=returned['input_tokens']
    assert receipt['budget']==context_budget(profile.model,counted_model=profile.model,permanent_tokens=values['permanent'],request_input_tokens=values['whole_request'],reserved_output_tokens=16384)
    assert receipt['budget']['ready'] and receipt['budget']['remaining_tokens']>=10000
    assert receipt['native_tools_sha256']==sha(json.dumps(wire['tools'],sort_keys=True,ensure_ascii=False).encode())
    if folder!='sonnet_public':
        package=load_package(root,canonical_manifest=ST/'manifest_staged.json',source_sha=binding['deployment']['source_sha256'],expected_model=HAIKU.model)
        _,snapshot=load_snapshot(root,lambda p:load_package(p,canonical_manifest=ST/'manifest_staged.json',source_sha=binding['deployment']['source_sha256']))
        verify_native_tools(wire,snapshot,trusted_tools=wire['tools'])
limits=read(A/'LIMITS_FINAL_R2.json')
for key in ('prefix','runtime_source','native_counts','declared_policy_reserve_pre_finalize'):checkpin(limits[key])
for v in limits['actual_runtime_synthetic_envelopes'].values():assert v['slack']==limits['window']-limits['margin']-v['input_bytes']-v['output_reserve']>=0
complete=read(A/'NATIVE_COUNTS_COMPLETE.json');assert complete['public_count_requests']==len(countrows)==6 and complete['generation_requests']==0
assert not attempts
out={'status':'PASS','reviewer':'codex-app-v409-review','scope':'Independent final staging plan and existing native count receipt review. Not deployment/restart authorization, runtime installation, live conversation or physical mobile verification.',
 'plan_sha256':sha((W/'install_plan.json').read_bytes()),'files':len(rows),'runtime_python_changes':0,
 'P2':{'resident':len(resident),'history':len(history['spans']),'full_cluster':len(blocks),'index_uncompacted':True,'source_scope_literal':True},
 'native_counts':{'existing_public_calls':6,'generation_calls':0,'new_count_calls_by_reviewer':0,'fingerprints_reconstructed':len(countrows)},
 'control_scripts_unchanged_from_R1':True,'preservation_pins':13,'runtime_source_baseline_files':len(read(A/'RUNTIME_BASELINE.json')['files']),
 'findings':[], 'human_gate':'Parent must obtain the version-specific human restart/deployment decision and satisfy approved_restart/quiet/CAS. Queue has its own independent gate and receipt.',
 'limitations':['Synthetic admission only; real history/ACOM requires per-call checks.','Remote token results are verified through existing intent/result receipts, not independently re-requested.','DeepSeek dynamic output consumes spare room; 106-byte synthetic residual is not the full history capacity.'],
 'auxiliary_refresh_tower':pin(W/'refresh_tower.py'),'evidence':[pin(A/'BUILDER_HANDOFF_R2.json'),pin(A/'PREPARED_BINDING.json'),pin(A/'COUNT_PREFLIGHT.json'),pin(A/'NATIVE_COUNTS_COMPLETE.json'),pin(A/'LIMITS_FINAL_R2.json'),pin(W/'validation/final_checks.json'),pin(W/'review/CONTROLS_R1.json'),pin(W/'review/PRUNING_R1.json')]}
for stem in ('transaction','maintenance','deploy_controlled','verify_installed','preservation_guard'):out[stem+'_sha256']=sha((W/(stem+'.py')).read_bytes())
out['preservation_baseline_sha256']=sha((W/'PRESERVATION_BASELINE.json').read_bytes())
# Recheck reviewed bytes immediately before emitting the immutable gate artifact.
for e in out['evidence']:checkpin(e)
assert out['plan_sha256']==sha((W/'install_plan.json').read_bytes())
for name,expected in controls['pins'].items():assert sha((W/name).read_bytes())==expected
with (W/'validation/review_final.json').open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2)
print(json.dumps({'status':out['status'],'files':out['files'],'plan_sha256':out['plan_sha256'],'remote_calls':0}))
