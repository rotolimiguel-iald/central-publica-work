"""Read-only binding of completed capture jobs, worker outputs and observed UI."""
from pathlib import Path
import runpy
from finalizer_guards import read, sha, file_pin, verify_pin, verify_embedded_pins, require_current

KINDS = {'film1':224, 'film2':360, 'loop':16}

def load_make(v):
    return runpy.run_path(str(v/'make_v7.py'))

def validate_worker_jobs(c, v, source):
    assert not (c/'MEDIA_V404_WORKER.lock').exists(), 'Worker is still active'
    assert not list((v/'render/.pipeline').glob('*.lock')), 'Encoding stage is still active'
    watch = read(c/'MEDIA_WATCH.json'); delivery = read(c/'DELIVERY_E.json')
    require_current(watch, source, {'COMPLETE'})
    require_current(delivery, source, {'MEDIA_VALIDATED_AWAITING_PARENT_PUBLIC_MANIFEST'})
    baseline = read(verify_pin(delivery['baseline'], c/'MEDIA_V404_BASELINE.json'))
    intent = read(c/'RENDER_INTENT.json')
    for value in (baseline, intent):
        assert value['source'] == 'v404' and value['source_sha256'] == source
    make = load_make(v); closure = make['collect_render_sources'](v)
    assert len(closure) == 43 and closure == baseline['render_closure'] == intent['render_closure']
    assert set(delivery['jobs']) == set(watch['completed']) == set(KINDS)
    assert delivery['jobs'] == watch['completed'], 'Worker and delivery job identities diverged'
    manifest = read(v/'RENDER_MANIFEST.json')
    assert manifest['source'] == 'v404' and manifest['source_sha256'] == source
    assert set(manifest['jobs']) == set(KINDS)
    rows = {}
    for kind, seconds in KINDS.items():
        path = verify_pin(delivery['jobs'][kind])
        assert path.parent.resolve() == (v/'cinema/render/jobs').resolve()
        job = read(path); meta = job['metadata']; raw = path.with_suffix('.h264')
        assert Path(job['file']).resolve() == raw.resolve()
        verify_pin({'path':str(raw), 'sha256':job['sha256'], 'bytes':job['bytes']})
        assert meta['kind'] == kind and meta['source'] == 'v404' and meta['source_sha256'] == source
        assert meta['fps'] == 60 and meta['duration'] == seconds
        assert meta['total'] == job['render']['encoded'] == seconds*60
        assert (meta['width'],meta['height']) == ((1920,1080) if kind == 'loop' else (3840,2160))
        assert job['source_files'] == closure
        candidates = []
        for other in path.parent.glob(kind+'_*.json'):
            if '.progress.' in other.name: continue
            data = read(other); metadata = data.get('metadata', {})
            if metadata.get('source') == 'v404' or metadata.get('source_sha256') == source or data.get('source_files') == closure:
                candidates.append(other.resolve())
        assert candidates == [path.resolve()], 'Alternate or duplicate current capture'
        selected = make['find_job'](kind)
        assert selected is not None and selected.resolve() == path.resolve(), 'Make would select a different capture'
        expected = {'job_sha256':sha(path), 'metadata':meta, 'encoded_sha256':job['sha256'],
                    'render':job['render'], 'source_files':job['source_files']}
        assert manifest['jobs'][kind] == expected, 'Manifest does not bind the worker capture'
        rows[kind] = {'receipt':file_pin(path), 'stream':file_pin(raw)}
    return {'status':'PASS_COMPLETED_WORKER_JOB_BINDING', 'source':'v404', 'source_sha256':source,
            'jobs':rows, 'render_closure':closure, 'baseline':file_pin(c/'MEDIA_V404_BASELINE.json'),
            'intent':file_pin(c/'RENDER_INTENT.json'), 'watch':file_pin(c/'MEDIA_WATCH.json'),
            'delivery':file_pin(c/'DELIVERY_E.json'), 'builder':file_pin(v/'make_v7.py')}

def validate_observation_bindings(c, v, source, completed):
    capture = read(c/'PARENT_CAPTURE_AUDIT.json'); ui = read(c/'FINAL_PLAYER_V404.json')
    require_current(capture, source, {'PASS_WITH_SCOPE'})
    require_current(ui, source, {'PASS_OBSERVED_UI'})
    verify_embedded_pins(capture); verify_embedded_pins(ui)
    assert capture['render_closure'] == completed['render_closure']
    assert set(capture['jobs']) == set(completed['jobs']) == set(KINDS)
    for kind, row in completed['jobs'].items():
        for field in ('receipt','stream'):
            actual = verify_pin(capture['jobs'][kind][field])
            expected = verify_pin(row[field])
            assert actual.resolve() == expected.resolve()
            assert capture['jobs'][kind][field]['sha256'] == row[field]['sha256']
    binding = ui['artifact_binding']
    assert binding['jobs'] == completed['jobs'], 'UI observations belong to different captures'
    paths = {verify_pin(p).resolve() for p in binding['manifests']}
    assert len(binding['manifests']) == 3 and paths == {
        (v/'PUBLIC_DELIVERY_V7.json').resolve(), (v/'RENDER_MANIFEST.json').resolve(),
        (v.parent/'PUBLIC_DELIVERY_V7.json').resolve()}
    public = read(v/'PUBLIC_DELIVERY_V7.json')
    published = {(v/e['path']).resolve():e for e in public['public_files']}
    observed = {verify_pin(p).resolve():p for p in binding['media']}
    assert len(observed) >= 4, 'Both films and both audio languages must be bound'
    for path, entry in observed.items():
        assert path.is_relative_to(v.resolve()) and path in published and path.suffix == '.mp4'
        assert (entry['sha256'],entry['bytes']) == (published[path]['sha256'],published[path]['bytes'])
    assert set(ui['observed_media']) == {'film1_en','film1_pt-BR','film2_en','film2_pt-BR'}
    assert {Path(x).resolve() for x in ui['observed_media'].values()} == set(observed)
    for label, value in ui['observed_media'].items():
        film, lang = label.split('_',1)
        suffix = '_pt-BR' if lang == 'pt-BR' else ''
        assert Path(value).resolve() == (v/'render'/f"filme{film[-1]}_1080p{suffix}.mp4").resolve()
    return {'status':'PASS_OBSERVATION_ARTIFACT_BINDING', 'capture':file_pin(c/'PARENT_CAPTURE_AUDIT.json'),
            'ui':file_pin(c/'FINAL_PLAYER_V404.json'), 'jobs':completed['jobs'], 'observed_media':binding['media']}
