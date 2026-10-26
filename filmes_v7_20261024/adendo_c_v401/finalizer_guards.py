"""Read-only receipt bindings for the v401 finalizers; never build or render."""
from pathlib import Path
import hashlib
import json
import math


def read(path): return json.loads(Path(path).read_bytes())
def sha(path):
    with Path(path).open('rb') as stream: return hashlib.file_digest(stream, 'sha256').hexdigest()


def verify_pin(entry, expected_path=None):
    path = Path(entry.get('path', entry.get('file', '')))
    assert path.is_file(), f'Missing pinned file: {path}'
    if expected_path is not None:
        assert path.resolve() == Path(expected_path).resolve(), f'Wrong pinned path: {path}'
    assert path.stat().st_size == entry['bytes'] and sha(path) == entry['sha256'], f'Stale pin: {path}'
    return path


def verify_embedded_pins(value):
    if isinstance(value, dict):
        if ('path' in value or 'file' in value) and 'sha256' in value and 'bytes' in value:
            verify_pin(value)
        for child in value.values(): verify_embedded_pins(child)
    elif isinstance(value, list):
        for child in value: verify_embedded_pins(child)


def require_current(receipt, source, statuses):
    assert receipt['status'] in statuses, f"Incomplete receipt: {receipt.get('status')}"
    assert receipt['source'] == 'v401' and receipt['source_sha256'] == source, 'Stale receipt source'


def validate_frozen_data(c, v, n, require_parent=True):
    capture = read(c / 'SOURCE_CAPTURE.json')
    verify_pin(capture['canonical_seal'], n / 'um_absoluto_selo.json')
    seal = read(n / 'um_absoluto_selo.json'); hud = read(v / 'data/hud.json')
    source = capture['source_sha256']
    assert seal['um_version'] == hud['seal_version'] == capture['source'] == 'v401'
    assert seal['sha256']['um.py'] == hud['seal_pin'] == source
    assert hud['seal_timestamp'] == hud['selo_timestamp'] == seal['timestamp']
    for name in ['um.py', 'um_absoluto.json', 'tgl_kernel_proof_manifest.json']:
        assert sha(n / name) == sha(v / 'source' / name) == seal['sha256'][name], name
    ready = read(c / 'DATA_READY.json'); comparison = read(c / 'NUMERIC_COMPARISON.json')
    require_current(ready, source, {'DATA_READY'}); require_current(comparison, source, {'PASS'})
    verify_pin(ready['comparison'], c / 'NUMERIC_COMPARISON.json')
    verify_pin(ready['integration'], c / 'INTEGRATION.json')
    verify_pin(ready['seal'], v / 'source/um_absoluto_selo.json')
    assert ready['seal']['sha256'] == capture['canonical_seal']['sha256']
    assert ready['unexpected_scientific_differences'] == 0 and comparison['unexpected_differences'] == []
    assert {Path(x['path']).name for x in ready['data_files']} == {'hud.json','frames.json','scene.json','PROVENANCE_PUBLIC.json','STDOUT_LINES.json','MANIFEST.json'}
    for entry in ready['data_files']: verify_pin(entry, v / 'data' / Path(entry['path']).name)
    for entry in ready['source_files']: verify_pin(entry, v / 'source' / Path(entry['path']).name)
    verify_pin(ready['root_provenance'], v / 'PROVENANCE_PUBLIC.json')
    for row in comparison['files']:
        target = v / 'data' / row['file']
        assert sha(target) == row['after']['sha256'] and target.stat().st_size == row['after']['bytes']
        assert row['unexpected'] == []
    assert (v / 'PROVENANCE_PUBLIC.json').read_bytes() == (v / 'data/PROVENANCE_PUBLIC.json').read_bytes()
    if require_parent:
        parent = read(c / 'PARENT_NUMERIC_REVIEW.json')
        require_current(parent, source, {'PASS_WITH_SCOPE'})
        assert parent['unexpected_differences'] == [] and parent['data_ready_sha256'] == sha(c / 'DATA_READY.json')
        for row in parent['files']:
            assert sha(v / 'data' / row['file']) == row['current_sha256'], row['file']
    return source


