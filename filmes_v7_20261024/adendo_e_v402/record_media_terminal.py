"""Verify completed receipts and hand off before parent make; no encoding/binding."""
from pathlib import Path
import datetime, json, runpy, subprocess, time

E = Path(__file__).resolve().parent
W = E.parent
m = runpy.run_path(str(E/'media_v402_worker.py'))
pin, load, verify = m['pin'], m['load'], m['verify']
write = runpy.run_path(str(E/'prepare_media_v402.py'))['immutable']


def session(payload):
    command = [r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py']
    result = subprocess.run(command,input=json.dumps({'reference':str(W/'SESSION_REFERENCE.json'),**payload},ensure_ascii=False),
        text=True,encoding='utf-8',capture_output=True)
    parsed = json.loads(result.stdout)
    assert parsed.get('ok'), parsed
    return parsed


def main():
    watch = load(E/'MEDIA_WATCH.json')
    assert watch['status'] == 'COMPLETE', 'Wait for the existing worker terminal state'
    for _ in range(15):
        if not m['LOCK'].exists(): break
        time.sleep(1)
    assert not m['LOCK'].exists(), 'Worker terminal cleanup still pending; no lock removal by observer'
    check = m['preflight']()
    globals_ = m['guard'].__globals__
    globals_['baseline'] = load(m['BASE'])
    globals_['audio_binding'] = load(E/'MEDIA_AUDIO_BINDING.json')
    m['guard']()
    source = globals_['baseline']['source_sha256']
    delivery_path = E/'DELIVERY_E.json'
    original_e = pin(delivery_path); delivery = load(delivery_path)
    validation = load(E/'MEDIA_VALIDATION.json')
    for value in (watch,delivery,validation):
        assert value['source'] == 'v402' and value['source_sha256'] == source
    assert delivery['status'] == 'MEDIA_VALIDATED_AWAITING_PARENT_PUBLIC_MANIFEST'
    assert validation['status'] == 'PASS' and len(validation['movies']) == 16 and len(validation['images']) == 25
    assert set(watch['completed']) == {'film1','film2','loop'} and watch['assets_complete'] is True
    assert all(item['full_decode'] is True for item in validation['movies'])
    for key in ('validation','baseline','backup','audio_binding','assets','render_manifest'): verify(delivery[key])
    assert pin(E/'MEDIA_VALIDATION.json')['sha256'] == delivery['validation']['sha256']
    for item in validation['movies'] + validation['images']: verify(item)
    capture = load(E/'PARENT_CAPTURE_AUDIT.json'); ui = load(E/'PLAYER_F1_V402.json')
    for value in (capture,ui): assert value['source'] == 'v402' and value['source_sha256'] == source
    assert capture['status'] == 'PASS_WITH_SCOPE' and ui['status'] == 'PASS_OBSERVED_UI'
    frame_total = 0
    for kind,item in watch['completed'].items():
        verify(item); job = load(Path(item['file'])); metadata = job['metadata']
        expected = {'film1':224,'film2':360,'loop':16}[kind]
        size = (1920,1080) if kind == 'loop' else (3840,2160)
        assert metadata['source'] == 'v402' and metadata['source_sha256'] == source
        assert (metadata['width'],metadata['height']) == size and metadata['fps'] == 60
        assert metadata['duration'] == expected and metadata['total'] == job['render']['encoded'] == expected*60
        assert job['source_files'] == globals_['baseline']['render_closure']
        frame_total += metadata['total']
    render_path = Path(delivery['render_manifest']['file'])
    snapshot = E/'MEDIA_RENDER_MANIFEST_PRE_FINAL.json'
    write(snapshot,render_path.read_bytes())
    assert snapshot.stat().st_size == delivery['render_manifest']['bytes']
    assert m['sha'](snapshot) == delivery['render_manifest']['sha256']
    output = E/'MEDIA_HANDOFF_PRE_FINAL.json'
    if output.exists():
        report = load(output)
        assert report['original_delivery_e'] == original_e and report['validation'] == pin(E/'MEDIA_VALIDATION.json')
    else:
        report = {'status':'PASS_MEDIA_COMPLETE_AWAITING_PARENT_FINAL_MAKE_AND_UI','source':'v402',
            'source_sha256':source,'actor':'codex-video-web','task_id':'V402_MEDIA',
            'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preflight':check,
            'original_delivery_e':original_e,'watch':pin(E/'MEDIA_WATCH.json'),'validation':pin(E/'MEDIA_VALIDATION.json'),
            'worker_start':pin(E/'MEDIA_START.json'),'pid':load(E/'MEDIA_START.json')['pid'],
            'media_count':len(validation['movies']),'image_count':len(validation['images']),
            'full_decode_pass_count':sum(x['full_decode'] is True for x in validation['movies']),
            'capture_frame_total':frame_total,'render_dependency_count':len(globals_['baseline']['render_closure']),
            'render_manifest':delivery['render_manifest'],'pre_final_snapshot':pin(snapshot),
            'parent_capture':pin(E/'PARENT_CAPTURE_AUDIT.json'),'parent_f1_ui':pin(E/'PLAYER_F1_V402.json'),
            'timings':watch['timings'],'elapsed_worker_seconds':watch['elapsed_seconds'],
            'initial_launch_refusal':pin(E/'MEDIA_LAUNCH_REFUSAL_R0.json'),
            'namespace_failure_preserved':delivery['namespace_failure_preserved'],
            'verification':'Existing full-decode PASS receipts plus current output SHA/source/closure checks; no repeated decode.',
            'final_make_executed':False,'final_binding_executed':False,'worker_restarted':False,
            'original_e_unchanged':True,'pending':['Parent FINAL_MAKE and FINAL_PLAYER; explicit authorization for additive binding/submission.']}
        write(output,(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
    assert pin(delivery_path) == original_e
    m['canonical_guard']()
    receipt = E/'MEDIA_HANDLE_COMPLETE.json'
    if not receipt.exists():
        state = session({'operation':'get'})['result']; start = load(E/'MEDIA_START.json')
        handles = state['p']['handles']; matches = [h for h in handles if h['id'] == start['handle_id']]
        assert len(matches) == 1 and matches[0]['pid'] == start['pid']
        matches[0].update(status='completed',evidence=str(output),source={'kind':'artifact','ref':str(output),'sha256':m['sha'](output)})
        result = session({'operation':'transition','actor':{'id':'codex-video-web','kind':'agent'},
            'expected_revision':state['revision'],'event_id':'ordem022-v402-media-worker-complete-20261027',
            'changes':{'records':[{'id':'v402-media-complete-pre-final','kind':'fact','statute':'REAL',
                'text':'V402 media worker COMPLETE; 16 videos and 25 images validated, current output hashes/43 render pins checked. Original E and pre-final render bytes preserved. Await parent final make/UI before additive binding or submission.',
                'sources':[{'kind':'artifact','ref':str(output),'sha256':m['sha'](output)}]}],
                'flow':{**state['p'],'phase':'v402_media_complete_awaiting_parent_final','next_action':'Parent final make and final UI; E binding/submission only after explicit notice.','handles':handles}}})
        write(receipt,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps({'status':report['status'],'media':report['media_count'],'images':report['image_count'],
        'frames':frame_total,'handoff':pin(output),'snapshot':pin(snapshot),'handle_receipt':pin(receipt)},ensure_ascii=False))


if __name__ == '__main__': main()
