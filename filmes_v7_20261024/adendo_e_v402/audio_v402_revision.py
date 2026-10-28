"""Version-specific text and provenance gates; no network or product writes on import."""
from pathlib import Path
import copy, datetime, json, os, time

REPLACEMENTS = {
    'en': [('{proof_ladder_clean} theorems', '{proof_ladder_clean} ladder flags (named declarations), all clean'),
           ('Together:', 'The three supports count together, each with its own status:')],
    'pt-BR': [('{proof_ladder_clean} teoremas', '{proof_ladder_clean} bandeiras da escada (declarações nomeadas), todas limpas'),
              ('Juntos:', 'Os três apoios contam juntos, cada um com o seu estatuto:')],
    'fr': [('{proof_ladder_clean} théorèmes', '{proof_ladder_clean} marqueurs de l’échelle (déclarations nommées), tous propres'),
           ('Ensemble :', 'Les trois appuis comptent ensemble, chacun avec son propre statut :')],
    'zh-Hans': [('{proof_ladder_clean} 个定理', '{proof_ladder_clean} 个阶梯标志（具名声明），全部干净'),
                ('共同显示：', '三个支撑共同发挥作用，各自保有其地位：')],
}


def verify_pin(c, row):
    assert c.old.digest(row['path']) == row['sha256'], ('PIN_CHANGED', row['path'])
    if 'bytes' in row:
        assert c.old.ep(row['path']).stat().st_size == row['bytes']


def seal_guard(c):
    intake = c.old.read(c.C/'SOURCE_INTAKE.json')
    assert intake['version'] == 'v402'
    for row in intake['sources'] + [intake['order'], intake['corrections']]:
        verify_pin(c, row)
    program = next(r for r in intake['sources'] if Path(r['path']).name == 'um.py')
    seal = next(r for r in intake['sources'] if Path(r['path']).name == 'um_absoluto_selo.json')
    return {'source':'v402', 'source_sha256':program['sha256'], 'seal':seal,
            'intake':c.old.pin(c.C/'SOURCE_INTAKE.json'), 'timestamp':intake['timestamp']}


def stable_new(c, path, body):
    if path.exists():
        assert c.old.read(path) == body, ('IMMUTABLE_CANDIDATE_CHANGED', str(path))
    else:
        c.old.write_new(path, body)


def templates(c):
    preflight = c.check(); guard = seal_guard(c)
    source = c.C/'baseline_audio_v401/audio/script_templates.json'
    original = c.old.read(source); revised = copy.deepcopy(original); changes = []
    allowed = {('film1','return',0), ('film1','nature',0),
               ('film2','einstein',1), ('film2','identity',0)}
    for film, spec in revised['films'].items():
        for segment in spec['segments']:
            for language, cues in segment['text'].items():
                for index, text in enumerate(cues):
                    new = text
                    for before, after in REPLACEMENTS[language]:
                        new = new.replace(before, after)
                    if new != text:
                        assert (film,segment['key'],index) in allowed
                        changes.append({'film':film,'segment':segment['key'],'cue_index':index,
                                        'language':language,'before':text,'after':new})
                        cues[index] = new
    assert len(changes) == 16
    revised['revision'] = 'V402_ADENDO_D_FLAGS_AND_THREE_SUPPORTS'
    c.builder_module().validate_templates(revised)
    target = c.C/'AUDIO_SCRIPT_TEMPLATES_V402.json'
    stable_new(c,target,revised)
    receipt = {'status':'TEMPLATES_PREPARED_OFFLINE','actor':c.ACTOR,**guard,
               'preflight':preflight,'baseline_template':c.old.pin(source),
               'templates':c.old.pin(target),'changes':changes,'numeric_literals_added':False,
               'network_calls':0,'tts_calls':0,'delivery_modified':False}
    c.old.write_new(c.C/f'AUDIO_TEMPLATE_PREPARATION_{time.time_ns()}.json',receipt)
    print(json.dumps({'status':receipt['status'],'changed_strings':len(changes),'templates':c.old.pin(target)}))


