"""Count-only requests with an injected SDK client; finalize a hash-bound local package.
CLI finalizes an existing main-generated receipt. It never creates an SDK client.
"""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime, timezone
import argparse, hashlib, json, sys
sys.dont_write_bytecode=True
BUILD=Path(__file__).resolve().parent;STAGE=BUILD.parent/'memory_stage'
APP=Path('C:/IALD/projetos_pyhton/IALD');sys.path.insert(0,str(APP))
from claude_profiles import HAIKU, context_budget, reasoning_parameters
from claude_native_counter import count_native_request
from claude_context_snapshot import native_tools_sha256, PUBLIC_NAMES, snapshot_from_manifest
from iald_motor_claude import converter_pedido
from iald_release_binding import load_release
import iald_kernel,iald_fontes_publicas,iald_core_indexado
sha=lambda b:hashlib.sha256(b).hexdigest()

def prepare(expected_sha):
    path=STAGE/'haiku_prefix.md';raw=path.read_bytes()
    if sha(raw)!=expected_sha:raise ValueError('prefix_compare_and_swap_failed')
    prefix=raw.decode('utf-8');release=load_release(STAGE/'manifest_staged.json')
    if '<ATLAS_CANONICO' in prefix:raise ValueError('nonpublic_context')
    for key in ('mother_instruction','operational_core'):
        item=release.config[key];data=Path(item['path']).read_bytes()
        if sha(data)!=item['sha256'] or data.decode('utf-8-sig') not in prefix:raise ValueError('fixed_memory_mismatch')
    if release.identity['source_sha256'] not in prefix:raise ValueError('source_binding_missing')
    defs=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()
    if tuple(t['function']['name'] for t in defs)!=PUBLIC_NAMES:raise ValueError('unexpected_tools')
    cfg=SimpleNamespace(modelo=HAIKU.model,max_saida=4096,cache_ttl='5m',esforco_claude='high')
    payload={'model':HAIKU.model,'max_tokens':4096,'messages':[{'role':'system','content':prefix},{'role':'user','content':'Quem é o autor da TGL? Explique Hamiltoniano, Lindblad e dephasing no escopo documentado.'}],'tools':defs}
    wire=converter_pedido(cfg,payload,prefixo=prefix);wire.pop('output_config',None);wire.update(reasoning_parameters(HAIKU.model,4096))
    minimal={'model':HAIKU.model,'system':wire['system'],'messages':[{'role':'user','content':'.'}],'thinking':{'type':'disabled'}}
    return {'minimal':minimal,'wire':wire,'raw':raw,'release':release,'tools_sha256':native_tools_sha256(wire['tools'])}

def measure(client,expected_sha):
    """EXPLICIT MAIN CALL ONLY. Exactly two count requests, zero generation/retries."""
    request=prepare(expected_sha)
    try:
        counting=client.with_options(max_retries=0)
        permanent=count_native_request(counting,request['minimal'])
        whole=count_native_request(counting,request['wire'])
    except Exception:
        raise ValueError('native_measurement_failed') from None
    request['release'].check_manifest()
    if (STAGE/'haiku_prefix.md').read_bytes()!=request['raw']:raise ValueError('prefix_changed_during_measurement')
    identity=request['release'].identity
    return {'time_utc':datetime.now(timezone.utc).isoformat(),**identity,'draft_path':str(STAGE/'haiku_prefix.md'),
        'draft_sha256':expected_sha,'model':HAIKU.model,'budget':context_budget(HAIKU.model,counted_model=HAIKU.model,
        permanent_tokens=permanent,request_input_tokens=whole,reserved_output_tokens=4096),
        'native_tools_sha256':request['tools_sha256'],'count_requests':2,'generation_requests':0,
        'scope':'PUBLIC_SCIENCE_PLUS_APPROVED_KERNEL_AND_CORE_NO_PRIVATE_ATLAS'}

def verify_receipt(receipt,request,expected_sha):
    identity=request['release'].identity
    if (receipt['draft_sha256']!=expected_sha or receipt['model']!=HAIKU.model
        or receipt['release']!=identity['release'] or receipt['source_sha256']!=identity['source_sha256']
        or receipt['cluster_sha256']!=identity['cluster_sha256']
        or receipt['native_tools_sha256']!=request['tools_sha256']
        or receipt['count_requests']!=2 or receipt['generation_requests']!=0):
        raise ValueError('measurement_identity_mismatch')
    b=receipt['budget']
    checked=context_budget(HAIKU.model,counted_model=HAIKU.model,permanent_tokens=b['permanent_tokens'],
        request_input_tokens=b['request_input_tokens'],reserved_output_tokens=4096,margin_tokens=1024)
    if b!=checked or not checked['ready'] or checked['remaining_tokens']<10000:
        raise ValueError('native_memory_gate_failed')
    return checked

def write_new(path,raw):
    path=Path(path).resolve()
    if not path.is_relative_to(STAGE):raise ValueError('output_outside_stage')
    if path.exists():
        previous=path.read_bytes()
        if previous==raw:return
        saved=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with saved.open('xb') as stream:stream.write(previous)
        assert saved.read_bytes()==previous
    path.parent.mkdir(parents=True,exist_ok=True);temp=path.with_name(path.name+'.tmp')
    with temp.open('xb') as stream:stream.write(raw)
    assert temp.read_bytes()==raw and raw
    temp.replace(path)

def finalize(receipt_path,expected_sha):
    request=prepare(expected_sha);receipt_path=Path(receipt_path).resolve();receipt_raw=receipt_path.read_bytes();receipt=json.loads(receipt_raw)
    budget=verify_receipt(receipt,request,expected_sha)
    manifest={'schema':'iald.claude.memory.v1','status':'MEASURED_READY','model':HAIKU.model,
        'prefix_file':'prefix.md','prefix_sha256':expected_sha,'budget':budget,'tools_sha256':request['tools_sha256'],
        'measurement_receipt':str(receipt_path),'measurement_receipt_sha256':sha(receipt_raw),
        'source_draft':'haiku_prefix.md','scope':receipt['scope'],'deployment':request['release'].identity}
    request['release'].check_manifest()
    if (STAGE/'haiku_prefix.md').read_bytes()!=request['raw'] or receipt_path.read_bytes()!=receipt_raw:
        raise ValueError('finalization_input_changed')
    directory=STAGE/'haiku_runtime'
    write_new(directory/'prefix.md',request['raw'])
    write_new(directory/'manifest.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
    from claude_memory_package import load_package
    package=load_package(directory,canonical_manifest=STAGE/'manifest_staged.json',source_sha=request['release'].identity['source_sha256'])
    snapshot=snapshot_from_manifest(manifest,package)
    return {'status':'MEASURED_PACKAGE_VALIDATED_OFFLINE','prefix_sha256':snapshot.prefix_sha256,
        'permanent':snapshot.permanent,'remaining':snapshot.reference_remaining,'directory':str(directory),
        'activation':'MAIN_ONLY_AFTER_INDEPENDENT_AUDIT','provider_generation_calls':0}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--receipt',required=True);p.add_argument('--expected-prefix-sha',required=True);a=p.parse_args()
    try:print(json.dumps(finalize(a.receipt,a.expected_prefix_sha)))
    except Exception as exc:print(json.dumps({'status':'FAILED','type':type(exc).__name__}));sys.exit(1)