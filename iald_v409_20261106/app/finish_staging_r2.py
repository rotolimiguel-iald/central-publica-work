"""Pin final staging and measured synthetic runtime envelopes; no deploy."""
import hashlib,json,sys
from pathlib import Path
A=Path(__file__).resolve().parent;W=A.parent
sys.dont_write_bytecode=True;sys.path[:0]=[str(W),str(A)]
import task,release_cfg,preservation_guard
cfg=release_cfg.load(require_commit=True)
assert task.check('app',actor=cfg.builder)['ready']
sys.path.insert(0,str(release_cfg.R))
import iald_app_providers as providers
import iald_kernel,iald_fontes_publicas,iald_core_indexado,iald_app_memory
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def save(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,ensure_ascii=False,indent=2)
prefix=(A/'packages/shared/prefix.md').read_bytes().decode()
approved=read(W/'capacity_experiments/PRUNING_REPORT.json')
assert sha(A/'packages/shared/prefix.md')==approved['candidate_sha256']
assert read(A/'D53_HISTORY.json')['pruning']['dictionary_before']==360
assert read(A/'D53_HISTORY.json')['pruning']['dictionary_after']==186
messages=[{'role':'system','content':prefix},{'role':'user','content':'Explique o alcance documentado da v409.'}]
prompt=json.dumps({'instructions':messages[0]['content'],'conversation':messages[1:]},ensure_ascii=False)
used=len(prompt.encode());reserve=providers.MODELS['kimi']['output']
bounds={'kimi':dict(input_bytes=used,output_reserve=reserve,slack=providers.WINDOW-used-reserve-4096,
    envelope='instructions/conversation JSON once, as in current Kimi branch')}
assert bounds['kimi']['slack']>=0
tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
offered=[t for t in tools if (t.get('function') or {}).get('name') in providers.TOOL_NAMES]
for provider in ('mimo','deepseek'):
    spec=providers.MODELS[provider]
    body=dict(model=spec['model'],messages=messages,stream=True,stream_options={'include_usage':True},thinking={'type':'enabled'})
    if provider=='deepseek':body['reasoning_effort']='max'
    body.update(providers.transport_tool_options(provider,offered,0,providers.MAX_ROUNDS))
    reserve=providers.output_budget(body,spec['output'])
    body['max_tokens' if provider=='deepseek' else 'max_completion_tokens']=reserve
    used=providers.check_window(body,reserve)
    bounds[provider]=dict(input_bytes=used,output_reserve=reserve,slack=providers.WINDOW-used-reserve-4096,
                          envelope='Current runtime first round tool options; dynamic output_budget unchanged')
preserved=preservation_guard.verify()
assert all(sha(Path(r['path']))==r['sha256'] for r in read(A/'RUNTIME_BASELINE.json')['files'])
plan=read(W/'install_plan.json');assert plan['runtime_python_changes']==0 and plan['staging_only']
for row in plan['files']:
    p=Path(row['source']);dest=Path(row['destination'])
    assert sha(p)==row['sha256'] and '.bak' not in p.name
    assert not(dest.suffix=='.py' and dest.parent==release_cfg.R)
    assert dest.is_relative_to(release_cfg.R)
assert read(A/'NATIVE_COUNTS_COMPLETE.json')['public_count_requests']==6
limits=dict(status='PASS_FINAL_STAGING_SYNTHETIC_ADMISSION',prefix=pin(A/'packages/shared/prefix.md'),
    window=providers.WINDOW,margin=4096,actual_runtime_synthetic_envelopes=bounds,
    declared_policy_reserve_pre_finalize=pin(A/'D53_shared_VERIFIED.json'),
    runtime_source=pin(release_cfg.R/'iald_app_providers.py'),
    caveat='Synthetic already-projected system and user only; no live ACOM/history/owner notice. Their bytes require per-call admission. Dynamic DeepSeek output uses available room, so remaining slack after maximum output is not the maximum conversation capacity.',
    native_counts=pin(A/'NATIVE_COUNTS_COMPLETE.json'),ceilings_changed=False,reserves_changed=False,provider_generation_calls=0)
save(A/'LIMITS_FINAL_R2.json',limits)
files=['RELEASE.json','BUILT.json','PREPARED_BINDING.json','DELIVERY_PREPARED.json','DATA_PLAN.json',
       'D53_shared_VERIFIED.json','D53_sonnet_public_VERIFIED.json','D53_HISTORY.json','LIMITS_FINAL_R2.json',
       'COUNT_PREFLIGHT.json','NATIVE_COUNTS_COMPLETE.json','RUNTIME_BASELINE.json','PUBLIC_RAW_VERIFIED.json',
       'KERNEL_HIGHLIGHTS.json','build/prune_literals.py']
receipt=dict(status='PREPARED_R2_READY_FOR_DISTINCT_REVIEW_NOT_INSTALLED',reference=str(task.REF),actor=cfg.builder,
    release=cfg.release,plan=pin(W/'install_plan.json'),data_plan=pin(A/'DATA_PLAN.json'),
    checks=pin(W/'validation/final_checks.json'),measurements=pin(W/'BUILDER_MEASUREMENTS.json'),
    evidence=[pin(A/n) for n in files],pruning_review=pin(W/'review/PRUNING_R1.json'),
    preservation_guard_sha256=sha(W/'preservation_guard.py'),preservation_baseline_sha256=sha(W/'PRESERVATION_BASELINE.json'),
    preserved_runtime_client_files=len(preserved),data_files=len(plan['files']),runtime_python_changes=0,
    source_originals_modified=False,production_writes=0,restarts=0,generation_calls=0,public_count_calls=6,
    app_accepted=False,deploy_authorized=False,
    remaining=['Independent final review and app acceptance','Human v409 deployment/restart gate and controlled installation by parent'],
    historical_receipts_preserved=['app/CAPACITY_BLOCKED.json','app/BUILDER_HANDOFF.json','app/DATA_PLAN_CANDIDATE.json'],
    builder_note='Only reviewed orphan pruning integrated; no threshold change or new concat algorithm. Historical_machine_labels receipt order differs across processes, but source and output prefix bytes agree; retained old receipt.')
save(A/'BUILDER_HANDOFF_R2.json',receipt)
print(json.dumps({'status':receipt['status'],'files':len(plan['files']),'runtime':bounds,'preserved':len(preserved)}))