def units(builder, plan):
    result = {}
    for film, content in plan['films'].items():
        for segment in content['segments']:
            for index, cue in enumerate(segment['cues']):
                for lang, voice in plan['voices'].items():
                    text = cue[lang]; key = builder.cache_key(voice,text)
                    row = result.setdefault(key,{'key':key,'voice':voice,'language':lang,'text':text,
                        'text_sha256':builder.sha(text.encode()),'occurrences':[]})
                    row['occurrences'].append({'film':film,'segment':segment['key'],'cue_index':index})
    return result


def data_gate(c):
    guard = seal_guard(c); d = c.old.read(c.C/'DATA_READY.json')
    assert d['status'].startswith('DATA_READY') or d['status']=='PASS', d['status']
    assert d['source']=='v402' and d['source_sha256']==guard['source_sha256']
    assert d['unexpected_scientific_differences']==0
    assert d['anchors']['all_ok'] and d['anchors']['total']==64
    for row in d['source_files']+d['data_files']+[d['seal'],d['comparison'],d['integration']]:
        verify_pin(c,row)
    comparison = c.old.read(d['comparison']['path'])
    assert comparison['status'].startswith('PASS') and comparison['unexpected_differences']==[]
    numeric_path=c.C/'PARENT_NUMERIC_REVIEW.json'
    if numeric_path.exists():
        n=c.old.read(numeric_path)
        assert n['status'].startswith('PASS') and n['unexpected_differences']==[]
        assert n['data_ready_sha256']==c.old.digest(c.C/'DATA_READY.json')
    return d


