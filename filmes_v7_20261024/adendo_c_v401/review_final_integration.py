"""Independent, read-only product verification. Writes only this review receipt."""
from pathlib import Path
import collections, datetime, hashlib, json, math, os, sys, time

C=Path(__file__).resolve().parent;W=C.parent
V=Path(r'C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/video_um/delivery_v7')
T=Path(r'C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_022/ADENDO_C')
sys.path.insert(0,str(W));import mission
seen={};findings=[];checks={};historical_links=[]

def read(path):
    path=Path(path);raw=path.read_bytes();pin(path)
    return json.loads(raw.decode('utf-8-sig'))

def pin(path):
    path=Path(path).resolve();stat=path.stat();key=str(path)
    if key in seen:
        assert seen[key]['stat']==(stat.st_size,stat.st_mtime_ns),'READ_INPUT_CHANGED: '+key
        return dict(seen[key]['pin'])
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
    item={'path':key,'bytes':stat.st_size,'sha256':h.hexdigest()}
    seen[key]={'pin':item,'stat':(stat.st_size,stat.st_mtime_ns)}
    return dict(item)

def verify(item,base=V):
    path=Path(item.get('path',item.get('file','')))
    if not path.is_absolute():path=base/path
    actual=pin(path)
    if actual['sha256']!=item['sha256'] and path.resolve()==(V/'RENDER_MANIFEST.json').resolve():
        link=read(C/'FINAL_RENDER_MANIFEST_LINK.json')
        if item['sha256']==link['snapshot']['sha256']:
            actual=pin(link['snapshot']['path']);historical_links.append({'original':item,'preserved_snapshot':actual})
    assert actual['sha256']==item['sha256'],'PIN_MISMATCH: '+str(path)
    if 'bytes' in item:assert actual['bytes']==item['bytes'],'SIZE_MISMATCH: '+str(path)
    return actual

def walk_pins(obj,base=V):
    if isinstance(obj,dict):
        if 'sha256' in obj and isinstance(obj['sha256'],str) and ('path' in obj or 'file' in obj):verify(obj,base)
        for value in obj.values():walk_pins(value,base)
    elif isinstance(obj,list):
        for value in obj:walk_pins(value,base)

def group(name,fn):
    try:checks[name]=fn()
    except Exception as e:findings.append({'id':name,'severity':'BLOCKING','detail':str(e),'exception':type(e).__name__})

projection=mission.call({'operation':'project','max_chars':160000})
result=read(T/'RESULTADO.json');construction=read(C/'CONSTRUCTION_DELIVERY_V401.json')
source=result['source'];source_sha=result['source_sha256']

def origin():
    assert source=='v401' and result==construction
    assert pin(T/'RESULTADO.json')['sha256']==pin(C/'CONSTRUCTION_DELIVERY_V401.json')['sha256']
    assert result['status']=='BUILT_FOR_MANAGEMENT_REVIEW'
    capture=read(C/'SOURCE_CAPTURE.json');walk_pins(capture['canonical_seal']);walk_pins(capture['isolated_seal'])
    seal=read(capture['canonical_seal']['path'])
    assert seal['um_version']==source and seal['sha256']['um.py']==source_sha
    assert seal['timestamp']==result['seal_timestamp']
    make=read(C/'FINAL_MAKE.json');assert make['status']=='PASS' and make['returncode']==0
    assert make['canonical_unchanged'] and make['canonical_before']==make['canonical_after']
    walk_pins(make);walk_pins(result)
    report=T/'RELATORIO.md';pin(report);lines=report.read_text('utf-8-sig').splitlines()
    assert len(lines)<=20 and source_sha in '\n'.join(lines)
    return {'source_and_current_seal_match':True,'result_copies_byte_identical':True,'report_lines':len(lines),'canonical_unchanged_receipt':True}

