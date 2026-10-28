"""Receipt guards and immutable manifest snapshot helpers; never build or render."""
from pathlib import Path
import hashlib
import json
import math
import os


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
    assert receipt['source'] == 'v402' and receipt['source_sha256'] == source, 'Stale receipt source'


def file_pin(path):
    return {'path':str(path), 'sha256':sha(path), 'bytes':path.stat().st_size}


def compare_render_manifests(before, after, source):
    """Ignore only a root worker annotation and JSON whitespace/key ordering."""
    for item in [before, after]:
        assert item['source'] == item['version'] == 'v402' and item['source_sha256'] == source
    assert 'adendo_worker' in before, 'Worker-stage annotation missing'
    assert 'adendo_worker' not in after or after['adendo_worker'] == before['adendo_worker'], 'Unexpected worker annotation change'
    def canonical(value):
        return json.dumps({k:v for k,v in value.items() if k != 'adendo_worker'},
                          sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()
    old = canonical(before); new = canonical(after)
    assert old == new, 'Render manifest changed beyond root adendo_worker/JSON serialization'
    return {'equal':True, 'ignored_root_fields':['adendo_worker'], 'numeric_tolerance':0,
            'canonical_sha256':hashlib.sha256(old).hexdigest(),
            'worker_annotation_removed':'adendo_worker' not in after}


def preserve_render_manifest_before_make(c, v, source):
    """Called by the parent only after COMPLETE, before invoking make."""
    watch = c/'MEDIA_WATCH.json'; delivery_path = c/'DELIVERY_E.json'
    require_current(read(watch), source, {'COMPLETE'})
    delivery = read(delivery_path)
    require_current(delivery, source, {'MEDIA_VALIDATED_AWAITING_PARENT_PUBLIC_MANIFEST','TECHNICAL_DELIVERY_READY_FOR_INDEPENDENT_REVIEW'})
    original = delivery['render_manifest']; current = v/'RENDER_MANIFEST.json'
    assert Path(original.get('path', original.get('file'))).resolve() == current.resolve()
    snapshot = c/'MEDIA_RENDER_MANIFEST_PRE_FINAL.json'
    if snapshot.exists():
        # An interrupted finalizer may have already rewritten V; never replace the original snapshot.
        assert snapshot.stat().st_size == original['bytes'] and sha(snapshot) == original['sha256'], 'Snapshot differs from original E pin'
        compare_render_manifests(read(snapshot), read(current), source)
    else:
        verify_pin(original, current)
        raw = current.read_bytes()
        assert len(raw) == original['bytes'] and hashlib.sha256(raw).hexdigest() == original['sha256']
        tmp = snapshot.with_suffix('.tmp')
        with tmp.open('xb') as stream: stream.write(raw)
        assert tmp.read_bytes() == raw; os.replace(tmp, snapshot)
    stage = {'delivery_e':file_pin(delivery_path), 'media_watch':file_pin(watch),
             'original_e_manifest':original, 'snapshot':file_pin(snapshot)}
    assert read(delivery_path)['render_manifest'] == original
    compare_render_manifests(read(snapshot), read(snapshot), source)
    return stage


def build_render_manifest_link(c, v, source, stage):
    """Return the link payload after make; no writes or build operations."""
    verify_pin(stage['delivery_e'], c/'DELIVERY_E.json')
    verify_pin(stage['media_watch'], c/'MEDIA_WATCH.json')
    snapshot = verify_pin(stage['snapshot'], c/'MEDIA_RENDER_MANIFEST_PRE_FINAL.json')
    original = read(c/'DELIVERY_E.json')['render_manifest']
    assert stage['original_e_manifest'] == original
    assert Path(original.get('path', original.get('file'))).resolve() == (v/'RENDER_MANIFEST.json').resolve()
    assert sha(snapshot) == original['sha256'] and snapshot.stat().st_size == original['bytes']
    final = v/'RENDER_MANIFEST.json'
    comparison = compare_render_manifests(read(snapshot), read(final), source)
    binding = {key:stage[key] for key in ['delivery_e','media_watch','original_e_manifest','snapshot']}
    return {'status':'PASS_SEMANTIC_MANIFEST_TRANSITION', 'source':'v402', 'source_sha256':source,
            **binding, 'final_manifest':file_pin(final), 'builder':file_pin(v/'make_v7.py'),
            'comparison':comparison,
            'scope':'Original E pin refers to the preserved byte-exact worker-stage snapshot. Final manifest may only remove root adendo_worker and change JSON serialization. E receipt is not rewritten; jobs, parameters, source files and numbers remain exact.'}


def validate_render_manifest_link(c, v, source):
    link = read(c/'FINAL_RENDER_MANIFEST_LINK.json')
    require_current(link, source, {'PASS_SEMANTIC_MANIFEST_TRANSITION'})
    verified = build_render_manifest_link(c, v, source, link)
    assert link == verified, 'Manifest transition link no longer describes current artifacts'
    verify_pin(link['builder'], v/'make_v7.py')
    return link


def validate_frozen_data(c, v, n, require_parent=True):
    capture = read(c / 'SOURCE_CAPTURE.json')
    verify_pin(capture['canonical_seal'], n / 'um_absoluto_selo.json')
    seal = read(n / 'um_absoluto_selo.json'); hud = read(v / 'data/hud.json')
    source = capture['source_sha256']
    assert seal['um_version'] == hud['seal_version'] == capture['source'] == 'v402'
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
    assert manifest['source']['version'] == 'v402' and manifest['source']['sha256'] == source
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
    full = read(v / 'replay/DELIVERY_ADENDO_E_V402.json')
    assert full['source'] == 'v402' and full['source_sha256'] == source
    fixed = read(v / 'replay/DELIVERY_C.json')
    assert fixed['source'] == 'v402' and fixed['source_sha256'] == source
    assert fixed['full_receipt']['sha256'] == sha(v / 'replay/DELIVERY_ADENDO_E_V402.json')
    assert fixed['public_files'] == full['public_files']
    for entry in full['public_file_pins']:
        verify_pin({**entry, 'path':str(v / entry['path'])})


def narration_units(plan):
    """Recompute the same content-addressed unit keys from reviewed public text."""
    def encoded(value):
        return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')
    body = {k:value for k,value in plan.items() if k != 'plan_sha256'}
    assert hashlib.sha256(encoded(body)).hexdigest() == plan['plan_sha256'], 'Narration plan digest mismatch'
    units = {}
    for film_name, film in plan['films'].items():
        for segment in film['segments']:
            for index, cue in enumerate(segment['cues']):
                for language, voice in plan['voices'].items():
                    text = cue[language]
                    key = hashlib.sha256(encoded({'voice':voice, 'text':text, 'rate':plan['rate'], 'format':plan['format']})).hexdigest()
                    unit = units.setdefault(key, {'key':key, 'voice':voice, 'language':language,
                        'text_sha256':hashlib.sha256(text.encode('utf-8')).hexdigest(), 'occurrences':[]})
                    unit['occurrences'].append({'film':film_name, 'segment':segment['key'], 'cue_index':index})
    return units


def validate_audio_units(c, audio, plan):
    assert len(audio['media']) == 8 and len(audio['subtitles']) == 26, 'Incomplete two-film bilingual/four-subtitle delivery'
    for field in ['media', 'subtitles']:
        paths = [str(Path(row['path']).resolve()) for row in audio[field]]
        assert len(paths) == len(set(paths)), 'Duplicate '+field+' entries'
    current = narration_units(plan)
    baseline = read(verify_pin(audio['baseline'], c/'baseline_audio_v401/BASELINE.json'))
    candidates = [row for row in baseline['files'] if Path(row['original']['path']).name == 'NARRATION_PLAN_v401_final.json']
    assert len(candidates) == 1
    old_pin = candidates[0]['backup']
    old = narration_units(read(verify_pin(old_pin)))
    assert old_pin['sha256'] == candidates[0]['original']['sha256']
    reused = set(current) & set(old)
    expected = {'unique_units':len(current), 'cue_occurrences':sum(len(u['occurrences']) for u in current.values()),
                'new_v402_units':len(set(current)-reused), 'reused_v401_units':len(reused),
                'subtitle_files':len(audio['subtitles']), 'wav_aac_files':len(audio['media'])}
    assert audio['counts'] == expected, 'Audio counts differ from actual current/baseline plans'
    bindings = audio['cache_bindings']
    assert len(bindings) == len(current) and {b['key'] for b in bindings} == set(current)
    for binding in bindings:
        unit = current[binding['key']]
        for field in ['voice','language','text_sha256','occurrences']:
            assert binding[field] == unit[field], 'Stale audio unit '+field
        assert binding['unchanged_from_v401'] == (binding['key'] in reused)
        verify_pin(binding['audio'])
        receipt = read(verify_pin(binding['receipt']))
        assert receipt['state'] == 'completed' and receipt['key'] == binding['key']
        assert receipt['voice'] == unit['voice'] and receipt['text_sha256'] == unit['text_sha256']
        assert receipt['audio_sha256'] == binding['audio']['sha256']
    return expected


def validate_formula_review(c, audio, source):
    review = read(c/'FORMULA_NARRATION_PARENT_REVIEW.json')
    require_current(review, source, {'PASS_APPROVED_FOR_PUBLIC_TTS'})
    assert review['plan_sha256'] == audio['plan_sha256'], 'Formula review approves another plan'
    assert review['plan'] == audio['plan'] and review['templates'] == audio['templates'], 'Reviewed text pins differ from generated text'
    for field in ['plan','templates','formula_review','operator_order','corrections_order']:
        verify_pin(review[field])
    verify_pin(review['formula_review'], c/'FORMULA_NARRATION_REVIEW.json')
    verify_pin(review['operator_order'], c/'OPERATOR_FORMULA_NARRATION.txt')
    assert review['formula_translation_checked'] is True and review['adendo_d_checked'] is True
    return review


def validate_audio(c, v, source):
    ready = read(c / 'AUDIO_READY.json'); audio = read(v / 'audit/DELIVERY_D_V402.json')
    require_current(ready, source, {'AUDIO_READY'})
    require_current(audio, source, {'PASS_BUILDER_READY_FOR_INDEPENDENT_REVIEW'})
    verify_pin(ready['receipt'], v / 'audit/DELIVERY_D_V402.json')
    assert ready['counts'] == audio['counts']
    assert audio['plan_current'] is True and audio['plan_sha256'] == ready['plan_sha256']
    verify_pin(audio['data_ready'], c / 'DATA_READY.json')
    for field in ['plan', 'builder', 'templates', 'build']: verify_pin(audio[field])
    plan = read(audio['plan']['path'])
    assert plan['plan_sha256'] == audio['plan_sha256']
    validate_audio_units(c, audio, plan)
    validate_formula_review(c, audio, source)
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
    player = read(c / 'FINAL_PLAYER_V402.json'); delivery = read(c / 'DELIVERY_E.json')
    require_current(final, source, {'PASS'}); require_current(media, source, {'PASS'})
    require_current(player, source, {'PASS_OBSERVED_UI'})
    require_current(delivery, source, {'MEDIA_VALIDATED_AWAITING_PARENT_PUBLIC_MANIFEST','TECHNICAL_DELIVERY_READY_FOR_INDEPENDENT_REVIEW'})
    assert final['returncode'] == 0 and final['canonical_unchanged'] is True
    verify_pin(final['builder'], v / 'make_v7.py')
    expected = {p.resolve() for p in [v/'PUBLIC_DELIVERY_V7.json',v/'RENDER_MANIFEST.json',v.parent/'PUBLIC_DELIVERY_V7.json']}
    assert {verify_pin(entry).resolve() for entry in final['manifests']} == expected
    verify_pin(final['render_manifest_link'], c/'FINAL_RENDER_MANIFEST_LINK.json')
    validate_render_manifest_link(c, v, source)
    verify_pin(delivery['validation'], v / 'render/MEDIA_VALIDATION.json')
    verify_embedded_pins(player)
    manifest = read(v / 'RENDER_MANIFEST.json')
    assert manifest['source'] == manifest['version'] == 'v402' and manifest['source_sha256'] == source
    assert set(manifest['jobs']) == set(delivery['jobs']) == {'film1','film2','loop'}
    for kind, entry in delivery['jobs'].items():
        job = read(verify_pin(entry)); row = manifest['jobs'][kind]
        assert row['job_sha256'] == entry['sha256']
        for field in ['metadata','render','source_files']: assert row[field] == job[field]
        assert row['encoded_sha256'] == job['sha256']