def prepare(c, isolated=False):
    preflight=c.check(); guard=seal_guard(c); builder=c.builder_module()
    base=c.C/'baseline_audio_v401'; template=c.C/'AUDIO_SCRIPT_TEMPLATES_V402.json'
    assert template.exists(), 'PREPARE_TEMPLATES_FIRST'
    if isolated:
        # Candidate data belongs to the data agent; this operation only reads it.
        root=c.C/'audio_plan_inputs'
        for name in ('hud','film1','film2'):
            src=(c.C/'candidate_v402' if name=='hud' else base)/f'data/{name}.json'
            dst=root/f'data/{name}.json';dst.parent.mkdir(parents=True,exist_ok=True)
            raw=c.old.ep(src).read_bytes()
            if dst.exists():assert dst.read_bytes()==raw,'PLAN_INPUT_ALREADY_PINNED'
            else:
                tmp=dst.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.rename(tmp,dst)
        ready=c.old.read(c.C/'SOURCE_CAPTURE.json')
        assert ready['source']=='v402' and ready['source_sha256']==guard['source_sha256']
    else:
        ready=data_gate(c); root=c.V
    previous=c.old.read(base/'audio/NARRATION_PLAN_v401_final.json')
    before=builder.hud_values(c.old.read(base/'data/hud.json'))
    after=builder.hud_values(c.old.read(root/'data/hud.json'))
    assert after['seal_version']=='v402' and after['seal_pin']==guard['source_sha256']
    assert after['seal_timestamp']==guard['timestamp']
    authorized={'proof_ladder_clean':(9561,9679),'proof_ladder_total':(9561,9679),
                'formal_count':(1430,1433),'declaration_count':(29318,29464)}
    changes={k:(before.get(k),after.get(k)) for k in set(before)|set(after) if before.get(k)!=after.get(k)}
    expected={**authorized,'theorems':authorized['proof_ladder_clean'],'n_formal':authorized['formal_count']}
    assert {k:v for k,v in changes.items() if k not in {'seal_version','seal_pin','seal_timestamp','um_sha16'}}==expected, changes
    assert after['um_sha16']==after['seal_pin'][:16]
    inputs=[c.old.pin(root/f'data/{n}.json') for n in ('hud','film1','film2')]+[c.old.pin(template),c.old.pin(c.old.BUILDER)]
    with c.old.local_only():
        plan=builder.make_plan(root,template)
    assert plan['pins']['builder_sha256']==previous['pins']['builder_sha256']
    for field in ('voices','rate','format','formats','music'):
        assert plan[field]==previous[field],field
    cue_changes=[]
    for film, content in plan['films'].items():
        prior=previous['films'][film]
        assert content['total_seconds']==prior['total_seconds']
        for seg, oldseg in zip(content['segments'],prior['segments']):
            for key in set(seg)-{'cues','speech_budget'}:
                assert seg[key]==oldseg[key],(film,seg['key'],key)
            for i,(cue,oldcue) in enumerate(zip(seg['cues'],oldseg['cues'])):
                for lang,text in cue.items():
                    if text!=oldcue[lang]:
                        assert (film,seg['key'],i) in {('film1','return',0),('film1','nature',0),('film2','einstein',1),('film2','identity',0)}
                        cue_changes.append({'film':film,'segment':seg['key'],'cue_index':i,'language':lang,'before':oldcue[lang],'after':text})
    assert len(cue_changes)==16
    old_units=units(builder,previous); current=units(builder,plan)
    for key,u in current.items():
        hit=builder.completed_cached_audio(builder.io_path(c.V/'audio/cache'),key)
        u['completed_cache']=None if hit is None else {'audio':c.old.pin(hit),'receipt':c.old.pin(hit.with_suffix('.json'))}
        u['unchanged_from_v401']=key in old_units
        if u['unchanged_from_v401']:assert hit is not None,('REUSE_MISSING',key)
    for row in inputs:verify_pin(c,row)
    seal_guard(c)
    path=c.C/('AUDIO_PLAN_V402_ISOLATED.json' if isolated else 'AUDIO_PLAN_V402_CANDIDATE.json')
    stable_new(c,path,plan)
    isolated_path=c.C/'AUDIO_PLAN_V402_ISOLATED.json'
    if not isolated and isolated_path.exists():assert c.old.read(isolated_path)==plan,'CANDIDATE_EFFECTIVE_PLAN_DIFFERED'
    count={'unique_units':len(current),'cue_occurrences':sum(len(u['occurrences']) for u in current.values()),
           'reused_v401_units':sum(u['unchanged_from_v401'] for u in current.values()),
           'new_v402_units':sum(not u['unchanged_from_v401'] for u in current.values()),
           'changed_texts_all_languages':len(cue_changes),'cache_missing':sum(u['completed_cache'] is None for u in current.values())}
    report={'schema':'iald.audio-v402-plan-review/v1','status':'PLAN_READY_PUBLIC_TEXT_REVIEW',
            'actor':c.ACTOR,**guard,'preflight':preflight,'isolated_candidate_only':isolated,
            'data_ready':None if isolated else c.old.pin(c.C/'DATA_READY.json'),
            'input_pins':inputs,'baseline':c.old.pin(base/'BASELINE.json'),'plan':c.old.pin(path),
            'plan_sha256':plan['plan_sha256'],'numeric_changes':changes,'cue_changes':cue_changes,
            'units':list(current.values()),'counts':count,'durations':{f:d['total_seconds'] for f,d in plan['films'].items()},
            'timing_budget':{f:{s['key']:s['speech_budget'] for s in d['segments']} for f,d in plan['films'].items()},
            'timing_not_measured_until_tts':True,'tts_calls_this_stage':0,'network_calls_this_stage':0,
            'delivery_modified':False,'personal_voice_excluded':True,
            'speech_version_or_pin_references':[],'formal_declaration_counts_spoken':False}
    report_path=c.C/('AUDIO_PLAN_REVIEW_ISOLATED.json' if isolated else 'AUDIO_PLAN_REVIEW.json')
    if report_path.exists():
        old=c.old.read(report_path);assert old['plan_sha256']==plan['plan_sha256']
    else:c.old.write_new(report_path,report)
    print(json.dumps({'status':report['status'],'plan_sha256':plan['plan_sha256'],'counts':count,'report':c.old.pin(report_path)}),flush=True)


