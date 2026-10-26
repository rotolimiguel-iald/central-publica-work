"""Preserve the completed v400 media bytes; do not render or encode."""
from pathlib import Path
import hashlib, json, os, runpy, shutil, time

C = Path(__file__).resolve().parent
W = C.parent
V = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
M = runpy.run_path(str(V / 'cinema/media_v7.py'))
pin, sha, load, save = M['pin'], M['sha'], M['load'], M['jsave']

def main():
    mission = runpy.run_path(str(W / 'mission.py'))
    p = mission['project']()
    task = next(t for t in p['projection']['active'] if t['id'] == 'V401_MEDIA')
    check = mission['call']({'operation':'check', **mission['current']('codex-video-web'),
                           'task_id':'V401_MEDIA', 'lease_id':task['lease']['id'], 'max_chars':100000})
    assert check['ready']
    destination = C / 'MEDIA_V400_BACKUP.json'
    if destination.exists():
        old = load(destination)
        for row in old['files']:
            assert pin(Path(row['backup']['file'])) == row['backup']
        print(json.dumps({'status':'ALREADY_PRESERVED', 'files':len(old['files'])})); return
    started = time.perf_counter()
    validation = load(V / 'render/MEDIA_VALIDATION.json')
    assert validation['status'] == 'PASS' and validation['source'] == 'v400'
    assert len(validation['movies']) == 16 and len(validation['images']) == 25
    expected = {Path(p['file']):p for p in validation['movies'] + validation['images']}
    # Preserve reusable silent streams too, and their completed stage receipts.
    receipts = list((V / 'render/.pipeline').glob('*.json'))
    for receipt in receipts:
        stage = load(receipt)
        if stage.get('status') != 'COMPLETE': continue
        for item in stage.get('outputs', []):
            path = Path(item['file'])
            if path.is_relative_to(V / 'render/private') and '_silent.' in path.name:
                expected[path] = item
    for item in expected.values():
        p = Path(item['file'])
        assert p.stat().st_size == item['bytes'] and sha(p) == item['sha256'], str(p)
    extras = receipts + list((V / 'render').glob('*.json'))
    extras += [V/'audit/DELIVERY_E.json', V/'cinema/studio.mjs', V/'make_v7.py',
               V/'cinema/media_v7.py', V/'cinema/mp4_metrics.py']
    for path in extras:
        if path.is_file(): expected.setdefault(path, pin(path))
    need = sum(x['bytes'] for x in expected.values())
    assert shutil.disk_usage(C).free > need + (2 << 30), 'Insufficient backup space'
    files = []
    for path, item in sorted(expected.items()):
        target = C / 'media_v400_history' / path.relative_to(V)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert target.stat().st_size == item['bytes'] and sha(target) == item['sha256']
        else:
            temporary = target.with_name(target.name + '.partial')
            assert not temporary.exists(), 'Unreconciled partial backup: ' + str(temporary)
            with path.open('rb') as src, temporary.open('xb') as dst:
                shutil.copyfileobj(src, dst, 4 << 20); dst.flush(); os.fsync(dst.fileno())
            assert temporary.stat().st_size == item['bytes'] and sha(temporary) == item['sha256']
            assert sha(path) == item['sha256'], 'Source changed during backup'
            os.replace(temporary, target)
        files.append({'original':{k:item[k] for k in ('file','bytes','sha256')}, 'backup':pin(target)})
    parent = C/'baseline_manifest_v400'
    manifest = load(parent/'PUBLIC_DELIVERY_V7.json')
    assert manifest['source'] == 'v400'
    metadata = []
    for path in (V/'cinema/studio.mjs', V/'make_v7.py'):
        text = path.read_text(encoding='utf-8')
        assert 'v400' not in text.lower(), str(path)
        assert 'seal_version' in text and 'seal_pin' in text
        metadata.append(pin(path))
    save(destination, {'status':'PASS_PRESERVED_BYTES', 'source':'v400',
         'source_sha256':validation['source_sha256'], 'files':files,
         'media_count':16, 'image_count':25, 'total_bytes':need,
         'public_baseline':[pin(parent/n) for n in ('MANIFEST.json','PUBLIC_DELIVERY_V7.json','RENDER_MANIFEST.json','ROOT_PUBLIC_DELIVERY_V7.json')],
         'metadata_files_unchanged':metadata, 'preflight':check,
         'elapsed_seconds':time.perf_counter()-started,
         'scope':'Byte backup only. No FFmpeg, browser, TTS, source/data/audio write or public finalization.'})
    print(json.dumps({'status':'PASS_PRESERVED_BYTES','files':len(files),'bytes':need,'seconds':time.perf_counter()-started}))

if __name__ == '__main__': main()
