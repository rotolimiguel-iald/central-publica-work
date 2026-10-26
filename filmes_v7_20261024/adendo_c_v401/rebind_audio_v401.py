"""ADENDO C audio: immutable v400 baseline and offline v401 plan comparison."""
from pathlib import Path
import contextlib, datetime, importlib.util, io, json, os, re, runpy, subprocess, sys, time, wave

C = Path(__file__).resolve().parent
W = C.parent
spec = importlib.util.spec_from_file_location('audio_v400_tools', W/'adendo_a/rebind_audio_v400.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
V = old.R
ACTOR = 'codex-video-audio'
TASK = 'V401_AUDIO'

def check():
    p = old.mission.call({'operation':'project','max_chars':160000})
    task = next(t for t in p['projection']['active'] if t['id']==TASK)
    assert task['lease']['owner']==ACTOR
    result = old.mission.call({'operation':'check','actor':{'id':ACTOR,'kind':'agent'},
        'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
        'task_id':TASK,'lease_id':task['lease']['id'],'max_chars':160000})
    assert result['ready']
    return result

def baseline():
    preflight = check()
    target = C/'baseline_audio_v400'
    receipt = target/'BASELINE.json'
    if receipt.exists():
        saved = old.read(receipt)
        for item in saved['files']:
            assert old.digest(item['backup']['path'])==item['original']['sha256']
        print(json.dumps({'status':'BASELINE_REUSED','files':len(saved['files'])}))
        return
    plan = old.read(V/'audio/NARRATION_PLAN_v400_final.json')
    assert plan['seal_version']=='v400'
    files = []
    for folder in [V/'audio',V/'subs']:
        files += [Path(str(p).removeprefix('\\\\?\\')) for p in old.ep(folder).rglob('*')
                  if p.is_file() and '.bak_' not in p.name and '__pycache__' not in p.parts]
    files += [V/f'data/film{i}_narration_timeline.json' for i in (1,2)]
    files += [V/'audit/DELIVERY_D.json',V/'audit/DELIVERY_D_V400.json']
    if old.read(V/'data/hud.json')['seal_version']=='v400':
        files += [V/f'data/{n}.json' for n in ('hud','film1','film2')]
    rows = []
    for src in sorted(set(files),key=str):
        dst = target/src.relative_to(V)
        data = old.ep(src).read_bytes()
        old.ep(dst.parent).mkdir(parents=True,exist_ok=True)
        if old.ep(dst).exists():
            assert old.ep(dst).read_bytes()==data
        else:
            temp = old.ep(dst.with_name(dst.name+'.tmp'))
            with temp.open('xb') as stream:
                stream.write(data);stream.flush();os.fsync(stream.fileno())
            assert old.digest(temp)==old.digest(src)
            os.rename(temp,old.ep(dst))
        assert old.digest(dst)==old.digest(src)
        rows.append({'original':old.pin(src),'backup':old.pin(dst)})
    old.write_new(receipt,{'status':'PASS_BYTES_PRESERVED','source':'v400','source_sha256':plan['seal_pin'],
        'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'preflight':preflight,'files':rows,'personal_voice_excluded':True})
    print(json.dumps({'status':'BASELINE_SAVED','files':len(rows),'bytes':sum(x['original']['bytes'] for x in rows),'receipt':old.pin(receipt)}))

def prepare(isolated=False):
    preflight = check()
    root = C/'audio_plan_candidate' if isolated else V
    gate_file = C/('SOURCE_CAPTURE.json' if isolated else 'DATA_READY.json')
    ready = old.read(gate_file)
    assert ready['source']=='v401'
    if not isolated:
        assert ready['status'].startswith('DATA_READY')
    else:
        for entry in ready['files']:
            assert old.digest(entry['isolated']['path'])==entry['isolated']['sha256']
        for key in ('canonical_seal','isolated_seal'):
            assert old.digest(ready[key]['path'])==ready[key]['sha256']
        # Rawls owns candidate_v401; stage only audio-plan inputs in our own directory.
        for name in ('hud','film1','film2'):
            source_root=C/'candidate_v401' if name=='hud' else C/'baseline_audio_v400'
            src=source_root/f'data/{name}.json';dst=root/f'data/{name}.json'
            raw=old.ep(src).read_bytes()
            dst.parent.mkdir(parents=True,exist_ok=True)
            if dst.exists():
                assert dst.read_bytes()==raw,'ISOLATED_INPUT_ALREADY_PINNED'
            else:
                temp=dst.with_suffix('.json.tmp')
                with temp.open('xb') as stream:
                    stream.write(raw);stream.flush();os.fsync(stream.fileno())
                assert old.digest(temp)==old.digest(src)
                os.rename(temp,dst)
    inputs = [old.pin(root/f'data/{name}.json') for name in ('hud','film1','film2')]
    inputs += [old.pin(old.BUILDER),old.pin(V/'audio/script_templates.json'),old.pin(gate_file)]
    base = C/'baseline_audio_v400'
    previous = old.read(base/'audio/NARRATION_PLAN_v400_final.json')
    before = old.read(base/'data/hud.json')
    after = old.read(root/'data/hud.json')
    assert after['seal_version']=='v401' and after['seal_pin']==ready['source_sha256']
    builder_spec = importlib.util.spec_from_file_location('audio_builder',old.BUILDER)
    builder = importlib.util.module_from_spec(builder_spec)
    builder_spec.loader.exec_module(builder)
    values_before,values_after = builder.hud_values(before),builder.hud_values(after)
    allowed = {'proof_ladder_clean':(9541,9561),'proof_ladder_total':(9541,9561),
               'formal_count':(1429,1430),'declaration_count':(29296,29318)}
    changes = {k:(values_before.get(k),values_after.get(k)) for k in set(values_before)|set(values_after)
               if values_before.get(k)!=values_after.get(k)}
    for values in (values_before,values_after):
        assert values['theorems']==values['proof_ladder_clean']
        assert values['n_formal']==values['formal_count']
        assert values['um_sha16']==values['seal_pin'][:16]
    expected_changes={**allowed,'theorems':allowed['proof_ladder_clean'],'n_formal':allowed['formal_count']}
    assert {k:v for k,v in changes.items() if k not in {'seal_version','seal_pin','seal_timestamp','um_sha16'}}==expected_changes, changes
    # Numeric literals above only enforce the authorized delta; all spoken text comes from the HUD builder.
    saved_argv=sys.argv
    output=io.StringIO()
    try:
        sys.argv=[str(old.BUILDER),'plan','--root',str(root),'--templates',str(V/'audio/script_templates.json')]
        with old.local_only(),contextlib.redirect_stdout(output):
            runpy.run_path(str(old.BUILDER),run_name='__main__')
    finally:
        sys.argv=saved_argv
    plan=json.loads(output.getvalue())
    assert plan['pins']['builder_sha256']==previous['pins']['builder_sha256']
    assert plan['pins']['template_sha256']==previous['pins']['template_sha256']
    expected = json.loads(json.dumps(previous['films']))
    cue_changes = []
    for film,content in expected.items():
        for segment in content['segments']:
            for index,cue in enumerate(segment['cues']):
                for lang,text in list(cue.items()):
                    replacement = text.replace(str(values_before['proof_ladder_clean']),str(values_after['proof_ladder_clean']))
                    if replacement!=text:
                        cue_changes.append({'film':film,'segment':segment['key'],'cue_index':index,
                            'language':lang,'before':text,'after':replacement})
                        cue[lang]=replacement
    assert plan['films']==expected, 'UNEXPECTED_TEXT_TIMING_OR_BUDGET_CHANGE'
    assert len(cue_changes)==8 and {(x['film'],x['segment']) for x in cue_changes}=={('film1','return'),('film2','einstein')}
    for k in previous:
        if k not in {'films','pins','seal_version','seal_pin','seal_timestamp','plan_sha256'}:
            assert previous[k]==plan[k],k
    reuse = old.units_verified()
    historical = {u['key']:u for u in reuse['units']}
    units = {}
    for film,content in plan['films'].items():
        for segment in content['segments']:
            for index,cue in enumerate(segment['cues']):
                for lang,voice in plan['voices'].items():
                    text=cue[lang];key=builder.cache_key(voice,text)
                    unit=units.setdefault(key,{'key':key,'voice':voice,'language':lang,'text':text,
                        'text_sha256':builder.sha(text.encode()),'occurrences':[]})
                    unit['occurrences'].append({'film':film,'segment':segment['key'],'cue_index':index})
    for key,unit in units.items():
        hit=builder.completed_cached_audio(builder.io_path(V/'audio/cache'),key)
        unit['completed_cache']=None if hit is None else {'audio':old.pin(hit),'receipt':old.pin(hit.with_suffix('.json'))}
        unit['unchanged_from_v400']=key in historical
    assert len(units)==60 and sum(x['unchanged_from_v400'] for x in units.values())==56
    assert all(x['completed_cache'] for x in units.values() if x['unchanged_from_v400'])
    for entry in inputs:
        assert old.digest(entry['path'])==entry['sha256'],'PLAN_INPUT_CHANGED_DURING_READ'
    target=C/('AUDIO_PLAN_V401_ISOLATED.json' if isolated else 'AUDIO_PLAN_V401_CANDIDATE.json')
    old.write_new(target,plan)
    report={'schema':'iald.audio-v401-plan-review/v1','status':'PLAN_READY_FOUR_CHANGED_SPEECH_UNITS',
        'actor':ACTOR,'source':ready['source'],'source_sha256':ready['source_sha256'],
        'preflight':preflight,'data_ready':None if isolated else old.pin(C/'DATA_READY.json'),
        'isolated_candidate_only':isolated,'input_pins':inputs,
        'timing_origin':'baseline_audio_v400/data/film1.json and film2.json' if isolated else 'delivery data',
        'baseline':old.pin(base/'BASELINE.json'),'plan':old.pin(target),'plan_sha256':plan['plan_sha256'],
        'numeric_changes':changes,'cue_changes':cue_changes,'units':list(units.values()),
        'counts':{'unique_units':60,'reusable_v400':56,'changed_en_pt':4,'changed_texts_all_languages':8,
                  'cache_missing':sum(x['completed_cache'] is None for x in units.values())},
        'durations':{k:f['total_seconds'] for k,f in plan['films'].items()},
        'speech_version_or_pin_references':[], 'formal_declaration_counts_spoken':False,
        'tts_calls_this_stage':0,'network_calls_this_stage':0,'delivery_modified':False,
        'next_action':'Conferir o plano concreto antes de sintetizar somente as quatro falas alteradas; preservar as 60 unidades anteriores e os recibos incertos.'}
    report_path=C/('AUDIO_PLAN_REVIEW_ISOLATED.json' if isolated else 'AUDIO_PLAN_REVIEW.json')
    old.write_new(report_path,report)
    print(json.dumps({'status':report['status'],'isolated':isolated,'plan_sha256':plan['plan_sha256'],'counts':report['counts'],'report':old.pin(report_path)}))

def builder_module():
    spec=importlib.util.spec_from_file_location('audio_builder_current',old.BUILDER)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def execution_gate():
    preflight=check()
    data=old.read(C/'DATA_READY.json');numeric=old.read(C/'PARENT_NUMERIC_REVIEW.json')
    parent=old.read(C/'PARENT_AUDIO_PLAN_REVIEW.json');plan=old.cli('plan')
    assert data['status']=='DATA_READY' and data['unexpected_scientific_differences']==0
    assert data['anchors']['all_ok'] and data['anchors']['total']==64
    assert numeric['status']=='PASS_WITH_SCOPE' and numeric['unexpected_differences']==[]
    assert numeric['data_ready_sha256']==old.digest(C/'DATA_READY.json')
    assert parent['status']=='PASS_FOUR_CHANGED_PUBLIC_TTS_UNITS'
    assert old.digest(parent['plan_file']['path'])==parent['plan_file']['sha256']
    assert old.digest(C/'AUDIO_PLAN_REVIEW_ISOLATED.json')==parent['delta_review_sha256']
    assert plan==old.read(C/'AUDIO_PLAN_V401_ISOLATED.json')==old.read(C/'AUDIO_PLAN_V401_CANDIDATE.json')
    assert plan['plan_sha256']==parent['plan_sha256']
    assert plan['seal_pin']==data['source_sha256']==numeric['source_sha256']
    assert plan['seal_version']==data['source']=='v401'
    for e in data['source_files']+data['data_files']+[data['seal'],data['comparison'],data['integration']]:
        assert old.digest(e['path'])==e['sha256'],e['path']
    capture=old.read(C/'SOURCE_CAPTURE.json')
    assert old.digest(capture['canonical_seal']['path'])==capture['canonical_seal']['sha256'],'CANONICAL_SEAL_ADVANCED_STOP'
    review=old.read(C/'AUDIO_PLAN_REVIEW.json');new=[u for u in review['units'] if not u['unchanged_from_v400']]
    assert len(new)==4 and len(review['units'])==60
    for unit,approved in zip(new,parent['new_units']):
        assert all(unit[k]==approved[k] for k in ('key','language','voice','text'))
    old.units_verified()
    return preflight,data,plan,review,new

def synthesize():
    preflight,data,plan,review,new=execution_gate()
    builder=builder_module();cache=builder.io_path(V/'audio/cache')
    auth=W/'EDGE_BOUNDED_RETRY_APPROVAL.json';context=builder.load_bounded_authorization(auth)
    # This wrapper can dispatch only the four reviewed new keys. Old uncertain keys never enter this loop.
    old_keys={u['key'] for u in old.read(W/'adendo_a/AUDIO_REUSE_REVIEW.json')['units']}
    assert all(u['key'] not in old_keys for u in new)
    subprocess.run([str(old.NODE),'-e','require.resolve(process.argv[1])',str(V.parent/'node_modules/msedge-tts')],capture_output=True,check=True,timeout=20)
    execution_id=str(time.time_ns());intent_path=C/f'AUDIO_SYNTHESIS_INTENT_{execution_id}.json'
    intent={'schema':'iald.audio-v401-synthesis/v1','status':'INTENT','preflight':preflight,
        'source':data['source'],'source_sha256':data['source_sha256'],'plan_sha256':plan['plan_sha256'],
        'parent_payload_review':old.pin(C/'PARENT_AUDIO_PLAN_REVIEW.json'),
        'human_authorizations':[old.pin(W/'EDGE_RETRY_HUMAN_APPROVAL.json'),old.pin(auth)],
        'adendo_c_authorization':old.pin(C/'AUTHORIZATION.json'),'units':[{'key':u['key'],'voice':u['voice'],'text_sha256':u['text_sha256']} for u in new],
        'personal_voice_included':False,'maximum_new_retries_per_failed_unit':context['limit']}
    old.write_new(intent_path,intent)
    results=[]
    for u in new:
        execution_gate()
        existing=builder.completed_cached_audio(cache,u['key'])
        print(json.dumps({'phase':'REUSE_COMPLETED' if existing else 'DISPATCH_NEW_PUBLIC_UNIT','key':u['key'],'voice':u['voice']}),flush=True)
        try:
            mp3=builder.bounded_tts(cache,u['voice'],u['text'],plan['plan_sha256'],V.parent/'node_modules',str(old.NODE),context)
            result={'key':u['key'],'status':'COMPLETED','reused_at_start':existing is not None,
                    'audio':old.pin(mp3),'receipt':old.pin(mp3.with_suffix('.json'))}
        except Exception as exc:
            result={'key':u['key'],'status':'PENDING','reason':str(exc)}
        results.append(result)
        old.write_new(C/f'AUDIO_SYNTHESIS_UNIT_{execution_id}_{len(results)}.json',result)
        print(json.dumps(result),flush=True)
    old.write_new(C/f'AUDIO_SYNTHESIS_EXECUTION_{execution_id}.json',{
        **intent,'status':'COMPLETED' if all(r['status']=='COMPLETED' for r in results) else 'PARTIAL_PENDING',
        'intent':old.pin(intent_path),'results':results})
    assert all(r['status']=='COMPLETED' for r in results),'PENDING_NEW_UNITS_NO_MIX_MUTATION'

def mix():
    preflight,data,plan,review,new=execution_gate();builder=builder_module()
    resolved=[]
    for u in review['units']:
        mp3=builder.completed_cached_audio(builder.io_path(V/'audio/cache'),u['key'])
        assert mp3 is not None,('MISSING_AUDIO_STOP',u['key'])
        resolved.append({**{k:u[k] for k in ('key','voice','language','text_sha256','occurrences','unchanged_from_v400')},
            'audio':old.pin(mp3),'receipt':old.pin(mp3.with_suffix('.json'))})
    receipt_path=C/'AUDIO_CACHE_ONLY_EXECUTION.json'
    assert not receipt_path.exists(),'BUILD_ALREADY_RETURNED_REUSE_RECEIPT'
    target=V/'audio/NARRATION_PLAN_v401_final.json'
    if target.exists():assert old.read(target)==plan
    else:old.write_new(target,plan)
    old.write_new(C/'AUDIO_BUILD_INTENT.json',{'status':'INTENT','preflight':preflight,
        'plan':old.pin(target),'plan_sha256':plan['plan_sha256'],'cache_bindings':resolved,
        'baseline':old.pin(C/'baseline_audio_v400/BASELINE.json'),'mode':'build --cache-only'})
    start=time.monotonic();outcome=old.cli('build')
    old.write_new(receipt_path,{'status':'RETURNED','result':outcome,'elapsed_seconds':time.monotonic()-start,
        'preflight':preflight,'source':data['source'],'source_sha256':data['source_sha256'],
        'plan_sha256':plan['plan_sha256'],'mode':'build --cache-only','tts_requested':False,
        'network_guard':'Python sockets refused; only fixed local Node module probes and FFmpeg allowed',
        'node':old.pin(old.NODE),'ffmpeg':old.pin(old.FF),'cache_bindings':resolved})
    print(json.dumps({'status':'CACHE_ONLY_RETURNED','seconds':time.monotonic()-start}),flush=True)

def validate():
    preflight,data,plan,review,new=execution_gate()
    build=old.read(V/'audio/NARRATION_BUILD.json');progress=old.read(V/'audio/NARRATION_PROGRESS.json')
    assert build['status']=='COMPLETED' and not build['tts'] and not build['tts_inflight'] and not build['pending']
    assert build['plan_sha256']==progress['plan_sha256']==plan['plan_sha256']
    assert progress['cache_only'] and progress['completed']==progress['total_unique_units']==60 and not progress['pending']
    assert progress['authorization_sha256'] is None
    assert plan==old.read(V/'audio/NARRATION_PLAN_v401_final.json')
    execution=old.read(C/'AUDIO_CACHE_ONLY_EXECUTION.json');assert not execution['tts_requested']
    transport=old.read(C/'AUDIO_TRANSPORT_VALIDATION.json')
    assert transport['status']=='PASS_FOUR_UNITS_RECEIVED' and transport['completed_units']==4
    for row in transport['units']:
        assert old.digest(row['transport']['path'])==row['transport']['sha256']
    for unit in execution['cache_bindings']:
        for key in ('audio','receipt'):assert old.digest(unit[key]['path'])==unit[key]['sha256']
        cache_receipt=old.read(unit['receipt']['path'])
        assert cache_receipt['state']=='completed' and cache_receipt['audio_sha256']==unit['audio']['sha256']
        assert cache_receipt['voice']==unit['voice'] and cache_receipt['text_sha256']==unit['text_sha256']
    preserved=[]
    baseline=old.read(C/'baseline_audio_v400/BASELINE.json')
    for row in baseline['files']:
        assert old.digest(row['backup']['path'])==row['original']['sha256']
        rel=Path(row['original']['path']).relative_to(V)
        if rel.parts[:2]==('audio','cache') and rel.suffix!='.wav':
            assert old.digest(row['original']['path'])==row['original']['sha256'];preserved.append(row['original'])
    media=[];timelines=[];subtitles=[]
    builder=builder_module()
    for film in ('film1','film2'):
        tp=V/f'data/{film}_narration_timeline.json';tl=old.read(tp)
        assert tl['status']==build['reports'][film]['status']=='AUDIO_MEASURED'
        assert tl['segments']==plan['films'][film]['segments'] and tl['plan_sha256']==plan['plan_sha256']
        assert tl['loudness']==build['reports'][film]['loudness']
        assert not tl['music'] and not tl['speedup'] and tl['voices']==plan['voices']
        for lang in ('en','pt-BR'):
            last=0
            for cue in tl['cues'][lang]:
                assert cue['start']>=last and cue['end']>cue['start'] and cue['end']<=tl['total_seconds']
                last=cue['end']
            measured=tl['loudness'][lang]
            for ext,h,m in [('wav',measured['sha256'],measured['after']),('m4a',measured['aac']['sha256'],measured['aac']['measurement'])]:
                path=V/f'audio/{film}/{lang}.{ext}';assert old.digest(path)==h
                assert abs(float(m['input_i'])+16)<=1 and float(m['input_tp'])<0
                media.append({**old.pin(path),'film':film,'language':lang,'lufs':float(m['input_i']),'true_peak_dbtp':float(m['input_tp'])})
            with wave.open(str(V/f'audio/{film}/{lang}.wav'),'rb') as wav:
                assert wav.getnframes()/wav.getframerate()==tl['total_seconds']==plan['films'][film]['total_seconds']
                assert wav.getframerate()==48000 and wav.getnchannels()==1
        subdir=V/'subs'/film.replace('film','filme')
        for lang in builder.LANGS:
            base=tl['cues']['pt-BR' if lang=='pt-BR' else 'en']
            variants=[(subdir/(lang+'.vtt'),base)]
            variants += [(subdir/('sync-'+voice)/(lang+'.vtt'),tl['cues'][voice]) for voice in ('en','pt-BR')]
            for path,cues in variants:
                expected=builder.vtt([{**cue,'text':cue['translations'][lang]} for cue in cues],lang)
                assert path.read_bytes()==expected
                subtitles.append({**old.pin(path),'language':lang,'cues':len(cues)})
        chapters=subdir/'chapters.vtt'
        assert chapters.read_bytes()==builder.vtt([{'start':s['start'],'end':s['end'],'text':s['title']['en']} for s in tl['segments']],'en')
        subtitles.append({**old.pin(chapters),'language':'en','cues':len(tl['segments'])})
        timelines.append(old.pin(tp))
    assert len(media)==8 and len(subtitles)==26
    new_attempts=[]
    for u in new:
        paths=[V/'audio/cache'/(u['key']+'.json')]
        paths+=list(old.ep(V/'audio/cache/bounded').rglob(u['key']+'.json'))
        for path in paths:
            if old.ep(path).exists():
                r=old.read(path);new_attempts.append({'key':u['key'],'state':r['state'],'receipt':old.pin(path),
                    'transport':old.pin(path.with_suffix('.transport.jsonl')) if old.ep(path.with_suffix('.transport.jsonl')).exists() else None})
    receipt={'schema':'iald.delivery-d.v401/v1','status':'PASS_BUILDER_READY_FOR_INDEPENDENT_REVIEW',
        'actor':ACTOR,'source':data['source'],'source_sha256':data['source_sha256'],
        'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preflight':preflight,
        'plan_current':True,'plan_sha256':plan['plan_sha256'],'plan':old.pin(V/'audio/NARRATION_PLAN_v401_final.json'),
        'builder':old.pin(old.BUILDER),'helper':old.pin(Path(__file__)),'templates':old.pin(V/'audio/script_templates.json'),
        'source_files':data['source_files'],'data_ready':old.pin(C/'DATA_READY.json'),
        'parent_numeric_review':old.pin(C/'PARENT_NUMERIC_REVIEW.json'),'parent_payload_review':old.pin(C/'PARENT_AUDIO_PLAN_REVIEW.json'),
        'human_authorizations_private':[old.pin(W/'EDGE_RETRY_HUMAN_APPROVAL.json'),old.pin(W/'EDGE_BOUNDED_RETRY_APPROVAL.json')],
        'counts':{'unique_units':60,'cue_occurrences':76,'reused_v400_units':56,'new_v401_units':4,'subtitle_files':26,'wav_aac_files':8},
        'new_synthesis_attempts':new_attempts,'cache_bindings':execution['cache_bindings'],
        'transport_validation':old.pin(C/'AUDIO_TRANSPORT_VALIDATION.json'),
        'synthesis_summary':{k:transport[k] for k in ('speech_requests','completed_units','retry_attempts','new_uncertain_units')},
        'build':old.pin(V/'audio/NARRATION_BUILD.json'),'progress':old.pin(V/'audio/NARRATION_PROGRESS.json'),
        'cache_only_execution':old.pin(C/'AUDIO_CACHE_ONLY_EXECUTION.json'),
        'baseline':old.pin(C/'baseline_audio_v400/BASELINE.json'),'old_cache_evidence_preserved':len(preserved),
        'media':media,'subtitles':subtitles,'timelines':timelines,'music':False,'speedup':False,
        'scope':'Real Microsoft Edge EN/PT speech, measured mixes and four subtitle languages. Parent payload review is not human consent; original human authorizations remain separate.',
        'limitations':['No perceptual audition in this mode.','No personal voice used.','No new scientific proof or unrestricted physical conclusion.','Final integration and acceptance belong to an independent reviewer.'],
        'private_receipt_do_not_publish':True}
    target=V/'audit/DELIVERY_D_V401.json';old.write_new(target,receipt)
    old.write_new(C/'AUDIO_READY.json',{'status':'AUDIO_READY','actor':ACTOR,'source':data['source'],
        'source_sha256':data['source_sha256'],'plan_sha256':plan['plan_sha256'],'receipt':old.pin(target),
        'counts':receipt['counts'],'media':media,'subtitles':subtitles,'timelines':timelines,
        'perceptual_audition':False,'acceptance':'BUILDER_CANDIDATE_ONLY'})
    print(json.dumps({'status':'AUDIO_READY','receipt':old.pin(target),'media':media,'attempt_states':[x['state'] for x in new_attempts]}),flush=True)

def submit():
    preflight=check();ready=old.read(C/'AUDIO_READY.json')
    assert old.digest(ready['receipt']['path'])==ready['receipt']['sha256']
    p=old.mission.call({'operation':'project','max_chars':160000})
    result=old.mission.call({'operation':'submit','actor':{'id':ACTOR,'kind':'agent'},
        'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
        'task_id':TASK,'lease_id':preflight['lease_id'],'event_id':'ordem022-adendo-c-v401-audio-submit',
        'evidence':[{'path':e['path'],'sha256':e['sha256']} for e in [old.pin(C/'AUDIO_READY.json'),old.pin(V/'audit/DELIVERY_D_V401.json')]]})
    old.write_new(C/'AUDIO_SUBMIT.json',result)
    print(json.dumps(result),flush=True)

if __name__=='__main__':
    {'baseline':baseline,'prepare':prepare,'prepare-isolated':lambda:prepare(True),
     'synthesize':synthesize,'mix':mix,'validate':validate,'submit':submit}[sys.argv[1]]()