def validate_replay(v, source):
    manifest = read(v / 'replay/replay-manifest.json')
    assert manifest['source']['version'] == 'v401' and manifest['source']['sha256'] == source
    assert manifest['core_sha256'] == sha(v / 'source/um_absoluto.json')
    assert manifest['seal']['sha256'] == sha(v / 'source/um_absoluto_selo.json')
    for entry in manifest['assets'].values():
        path = v / 'replay' / entry['url']
        assert path.resolve().is_relative_to(v.resolve())
        verify_pin({'path':str(path), 'sha256':entry['sha256'], 'bytes':entry['bytes']})
    for name in ['TEST_OFFLINE.json', 'TEST_BROWSER.json']:
        receipt = read(v / 'replay' / name)
        require_current(receipt, source, {'PASS'})
        assert receipt['manifest_sha256'] == sha(v / 'replay/replay-manifest.json')
    offline = read(v / 'replay/TEST_OFFLINE.json'); browser = read(v / 'replay/TEST_BROWSER.json')
    assert offline['tests'] == 13 and offline['failures'] == offline['errors'] == 0
    checks = {x['name']: x for x in browser['checks']}
    required = {'browser_numeric_conformance','numerical_negative_controls','excerpt_tamper_visible','hud_tamper_visible','missing_runtime_visible','no_external_requests'}
    assert required <= checks.keys() and all(x['ok'] is True for x in checks.values())
    assert browser['external_requests'] == [] and browser['result']['status'] == 'OK'
    assert len(browser['result']['rows']) == 61
    for row in browser['result']['rows']:
        assert row['ok'] is True and math.isfinite(row['residual']) and math.isfinite(row['atol'])
        assert 0 <= row['residual'] <= row['atol']
    full = read(v / 'replay/DELIVERY_ADENDO_C_V401.json')
    assert full['source'] == 'v401' and full['source_sha256'] == source
    fixed = read(v / 'replay/DELIVERY_C.json')
    assert fixed['source'] == 'v401' and fixed['source_sha256'] == source
    assert fixed['full_receipt']['sha256'] == sha(v / 'replay/DELIVERY_ADENDO_C_V401.json')
    assert fixed['public_files'] == full['public_files']
    for entry in full['public_file_pins']:
        verify_pin({**entry, 'path':str(v / entry['path'])})


def validate_audio(c, v, source):
    ready = read(c / 'AUDIO_READY.json'); audio = read(v / 'audit/DELIVERY_D_V401.json')
    require_current(ready, source, {'AUDIO_READY'})
    require_current(audio, source, {'PASS_BUILDER_READY_FOR_INDEPENDENT_REVIEW'})
    verify_pin(ready['receipt'], v / 'audit/DELIVERY_D_V401.json')
    assert ready['counts'] == audio['counts']
    expected = {'unique_units':60, 'subtitle_files':26, 'wav_aac_files':8, 'new_v401_units':4, 'reused_v400_units':56}
    assert all(audio['counts'][key] == value for key,value in expected.items())
    assert audio['plan_current'] is True and audio['plan_sha256'] == ready['plan_sha256']
    verify_pin(audio['data_ready'], c / 'DATA_READY.json')
    for field in ['plan', 'builder', 'templates', 'build']: verify_pin(audio[field])
    for field in ['media', 'subtitles', 'timelines']:
        assert ready[field] == audio[field]
        verify_embedded_pins(audio[field])
    build = read(verify_pin(audio['build'], v / 'audio/NARRATION_BUILD.json'))
    assert build['status'] == 'COMPLETED' and not build.get('pending') and not build.get('tts_inflight')
    assert build['plan_sha256'] == audio['plan_sha256']
    return audio


def validate_public_pointer(manifest, pointer, v):
    assert pointer['delivery'] == 'delivery_v7/PUBLIC_DELIVERY_V7.json'
    assert pointer['sha256'] == sha(v / 'PUBLIC_DELIVERY_V7.json')
    expected = [{**entry, 'path':'delivery_v7/' + entry['path']} for entry in manifest['public_files']]
    assert pointer['public_files'] == expected, 'Root public file list differs from manifest'
    for entry in manifest['public_files']:
        path = v / entry['path']
        assert not Path(entry['path']).is_absolute() and path.resolve().is_relative_to(v.resolve())
        parts = [part.lower() for part in path.relative_to(v).parts]
        assert not any(part in {'private','source','cache','voice_sample','voice_test'} for part in parts)
        assert not any(token in path.name.lower() for token in ['.bak_', '.tmp', 'voice_sample', 'voice_test'])


def validate_final_receipts(c, v, source):
    final = read(c / 'FINAL_MAKE.json'); media = read(v / 'render/MEDIA_VALIDATION.json')
    player = read(c / 'FINAL_PLAYER_V401.json'); delivery = read(c / 'DELIVERY_E.json')
    require_current(final, source, {'PASS'}); require_current(media, source, {'PASS'})
    require_current(player, source, {'PASS_OBSERVED_UI'})
    require_current(delivery, source, {'MEDIA_VALIDATED_AWAITING_PARENT_PUBLIC_MANIFEST','TECHNICAL_DELIVERY_READY_FOR_INDEPENDENT_REVIEW'})
    assert final['returncode'] == 0 and final['canonical_unchanged'] is True
    verify_pin(final['builder'], v / 'make_v7.py')
    expected = {p.resolve() for p in [v/'PUBLIC_DELIVERY_V7.json',v/'RENDER_MANIFEST.json',v.parent/'PUBLIC_DELIVERY_V7.json']}
    assert {verify_pin(entry).resolve() for entry in final['manifests']} == expected
    verify_pin(delivery['validation'], v / 'render/MEDIA_VALIDATION.json')
    verify_embedded_pins(player)
    manifest = read(v / 'RENDER_MANIFEST.json')
    assert manifest['source'] == manifest['version'] == 'v401' and manifest['source_sha256'] == source
    assert set(manifest['jobs']) == set(delivery['jobs']) == {'film1','film2','loop'}
    for kind, entry in delivery['jobs'].items():
        job = read(verify_pin(entry)); row = manifest['jobs'][kind]
        assert row['job_sha256'] == entry['sha256']
        for field in ['metadata','render','source_files']: assert row[field] == job[field]
        assert row['encoded_sha256'] == job['sha256']