def manifest_transition():
    link=read(C/'FINAL_RENDER_MANIFEST_LINK.json');e=read(C/'DELIVERY_E.json')
    walk_pins(link);walk_pins(e)
    assert e['actor']=='codex-video-web' and e['actor']!='codex-video-audio'
    assert e['render_manifest']['sha256']==link['snapshot']['sha256']
    before=read(link['snapshot']['path']);after=read(link['final_manifest']['path'])
    assert 'adendo_worker' in before and 'adendo_worker' not in after
    assert {k:v for k,v in before.items() if k!='adendo_worker'}==after
    assert link['comparison']['equal'] and link['comparison']['numeric_tolerance']==0
    assert before['source']==after['source']==source and before['source_sha256']==after['source_sha256']==source_sha
    final_binding=read(C/'MEDIA_FINAL_BINDING.json');walk_pins(final_binding)
    assert final_binding['status']=='PASS_FINAL_BINDING_READY_FOR_INDEPENDENT_REVIEW'
    assert final_binding['actor']=='codex-video-web' and final_binding['source']==source and final_binding['source_sha256']==source_sha
    assert final_binding['original_delivery_e']['sha256']==pin(C/'DELIVERY_E.json')['sha256']
    legacy=final_binding['preserved_audit_delivery_e'];verify(legacy['pin'])
    assert legacy['source']=='v400' and read(legacy['pin']['file'])['source']=='v400'
    assert legacy['pin']['file'] not in [x.get('path') for x in result['evidence']]
    watch=read(C/'MEDIA_WATCH.json');assert watch['status']=='COMPLETE';walk_pins(watch)
    return {'original_e_pin_preserved':True,'only_root_adendo_worker_removed':True,
            'legacy_audit_e_explicitly_historical_and_excluded_from_current_evidence':legacy,
            'final_binding':pin(C/'MEDIA_FINAL_BINDING.json'),'worker_complete':True,'snapshot':link['snapshot'],'final_manifest':link['final_manifest']}

def public_files():
    manifest=read(V/'PUBLIC_DELIVERY_V7.json');root=read(V.parent/'PUBLIC_DELIVERY_V7.json')
    assert manifest['source']==root['source']==source and manifest['source_sha256']==root['source_sha256']==source_sha
    assert root['sha256']==pin(V/'PUBLIC_DELIVERY_V7.json')['sha256'] and root['delivery']=='delivery_v7/PUBLIC_DELIVERY_V7.json'
    entries=manifest['public_files'];assert len(entries)==result['public_files']==132
    assert root['public_files']==[{**e,'path':'delivery_v7/'+e['path']} for e in entries]
    old400=read(W/'adendo_a/CONSTRUCTION_DELIVERY_V400.json')['source_sha256']
    old399=read(V/'audio/NARRATION_PLAN_v399_final.json')['seal_pin']
    forbidden_pins=[old399[:8].encode(),old400[:8].encode()]
    hits=[];paths=set();total=0
    for entry in entries:
        rel=Path(entry['path']);assert not rel.is_absolute() and '..' not in rel.parts
        path=(V/rel).resolve();assert path.is_relative_to(V.resolve())
        lower=entry['path'].lower();parts={p.lower() for p in rel.parts}
        assert not parts.intersection({'private','cache','source','voice_test','voice_sample','audit','backups'})
        assert not any(s in lower for s in ('.bak_','authorization','approval','voice_test','voice_sample','voice_plan'))
        assert lower not in paths;paths.add(lower);verify(entry);total+=entry['bytes']
        tail=b''
        with path.open('rb') as stream:
            for chunk in iter(lambda:stream.read(8*1024*1024),b''):
                blob=tail+chunk
                for needle in forbidden_pins:
                    if needle in blob:hits.append({'file':entry['path'],'old_pin_prefix':needle.decode()})
                tail=blob[-63:]
    assert not hits,hits
    assert total==result['public_bytes']
    return {'files':len(entries),'bytes_scanned':total,'old_pin_occurrences':hits,'private_items_excluded':True,
            'root_list_exactly_matches_inner':True,'public_videos':sum(Path(e['path']).suffix in ('.mp4','.webm') for e in entries)}

