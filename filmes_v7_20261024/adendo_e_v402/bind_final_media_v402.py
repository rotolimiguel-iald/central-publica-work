"""Create an additive E receipt; preserve original receipts and final manifests."""
from pathlib import Path
import datetime, hashlib, json, os, runpy, time

C=Path(__file__).resolve().parent
m=runpy.run_path(str(C/'media_v402_worker.py'))
R=m['R']; load,pin,sha,verify=m['load'],m['pin'],m['sha'],m['verify']

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')

def main():
    output=C/'MEDIA_FINAL_BINDING.json'
    assert not output.exists(), 'Existing complementary receipt must be recovered, never overwritten'
    check=m['preflight']()
    protected=[C/'DELIVERY_E.json',R/'audit/DELIVERY_E.json',C/'FINAL_MAKE.json',
               C/'FINAL_RENDER_MANIFEST_LINK.json',C/'MEDIA_RENDER_MANIFEST_PRE_FINAL.json',
               R/'PUBLIC_DELIVERY_V7.json',R/'RENDER_MANIFEST.json',R.parent/'PUBLIC_DELIVERY_V7.json']
    before=[pin(path) for path in protected]
    source=m['canonical_guard']()['source_sha256']
    e=load(C/'DELIVERY_E.json');final=load(C/'FINAL_MAKE.json');link=load(C/'FINAL_RENDER_MANIFEST_LINK.json')
    for item in (e,final,link):assert item['source']=='v402' and item['source_sha256']==source
    assert final['status']=='PASS' and final['returncode']==0 and final['canonical_unchanged'] is True
    assert final['canonical_before']==final['canonical_after']
    for item in final['canonical_after']+final['manifests']+[final['render_manifest_link']]:verify(item)
    assert link['status']=='PASS_SEMANTIC_MANIFEST_TRANSITION'
    for key in ('delivery_e','media_watch','snapshot','final_manifest','builder'):verify(link[key])
    assert link['delivery_e']['sha256']==sha(C/'DELIVERY_E.json')
    assert link['original_e_manifest']==e['render_manifest']
    assert link['snapshot']['sha256']==e['render_manifest']['sha256']
    assert link['snapshot']['bytes']==e['render_manifest']['bytes']
    old=load(C/'MEDIA_RENDER_MANIFEST_PRE_FINAL.json');current=load(R/'RENDER_MANIFEST.json')
    assert 'adendo_worker' in old and 'adendo_worker' not in current
    old.pop('adendo_worker')
    assert canonical(old)==canonical(current), 'Manifest change exceeds root worker annotation/serialization'
    assert link['comparison']['equal'] is True and link['comparison']['numeric_tolerance']==0
    assert link['comparison']['ignored_root_fields']==['adendo_worker']
    public=load(R/'PUBLIC_DELIVERY_V7.json');root=load(R.parent/'PUBLIC_DELIVERY_V7.json')
    assert public['source']==root['source']=='v402' and public['source_sha256']==root['source_sha256']==source
    assert public['anchors_all_ok'] is True
    for item in public['public_files']:
        path=(R/item['path']).resolve();assert path.is_relative_to(R.resolve())
        verify({'file':str(path),'sha256':item['sha256'],'bytes':item['bytes']})
    verify(e['validation']);verify(e['baseline'])
    validation=load(C/'MEDIA_VALIDATION.json');watch=load(C/'MEDIA_WATCH.json')
    assert sha(C/'MEDIA_VALIDATION.json')==e['validation']['sha256']
    assert validation['status']=='PASS' and watch['status']=='COMPLETE'
    assert validation['source']==watch['source']=='v402' and validation['source_sha256']==watch['source_sha256']==source
    assert len(validation['movies'])==16 and len(validation['images'])==25
    assert all(item['full_decode'] is True for item in validation['movies'])
    assert not m['LOCK'].exists()
    baseline=load(m['BASE']);assert m['collect'](R)==baseline['render_closure']
    for item in baseline['frozen_files']:verify(item)
    binding=load(C/'MEDIA_AUDIO_BINDING.json')
    for item in binding['files']:verify(item)
    ui=load(C/'FINAL_PLAYER_V402.json');capture=load(C/'PARENT_CAPTURE_AUDIT.json')
    assert ui['status']=='PASS_OBSERVED_UI' and capture['status']=='PASS_WITH_SCOPE'
    assert ui['source']==capture['source']=='v402' and ui['source_sha256']==capture['source_sha256']==source
    names=['FINAL_MAKE.json','FINAL_RENDER_MANIFEST_LINK.json','MEDIA_RENDER_MANIFEST_PRE_FINAL.json',
           'MEDIA_VALIDATION.json','MEDIA_WATCH.json','MEDIA_V402_BASELINE.json','MEDIA_V401_BACKUP.json',
           'DATA_READY.json','PARENT_NUMERIC_REVIEW.json','AUDIO_READY.json','MEDIA_AUDIO_BINDING.json',
           'FINAL_PLAYER_V402.json','PARENT_CAPTURE_AUDIT.json','MEDIA_START.json','MEDIA_HANDLE_COMPLETE.json',
           'MEDIA_PREPARED.json','MEDIA_WORKER_TESTS.json','MEDIA_READY_CONTRACT_TESTS.json',
           'H264_FILM1_READY.json','H264_FILM2_READY.json']
    receipt={'schema':'iald.media-final-binding.v402/v1','status':'PASS_FINAL_BINDING_READY_FOR_INDEPENDENT_REVIEW',
        'source':'v402','source_sha256':source,'actor':'codex-video-web','task_id':'V402_MEDIA',
        'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preflight':check,
        'original_delivery_e':pin(C/'DELIVERY_E.json'),
        'preserved_audit_delivery_e':{'pin':pin(R/'audit/DELIVERY_E.json'),
             'source':load(R/'audit/DELIVERY_E.json')['source'],
             'role':'Historical receipt preserved at the coordinator request; not promoted to current-v402 evidence.'},
        'final_make':pin(C/'FINAL_MAKE.json'),'final_render_manifest_link':pin(C/'FINAL_RENDER_MANIFEST_LINK.json'),
        'original_render_pin_resolution':{'original':e['render_manifest'],'preserved_bytes':pin(C/'MEDIA_RENDER_MANIFEST_PRE_FINAL.json'),
             'final':pin(R/'RENDER_MANIFEST.json'),'comparison':'Exact typed JSON equality after removing only root adendo_worker; no numeric tolerance.'},
        'final_manifests':[pin(p) for p in (R/'PUBLIC_DELIVERY_V7.json',R/'RENDER_MANIFEST.json',R.parent/'PUBLIC_DELIVERY_V7.json')],
        'public_files_verified':len(public['public_files']),'media_count':len(validation['movies']),
        'image_count':len(validation['images']),'full_decode_repeated':False,
        'current_render_dependency_count':len(baseline['render_closure']),'timings':watch['timings'],
        'elapsed_worker_seconds':watch['elapsed_seconds'],'evidence':[pin(C/name) for name in names],
        'namespace_failure_preserved':baseline['negative_history'],
        'protected_before':before,'original_e_receipts_unchanged':True,'final_manifests_unchanged':True,
        'worker_started_once':True,'worker_restarted':False,'encoding_repeated_this_closure':False,
        'scope':'Additive engineering receipt; no original E, public manifest, source, data, renderer, audio, review or historical evidence rewritten.',
        'limitations':['Independent acceptance remains with the coordinator. No publication by E.',
                      'Parent UI/capture observations are reused with their stated scope; no new GPU benchmark or subjective audio audition.',
                      'Local stage elapsed/FFmpeg time is measured; monetary CPU/energy cost is unmeasured.']}
    assert [pin(path) for path in protected]==before, 'Protected artifact changed concurrently'
    m['canonical_guard']()
    raw=(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    temp=output.with_name(output.name+'.'+str(time.time_ns())+'.tmp')
    with temp.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    assert temp.read_bytes()==raw and raw
    os.rename(temp,output)
    assert [pin(path) for path in protected]==before
    print(json.dumps({'status':receipt['status'],'public_files':receipt['public_files_verified'],'receipt':pin(output)}))

if __name__=='__main__':main()
