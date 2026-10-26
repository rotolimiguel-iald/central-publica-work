"""Local-only v400 narration rebind; preserves original synthesis evidence."""
from pathlib import Path
import collections, contextlib, datetime, hashlib, io, json, os, runpy, socket, re
import subprocess, sys, time, uuid, wave

W = Path(__file__).resolve().parent.parent
A = W / 'adendo_a'
R = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
BUILDER = R / 'audio/build_narration.py'
NODE = Path(r'C:\Program Files\nodejs\node.exe')
FF = R.parent / 'node_modules/@ffmpeg-installer/win32-x64/ffmpeg.exe'
sys.path.insert(0, str(W))
import mission

def ep(p):
    return Path('\\\\?\\' + str(Path(str(p).removeprefix('\\\\?\\')).absolute()))

def digest(p):
    return hashlib.sha256(ep(p).read_bytes()).hexdigest()

def read(p):
    return json.loads(ep(p).read_text('utf-8-sig'))

def pin(p):
    p = Path(str(p).removeprefix('\\\\?\\'))
    return {'path': str(p), 'sha256': digest(p), 'bytes': ep(p).stat().st_size}

def write_new(p, obj):
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
    p = ep(p)
    assert not p.exists(), str(p)
    temp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    with temp.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    assert temp.stat().st_size == len(data)
    os.rename(temp, p)

def preflight():
    p = mission.project()
    t = next(t for t in p['projection']['active'] if t['id'] == 'ADENDO_D')
    assert t['lease']['owner'] == 'codex-video-audio'
    c = mission.call({'operation': 'check', 'actor': {'id': 'codex-video-audio', 'kind': 'agent'},
        'expected_revision': p['receipt']['revision'], 'projection_sha256': p['projection_sha256'],
        'task_id': 'ADENDO_D', 'lease_id': t['lease']['id'], 'max_chars': 100000})
    assert c['ready']
    return c

def gates():
    d = read(A / 'DATA_READY.json'); n = read(A / 'NUMERIC_COMPARISON.json')
    assert d['status'] == 'DATA_READY_FOR_V400_RENDER' and d['scientific_differences'] == 0
    assert n['status'] == 'PASS_EXACT_SCIENTIFIC_VALUES_UNCHANGED' and not n['unexpected_differences']
    assert n['anchors']['count'] == 64 and n['anchors']['all_ok'] and n['anchors']['identical_to_baseline']
    assert d['source'] == n['source'] == 'v400' and d['source_sha256'] == n['source_sha256']
    for e in d['data_pins'] + d['source_pins'] + [d['seal'], d['numeric_comparison']]:
        assert digest(e['path']) == e['sha256'], e['path']
    return d

@contextlib.contextmanager
def local_only():
    """Block Python sockets and permit only known local Node probes/FFmpeg."""
    popen = subprocess.Popen; connect = socket.socket.connect
    connect_ex = socket.socket.connect_ex; create = socket.create_connection
    def denied(*a, **k):
        raise RuntimeError('OFFLINE_SOCKET_DENIED')
    def guarded(args, *a, **kw):
        assert isinstance(args, (list, tuple)) and not kw.get('shell'), 'SUBPROCESS_FORM_REFUSED'
        exe = Path(args[0]).resolve()
        assert exe in (NODE.resolve(), FF.resolve()), ('SUBPROCESS_REFUSED', str(exe))
        assert not any('://' in str(x) for x in args), 'NETWORK_PROTOCOL_REFUSED'
        if exe == NODE.resolve():
            assert args[1] == '-e' and args[2] in (
                'require.resolve(process.argv[1])',
                'process.stdout.write(require(process.argv[1]).path)'), 'NODE_CODE_REFUSED'
        return popen(args, *a, **kw)
    socket.socket.connect = socket.socket.connect_ex = socket.create_connection = denied
    subprocess.Popen = guarded
    try:
        yield
    finally:
        subprocess.Popen = popen; socket.socket.connect = connect
        socket.socket.connect_ex = connect_ex; socket.create_connection = create

def cli(command):
    old = sys.argv
    sys.argv = [str(BUILDER), command, '--root', str(R)]
    if command == 'build':
        sys.argv += ['--cache-only', '--node', str(NODE), '--ffmpeg', str(FF)]
    output = io.StringIO()
    try:
        with local_only(), contextlib.redirect_stdout(output):
            runpy.run_path(str(BUILDER), run_name='__main__')
    finally:
        sys.argv = old
    return json.loads(output.getvalue())