def numbers_and_replay():
    ready=read(C/'DATA_READY.json');numeric=read(C/'NUMERIC_COMPARISON.json');parent=read(C/'PARENT_NUMERIC_REVIEW.json')
    assert ready['source']==numeric['source']==parent['source']==source
    assert ready['source_sha256']==numeric['source_sha256']==parent['source_sha256']==source_sha
    assert ready['status']=='DATA_READY' and numeric['status']=='PASS' and parent['status']=='PASS_WITH_SCOPE'
    assert not numeric['unexpected_differences'] and not parent['unexpected_differences']
    assert parent['data_ready_sha256']==pin(C/'DATA_READY.json')['sha256']
    walk_pins(ready);walk_pins({k:v for k,v in numeric.items() if k!='files'})
    for row in numeric['files']:
        verify(row['before']);verify(row['after'])
        # before/after fragments are data values with source-relative paths, not delivery-root references.
        for difference in row['differences']:
            walk_pins(difference.get('before'),C/'baseline_v400/source')
            walk_pins(difference.get('after'),V/'source')
    expected={k:v['after'] for k,v in numeric['authorized_counts'].items()}
    assert expected==result['authorized_kernel_counts']==parent['expected_counts_read_from_sealed_sources']
    assert set(expected)=={'proof_ladder_clean','proof_ladder_total','formal_count','declaration_count'}
    current=read(V/'data/hud.json');baseline=read(C/'baseline_v400/data/hud.json')
    actual_deltas={k:(baseline['extra'][k],v) for k,v in current['extra'].items() if baseline['extra'][k]!=v}
    assert actual_deltas=={k:(v['before'],v['after']) for k,v in numeric['authorized_counts'].items()}
    before_items={r['key']:r['value'] for r in baseline['items']};after_items={r['key']:r['value'] for r in current['items']}
    # The selected HUD values duplicate four authorized documentary counts; all other numeric values stay exact.
    for key,value in after_items.items():
        old=before_items[key]
        if isinstance(value,(int,float)) and old!=value:
            assert (old,value) in actual_deltas.values(),key
    prov=read(V/'data/PROVENANCE_PUBLIC.json')
    assert len(prov['anchors'])>=64 and all(x['ok'] for x in prov['anchors'])
    for row in numeric['files']:
        verify(row['before']);verify(row['after'])
        target=V/'data'/row['file']
        if target.exists():assert pin(target)['sha256']==row['after']['sha256']
    browser=read(V/'replay/TEST_BROWSER.json');offline=read(V/'replay/TEST_OFFLINE.json')
    manifest_pin=pin(V/'replay/replay-manifest.json')['sha256']
    assert browser['status']==offline['status']=='PASS' and not browser['external_requests']
    assert browser['source']==offline['source']==source
    assert browser['source_sha256']==offline['source_sha256']==source_sha
    assert browser['manifest_sha256']==offline['manifest_sha256']==manifest_pin
    assert offline['tests']==13 and not offline['errors'] and not offline['failures']
    return {'authorized_counts':expected,'other_hud_numeric_values_exact':True,'anchors':len(prov['anchors']),
            'anchors_all_ok':True,'offline_tests':offline['tests'],'browser_manifest_bound':True,'browser_external_requests':0,
            'scope':'Receipt/pin and data comparison only; no execution of Python science, Lean or browser replay.'}

