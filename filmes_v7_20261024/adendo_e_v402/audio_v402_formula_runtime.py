"""Approved R3 audio runtime; existing cache/retry engine, exact formula gate."""
from pathlib import Path
import json, os, time
from audio_v402_revision import verify_pin, seal_guard, stable_new
from formula_narration_gate import execution_gate as formula_execution_gate

def execution_gate(context):
    return formula_execution_gate()

def optional_pin(c, path):
    return c.old.pin(path) if path.exists() else None


def synthesize(c):
    import subprocess
    preflight,data,plan,review,new=execution_gate(c);builder=c.builder_module()
    cache=builder.io_path(c.V/'audio/cache');auth=c.W/'EDGE_BOUNDED_RETRY_APPROVAL.json'
    context=builder.load_bounded_authorization(auth)
    baseline=c.old.read(c.C/'baseline_audio_v401/BASELINE.json')
    protected={Path(r['original']['path']).stem for r in baseline['files']
               if '/audio/cache/' in r['original']['path'].replace('\\','/') and r['original']['path'].endswith('.json')}
    assert all(u['key'] not in protected for u in new),'NEVER_REOPEN_HISTORICAL_KEY'
    subprocess.run([str(c.old.NODE),'-e','require.resolve(process.argv[1])',str(c.V.parent/'node_modules/msedge-tts')],capture_output=True,check=True,timeout=20)
    run=str(time.time_ns());intent_path=c.C/f'AUDIO_SYNTHESIS_INTENT_{run}.json'
    intent={'schema':'iald.audio-v402-synthesis/v1','status':'INTENT','preflight':preflight,
            'source':'v402','source_sha256':data['source_sha256'],'plan_sha256':plan['plan_sha256'],
            'plan':c.old.pin(c.V/'audio/NARRATION_PLAN_v402_formula_final.json'),
            'parent_payload_review':c.old.pin(c.C/'PARENT_AUDIO_PLAN_REVIEW.json'),
            'formula_parent_review':c.old.pin(c.C/'FORMULA_NARRATION_PARENT_REVIEW.json'),
            'formula_review':c.old.pin(c.C/'FORMULA_NARRATION_REVIEW.json'),
            'old_hold_preserved_resolved_by_exact_new_plan_review':True,
            'human_authorizations_private':[c.old.pin(auth),c.old.pin(c.C/'HUMAN_AUTHORIZATION.json')],
            'intake':c.old.pin(c.C/'SOURCE_INTAKE.json'),'personal_voice_included':False,
            'maximum_new_retries_per_failed_unit':context['limit'],
            'units':[{k:u[k] for k in ('key','voice','language','text_sha256')} for u in new]}
    c.old.write_new(intent_path,intent)
    original=builder.cached_tts
    def guarded_attempt(*args,**kwargs):
        execution_gate(c)
        return original(*args,**kwargs)
    builder.cached_tts=guarded_attempt
    results=[]
    for unit in new:
        execution_gate(c)
        hit=builder.completed_cached_audio(cache,unit['key'])
        print(json.dumps({'phase':'REUSE_COMPLETED' if hit else 'DISPATCH_NEW_PUBLIC_UNIT','key':unit['key'],'voice':unit['voice'],'unit':len(results)+1,'total':len(new)}),flush=True)
        try:
            mp3=builder.bounded_tts(cache,unit['voice'],unit['text'],plan['plan_sha256'],c.V.parent/'node_modules',str(c.old.NODE),context)
            result={'key':unit['key'],'status':'COMPLETED','reused_at_start':hit is not None,
                    'audio':c.old.pin(mp3),'receipt':c.old.pin(mp3.with_suffix('.json'))}
        except Exception as error:
            result={'key':unit['key'],'status':'PENDING','reason':str(error)}
        results.append(result)
        c.old.write_new(c.C/f'AUDIO_SYNTHESIS_UNIT_{run}_{len(results)}.json',result)
        print(json.dumps({k:result[k] for k in ('key','status','reused_at_start') if k in result}),flush=True)
        # Custody above precedes a source change stop; no additional speech starts after it.
        seal_guard(c)
    c.old.write_new(c.C/f'AUDIO_SYNTHESIS_EXECUTION_{run}.json',{
        **intent,'status':'COMPLETED' if all(r['status']=='COMPLETED' for r in results) else 'PARTIAL_PENDING',
        'intent':c.old.pin(intent_path),'results':results})
    assert all(r['status']=='COMPLETED' for r in results),'PENDING_UNITS_NO_MIX'


