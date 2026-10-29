"""Adendo H audio candidate. No synthesis on import or prepare; no um imports.

Run with Python -B. DATA owns hud and scientific comparison. This executor owns
only the audio/subtitle candidate and the two film timelines. All evidence is
local; synthesize requires an independently supplied exact-plan release receipt.
"""
from pathlib import Path
import argparse, contextlib, copy, hashlib, importlib.util, json, os, re
import socket, subprocess, sys, time, wave

sys.dont_write_bytecode = True
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H))
import context as ctx

S, V, G = ctx.S, ctx.V, ctx.G
B = H / 'baseline_audio_v402'
ACTOR = 'codex-video-v404-audio'
NODE = Path(r'C:\Program Files\nodejs\node.exe')
FF = V.parent / 'node_modules/@ffmpeg-installer/win32-x64/ffmpeg.exe'

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def read(path):
    return json.loads(io_path(path).read_text('utf-8-sig'))

def io_path(path):
    path=Path(str(path).removeprefix('\\\\?\\')).absolute()
    return Path('\\\\?\\'+str(path)) if os.name=='nt' else path

def digest(path):
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()

def pin(path):
    path = Path(path)
    return {'path':str(path), 'sha256':digest(path), 'bytes':io_path(path).stat().st_size}

def verify(row):
    require(digest(row['path']) == row['sha256'], 'PIN_CHANGED:' + row['path'])
    if 'bytes' in row:
        require(io_path(row['path']).stat().st_size == row['bytes'], 'SIZE_CHANGED')

def allowed(path):
    p = Path(str(path).removeprefix('\\\\?\\')).resolve()
    for root in (B, H/'audio_timing_measurements', S/'audio', S/'subs'):
        if p.is_relative_to(root.resolve()):
            return True
    if p.parent == H:
        return (p.name.startswith('AUDIO_') and p.suffix == '.json') or (p.name.startswith('audio_') and p.suffix == '.py')
    return p.parent == S/'data' and (p.name in ('film1.json','film2.json') or p.name.endswith('_narration_timeline.json'))