def execution_gate(c):
    preflight=c.check();data=data_gate(c);builder=c.builder_module()
    review=c.old.read(c.C/'AUDIO_PLAN_REVIEW.json');plan=c.old.read(c.C/'AUDIO_PLAN_V402_CANDIDATE.json')
    verify_pin(c,review['plan'])
    with c.old.local_only():
        actual=builder.make_plan(c.V,c.C/'AUDIO_SCRIPT_TEMPLATES_V402.json')
    assert actual==plan and plan['plan_sha256']==review['plan_sha256']
    assert plan['seal_pin']==data['source_sha256']
    for row in review['input_pins']:verify_pin(c,row)
    parent=c.C/'PARENT_AUDIO_PLAN_REVIEW.json'
    if parent.exists():
        approval=c.old.read(parent)
        assert approval['status'].startswith('PASS') and approval['plan_sha256']==plan['plan_sha256']
    new=[u for u in review['units'] if not u['unchanged_from_v401']]
    assert len(new)==review['counts']['new_v402_units']
    return preflight,data,plan,review,new


def optional_pin(c, path):
    return c.old.pin(path) if path.exists() else None


def synthesize(c):
    assert not list(c.C.glob('AUDIO_FORMULA_HOLD_*.json')), 'FORMULA_REVISION_HOLD_NO_TTS_ON_PREVIOUS_PLAN'
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
            'plan':c.old.pin(c.C/'AUDIO_PLAN_V402_CANDIDATE.json'),
            'parent_payload_review':optional_pin(c,c.C/'PARENT_AUDIO_PLAN_REVIEW.json'),
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
        print(json.dumps({'phase':'REUSE_COMPLETED' if hit else 'DISPATCH_NEW_PUBLIC_UNIT','key':unit['key'],'voice':unit['voice']}),flush=True)
        try:
            mp3=builder.bounded_tts(cache,unit['voice'],unit['text'],plan['plan_sha256'],c.V.parent/'node_modules',str(c.old.NODE),context)
            result={'key':unit['key'],'status':'COMPLETED','reused_at_start':hit is not None,
                    'audio':c.old.pin(mp3),'receipt':c.old.pin(mp3.with_suffix('.json'))}
        except Exception as error:
            result={'key':unit['key'],'status':'PENDING','reason':str(error)}
        results.append(result)
        c.old.write_new(c.C/f'AUDIO_SYNTHESIS_UNIT_{run}_{len(results)}.json',result)
        print(json.dumps(result),flush=True)
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
            'speech_requests':speech,'completed_units':len(rows),'retry_attempts':retry,'new_uncertain_units':uncertain,
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
    assert not list(c.C.glob('AUDIO_FORMULA_HOLD_*.json')), 'FORMULA_REVISION_HOLD_NO_BUILD_ON_PREVIOUS_PLAN'
    assert timelines_authorized,'TIMELINE_WRITE_SCOPE_REQUIRED:data/film1_narration_timeline.json,data/film2_narration_timeline.json'
    preflight,data,plan,review,new=execution_gate(c);measurement=timing(c);builder=c.builder_module()
    assert not (c.C/'AUDIO_CACHE_ONLY_EXECUTION.json').exists(),'BUILD_RETURNED_ALREADY_USE_RECEIPT'
    template=c.V/'audio/script_templates.json';candidate=c.C/'AUDIO_SCRIPT_TEMPLATES_V402.json'
    raw=candidate.read_bytes()
    if template.read_bytes()!=raw:
        assert c.old.digest(template)==c.old.digest(c.C/'baseline_audio_v401/audio/script_templates.json')
        backup=template.with_name(template.name+'.bak_v401_'+str(time.time_ns()));backup.write_bytes(template.read_bytes())
        tmp=template.with_suffix('.tmp_v402');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,template)
    assert builder.make_plan(c.V,template)==plan
    target=c.V/'audio/NARRATION_PLAN_v402_final.json';stable_new(c,target,plan)
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