def transport(c):
    preflight,data,plan,review,new=execution_gate(c);builder=c.builder_module()
    rows=[];attempts=[];speech=0;retry=0;uncertain=0
    for unit in new:
        key=unit['key'];mp3=builder.completed_cached_audio(builder.io_path(c.V/'audio/cache'),key)
        assert mp3 is not None,('PENDING_UNIT',key)
        receipt=c.old.read(mp3.with_suffix('.json'));verify_pin(c,{'path':str(mp3),'sha256':receipt['audio_sha256'],'bytes':receipt['bytes']})
        assert receipt['voice']==unit['voice'] and receipt['text_sha256']==unit['text_sha256']
        paths=[c.V/'audio/cache'/(key+'.json')]+list(c.old.ep(c.V/'audio/cache/bounded').rglob(key+'.json'))
        for path in paths:
            if not c.old.ep(path).exists():continue
            r=c.old.read(path);log=path.with_suffix('.transport.jsonl')
            events=[json.loads(line) for line in c.old.ep(log).read_text('utf-8').splitlines()] if c.old.ep(log).exists() else []
            sent=sum(ev.get('phase')=='speech_send_intent' for ev in events)
            speech+=sent;retry+=int('bounded_attempt' in r);uncertain+=int(r['state']=='uncertain')
            attempts.append({'key':key,'state':r['state'],'receipt':c.old.pin(path),'transport':c.old.pin(log) if c.old.ep(log).exists() else None,'speech_requests':sent})
        log=mp3.with_suffix('.transport.jsonl');events=[json.loads(line) for line in c.old.ep(log).read_text('utf-8').splitlines()]
        phases=[ev['phase'] for ev in events]
        assert 'audio_stream_ended' in phases and 'audio_returned_to_parent' in phases,('NO_AUDIO_COMPLETION_EVENT',key)
        assert phases.index('audio_stream_ended')<phases.index('audio_returned_to_parent')
        rows.append({'key':key,'audio':c.old.pin(mp3),'receipt':c.old.pin(mp3.with_suffix('.json')),
                     'transport':c.old.pin(log),'returned_bytes':receipt['bytes']})
    result={'status':'PASS_NEW_UNITS_RECEIVED','actor':c.ACTOR,'source':'v402','source_sha256':data['source_sha256'],
            'plan_sha256':plan['plan_sha256'],'preflight':preflight,'units':rows,'attempts':attempts,
            'speech_requests':speech,'completed_units':len(rows),'retry_attempts':retry,'new_uncertain_units':len({a['key'] for a in attempts if a['state']=='uncertain'}),
            'new_uncertain_attempts':uncertain,'unresolved_new_units':[],
            'uncertainty_note':'Historical uncertain receipts remain unchanged; a completed child does not assert a reply to its parent attempt.'}
    stable_new(c,c.C/'AUDIO_TRANSPORT_VALIDATION.json',result)
    print(json.dumps({k:result[k] for k in ('status','speech_requests','completed_units','retry_attempts','new_uncertain_units')}),flush=True)