def media_and_closure():
    e=read(C/'DELIVERY_E.json');validation=read(V/'render/MEDIA_VALIDATION.json');rm=read(V/'RENDER_MANIFEST.json')
    assert validation['status']=='PASS' and validation['source']==source and validation['source_sha256']==source_sha
    assert len(validation['movies'])==16 and len(validation['images'])==25
    walk_pins(validation)
    required={str(Path(x['file']).resolve()):x['sha256'] for x in validation['movies']+validation['images']}
    tracks=[]
    for movie in validation['movies']:
        name=Path(movie['file']).name
        expected=16 if 'loop' in name else 224 if 'filme1' in name else 360
        if movie['metrics'] is None:
            assert name.endswith('.webm') and movie['full_decode'] and movie['decode_frames']==expected*60
            kind='loop' if 'loop' in name else 'film1' if 'filme1' in name else 'film2'
            stage=read(V/'render/.pipeline'/(kind+'.json' if kind=='loop' else kind+'_silent_vp9.json'))
            walk_pins(stage);assert stage['parameters']['fps']==60
            assert stage['parameters']['source']==source and stage['parameters']['source_sha256']==source_sha
            if kind!='loop':
                mux=read(V/'render/.pipeline'/(kind+'_en_vp9_mux.json'));walk_pins(mux)
                assert mux['parameters']['video_copy'] and mux['parameters']['language']=='en'
                assert any(x['sha256']==movie['sha256'] for x in mux['outputs'])
                assert any(x['sha256']==stage['outputs'][0]['sha256'] for x in mux['inputs'])
            tracks.append({'file':movie['file'],'frames':movie['decode_frames'],'iso_container_metrics':None,
                'fps_from_pinned_encode_stage':60,'duration_from_frames_and_stage_fps':expected,
                'scope':'Existing full-decode frame count and encoder-chain parameters; ISO metrics are not provided for WebM.'})
            continue
        video=next(x for x in movie['metrics']['tracks'] if x['type']=='vide')
        assert movie['full_decode'] and movie['decode_frames']==video['samples']
        assert video['fps']==60 and video['width'] in (1280,1920,3840) and video['height'] in (720,1080,2160)
        assert abs(video['duration']-expected)<.05 and abs(movie['metrics']['duration']-expected)<.1
        sound=[x for x in movie['metrics']['tracks'] if x['type']=='soun']
        if name.startswith(('filme1','filme2')) and 'loop' not in name:
            assert len(sound)==1
            assert sound[0]['language']==('por' if 'pt-BR' in name else 'eng')
        tracks.append({'file':movie['file'],'width':video['width'],'height':video['height'],'duration':video['duration'],'frames':movie['decode_frames'],'audio_track_language':[x['language'] for x in sound]})
    closure={}
    capture=read(C/'PARENT_CAPTURE_AUDIT.json');walk_pins(capture)
    for kind,ref in e['jobs'].items():
        verify(ref);job=read(ref['file']);verify(job)
        assert job['metadata']==result['jobs'][kind]['metadata']==rm['jobs'][kind]['metadata']
        assert job['metadata']['source']==source and job['metadata']['source_sha256']==source_sha
        assert job['render']['encoded']==job['metadata']['total']==result['jobs'][kind]['frames']
        assert job['sha256']==rm['jobs'][kind]['encoded_sha256']
        assert job['render']==rm['jobs'][kind]['render'] and job['source_files']==rm['jobs'][kind]['source_files']
        for rel,p in job['source_files'].items():
            path=(V/'cinema'/rel).resolve();assert path.is_relative_to(V.resolve());verify({'path':str(path),**p})
        assert capture['jobs'][kind]['receipt']['sha256']==ref['sha256']
        assert capture['jobs'][kind]['coverage']==result['coverage'][kind]
        assert len(job['render']['samples'])==job['metadata']['duration']
        closure[kind]={'files':len(job['source_files']),'job':verify(ref),'stream':verify(job)}
    stages=[];covered=set()
    for p in (V/'render/.pipeline').glob('*.json'):
        stage=read(p)
        if stage.get('status')!='COMPLETE':continue
        outputs=stage.get('outputs',[])
        matches=[x for x in outputs if required.get(str(Path(x['file']).resolve()))==x['sha256']]
        if not matches:continue
        walk_pins(stage)
        payload={'inputs':stage['inputs'],'parameters':stage['parameters']}
        key=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        assert key==stage['key'],'STAGE_KEY_MISMATCH: '+p.name
        covered.update(str(Path(x['file']).resolve()) for x in matches);stages.append(pin(p))
    assert set(required)<=covered,'VALIDATED_OUTPUT_WITHOUT_CURRENT_STAGE'
    binding=read(C/'MEDIA_AUDIO_BINDING.json');walk_pins(binding)
    assert binding['source']==source and binding['source_sha256']==source_sha
    return {'validated_video_pins':16,'validated_image_pins':25,'documented_full_decode':True,'decode_repeated':False,
            'tracks':tracks,'job_closure':closure,'pipeline_stages':stages,'audio_binding_scope':'Integrity/track integration only; no independent review of this actor audio build.'}

def ui_and_code_review():
    player=read(C/'FINAL_PLAYER_V401.json');f1=read(C/'PLAYER_F1_V401.json');walk_pins(player);walk_pins(f1)
    assert player['status']==f1['status']=='PASS_OBSERVED_UI'
    assert player['source']==f1['source']==source and player['source_sha256']==f1['source_sha256']==source_sha
    assert f1['duration_seconds']==224 and player['film2']['duration_seconds']==360
    assert f1['dimensions']==player['film2']['dimensions']==[1920,1080]
    assert any(x.get('observed',{}).get('ended') for x in player['film2']['observations'] if isinstance(x.get('observed'),dict))
    for film in (f1,player['film2']):
        for item in film['files']:verify(item)
        assert len(film['files'])==2
    code_review=read(C/'FINALIZER_REVIEW.json');assert code_review['actor']=='codex-video-replay'
    assert not code_review['open_medium_high']
    for item in code_review['effective_finalizer_code_pins']:verify(item)
    submit_review=read(C/'SUBMIT_FINALIZER_REVIEW.json');verify(submit_review['code'])
    assert all(x['pass'] for x in submit_review['tests'])
    transition_review=read(C/'MANIFEST_LINK_REVIEW.json')
    assert all(x['passed'] for x in transition_review['results'])
    return {'both_films_en_pt_current_media_pins':True,'archived_closing_screenshots_inspected':['PLAYER_F1_CLOSING.png','PLAYER_F2_CLOSING.png'],
            'closing_screenshots_show':'v401, program SHA16, 9561/9561 and matching seal timestamp; F1 221/224s, F2 357/360s',
            'new_live_ui_test':False,'parent_ui_observations':player['checks'],'script_review_actor':code_review['actor'],
            'script_reviews':[pin(C/n) for n in ('FINALIZER_REVIEW.json','SUBMIT_FINALIZER_REVIEW.json','MANIFEST_LINK_REVIEW.json')]}