def put_bytes(path, raw):
    path = Path(path)
    require(allowed(path), 'WRITE_OUTSIDE_AUDIO_SCOPE:' + str(path))
    path=io_path(path)
    if path.exists():
        require(path.read_bytes() == raw, 'IMMUTABLE_FILE_CHANGED:' + str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp_audio_' + str(time.time_ns()))
    with temp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    require(temp.read_bytes() == raw, 'TEMP_VERIFICATION')
    os.rename(temp, path)

def put(path, obj):
    put_bytes(path, (json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode())

def event(name, obj):
    path = H / ('AUDIO_'+name+'_'+str(time.time_ns())+'.json')
    put(path, obj)
    return pin(path)

@contextlib.contextmanager
def offline():
    """No Python sockets, no arbitrary subprocess, only FFmpeg/local Node probe."""
    original = subprocess.Popen
    def denied(*args, **kwargs):
        raise ValueError('OFFLINE_NETWORK_DENIED')
    def process(args, *a, **kw):
        require(isinstance(args, (list,tuple)) and not kw.get('shell'), 'OFFLINE_PROCESS_DENIED')
        exe = Path(args[0]).resolve()
        probe = (exe == NODE.resolve() and len(args)==4 and args[1]=='-e' and
                 args[2]=='require.resolve(process.argv[1])' and args[3]==str(V.parent/'node_modules/msedge-tts'))
        require(exe == FF.resolve() or probe, 'OFFLINE_PROCESS_DENIED')
        return original(args, *a, **kw)
    old = (socket.socket.connect, socket.socket.connect_ex, socket.create_connection)
    socket.socket.connect = socket.socket.connect_ex = socket.create_connection = denied
    subprocess.Popen = process
    try:
        yield
    finally:
        socket.socket.connect, socket.socket.connect_ex, socket.create_connection = old
        subprocess.Popen = original

def builder():
    path = S/'audio/build_narration.py'
    spec = importlib.util.spec_from_file_location('h_audio_engine', path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    for name in ('atomic','exclusive'):
        original=getattr(mod,name)
        def checked(path,*a,_original=original,**kw):
            require(allowed(path),'ENGINE_WRITE_OUTSIDE_AUDIO_SCOPE')
            return _original(path,*a,**kw)
        setattr(mod,name,checked)
    return mod

def source_guard():
    # Parent-owned preflight: delegated implementation, not a new mission claim.
    preflight = ctx.check()
    ctx.stable_seal()
    manifest = read(H/'AUDIO_INPUT_PINS.json')
    for row in manifest['files']:
        verify(row)
    return preflight

def units(b, plan):
    result = {}
    for film, content in plan['films'].items():
        for s in content['segments']:
            for i, cue in enumerate(s['cues']):
                for lang, voice in plan['voices'].items():
                    text = cue[lang]; key = b.cache_key(voice,text)
                    row = result.setdefault(key, {'key':key,'voice':voice,'language':lang,'text':text,
                        'text_sha256':b.sha(text.encode()),'occurrences':[]})
                    row['occurrences'].append({'film':film,'segment':s['key'],'cue_index':i})
    return result

def payload_guard(b, plan, scope):
    require(plan['voices']==scope['voices'] and plan['rate']==scope['rate'] and plan['format']==scope['format'], 'VOICE_RATE_FORMAT_CHANGED')
    actual = units(b,plan)
    expected = {u['key']:u for u in scope['all_units']}
    require(len(actual)==58 and set(actual)==set(expected), 'SEVENTH_OR_CHANGED_UNIT_STOP')
    for key,u in actual.items():
        require(all(u[k]==expected[key][k] for k in ('voice','language','text','text_sha256','occurrences')), 'PAYLOAD_MISMATCH:'+key)
    baseline = read(B/'audio/NARRATION_PLAN_v402_formula_final.json')
    changes = {(r['film'],r['segment'],r['cue_index'],r['language']):r for r in scope['changes']}
    seen = set()
    for film, content in plan['films'].items():
        before = baseline['films'][film]['segments']
        require(len(content['segments'])==len(before), 'SEGMENT_COUNT_CHANGED')
        for s,old in zip(content['segments'],before):
            require(all(s[k]==old[k] for k in ('key','start','end','duration','title')), 'TIMELINE_OR_TITLE_CHANGED')
            require(len(s['cues'])==len(old['cues']), 'CUE_COUNT_CHANGED')
            for i,(cue,prior) in enumerate(zip(s['cues'],old['cues'])):
                require(set(cue)==set(prior), 'LANGUAGE_CHANGED')
                for lang,text in cue.items():
                    key=(film,s['key'],i,lang)
                    if key in changes:
                        r=changes[key]
                        require(prior[lang]==r['before'] and text==r['after'], 'VERBATIM_OR_DYNAMIC_NUMBER_CHANGED')
                        seen.add(key)
                    else:
                        require(text==prior[lang], 'UNAUTHORIZED_TEXT_OR_SCIENTIFIC_NUMBER_CHANGE')
    require(seen==set(changes), 'MISSING_APPROVED_CHANGE')
    new = scope['authorized_new_units'] + scope['additional_new_units']
    require(len(new)==6 and len({u['key'] for u in new})==6, 'SIX_ONLY')
    return actual, new

def bootstrap():
    ctx.check(); ctx.stable_seal()
    scope = read(G/'AUDIO_SCOPE_CHECK.json')
    inputs = [G/'AUDIO_SCOPE_CHECK.json',ctx.ORDER,Path(scope['order']['path']),H/'SOURCE_INTAKE.json',
              V/'audio/build_narration.py',V/'audio/script_templates.json',V/'audio/NARRATION_PLAN_v402_formula_final.json',
              ctx.W/'EDGE_BOUNDED_RETRY_APPROVAL.json']
    if not (H/'AUDIO_INPUT_PINS.json').exists():
        for k in ('builder','templates','existing_plan','order'):
            verify(scope[k])
        put(H/'AUDIO_INPUT_PINS.json', {'files':[pin(p) for p in inputs]})
    source_guard()
    rows=[]
    sources = [V/'audio/build_narration.py',V/'audio/script_templates.json',V/'audio/NARRATION_PLAN_v402_formula_final.json']
    sources += [p for p in (V/'audio/cache').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    for src in sources:
        rel=src.relative_to(V); raw=src.read_bytes(); dst=B/rel
        put_bytes(dst,raw)
        rows.append({'source':pin(src),'backup':pin(dst)})
        if rel.parts[:2]==('audio','cache'):
            put_bytes(S/rel,raw)
    put(B/'BASELINE.json', {'source':'v402','files':rows})
    raw=(B/'audio/build_narration.py').read_bytes()
    needle=b'modules = root.parent / "node_modules"'
    require(raw.count(needle)==1,'ENGINE_ADAPTATION_DRIFT')
    raw=raw.replace(needle,('modules = Path('+repr(str(V.parent/'node_modules'))+')').encode())
    decode=b'wav = mp3.with_suffix(".wav")'
    require(raw.count(decode)==1,'ENGINE_DECODE_ADAPTATION_DRIFT')
    raw=raw.replace(decode,b'wav = io_path(root / "audio" / "decoded" / (cache_key(voice, text) + ".wav")); wav.parent.mkdir(parents=True, exist_ok=True)')
    put_bytes(S/'audio/build_narration.py',raw)
    put(H/'AUDIO_ENGINE_ADAPTATION.json', {'source':pin(B/'audio/build_narration.py'),
        'candidate':pin(S/'audio/build_narration.py'),'change':'Local dependency path and isolated decoded WAV directory; transport/cache engine unchanged'})
    b=builder(); template=copy.deepcopy(read(B/'audio/script_templates.json'))
    for r in scope['changes']:
        if r['segment']=='return':
            continue # Existing proof_ladder_clean placeholder remains untouched.
        text=r['after']; fields=['flags_computed'] if r['segment']=='horizon' else ['proof_ladder_clean','flags_computed']
        tokens=list(re.finditer(r'\d+',text));require(len(tokens)==len(fields),'NUMBER_TEMPLATE_SHAPE')
        for match,field in reversed(list(zip(tokens,fields))):
            text=text[:match.start()]+'{'+field+'}'+text[match.end():]
        seg=next(s for s in template['films'][r['film']]['segments'] if s['key']==r['segment'])
        seg['text'][r['language']][r['cue_index']]=text
    b.validate_templates(template)
    put(S/'audio/script_templates.json',template)
    return scope,b

def data_guard():
    path=H/'DATA_READY.json'
    require(path.exists(),'DATA_NOT_READY_PREPARE_DEFERRED')
    data=read(path)
    require(data['status'].startswith(('PASS','DATA_READY')) and data['source']=='v404','DATA_NOT_ACCEPTED')
    require(data['source_sha256']==read(H/'SOURCE_INTAKE.json')['files']['um.py']['sha256'],'DATA_SOURCE_PIN')
    require(data.get('unexpected_scientific_differences')==0,'SCIENTIFIC_DIFFERENCES_STOP')
    rows=data.get('data_files',data.get('data_pins',[]))
    require(bool(rows),'DATA_PINS_REQUIRED')
    for row in rows:
        verify(row)
    bypath={str(Path(r['path']).resolve()):r for r in rows}
    for name in ('hud','film1','film2'):
        require(str((S/f'data/{name}.json').resolve()) in bypath,'CANDIDATE_DATA_NOT_PINNED:'+name)
    comp=data.get('comparison',data.get('numeric_comparison'))
    require(isinstance(comp,dict),'NUMERIC_COMPARISON_REQUIRED');verify(comp)
    comparison=read(comp['path'])
    require(comparison['status'].startswith('PASS') and comparison['unexpected_differences']==[],'SCIENTIFIC_DIFFERENCES_STOP')
    return data

def cache_guard(b, scope):
    for row in read(B/'BASELINE.json')['files']:
        verify(row['source']); verify(row['backup'])
        rel=Path(row['source']['path']).relative_to(V)
        if rel.parts[:2]==('audio','cache'):
            require(digest(S/rel)==row['source']['sha256'],'HISTORICAL_CACHE_CHANGED')
    newkeys={u['key'] for u in scope['authorized_new_units']+scope['additional_new_units']}
    historical={p.stem for p in (B/'audio/cache').rglob('*.json')}
    require(not newkeys.intersection(historical),'NEVER_REOPEN_HISTORICAL_KEY')
    reused=[]
    for u in scope['all_units']:
        if u['key'] in newkeys: continue
        require(u['cache_hit'] is not None and u['cache_receipt'] is not None,'REUSE_RECEIPT_MISSING')
        verify(u['cache_hit']);verify(u['cache_receipt'])
        p=b.completed_cached_audio(b.io_path(S/'audio/cache'),u['key'])
        require(p is not None and digest(p)==u['cache_hit']['sha256'],'CACHE_REUSE_CHANGED')
        r=read(p.with_suffix('.json'))
        require(r['voice']==u['voice'] and r['text_sha256']==u['text_sha256'],'CACHE_PAYLOAD_CHANGED')
        reused.append(pin(p))
    require(len(reused)==52,'EXACTLY_52_REUSES_REQUIRED')
    return reused

def prepare():
    scope,b=bootstrap(); reused=cache_guard(b,scope)
    if not (H/'DATA_READY.json').exists():
        return {'status':'CODE_AND_CACHE_READY_PREPARE_DEFERRED_DATA','reused_units':len(reused),'tts_calls':0}
    data_guard()
    with offline(): plan=b.make_plan(S,S/'audio/script_templates.json')
    require(plan['seal_version']=='v404' and plan['seal_pin']==read(H/'SOURCE_INTAKE.json')['files']['um.py']['sha256'],'PLAN_SEAL')
    actual,new=payload_guard(b,plan,scope)
    put(S/'audio/NARRATION_PLAN_v404.json',plan)
    put(H/'AUDIO_PLAN.json',{'status':'PREPARED_OFFLINE','actor':ACTOR,'plan':pin(S/'audio/NARRATION_PLAN_v404.json'),
        'templates':pin(S/'audio/script_templates.json'),'data_ready':pin(H/'DATA_READY.json'),
        'units':list(actual.values()),'new_units':new,'reused_units':52,'tts_calls':0})
    return {'status':'PREPARED_OFFLINE','unique_units':58,'new_units':6,'reused_units':52,'tts_calls':0}

def guard():
    preflight=source_guard();data_guard()
    b=builder();scope=read(G/'AUDIO_SCOPE_CHECK.json')
    verify(read(H/'AUDIO_ENGINE_ADAPTATION.json')['candidate'])
    review=read(H/'AUDIO_PLAN.json')
    for key in ('plan','templates','data_ready'):verify(review[key])
    plan=read(review['plan']['path'])
    with offline():require(b.make_plan(S,S/'audio/script_templates.json')==plan,'PLAN_CHANGED')
    require(plan['seal_version']=='v404' and plan['seal_pin']==read(H/'SOURCE_INTAKE.json')['files']['um.py']['sha256'],'PLAN_SEAL')
    actual,new=payload_guard(b,plan,scope);cache_guard(b,scope)
    return b,plan,new,preflight

def release_guard(plan):
    r=read(H/'AUDIO_EXECUTION_RELEASE.json')
    require(r['status']=='RELEASED_FOR_EXECUTION' and r['actor']!=ACTOR,'PARENT_RELEASE_REQUIRED')
    require(r['plan_sha256']==plan['plan_sha256'] and r['source']=='v404','RELEASE_PLAN_CHANGED')
    verify(r['audio_plan']);require(r['audio_plan']['sha256']==digest(H/'AUDIO_PLAN.json'),'RELEASE_RECEIPT_CHANGED')
    return pin(H/'AUDIO_EXECUTION_RELEASE.json')

def synthesize():
    b,plan,new,pf=guard();release=release_guard(plan)
    auth=b.load_bounded_authorization(ctx.W/'EDGE_BOUNDED_RETRY_APPROVAL.json')
    require(auth['limit']==2,'RETRY_LIMIT')
    intent=event('SYNTHESIS_INTENT',{'status':'INTENT','actor':ACTOR,'preflight':pf,'release':release,
        'plan_sha256':plan['plan_sha256'],'units':new,'bounded_authorization':auth,
        'direct_cost_estimate':read(G/'AUDIO_SCOPE_CHECK.json')['cost'],'invoice':False})
    original=b.cached_tts
    permitted={u['key']:u for u in new}
    def checked(cache,voice,text,*args,**kwargs):
        guard();release_guard(plan)
        key=b.cache_key(voice,text)
        require(key in permitted and permitted[key]['text']==text,'SEVENTH_UNIT_REFUSED')
        require(Path(str(cache).removeprefix('\\\\?\\')).resolve().is_relative_to((S/'audio/cache').resolve()),'CACHE_DESTINATION_REFUSED')
        return original(cache,voice,text,*args,**kwargs)
    b.cached_tts=checked
    for u in new:
        guard()
        try:
            mp3=b.bounded_tts(b.io_path(S/'audio/cache'),u['voice'],u['text'],plan['plan_sha256'],V.parent/'node_modules',str(NODE),auth)
            event('SYNTHESIS_RETURN',{'status':'COMPLETED','intent':intent,'key':u['key'],'audio':pin(mp3),'receipt':pin(mp3.with_suffix('.json'))})
        except BaseException as exc:
            event('SYNTHESIS_STOP',{'status':'PENDING_RECONCILIATION','intent':intent,'key':u['key'],'error_type':type(exc).__name__})
            raise
        ctx.stable_seal()
    return {'status':'SIX_UNITS_RESOLVED','invoice':False,'actual_provider_invoice':'NOT_AVAILABLE'}

def timing():
    b,plan,_,_=guard();durations={};bindings=[]
    for u in units(b,plan).values():
        mp3=b.completed_cached_audio(b.io_path(S/'audio/cache'),u['key']);require(mp3 is not None,'AUDIO_PENDING')
        wav=H/'audio_timing_measurements'/(u['key']+'.wav')
        wav.parent.mkdir(exist_ok=True)
        with offline():
            b.run_ff(str(FF),['-y','-hide_banner','-loglevel','error','-i',mp3,'-ar','48000','-ac','1','-c:a','pcm_s16le',wav])
        durations[u['key']]=b.wav_duration(wav)
        bindings.append({'key':u['key'],'audio':pin(mp3),'wav':pin(wav),'seconds':durations[u['key']]})
    rows=[]
    for name,f in plan['films'].items():
        for s in f['segments']:
            for lang,voice in plan['voices'].items():
                seconds=sum(durations[b.cache_key(voice,c[lang])] for c in s['cues'])
                rows.append({'film':name,'segment':s['key'],'language':lang,'seconds':seconds,'room':s['duration']-.6,'fits':seconds<=s['duration']-.6})
    ok=all(r['fits'] for r in rows)
    event('TIMING',{'status':'PASS' if ok else 'STOP_DURATION_EXCEEDED','segments':rows,'bindings':bindings,'speedup':False,'plan_sha256':plan['plan_sha256']})
    require(ok,'STOP_DURATION_EXCEEDED_NO_SPEEDUP');return {'status':'PASS_TIMING','segments':len(rows)}

def mix():
    b,plan,_,pf=guard();release=release_guard(plan);timing()
    event('MIX_INTENT',{'status':'INTENT','preflight':pf,'release':release,'plan_sha256':plan['plan_sha256'],'cache_only':True})
    def no_tts(*a,**kw):raise ValueError('MIX_TTS_FORBIDDEN')
    b.cached_tts=b.bounded_tts=no_tts
    with offline():b.build(plan,S,enable_tts=True,cache_only=True,node=str(NODE),ffmpeg=str(FF))
    ctx.stable_seal();return validate()

def validate():
    b,plan,new,_=guard();build=read(S/'audio/NARRATION_BUILD.json')
    require(build['status']=='COMPLETED' and not build['tts'] and not build['pending'] and not build['tts_inflight'],'BUILD_NOT_COMPLETE')
    require(build['plan_sha256']==plan['plan_sha256'],'BUILD_PLAN')
    evidence=[];transports=[]
    for u in new:
        mp3=b.completed_cached_audio(b.io_path(S/'audio/cache'),u['key']);require(mp3 is not None,'NEW_AUDIO_PENDING')
        r=read(mp3.with_suffix('.json'));log=mp3.with_suffix('.transport.jsonl')
        require(r['voice']==u['voice'] and r['text_sha256']==u['text_sha256'],'TRANSPORT_PAYLOAD')
        phases=[json.loads(line)['phase'] for line in log.read_text('utf-8').splitlines()]
        require('audio_stream_ended' in phases and 'audio_returned_to_parent' in phases,'TRANSPORT_COMPLETION_MISSING')
        require(phases.index('audio_stream_ended')<phases.index('audio_returned_to_parent'),'TRANSPORT_ORDER')
        transports.append({'audio':pin(mp3),'receipt':pin(mp3.with_suffix('.json')),'log':pin(log)})
    for name,f in plan['films'].items():
        tl=read(S/f'data/{name}_narration_timeline.json')
        require(tl['status']=='AUDIO_MEASURED' and tl['plan_sha256']==plan['plan_sha256'] and tl['segments']==f['segments'],'TIMELINE_CHANGED')
        require(not tl['speedup'] and not tl['music'],'SPEEDUP_OR_MUSIC')
        for lang in plan['voices']:
            levels=tl['loudness'][lang]
            for ext,hashval,measurement in [('wav',levels['sha256'],levels['after']),('m4a',levels['aac']['sha256'],levels['aac']['measurement'])]:
                p=S/f'audio/{name}/{lang}.{ext}';require(digest(p)==hashval,'MEDIA_CHANGED')
                require(abs(float(measurement['input_i'])+16)<=1 and float(measurement['input_tp'])<0,'LOUDNESS_OR_PEAK')
                evidence.append(pin(p))
            with wave.open(str(S/f'audio/{name}/{lang}.wav'),'rb') as w:
                require(w.getframerate()==48000 and w.getnchannels()==1 and w.getnframes()/w.getframerate()==f['total_seconds'],'WAV_FORMAT_OR_DURATION')
        sub=S/'subs'/name.replace('film','filme')
        for lang in b.LANGS:
            variants=[(sub/(lang+'.vtt'),tl['cues']['pt-BR' if lang=='pt-BR' else 'en'])]
            variants += [(sub/('sync-'+v)/(lang+'.vtt'),tl['cues'][v]) for v in plan['voices']]
            for path,cues in variants:
                require(path.read_bytes()==b.vtt([{**c,'text':c['translations'][lang]} for c in cues],lang),'SUBTITLE_CHANGED')
                evidence.append(pin(path))
    result={'status':'PASS_BUILDER_READY_FOR_INDEPENDENT_REVIEW','actor':ACTOR,'source':'v404',
        'source_sha256':plan['seal_pin'],'plan_sha256':plan['plan_sha256'],'media_subtitles':evidence,
        'transports':transports,'perceptual_audition':False,'invoice':False,'integration':'CANDIDATE_ONLY_PARENT_PROJECTS_TO_V_AUDIT',
        'cost_estimate':read(G/'AUDIO_SCOPE_CHECK.json')['cost'],'actual_provider_invoice':'NOT_AVAILABLE'}
    receipt=event('DELIVERY_D_V404',result)
    put(H/'AUDIO_READY.json',{'status':'AUDIO_READY','actor':ACTOR,'source':'v404','source_sha256':plan['seal_pin'],
        'plan_sha256':plan['plan_sha256'],'receipt':receipt,'integration':'CANDIDATE_ONLY','production_modified':False})
    return {'status':result['status'],'receipt':receipt}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','guard','synthesize','timing','mix','validate'])
    action=parser.parse_args().action
    result=globals()[action]()
    if action=='guard':result={'status':'PASS_EXACT_SIX','plan_sha256':result[1]['plan_sha256']}
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
