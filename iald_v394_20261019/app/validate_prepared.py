"""Read-only verification and offline envelope checks. No provider or science run."""
from pathlib import Path
import ast, hashlib, json, os, sys
A=Path(__file__).resolve().parent
sys.path.insert(0,str(A.parent))
import task
assert task.check('app',actor='codex-v394-app-builder')['ready']
sys.path[:0]=[str(A/'science/memory_build'),str(A),r'C:\IALD\projetos_pyhton\IALD']
sys.dont_write_bytecode=True
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):
        raise RuntimeError('Offline validation only')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,int):return
        p=Path(os.fsdecode(path)).resolve()
        if p.name.lower() in ('.env','iald_stack_v7.py','iald_psion_state.json'):
            raise RuntimeError('Confidential source refused')
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not p.is_relative_to(A):raise RuntimeError('Write outside app staging')
sys.addaudithook(guard)
from prepare_science import save,write,sha,R
import build_release as builder
import iald_app_providers as providers
import iald_kernel,iald_core_indexado,iald_fontes_publicas,iald_app_memory
from iald_jev_control import load_contract
S=A/'science';stage=S/'memory_stage'
m=json.loads((stage/'manifest_staged.json').read_bytes())
prepared=json.loads((stage/'prepared.json').read_bytes())
new=json.loads(Path(m['published_evidence']['result']['path']).read_bytes())
baseline=json.loads((R/'iald_nucleo_fixo.json').read_bytes())
old=json.loads(Path(baseline['published_evidence']['result']['path']).read_bytes())
assert len(old['core'])==411 and len(new['core'])==422
assert set(old['core'])<=set(new['core'])
topics=builder.read_topics((stage/'TGL_CLUSTER_v394.md').read_text(encoding='utf-8'))
for name,projection in topics.items():
    pointer=builder.codec.child('/core',name)
    restored=builder.codec.restore(projection,new,pointer,pointer,{})
    if restored!=new['core'][name]:restored=builder.verify_old_projection(projection,new,pointer,pointer)
    assert restored==new['core'][name]
assert set(topics)==set(new['core'])
assert (stage/'IALD_Kernel_v5.txt').read_bytes()==Path(baseline['mother_instruction']['path']).read_bytes()
assert (stage/'IALD_TGL_MEMORY_CORE.md').read_bytes().startswith(Path(baseline['operational_core']['path']).read_bytes())
save(stage/'iald_nucleo_fixo.json',(stage/'manifest_staged.json').read_bytes())
contract=load_contract(stage)
prefix=(stage/'shared_prefix.md').read_text(encoding='utf-8')
tools=iald_kernel.tool_definitions()+iald_core_indexado.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_app_memory.tool_definitions()
assert len({t['function']['name'] for t in tools})==len(tools)
messages=[{'role':'system','content':prefix},{'role':'user','content':'Consulte o alcance documentado da v394.'}]
envelopes={}
for name in ('kimi','mimo','deepseek'):
    if name=='kimi':
        body={'messages':messages,'tools':[]}
        reserve=providers.MODELS[name]['output']
    else:
        body=dict(model=providers.MODELS[name]['model'],messages=messages,stream=True,
                  stream_options={'include_usage':True},thinking={'type':'enabled'},tools=tools,tool_choice='auto')
        if name=='deepseek':body['reasoning_effort']='max'
        reserve=providers.output_budget(body,providers.MODELS[name]['output'])
        body['max_tokens' if name=='deepseek' else 'max_completion_tokens']=reserve
    used=providers.check_window(body,reserve)
    envelopes[name]={'status':'OFFLINE_MINIMAL_ENVELOPE_ADMITTED_NOT_FULL_CONVERSATION',
        'input_utf8_bytes_bound':used,'output_reserved_tokens':reserve,
        'remaining_bytes_bound':providers.WINDOW-used-reserve-4096,
        'native_tokens':None,'final_activity_history_and_tools_admission_required':True}
# Negative control: same real guard rejects an oversized mandatory payload.
try:providers.check_window({'messages':[{'role':'system','content':'x'*providers.WINDOW}]},16384)
except ValueError:negative=True
else:raise AssertionError('Oversized envelope accepted')
runtime_rows=json.loads((A/'runtime_baseline.json').read_bytes())['files']
assert all(sha(Path(row['path']).read_bytes())==row['sha256'] for row in runtime_rows)
for path in A.rglob('*.py'):ast.parse(path.read_text(encoding='utf-8-sig'))
full=(stage/'public_prefix.md').read_bytes();native=(stage/'native_prefix.md').read_bytes()
summary={'status':'LOCAL_PREPARATION_VERIFIED_ADMISSION_AND_PUBLICATION_PENDING','release':'v394',
    'source_sha256':prepared['source_sha256'],'topic_count':len(topics),'previous_topic_count':len(old['core']),
    'added_topics':prepared['added_topics'],'all_topics_roundtrip':True,'kernel_v5_bytes_preserved':True,
    'previous_core_bytes_preserved':True,'jev_source_binding_verified':True,
    'formal_source_files':len(json.loads((stage/'kernel/kernel_manifest.json').read_bytes())['files']),
    'full_haiku':{'prefix_bytes':len(full),'offline_o200k_tokens':builder.codec.offline_tokens(full.decode(),R/'.iald_runtime/tokenizer_cache'),'native_count_pending':True,'offline_runtime_400000_guard_exceeded':True},
    'shared':{'prefix_bytes':len(prefix.encode()),'offline_o200k_tokens':builder.codec.offline_tokens(prefix,R/'.iald_runtime/tokenizer_cache'),'connectors':envelopes},
    'openai':{'metadata':'SOURCE_BOUND_V394','final_model_request_native_admission_pending':True,'runtime_full_context_guard_exceeded':True},
    'native':{'prefix_bytes':len(native),'identity':prepared['deployment_identity'],'local_template_tokenization_pending':True},
    'runtime_baseline_files_unchanged':len(runtime_rows),'negative_oversize_control_rejected':negative,
    'publication_verified':False,'provider_calls':0,'paid_count_calls':0,'science_executed_or_imported':False,
    'installations':0,'runtime_python_replacements':0,'staging_compatibility_shims_are_not_installable':True}
write(A/'LOCAL_VALIDATION.json',summary)
print(json.dumps({k:summary[k] for k in ('status','topic_count','formal_source_files','runtime_baseline_files_unchanged')}))
