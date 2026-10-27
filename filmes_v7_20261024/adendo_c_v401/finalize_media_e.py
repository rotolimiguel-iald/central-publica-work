"""Pin the parent's completed make into E receipts; never run make or encode."""
from pathlib import Path
import datetime, json, os, runpy, time

C=Path(__file__).resolve().parent
m=runpy.run_path(str(C/'media_v401_worker.py'))
R=m['R']; load,pin,sha,verify=m['load'],m['pin'],m['sha'],m['verify']

def main():
    preflight=m['preflight']()
    g=m['main'].__globals__
    g['baseline']=load(m['BASE']);g['audio_binding']=load(C/'MEDIA_AUDIO_BINDING.json')
    m['guard']()
    assert load(C/'MEDIA_WATCH.json')['status']=='COMPLETE' and not m['LOCK'].exists()
    final=load(C/'FINAL_MAKE.json')
    assert final['status']=='PASS' and final['returncode']==0 and final['canonical_unchanged'] is True
    source=g['baseline']['source_sha256']
    assert final['source']=='v401' and final['source_sha256']==source
    for item in final['manifests']:verify(item)
    public=load(R/'PUBLIC_DELIVERY_V7.json');root_public=load(R.parent/'PUBLIC_DELIVERY_V7.json')
    assert public['source']==root_public['source']=='v401'
    assert public['source_sha256']==root_public['source_sha256']==source
    assert public['anchors_all_ok'] is True
    # Final manifest byte check only: the completed full decode is not repeated.
    for item in public['public_files']:
        path=(R/item['path']).resolve();assert path.is_relative_to(R.resolve())
        verify({'file':str(path),'bytes':item['bytes'],'sha256':item['sha256']})
    validation=load(C/'MEDIA_VALIDATION.json')
    assert validation['status']=='PASS' and validation['source']=='v401' and validation['source_sha256']==source
    assert len(validation['movies'])==16 and len(validation['images'])==25
    assert all(row['full_decode'] is True for row in validation['movies'])
    ui=load(C/'FINAL_PLAYER_V401.json');capture=load(C/'PARENT_CAPTURE_AUDIT.json')
    assert ui['status']=='PASS_OBSERVED_UI' and capture['status']=='PASS_WITH_SCOPE'
    assert ui['source']==capture['source']=='v401' and ui['source_sha256']==capture['source_sha256']==source
    original=load(C/'DELIVERY_E.json')
    assert original['status']=='MEDIA_VALIDATED_AWAITING_PARENT_PUBLIC_MANIFEST'
    targets=[C/'DELIVERY_E.json',R/'audit/DELIVERY_E.json'];previous=[]
    for path in targets:
        old=pin(path);raw=path.read_bytes();backup=path.with_name(path.name+'.bak_before_v401_final_'+str(time.time_ns()))
        with backup.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
        assert sha(backup)==old['sha256'];previous.append({'original':old,'backup':pin(backup)})
    names=['FINAL_MAKE.json','DATA_READY.json','PARENT_NUMERIC_REVIEW.json','AUDIO_READY.json',
           'MEDIA_AUDIO_BINDING.json','MEDIA_V400_BACKUP.json','MEDIA_SCHEMA_FIX.json','MEDIA_SCHEMA_FIX_TESTS.json',
           'MEDIA_START.json','MEDIA_HANDLE_COMPLETE.json','MEDIA_LIVENESS_R1.json',
           'H264_FILM1_READY.json','H264_FILM2_READY.json','ENCODE_FILM1.json','ENCODE_FILM2.json',
           'ENCODE_LOOP.json','ENCODE_VALIDATION.json','ASSETS_V401.json']
    receipt={**original,'status':'TECHNICAL_DELIVERY_READY_FOR_INDEPENDENT_REVIEW',
        'finalized_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preflight':preflight,
        'public_manifest':pin(R/'PUBLIC_DELIVERY_V7.json'),'root_public_pointer':pin(R.parent/'PUBLIC_DELIVERY_V7.json'),
        'render_manifest':pin(R/'RENDER_MANIFEST.json'),'public_files_verified':len(public['public_files']),
        'current_render_dependency_count':len(m['collect'](R)),'full_decode_repeated':False,
        'final_ui':pin(C/'FINAL_PLAYER_V401.json'),'capture_audit':pin(C/'PARENT_CAPTURE_AUDIT.json'),
        'evidence':[pin(C/name) for name in names],'previous_delivery_backups':previous,
        'worker_launched_once':True,'worker_restarted':False,'source_edits':False,
        'canonical_unchanged_scope':'Current v401 seal rechecked; source/data/render dependencies remain pinned. No scientific import or proof execution by E.',
        'closure_scope':'Parent observed UI and capture; E reused those receipts. Integrated-GPU timing and subjective audio audition were not repeated.',
        'pending':['Independent review and acceptance by the coordinator; no self-acceptance or publication.']}
    raw=(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    m['guard']()
    for path,old in zip(targets,previous):
        assert pin(path)==old['original'],'Receipt changed concurrently'
        temp=path.with_name(path.name+'.'+str(time.time_ns())+'.tmp')
        with temp.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
        assert temp.read_bytes()==raw and len(raw)>0
        os.replace(temp,path)
    assert targets[0].read_bytes()==targets[1].read_bytes()
    print(json.dumps({'status':receipt['status'],'public_files':receipt['public_files_verified'],
                      'receipts':[pin(p) for p in targets]}))

if __name__=='__main__':main()
