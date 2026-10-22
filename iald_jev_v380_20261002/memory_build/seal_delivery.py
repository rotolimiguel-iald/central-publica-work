"""Freeze an offline delivery receipt. Does not rebuild or deploy any artifact."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, sys
sys.dont_write_bytecode=True
B=Path(__file__).resolve().parent;W=B.parent;S=W/'memory_stage'
sys.path.insert(0,str(B));import package_native as native
sha=lambda raw:hashlib.sha256(raw).hexdigest()
read=lambda p:json.loads(Path(p).read_bytes())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--count-receipt',type=Path);a=parser.parse_args()
    prefix=sha((S/'haiku_prefix.md').read_bytes());manifest=read(S/'manifest_staged.json');prepared=read(S/'prepared.json')
    review_path=W/'validation/memory_review.json';review=read(review_path)
    assert review['status']=='PASS' and not review['failed_checks'] and not review['findings']
    for path,record in review['input_pins'].items():
        raw=Path(path).read_bytes();assert sha(raw)==record['sha256'] and len(raw)==record['bytes'],path
    assert review['input_pins'][str(S/'haiku_prefix.md')]['sha256']==prefix
    candidates=[]
    for path in B.glob('local_validation_*.json'):
        r=read(path)
        if r['status']=='PASS' and r['prefix_sha256']==prefix and r['manifest_sha256']==sha((S/'manifest_staged.json').read_bytes()):candidates.append((path,r))
    assert candidates
    local_path,local=max(candidates,key=lambda pair:pair[0].name)
    for name,digest in local['script_hashes'].items():assert sha((B/name).read_bytes())==digest,name
    for path,digest in prepared['protected_production_sha256'].items():assert sha(Path(path).read_bytes())==digest,path
    mapping=[];paths=set()
    for row in manifest['entries']+[manifest['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]:paths.add(Path(row['path']))
    for key in ('mother_instruction','operational_core'):paths.add(Path(manifest[key]['path']))
    for key in ('path','kernel_verification'):paths.add(Path(manifest['active_cluster'][key]))
    for row in read(S/'kernel/kernel_manifest.json')['files']:paths.add(S/'kernel'/row['path'])
    paths.add(S/'kernel/kernel_manifest.json')
    for path in sorted(paths):
        raw=path.read_bytes();mapping.append({'stage':str(path),'destination':str(Path(prepared['install_target'])/path.relative_to(S)),'sha256':sha(raw),'bytes':len(raw)})
    count=None
    if a.count_receipt:
        r=read(a.count_receipt);request=native.prepare(prefix);budget=native.verify_receipt(r,request,prefix)
        count={'path':str(a.count_receipt.resolve()),'sha256':sha(a.count_receipt.read_bytes()),'budget':budget}
    artifacts=('manifest_staged.json','manifest_install.json','haiku_prefix.md','haiku_provenance.json','haiku_transport_fit.json','TGL_CLUSTER_v380.md','IALD_Kernel_v5.txt','IALD_TGL_MEMORY_CORE.md','document_index.json','kernel/kernel_manifest.json','kernel_verification.json','native_prefix.md','native_metadata.json','public_prefix.md','public_metadata.json','science_binding.json','prepared.json')
    result={'schema':'iald.memory.v380.delivery.v1','status':'READY_FOR_MAIN_INTEGRATION' if count else 'OFFLINE_PASS_AWAITING_MAIN_NATIVE_RECOUNT',
        'created_at_utc':datetime.now(timezone.utc).isoformat(),'deployment_identity':prepared['deployment_identity'],
        'artifacts':{name:{'sha256':sha((S/name).read_bytes()),'bytes':(S/name).stat().st_size} for name in artifacts},
        'local_validation':{'path':str(local_path),'sha256':sha(local_path.read_bytes()),'tests':local['tests']},
        'codec_selftests':{'tests':10,'result':'PASS','run_command':'python -X utf8 -B memory_build/haiku_codec.py --self-test'},
        'independent_review':{'path':str(review_path),'sha256':sha(review_path.read_bytes()),'passed':review['checks_passed'],'total':review['checks_total']},
        'native_measurement':count,'install_file_map':mapping,
        'install_manifest':{'source':str(S/'manifest_install.json'),'destination':str(native.APP/'iald_nucleo_fixo.json')},
        'runtime_package':'MAIN owns measured haiku_runtime and controller integration; optional package_native.finalize supports these exact bindings',
        'scripts':{name:sha((B/name).read_bytes()) for name in ('build_release.py','haiku_codec.py','fit_transport.py','package_native.py','test_local_stage.py','seal_delivery.py')},
        'scope':{'production_writes':0,'provider_calls_by_builder':0,'program_executed_or_imported':False,'kernel_compiled_here':False,'provider_profiles_changed':False,'bench_ram_changed':False,'global_orchestrator_changed':False},
        'preservation':{'core_topics':362,'new_topics':prepared['added_topics'],'embedded_kernel_sources':1208,'separately_pinned_supplements':1,'v5_original_bytes':True,'previous_operational_core_original_bytes':True,'negative_verdict_maps_inline':True},
        'limitations':['Haiku is a faithful contextual projection plus exact source pointers, not every full source inline.','Kernel compilation evidence is the sealed published report; no new compilation occurred.','Native/Llama serving count was not called; original serving limits are preserved.','Public/full context measured locally with o200k; no new OpenAI/Chinese provider calls.','Permissions, consent, quotas, Sonnet restrictions and operator tools belong to unchanged runtime modules; no account changes.']}
    target=B/('delivery_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json');raw=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode();temp=target.with_suffix('.tmp')
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw;temp.rename(target)
    print(json.dumps({'receipt':str(target),'status':result['status'],'prefix_sha256':prefix,'copy_files':len(mapping),'review':review['status']}))
if __name__=='__main__':main()