def units_verified():
    review = read(A / 'AUDIO_REUSE_REVIEW.json')
    for u in review['units']:
        for e in [u['selected_completed_cache']['receipt'], u['selected_completed_cache']['audio']]:
            assert digest(e['path']) == e['sha256'], e['path']
        for old in u['prior_receipts_preserved']:
            assert digest(old['receipt']['path']) == old['receipt']['sha256']
    return review

def prepare():
    check = preflight(); d = gates(); reuse = units_verified()
    plan = cli('plan'); previous = read(R / 'audio/NARRATION_PLAN_v399_final.json')
    assert plan['seal_version'] == d['source'] and plan['seal_pin'] == d['source_sha256']
    assert plan['films'] == previous['films'], 'TEXT_OR_TIMING_CHANGED_STOP'
    for k in ['voices', 'rate', 'format', 'formats', 'music']:
        assert plan[k] == previous[k], ('CONTRACT_CHANGED_STOP', k)
    allowed = {'seal_version', 'seal_pin', 'seal_timestamp', 'plan_sha256', 'pins'}
    assert {k:v for k,v in plan.items() if k not in allowed} == {k:v for k,v in previous.items() if k not in allowed}
    for k,v in plan['pins'].items():
        if k != 'hud_sha256': assert v == previous['pins'][k], ('UNEXPECTED_INPUT_CHANGE', k)
    write_new(A / 'AUDIO_PLAN_V400_CANDIDATE.json', plan)
    inputs = [pin(BUILDER), pin(R/'audio/script_templates.json'), pin(R/'data/hud.json'),
              pin(R/'data/film1.json'), pin(R/'data/film2.json'), pin(A/'DATA_READY.json'),
              pin(A/'NUMERIC_COMPARISON.json'), pin(A/'AUDIO_REUSE_REVIEW.json')]
    write_new(A / 'AUDIO_REBIND_PREPARED.json', {'status':'PASS_READY_CACHE_ONLY', 'source':d['source'],
        'source_sha256':d['source_sha256'], 'preflight':check, 'inputs':inputs,
        'plan_sha256':plan['plan_sha256'], 'previous_plan_sha256':previous['plan_sha256'],
        'all_four_language_texts_and_timings_exactly_equal':True, 'units_verified':len(reuse['units']),
        'network_calls':0, 'tts_calls':0})
    print(json.dumps({'status':'PREPARED', 'plan_sha256':plan['plan_sha256']}), flush=True)

def build():
    check = preflight(); gates(); reuse = units_verified(); prepared = read(A/'AUDIO_REBIND_PREPARED.json')
    for e in prepared['inputs']: assert digest(e['path']) == e['sha256']
    plan = cli('plan'); assert plan == read(A/'AUDIO_PLAN_V400_CANDIDATE.json')
    paths = [R/'audio/NARRATION_BUILD.json',R/'audio/NARRATION_PROGRESS.json']
    paths += list((R/'subs').rglob('*.vtt'))
    for film in ('film1','film2'):
        paths += [R/f'data/{film}_narration_timeline.json']
        paths += list((R/'audio'/film).glob('*.wav')) + list((R/'audio'/film).glob('*.m4a'))
    for u in reuse['units']:
        p = Path(u['selected_completed_cache']['audio']['path']).with_suffix('.wav')
        if ep(p).exists(): paths.append(p)
    paths = sorted(set(paths), key=str)
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backups=[]
    for p in paths:
        raw=ep(p).read_bytes(); dest=p.with_name(p.name+'.bak_'+stamp)
        with ep(dest).open('xb') as f: f.write(raw)
        assert digest(dest)==hashlib.sha256(raw).hexdigest()
        backups.append({'original':pin(p),'backup':pin(dest)})
    write_new(A/'AUDIO_REBIND_BACKUPS.json',{'preflight':check,'files':backups})
    write_new(R/'audio/NARRATION_PLAN_v400_final.json',plan)
    print(json.dumps({'status':'BACKUPS_COMPLETE_BUILD_CACHE_ONLY','files':len(backups)}),flush=True)
    start=time.monotonic(); outcome=cli('build')
    write_new(A/'AUDIO_CACHE_ONLY_EXECUTION.json',{'status':'RETURNED','source':plan['seal_version'],
        'source_sha256':plan['seal_pin'],'result':outcome,'elapsed_seconds':time.monotonic()-start,
        'mode':'build --cache-only','node':pin(NODE),'ffmpeg':pin(FF), 'network_guard':'Python sockets denied; only fixed local Node probes and local FFmpeg subprocesses allowed',
        'tts_requested':False,'retry_authorization_used':False,'preflight':check})
    print(json.dumps(outcome),flush=True)

