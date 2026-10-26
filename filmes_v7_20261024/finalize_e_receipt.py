"""Verify completed artifacts, freeze E evidence; never encode or edit sources."""
import datetime, hashlib, json, os, pathlib, runpy

W = pathlib.Path(__file__).resolve().parent
R = pathlib.Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
M = runpy.run_path(str(R / 'cinema/media_v7.py'))
load, pin = M['load'], M['pin']

def verify(entry, base=None):
    p = pathlib.Path(entry.get('file', entry.get('path')))
    if not p.is_absolute():
        assert base is not None
        p = (base / p).resolve()
        assert p.is_relative_to(base.resolve())
    actual = pin(p)
    assert actual['sha256'] == entry['sha256'], str(p)
    if 'bytes' in entry:
        assert actual['bytes'] == entry['bytes'], str(p)
    return actual

def main():
    target = R / 'audit/DELIVERY_E.json'
    assert not target.exists(), 'Immutable final receipt already exists'
    mission = runpy.run_path(str(W / 'mission.py'))
    pr = mission['project']()
    task = next(t for t in pr['projection']['active'] if t['id'] == 'E')
    assert task['status'] == 'working' and task['lease']['owner'] == 'codex-video-web'
    check = mission['call']({'operation':'check', 'actor':{'id':'codex-video-web','kind':'agent'},
        'expected_revision':pr['receipt']['revision'], 'projection_sha256':pr['projection_sha256'],
        'task_id':'E', 'lease_id':task['lease']['id']})
    assert check['ready']
    manifest = load(R / 'PUBLIC_DELIVERY_V7.json')
    pointer = load(R.parent / 'PUBLIC_DELIVERY_V7.json')
    entries = manifest['public_files']
    assert len(entries) == 132 and len({e['path'] for e in entries}) == 132
    assert pointer['delivery'] == 'delivery_v7/PUBLIC_DELIVERY_V7.json'
    assert pointer['sha256'] == pin(R / 'PUBLIC_DELIVERY_V7.json')['sha256']
    assert pointer['public_files'] == [{**e,'path':'delivery_v7/'+e['path']} for e in entries]
    public = {e['path']:verify(e,R) for e in entries}
    assert not any('/private/' in n or '_silent' in n or '/jobs/' in n for n in public)
    validation = load(R / 'render/MEDIA_VALIDATION.json')
    delivery = load(R / 'render/DELIVERY_E.json')
    assert validation['status'] == 'PASS'
    assert len(validation['movies']) == 16 and len(validation['images']) == 25
    assert load(R / 'render/MEDIA_WATCH.json')['status'] == 'COMPLETE'
    for e in validation['movies'] + validation['images']:
        v = verify(e)
        rel = pathlib.Path(v['file']).relative_to(R).as_posix()
        if '/private/' not in rel:
            assert public[rel] == v
    render = load(R / 'RENDER_MANIFEST.json')
    assert render['version'] == manifest['version']
    assert render['source_sha256'] == manifest['source_sha256']
    jobs = []
    for e in delivery['source_jobs']:
        v = verify(e)
        metadata = load(pathlib.Path(v['file']))['metadata']
        film = metadata.get('film') if metadata['kind'] != 'loop' else None
        _, _, job, duration = M['read_job'](R,pathlib.Path(v['file']),film)
        kind = job['metadata']['kind']
        declared = render['jobs'][kind]
        assert declared['job_sha256'] == v['sha256']
        assert declared['source_files'] == job['source_files']
        assert len(job['source_files']) == 43
        jobs.append({'kind':kind,'job':v,'current_dependencies':43,'duration':duration})
    web = load(R / 'audit/WEB_BUILD.json')
    for entry in web['files']:
        verify(entry)
    for entry in delivery['web_files']:
        verify(entry)
    ui = load(W / 'FINAL_PLAYER_CHECKS.json')
    assert ui['status'] == 'PASS_OBSERVED_UI'
    receipts = [R/'PUBLIC_DELIVERY_V7.json', R.parent/'PUBLIC_DELIVERY_V7.json',
        R/'RENDER_MANIFEST.json', R/'PROVENANCE_PUBLIC.json', R/'render/DELIVERY_E.json',
        R/'render/MEDIA_VALIDATION.json', R/'render/MEDIA_WATCH.json',
        R/'render/ASSETS_AUDIT.json', R/'audit/WEB_BUILD.json',
        R/'audit/MEDIA_PIPELINE_BUILD.json', R/'audio/NARRATION_BUILD.json',
        W/'FINAL_PLAYER_CHECKS.json', R/'replay/REVIEW_CAPTION_WRAP_SUPPLEMENT_R1.json']
    evidence = [pin(p) for p in receipts]
    report = {'schema':'tgl.delivery.E.final.v1','status':'TECHNICAL_DELIVERY_READY_FOR_INDEPENDENT_REVIEW',
        'actor':'codex-video-web','task_id':'E','reference':str(W/'SESSION_REFERENCE.json'),
        'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'preflight':check,'public_files_verified':len(public),'public_manifest_pointer_verified':True,
        'version':manifest['version'],'source_sha256':manifest['source_sha256'],
        'media_validation':{'status':'PASS','media':16,'images':25,'full_decode_reused':True,'decode_rerun':False},
        'current_render_jobs':jobs,'final_web_files':[verify(e) for e in web['files']],
        'evidence':evidence,'measured_stage_times':delivery['stage_times'],
        'cost_scope':delivery['cost_scope'],'public_media':delivery['public_media'],
        'private_media':delivery['private_media'],'remote_api_calls_this_finalization':0,
        'source_edits_this_finalization':0,'integrated_gpu_measured':False,
        'background_budget_and_fallback':web['budget'],
        'limits':['Integrated GPU was not measured; fallback and recorded desktop checks have their stated scope.',
                  'UI observations belong to parent and focused review to C; their receipts are pinned.',
                  'This immutable technical receipt precedes mission submit; submission receipt is separate.',
                  'Independent acceptance and publication are not performed by this actor.'],
        'producer':pin(pathlib.Path(__file__))}
    raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    temporary=target.with_suffix('.json.tmp')
    with temporary.open('xb') as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
    assert temporary.read_bytes() == raw
    temporary.rename(target)
    print(json.dumps({'status':report['status'],'receipt':pin(target),'public_files':132,'media':16,'images':25}))

if __name__ == '__main__':
    main()