for name,fn in [('origin_result_report',origin),('manifest_transition',manifest_transition),('public_contract',public_files),
                ('numbers_replay',numbers_and_replay),('media_closure',media_and_closure),('documented_ui_and_code',ui_and_code_review)]:
    group(name,fn)
    print(json.dumps({'check':name,'passed':name in checks,'findings':findings[-1:] if name not in checks else []}),flush=True)

def stable():
    for path,item in seen.items():
        s=Path(path).stat();assert item['stat']==(s.st_size,s.st_mtime_ns),'FINAL_INPUT_CHANGED: '+path
    return {'files':len(seen),'all_read_files_stable':True}
group('read_stability',stable)
report={'schema':'iald.final-integration-review.v401/v1','status':'PASS_WITH_SCOPE' if not findings else 'FINDINGS',
    'actor':'codex-video-audio','reviewer':'codex-video-audio','source':source,'source_sha256':source_sha,
    'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'mission_reference':str(W/'SESSION_REFERENCE.json'),'mission_revision_observed':projection['receipt']['revision'],
    'mission_project_receipt':projection['receipt'],
    'preflight_scope':'Directly delegated documentary review; no separate reviewer lease assigned. No claim or mutation of builder tasks.',
    'result':pin(T/'RESULTADO.json'),'construction':pin(C/'CONSTRUCTION_DELIVERY_V401.json'),
    'report':pin(T/'RELATORIO.md'),'public_manifest':pin(V/'PUBLIC_DELIVERY_V7.json'),
    'root_pointer':pin(V.parent/'PUBLIC_DELIVERY_V7.json'),'delivery_e':pin(C/'DELIVERY_E.json'),
    'manifest_transition':pin(C/'FINAL_RENDER_MANIFEST_LINK.json'),'checks':checks,'findings':findings,
    'historical_pin_links_verified':historical_links,'verified_pins':[x['pin'] for x in seen.values()],
    'independence':{'construction_actor':'codex-video-v7','media_actor':'codex-video-web','reviewer':'codex-video-audio',
        'own_audio_build_excluded_from_independent_verdict':True,'own_audio_accepted':False},
    'limits':['Documentary/byte verification and two archived closing screenshots; no new live UI operation, complete visual inspection or perceptual audition.',
        'Existing full-decode and media measurements are bound to current bytes; they were not rerun.',
        'Own audio is referenced only for package/track integrity, not independently approved or reaudited.',
        'No new scientific execution/proof or empirical conclusion; anchors and tests retain the scope of their receipts.',
        'Mission acceptance, management integration and publication remain separate acts.'],
    'actions':{'product_or_manifest_edits':False,'render':False,'tts':False,'mission_accept':False,'publication':False},
    'review_script':pin(Path(__file__))}
target=C/'FINAL_INTEGRATION_REVIEW.json'
if target.exists():
    previous=target.with_name(target.name+'.bak_'+str(time.time_ns()))
    raw_before=target.read_bytes()
    with previous.open('xb') as f:f.write(raw_before);f.flush();os.fsync(f.fileno())
    assert previous.read_bytes()==raw_before
    report['previous_verifier_result_preserved']=pin(previous)
    report['verifier_corrections']=[
        {'check':'manifest_transition','reason':'Removed unsupported requirement that private historical v400 E equal current v401 E; verified explicit MEDIA_FINAL_BINDING instead.'},
        {'check':'numbers_replay','reason':'Resolved provenance before/after data fragments against their respective baseline/current source directories.'},
        {'check':'media_closure','reason':'WebM records deliberately have metrics=null; verified existing full-decode frames and pinned FPS/stream-copy chain instead of indexing an ISO-only metrics object.'}]
raw=(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
temp=target.with_suffix('.json.tmp')
with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert temp.stat().st_size==len(raw);os.replace(temp,target)
print(json.dumps({'status':report['status'],'receipt':pin(target),'findings':findings,'verified_files':len(seen)}),flush=True)
