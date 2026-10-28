"""Preserve v401 bytes before any v402 capture/export. No encode or renderer."""
from pathlib import Path
import hashlib, json, os, runpy, shutil, time

E = Path(__file__).resolve().parent
W = E.parent
V = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
OLD = W / 'adendo_c_v401'
M = runpy.run_path(str(V / 'cinema/media_v7.py'))
pin, sha, load = M['pin'], M['sha'], M['load']


def immutable(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        assert path.read_bytes() == raw, 'Immutable destination differs: ' + str(path)
        return
    tmp = path.with_name(path.name + '.partial')
    assert not tmp.exists(), 'Unreconciled partial: ' + str(tmp)
    with tmp.open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    os.rename(tmp, path)


def copy_verified(source, destination, expected):
    assert pin(source) == expected, 'Source changed: ' + str(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        tmp = destination.with_name(destination.name + '.partial')
        assert not tmp.exists(), 'Unreconciled partial: ' + str(tmp)
        with source.open('rb') as src, tmp.open('xb') as dst:
            shutil.copyfileobj(src, dst, 4 << 20); dst.flush(); os.fsync(dst.fileno())
        assert tmp.stat().st_size == expected['bytes'] and sha(tmp) == expected['sha256']
        assert pin(source) == expected, 'Source changed during backup'
        os.rename(tmp, destination)
    assert destination.stat().st_size == expected['bytes'] and sha(destination) == expected['sha256']
    return {'original': expected, 'backup': pin(destination)}


def main():
    mission = runpy.run_path(str(W / 'mission.py')); p = mission['project']()
    task = next(t for t in p['projection']['active'] if t['id'] == 'V402_MEDIA')
    check = mission['call']({'operation':'check', 'actor':{'id':'codex-video-web','kind':'agent'},
        'task_id':'V402_MEDIA','lease_id':task['lease']['id'],'expected_revision':p['receipt']['revision'],
        'projection_sha256':p['projection_sha256'],'max_chars':100000})
    assert check['ready']
    output = E / 'MEDIA_V401_BACKUP.json'
    if output.exists():
        report = load(output)
        for row in report['files']: assert pin(Path(row['backup']['file'])) == row['backup']
        for entry in report['public_baseline']: assert pin(Path(entry['file'])) == entry
        print(json.dumps({'status':'ALREADY_PRESERVED','files':len(report['files'])})); return
    start = time.perf_counter()
    validation = load(V / 'render/MEDIA_VALIDATION.json')
    assert validation['status'] == 'PASS' and validation['source'] == 'v401'
    assert len(validation['movies']) == 16 and len(validation['images']) == 25
    expected, recovered = {}, {}
    def add(path, known=None):
        path = Path(path); entry = pin(path)
        if known:
            assert all(entry[k] == known[k] for k in ('bytes','sha256')), 'Baseline pin differs: ' + str(path)
        expected[path] = entry
    for item in validation['movies'] + validation['images']: add(item['file'], item)
    # Silent streams and their receipts permit later byte-verifiable recovery.
    receipts = list((V/'render/.pipeline').glob('*.json'))
    for receipt in receipts:
        stage = load(receipt)
        if stage.get('status') != 'COMPLETE': continue
        for item in stage.get('outputs', []):
            path = Path(item['file'])
            if path.is_relative_to(V/'render/private') and '_silent.' in path.name: add(path, item)
    # Preserve exactly the captured inputs used by the accepted v401 media.
    watch = load(OLD/'MEDIA_WATCH.json'); assert watch['status'] == 'COMPLETE'
    for item in watch['completed'].values():
        add(item['file'], item); job = load(Path(item['file']))
        raw = Path(job['file']); raw = raw if raw.is_absolute() else V/'cinema/render/jobs'/raw
        add(raw, job)
    assets = load(V/'render/ASSETS_AUDIT.json'); assert assets['source'] == 'v401'
    for stage in assets['stages']:
        for item in stage['inputs']:
            if Path(item['file']).is_relative_to(V/'cinema/render/stills'): add(item['file'], item)
    extras = receipts + list((V/'render').glob('*.json'))
    extras += list((V/'web').glob('*')) + list((V/'slides').glob('*'))
    extras += [V/'audit/DELIVERY_E.json',V/'cinema/studio.mjs',V/'make_v7.py',
               V/'cinema/media_v7.py',V/'cinema/mp4_metrics.py',V/'cinema/render_sources.py']
    for path in extras:
        if path.is_file() and '.bak_' not in path.name: add(path)
    trust_receipt = E/'WEB_TRUST_INTEGRATION.json'
    if trust_receipt.exists():
        trust = load(trust_receipt)
        assert trust['status'] == 'PASS' and trust['source'] == 'v402'
        target = V/'web/replay-trust.mjs'
        saved = Path(trust['backup']['path'])
        for field in ('bytes','sha256'):
            assert pin(saved)[field] == trust['backup'][field] == trust['before'][field]
            assert pin(target)[field] == trust['installed'][field]
        expected[target] = {'file':str(target),'bytes':trust['before']['bytes'],'sha256':trust['before']['sha256']}
        recovered[target] = saved
    # Historical receipts are copied, not repaired/relabelled as v402.
    for name in ('DELIVERY_E.json','MEDIA_FINAL_BINDING.json','MEDIA_SUBMIT_RESULT.json',
                 'MEDIA_VALIDATION.json','MEDIA_WATCH.json','FINAL_MAKE.json',
                 'MEDIA_RENDER_MANIFEST_PRE_FINAL.json','FINAL_RENDER_MANIFEST_LINK.json',
                 'MEDIA_V401_BASELINE.json','MEDIA_SCHEMA_FIX.json','MEDIA_LIVENESS_R1.json'):
        add(OLD/name)
    need = sum(x['bytes'] for x in expected.values())
    assert shutil.disk_usage(E).free > need + (4 << 30), 'Insufficient free space for byte backup'
    manifest_dir = E/'baseline_manifest_v401'; rows = []
    for path, name in ((V.parent/'PUBLIC_DELIVERY_V7.json','ROOT_PUBLIC_DELIVERY_V7.json'),
                       (V/'PUBLIC_DELIVERY_V7.json','PUBLIC_DELIVERY_V7.json'),
                       (V/'RENDER_MANIFEST.json','RENDER_MANIFEST.json')):
        assert load(path)['source'] == 'v401'
        row = copy_verified(path, manifest_dir/name, pin(path))
        rows.append({'origin':str(path),'copy':str(manifest_dir/name),'sha256':row['backup']['sha256']})
    immutable(manifest_dir/'MANIFEST.json',(json.dumps(rows,ensure_ascii=False,indent=2)+'\n').encode())
    files = []
    for path, item in sorted(expected.items()):
        relative = path.relative_to(V) if path.is_relative_to(V) else Path('adendo_c_v401')/path.relative_to(OLD)
        source = recovered.get(path,path)
        row = copy_verified(source,E/'media_v401_history'/relative,pin(source) if path in recovered else item)
        if path in recovered:
            row['recovered_from'] = pin(source); row['original'] = item
        files.append(row)
    assert sum(1 for p in expected if p.is_relative_to(V/'cinema/render/stills') and p.suffix == '.png') == 22
    report = {'status':'PASS_PRESERVED_BYTES','source':'v401','source_sha256':validation['source_sha256'],
        'target_source':'v402','media_count':16,'image_count':25,'captured_stills':22,'captured_jobs':3,
        'files':files,'total_bytes':need,'elapsed_seconds':time.perf_counter()-start,'preflight':check,
        'public_baseline':[pin(manifest_dir/n) for n in ('MANIFEST.json','PUBLIC_DELIVERY_V7.json','RENDER_MANIFEST.json','ROOT_PUBLIC_DELIVERY_V7.json')],
        'known_failure':pin(E/'MEDIA_PREPARE_FAILURE_R0.json') if (E/'MEDIA_PREPARE_FAILURE_R0.json').exists() else None,
        'concurrent_web_update':pin(trust_receipt) if trust_receipt.exists() else None,
        'scope':'Byte-exact copies of validated media, silent streams, capture inputs, stage receipts, web/slides and manifest/history. No render, encode, audio/data/source write or finalization.'}
    immutable(output,(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps({'status':report['status'],'files':len(files),'bytes':need,'seconds':report['elapsed_seconds']}))


if __name__ == '__main__': main()