def timing(c):
    preflight,data,plan,review,new=execution_gate(c);builder=c.builder_module()
    measured={};bindings=[]
    for unit in review['units']:
        mp3=builder.completed_cached_audio(builder.io_path(c.V/'audio/cache'),unit['key'])
        assert mp3 is not None,('MISSING_AUDIO',unit['key'])
        wav=c.C/'audio_timing_measurements'/(unit['key']+'.wav');wav.parent.mkdir(exist_ok=True)
        with c.old.local_only():
            if not wav.exists():builder.run_ff(str(c.old.FF),['-n','-hide_banner','-loglevel','error','-i',mp3,'-ar','48000','-ac','1','-c:a','pcm_s16le',wav])
        measured[unit['key']]=builder.wav_duration(wav)
        bindings.append({'key':unit['key'],'audio':c.old.pin(mp3),'decoded':c.old.pin(wav),'seconds':measured[unit['key']]})
    segments=[]
    for film,content in plan['films'].items():
        for segment in content['segments']:
            for language,voice in plan['voices'].items():
                duration=sum(measured[builder.cache_key(voice,cue[language])] for cue in segment['cues'])
                room=segment['duration']-.6
                segments.append({'film':film,'segment':segment['key'],'language':language,
                                 'speech_seconds':duration,'available_seconds':room,'fits':duration<=room,'slack_seconds':room-duration})
    result={'status':'PASS_TIMING_NO_SPEEDUP' if all(s['fits'] for s in segments) else 'STOP_DURATION_EXCEEDED',
            'actor':c.ACTOR,'preflight':preflight,'source':'v402','source_sha256':data['source_sha256'],
            'plan_sha256':plan['plan_sha256'],'bindings':bindings,'segments':segments,'speedup':False,'product_modified':False}
    c.old.write_new(c.C/f'AUDIO_TIMING_{time.time_ns()}.json',result)
    assert all(s['fits'] for s in segments),json.dumps([s for s in segments if not s['fits']])
    return result


def mix(c, timelines_authorized=False):
    assert timelines_authorized,'TIMELINE_WRITE_SCOPE_REQUIRED:data/film1_narration_timeline.json,data/film2_narration_timeline.json'
    preflight,data,plan,review,new=execution_gate(c);measurement=timing(c);builder=c.builder_module()
    assert not (c.C/'AUDIO_CACHE_ONLY_EXECUTION.json').exists(),'BUILD_RETURNED_ALREADY_USE_RECEIPT'
    template=c.V/'audio/script_templates.json';candidate=c.C/'AUDIO_SCRIPT_TEMPLATES_V402_FORMULA_R3.json'
    raw=candidate.read_bytes()
    if template.read_bytes()!=raw:
        assert c.old.digest(template)==c.old.digest(c.C/'baseline_audio_v401/audio/script_templates.json')
        backup=template.with_name(template.name+'.bak_v401_'+str(time.time_ns()));backup.write_bytes(template.read_bytes())
        tmp=template.with_suffix('.tmp_v402');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,template)
    assert builder.make_plan(c.V,template)==plan
    target=c.V/'audio/NARRATION_PLAN_v402_formula_final.json';stable_new(c,target,plan)
    resolved=[]
    for unit in review['units']:
        mp3=builder.completed_cached_audio(builder.io_path(c.V/'audio/cache'),unit['key'])
        resolved.append({**{k:unit[k] for k in ('key','voice','language','text_sha256','occurrences','unchanged_from_v401')},
                         'audio':c.old.pin(mp3),'receipt':c.old.pin(mp3.with_suffix('.json'))})
    c.old.write_new(c.C/'AUDIO_BUILD_INTENT.json',{'status':'INTENT','preflight':preflight,
        'plan':c.old.pin(target),'plan_sha256':plan['plan_sha256'],'cache_bindings':resolved,
        'baseline':c.old.pin(c.C/'baseline_audio_v401/BASELINE.json'),'mode':'build --cache-only',
        'timeline_write_scope_explicit':True,'timing_passed_before_product_mutation':True})
    start=time.monotonic();outcome=c.old.cli('build');seal_guard(c)
    c.old.write_new(c.C/'AUDIO_CACHE_ONLY_EXECUTION.json',{'status':'RETURNED','result':outcome,'elapsed_seconds':time.monotonic()-start,
        'preflight':preflight,'source':'v402','source_sha256':data['source_sha256'],'plan_sha256':plan['plan_sha256'],
        'mode':'build --cache-only','tts_requested':False,'network_guard':'Python sockets refused; fixed local Node probes and FFmpeg only',
        'node':c.old.pin(c.old.NODE),'ffmpeg':c.old.pin(c.old.FF),'cache_bindings':resolved})
    print(json.dumps({'status':'CACHE_ONLY_RETURNED','seconds':time.monotonic()-start}),flush=True)