def validate():
    check=preflight(); d=gates(); reuse=units_verified(); plan=cli('plan')
    assert plan==read(R/'audio/NARRATION_PLAN_v400_final.json')
    assert plan==read(A/'AUDIO_PLAN_V400_CANDIDATE.json')
    build=read(R/'audio/NARRATION_BUILD.json')
    assert build['status']=='COMPLETED' and not build['tts'] and not build['tts_inflight'] and not build['pending']
    assert build['plan_sha256']==plan['plan_sha256']
    progress=read(R/'audio/NARRATION_PROGRESS.json')
    assert progress['cache_only'] and progress['completed']==progress['total_unique_units']==60 and not progress['pending']
    assert progress['authorization_sha256'] is None
    previous=read(A/'AUDIO_REBIND_BACKUPS.json')
    bypath={e['original']['path']:e for e in previous['files']}
    unchanged=[]; changed=[]
    for e in previous['files']:
        assert digest(e['backup']['path'])==e['original']['sha256']
        current=pin(e['original']['path'])
        (unchanged if current['sha256']==e['original']['sha256'] else changed).append(current)
    allowed_changes={str(R/'audio/NARRATION_BUILD.json'),str(R/'audio/NARRATION_PROGRESS.json'),
                     str(R/'data/film1_narration_timeline.json'),str(R/'data/film2_narration_timeline.json')}
    assert all(e['path'] in allowed_changes for e in changed), ('AUDIO_OR_CAPTION_BYTES_CHANGED',changed)
    waves=[]; media=[]; timelines=[]
    for film in ('film1','film2'):
        tp=R/f'data/{film}_narration_timeline.json'; tl=read(tp)
        old=read(bypath[str(tp)]['backup']['path'])
        assert {k:v for k,v in old.items() if k!='plan_sha256'}=={k:v for k,v in tl.items() if k!='plan_sha256'}
        assert tl['status']=='AUDIO_MEASURED' and tl['plan_sha256']==plan['plan_sha256']
        assert build['reports'][film]['status']=='AUDIO_MEASURED'
        assert tl['loudness']==build['reports'][film]['loudness']
        assert not tl['music'] and not tl['speedup']
        for lang in ('en','pt-BR'):
            last=0
            for cue in tl['cues'][lang]:
                assert cue['start']>=last and cue['end']>cue['start'] and cue['end']<=tl['total_seconds']
                last=cue['end']
            m=tl['loudness'][lang]
            for ext,h,measure in [('wav',m['sha256'],m['after']),('m4a',m['aac']['sha256'],m['aac']['measurement'])]:
                path=R/f'audio/{film}/{lang}.{ext}'; assert digest(path)==h
                assert abs(float(measure['input_i'])+16)<=1 and float(measure['input_tp'])<0
                media.append({**pin(path),'film':film,'language':lang,'measured_lufs':float(measure['input_i']),
                              'measured_true_peak_dbtp':float(measure['input_tp']),'byte_identical_to_v399_mix':True})
            with wave.open(str(R/f'audio/{film}/{lang}.wav'),'rb') as wav:
                duration=wav.getnframes()/wav.getframerate()
                assert duration==tl['total_seconds'] and wav.getframerate()==48000 and wav.getnchannels()==1
                waves.append({'film':film,'language':lang,'seconds':duration,'rate':wav.getframerate(),
                              'channels':wav.getnchannels(),'sample_width':wav.getsampwidth()})
        timelines.append(pin(tp))
    subtitles=[]
    def seconds(text):
        a,b,c=text.split(':');return int(a)*3600+int(b)*60+float(c)
    for p in sorted((R/'subs').rglob('*.vtt')):
        text=p.read_text('utf-8-sig'); assert text.startswith('WEBVTT')
        film='film1' if p.relative_to(R/'subs').parts[0]=='filme1' else 'film2'
        last=0; count=0
        for start,end in re.findall(r'(\d+:\d\d:\d\d\.\d{3}) --> (\d+:\d\d:\d\d\.\d{3})',text):
            start,end=seconds(start),seconds(end)
            assert start>=last and end>start and end<=plan['films'][film]['total_seconds']
            last=end; count+=1
        assert count>0 and digest(p)==bypath[str(p)]['original']['sha256']
        subtitles.append({**pin(p),'cues':count,'byte_identical_to_previous':True})
    assert len(subtitles)==26
    execution=read(A/'AUDIO_CACHE_ONLY_EXECUTION.json');assert not execution['tts_requested']
    receipt={'schema':'iald.delivery-d.v400/v1','status':'PASS_BUILDER_READY_FOR_INDEPENDENT_REVIEW',
        'source':d['source'],'source_sha256':d['source_sha256'],'actor':'codex-video-audio',
        'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preflight':check,
        'plan_current':True,'plan_sha256':plan['plan_sha256'],'plan':pin(R/'audio/NARRATION_PLAN_v400_final.json'),
        'builder':pin(BUILDER),'helper':pin(Path(__file__)),'templates':pin(R/'audio/script_templates.json'),
        'data_ready':pin(A/'DATA_READY.json'),'numeric_comparison':pin(A/'NUMERIC_COMPARISON.json'),
        'build':pin(R/'audio/NARRATION_BUILD.json'),'progress':pin(R/'audio/NARRATION_PROGRESS.json'),
        'execution':pin(A/'AUDIO_CACHE_ONLY_EXECUTION.json'),'backups':pin(A/'AUDIO_REBIND_BACKUPS.json'),
        'historical_lineage':{'previous_synthesis':'v399 and prior authorized attempts; original receipts preserved',
                              'reuse_review':pin(A/'AUDIO_REUSE_REVIEW.json')},
        'cache_bindings':[{'key':u['key'],'voice':u['voice'],'text_sha256':u['text_sha256'],
                          'completed_cache':u['selected_completed_cache']} for u in reuse['units']],
        'counts':{'unique_units':60,'cue_occurrences':76,'root_caches':51,'authorized_child_caches':9,
                  'vtt_files':26,'wav_aac_files':8,'backed_up_files':len(previous['files']),
                  'unchanged_backed_up_files':len(unchanged),'changed_metadata_files':len(changed)},
        'changed_metadata_files':changed,'media':media,'wave_measurements':waves,'subtitles':subtitles,'timelines':timelines,
        'validation':{'texts_all_four_languages_unchanged':True,'timings_unchanged':True,'caption_nonoverlap':True,
                      'audio_bytes_unchanged':True,'clips_and_historical_receipts_unchanged':True,
                      'loudness_remeasured_by_cache_only_builder':True,'music':False,'speedup':False},
        'network':{'tts_requested':False,'tts_sent':False,'retry_authorization_used':False,
                   'mode':'cache-only','guard':'Python sockets denied; fixed local Node probes and local FFmpeg only'},
        'limits':['Not perceptually auditioned. Human timbre/pronunciation assessment not claimed.',
                  'Personal voice previews excluded and unchanged.',
                  'Builder submission only, no self-acceptance, full-adendo approval or publication.']}
    write_new(R/'audit/DELIVERY_D_V400.json',receipt)
    write_new(A/'AUDIO_D_V400_READY.json',{'status':'READY_FOR_REVIEW','source':d['source'],
        'source_sha256':d['source_sha256'],'receipt':pin(R/'audit/DELIVERY_D_V400.json'),
        'plan_sha256':plan['plan_sha256'],'counts':receipt['counts']})
    print(json.dumps({'status':'VALIDATED','receipt':pin(R/'audit/DELIVERY_D_V400.json'),'counts':receipt['counts']}),flush=True)

def submit():
    check=preflight(); receipt=R/'audit/DELIVERY_D_V400.json'; data=read(receipt)
    assert data['plan_sha256']==cli('plan')['plan_sha256'];gates();units_verified()
    payload={'operation':'submit',**mission.current('codex-video-audio'),'task_id':'ADENDO_D',
        'lease_id':check['lease_id'],'event_id':'ordem022-adendo-d-v400-cache-only-submit-20261025',
        'evidence':[{'path':str(receipt),'sha256':digest(receipt)}]}
    write_new(A/'ADENDO_D_SUBMIT_REQUEST.json',payload)
    outcome=mission.call(payload);write_new(A/'ADENDO_D_SUBMIT_RESULT.json',outcome)
    print(json.dumps(outcome,ensure_ascii=False),flush=True)

if __name__=='__main__':
    {'prepare':prepare,'build':build,'validate':validate,'submit':submit}[sys.argv[1]]()
