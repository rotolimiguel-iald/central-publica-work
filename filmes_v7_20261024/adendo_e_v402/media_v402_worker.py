"""Offline ADENDO E worker. Launch only after the coordinator's explicit signal.

Reuses the v400 pipeline and its Namespace.action repair. No renderer, TTS,
source/data/audio edits, public finalizer or mission submission is invoked here.
"""
from pathlib import Path
import argparse, ast, json, os, runpy, subprocess, sys, time

C = Path(__file__).resolve().parent
W = C.parent
R = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
OLD = W / 'adendo_a/media_v400_worker.py'
legacy = runpy.run_path(str(OLD))
M = legacy['M']
G = M['encode_film'].__globals__
load, pin, sha, save_original = M['load'], M['pin'], M['sha'], M['jsave']
mission, collect = legacy['mission'], legacy['collect']
BASE = C / 'MEDIA_V402_BASELINE.json'
STATE = C / 'MEDIA_WATCH.json'
LOCK = C / 'MEDIA_V402_WORKER.lock'
TASK, ACTOR, VERSION = 'V402_MEDIA', 'codex-video-web', 'v402'
baseline = None
prior_elapsed = 0.0
audio_binding = None
done, prepared, completed_outputs = {}, {}, {}
timings = []
assets = False
last_state = None
started = time.monotonic()
options = None

def verify(item):
    path = Path(item.get('file', item.get('path', '')))
    assert path.is_file() and path.stat().st_size == item['bytes'] and sha(path) == item['sha256'], 'Changed pin: ' + str(path)

def preflight():
    p = mission['project']()
    task = next(t for t in p['projection']['active'] if t['id'] == TASK)
    assert task['status'] == 'working' and task['lease']['owner'] == ACTOR
    result = mission['call']({'operation':'check','actor':{'id':ACTOR,'kind':'agent'},
             'task_id':TASK,'lease_id':task['lease']['id'],'expected_revision':p['receipt']['revision'],
             'projection_sha256':p['projection_sha256'],'max_chars':100000})
    assert result['ready']; return result

def canonical_guard():
    capture = load(C/'SOURCE_CAPTURE.json')
    assert capture['source'] == VERSION
    seal = capture['canonical_seal']; verify(seal)
    content = load(Path(seal.get('path', seal.get('file'))))
    assert content['um_version'] == VERSION and content['sha256']['um.py'] == capture['source_sha256'], 'STOP: canonical source advanced'
    return capture

def save(path, value):
    if isinstance(value, dict):
        source_pin = baseline['source_sha256'] if baseline else load(C/'SOURCE_CAPTURE.json')['source_sha256']
        value = {**value,'source':VERSION,'source_sha256':source_pin,'adendo_worker':pin(Path(__file__))}
    save_original(path, value)

def state(status, **extra):
    global last_state
    value = {'status':status,'completed':done,'prepared':prepared,'completed_outputs':completed_outputs,
             'assets_complete':assets,'timings':timings,**extra}
    signature = json.dumps(value, sort_keys=True)
    if signature != last_state:
        save(STATE, {**value,'elapsed_seconds':prior_elapsed+time.monotonic()-started})
        last_state = signature; print(status, extra, flush=True)

def readiness():
    capture = canonical_guard()
    if not options.data_ready.exists(): return None
    ready = load(options.data_ready)
    assert ready.get('source') == VERSION and ready.get('source_sha256') == capture['source_sha256'], 'STOP: DATA_READY source mismatch'
    assert ready['status'] == 'DATA_READY', 'DATA_READY is not approved'
    assert ready.get('unexpected_scientific_differences') == 0
    anchors = ready['anchors']
    assert anchors['total'] >= 64 and anchors['all_ok'] is True
    comparison_pin = ready['comparison']; verify(comparison_pin)
    comparison = load(Path(comparison_pin.get('path', comparison_pin.get('file'))))
    assert comparison['source'] == VERSION and comparison['source_sha256'] == capture['source_sha256']
    assert comparison['status'] == 'PASS' and comparison.get('unexpected_differences') == [], 'STOP: unauthorized numeric difference'
    parent_path = C/'PARENT_NUMERIC_REVIEW.json'
    if not parent_path.exists(): return None
    parent = load(parent_path)
    assert parent['status'] == 'PASS_WITH_SCOPE' and parent['actor'] == 'codex-video-v7'
    assert parent['source'] == VERSION and parent['source_sha256'] == capture['source_sha256']
    assert parent['unexpected_differences'] == [] and parent['anchors_all_ok'] is True and parent['anchors'] >= 64
    assert parent['data_ready_sha256'] == sha(options.data_ready), 'STOP: parent numeric review pins another DATA_READY'
    # Rawls owns scientific comparison/selectors. This consumer binds their receipt.
    frozen = ready['data_files'] + ready['source_files'] + [ready['seal'], capture['canonical_seal'],
              pin(options.data_ready), comparison_pin, ready['integration'], ready['root_provenance'],
              pin(parent_path), pin(C/'SOURCE_CAPTURE.json')]
    for item in frozen: verify(item)
    hud = load(R/'data/hud.json')
    assert hud['seal_version'] == VERSION and hud['seal_pin'] == capture['source_sha256']
    return ready, frozen

def duration_contract():
    for film, expected in ((1,224),(2,360)):
        _, _, actual = M['timeline'](R,film)
        assert actual == expected, 'STOP: film duration changed'


def verify_intent(intent):
    assert intent['status'] == 'INTENT_BEFORE_SINGLE_BROWSER_PIPELINE'
    for key, expected in (('data_ready',options.data_ready),('audio_ready',options.audio_ready),
                          ('numeric_review',C/'PARENT_NUMERIC_REVIEW.json'),('media_prepared',C/'MEDIA_PREPARED.json')):
        verify(intent[key])
        assert Path(intent[key].get('path',intent[key].get('file'))).resolve() == expected.resolve()


def launch_guard():
    assert options.start_authorized, 'Await explicit coordinator signal; --start-authorized required'
    path = C/'MEDIA_GO.json'
    assert path.exists(), 'Await explicit coordinator GO receipt'
    go = load(path); capture = canonical_guard()
    assert go['status'] == 'GO' and go['actor'] in (ACTOR,'codex-video-v7')
    assert go['authorization'] == 'explicit_parent_go' and go['authorization_text'].strip()
    assert go['source'] == VERSION and go['source_sha256'] == capture['source_sha256']
    for key, expected in (('worker',Path(__file__)),('render_intent',C/'RENDER_INTENT.json'),
                          ('data_ready',options.data_ready),('audio_ready',options.audio_ready)):
        verify(go[key]); assert Path(go[key].get('path',go[key].get('file'))).resolve() == expected.resolve()
    tests = load(C/'MEDIA_WORKER_TESTS.json')
    assert tests['status'] == 'PASS' and tests['worker'] == pin(Path(__file__))
    assert tests['helper'] == pin(R/'cinema/media_v7.py')
    contract_tests = load(C/'MEDIA_READY_CONTRACT_TESTS.json')
    assert contract_tests['status'] == 'PASS' and contract_tests['worker'] == pin(Path(__file__))
    intent = load(C/'RENDER_INTENT.json')
    verify_intent(intent)
    assert intent['source'] == VERSION and intent['source_sha256'] == capture['source_sha256']
    assert intent['render_closure'] == collect(R), 'STOP: GO dependency freeze changed'
    assert readiness() is not None, 'Approved DATA_READY and parent numeric review required'
    duration_contract()
    return pin(path)


def initialize():
    global baseline, audio_binding, done, prepared, assets, timings, completed_outputs, prior_elapsed
    preflight()
    backup = load(C/'MEDIA_V401_BACKUP.json')
    assert backup['status'] == 'PASS_PRESERVED_BYTES' and backup['media_count'] == 16 and backup['image_count'] == 25
    for row in backup['files']: verify(row['backup'])
    if BASE.exists():
        baseline = load(BASE); guard()
        previous = load(STATE)
        prior_elapsed = previous.get('elapsed_seconds',0)
        archived = C/('MEDIA_WATCH_BEFORE_RESUME_'+str(time.time_ns())+'.json')
        M['atomic'](archived,STATE.read_bytes())
        assert sha(archived) == sha(STATE)
        assert previous['source'] == VERSION and previous['source_sha256'] == baseline['source_sha256']
        for outputs in previous.get('completed_outputs', {}).values():
            for item in outputs: verify(item)
        done, prepared = previous.get('completed', {}), previous.get('prepared', {})
        for item in list(done.values()) + list(prepared.values()): verify(item)
        assets, timings = previous.get('assets_complete', False), previous.get('timings', [])
        completed_outputs = previous.get('completed_outputs', {})
        # A status alone is never a checkpoint: every completed action needs pins.
        assert all(k in completed_outputs for k in done)
        assert not assets or 'assets' in completed_outputs
        if (C/'MEDIA_AUDIO_BINDING.json').exists(): audio_binding = load(C/'MEDIA_AUDIO_BINDING.json'); guard()
        save(C/('MEDIA_RESUME_'+str(time.time_ns())+'.json'),
             {'status':'CACHE_VERIFIED_RESUME','previous_state':pin(archived),'baseline':pin(BASE),'completed':list(done),'preflight':preflight()})
        return
    while True:
        result = readiness()
        if result: break
        state('WAITING_DATA_READY'); time.sleep(10)
    ready, frozen = result
    duration_contract()
    closure = collect(R)
    assert len(closure) >= 43, 'Missing dependency closure'
    intent = load(C/'RENDER_INTENT.json')
    assert intent['source'] == VERSION and intent['source_sha256'] == ready['source_sha256']
    verify_intent(intent)
    assert intent['render_closure'] == closure, 'STOP: capture intent differs from current render pins'
    frozen += [pin(C/'RENDER_INTENT.json'),pin(C/'MEDIA_GO.json')]
    baseline = {'source':VERSION,'source_sha256':ready['source_sha256'],'frozen_files':frozen,
        'render_closure':closure,'helper':pin(R/'cinema/media_v7.py'),
        'closure_helper':pin(R/'cinema/render_sources.py'),'worker':pin(Path(__file__)),
        'legacy_worker':pin(OLD),'namespace_repair':pin(W/'adendo_a/resume_media_v400_r1.py'),
        'negative_history':pin(W/'adendo_a/namespace_failure_r0/MEDIA_WATCH.json'),
        'backup_receipt':pin(C/'MEDIA_V401_BACKUP.json'),'preflight':preflight(),
        'old_render_parameters':load(C/'baseline_manifest_v401/RENDER_MANIFEST.json')['parameters']}
    save_original(BASE, baseline)

def guard():
    canonical_guard()
    assert baseline is not None
    assert collect(R) == baseline['render_closure'], 'STOP: render dependencies changed'
    for item in baseline['frozen_files'] + [baseline[k] for k in ('helper','closure_helper','worker','legacy_worker','namespace_repair','backup_receipt')]: verify(item)
    duration_contract()
    if audio_binding:
        for item in audio_binding['files']: verify(item)

def args_for(film=None, job=None):
    args = legacy['args_for'](film, job)
    args.action = 'film' if film else 'loop'  # Actual media_v7 API; fixes the preserved v400 failure.
    args.audio_dir = options.audio_dir if options else R/'audio'
    return args

def audio_ready():
    global audio_binding
    if audio_binding: guard(); return True
    if not options.audio_ready.exists(): return False
    ready = load(options.audio_ready)
    assert ready.get('source') == VERSION and ready.get('source_sha256') == baseline['source_sha256'], 'STOP: stale audio readiness'
    assert ready['status'] == 'AUDIO_READY' and ready['actor'] == 'codex-video-audio', 'Audio not ready'
    verify(ready['receipt'])
    delivery_path = Path(ready['receipt'].get('path',ready['receipt'].get('file')))
    assert delivery_path.resolve() == (R/'audit/DELIVERY_D_V402.json').resolve()
    delivery = load(delivery_path)
    assert delivery['source'] == VERSION and delivery['source_sha256'] == baseline['source_sha256']
    assert delivery['status'] == 'PASS_BUILDER_READY_FOR_INDEPENDENT_REVIEW'
    build = load(R/'audio/NARRATION_BUILD.json')
    assert build.get('status') == 'COMPLETED' and build.get('tts_inflight') is False and not build.get('pending')
    assert build['plan_sha256'] == ready['plan_sha256'], 'Audio READY plan mismatch'
    files = [options.audio_ready, Path(ready['receipt'].get('path',ready['receipt'].get('file'))), R/'audio/NARRATION_BUILD.json']
    for film in (1,2):
        paths, receipt = M['audio_inputs'](R, options.audio_dir, film)
        files.extend([*paths.values(),receipt])
        files += [Path(x['file']) for x in M['captions'](R,film)['files']]
    plans = [p for p in options.audio_dir.glob('NARRATION_PLAN*.json') if load(p).get('plan_sha256') == build['plan_sha256']]
    files.extend(plans)
    audio_binding = {'status':'VERIFIED_CURRENT_PLAN_WAV_CAPTIONS','plan_sha256':build['plan_sha256'],
                     'files':[pin(p) for p in sorted(set(files))]}
    save(C/'MEDIA_AUDIO_BINDING.json', audio_binding)
    return True

def job_matches(job):
    metadata = job.get('metadata', {})
    return metadata.get('source') == VERSION and metadata.get('source_sha256') == baseline['source_sha256']

def candidate(kind):
    valid = []
    for path in (R/'cinema/render/jobs').glob(kind+'_*.json'):
        if '.progress.' in path.name or '.bak_' in path.name: continue
        job = load(path)
        if not job_matches(job): continue
        metadata = job['metadata']
        if not metadata.get('total') or job.get('render',{}).get('encoded') != metadata['total']: continue
        assert job['source_files'] == baseline['render_closure'], 'STOP: current-version job has different pins'
        assert len(job['source_files']) >= 43 and metadata['fps'] == 60
        expected = 16 if kind == 'loop' else M['timeline'](R,int(kind[-1]))[2]
        size = (1920,1080) if kind == 'loop' else (3840,2160)
        assert (metadata['width'],metadata['height']) == size, 'STOP: job dimensions changed'
        assert metadata['total'] == expected*60 and metadata['duration'] == expected, 'STOP: duration/frame count changed'
        M['read_job'](R,path,None if kind == 'loop' else int(kind[-1]))
        valid.append(path)
    assert len(valid) <= 1, 'Multiple current complete jobs need explicit reconciliation'
    return valid[0] if valid else None

def stills_ready():
    expected = {(1,x['key']) for x in load(R/'data/film1.json')['scenes']}
    old = load(C/'media_v401_history/render/ASSETS_AUDIT.json')
    expected |= {(2,s['stage'].removeprefix('asset_film2_')) for s in old['stages'] if s['stage'].startswith('asset_film2_')}
    found = {}
    for path in (R/'cinema/render/stills').glob('*.json'):
        if '.bak_' in path.name: continue
        record = load(path); source = record.get('state',{})
        if source.get('source') != VERSION or source.get('source_sha256') != baseline['source_sha256']: continue
        key = (source.get('film'),source.get('key'))
        if key not in expected: continue
        assert (record['width'],record['height']) == (3840,2160)
        found[key] = (path,record)
    if set(found) != expected: return None
    for path,record in found.values():
        png = Path(record['file'])
        if not png.is_absolute(): png = R/'cinema/render/stills'/png
        assert sha(png) == record['sha256']
    return [pin(path) for path,record in found.values()]

original_stage = M['Pipeline'].stage
def guarded_stage(self,name,inputs,parameters,outputs,work):
    guard()
    def checked(tmp):
        result = work(tmp); guard(); return result
    return original_stage(self,name,inputs+[Path(__file__),OLD,BASE],
                         {**parameters,'source':VERSION,'source_sha256':baseline['source_sha256']},outputs,checked)

def guarded_run(self,args,label):
    guard(); assert self.current is not None
    start = time.perf_counter(); child = None; failure = None
    command = [str(self.ff),'-y','-nostdin','-hide_banner',*map(str,args)]
    try:
        child = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
        save(C/'ENCODE_STAGE.json',{'status':'RUNNING','label':label,'worker_pid':os.getpid(),'ffmpeg_pid':child.pid,'stage_directory':str(self.current)})
        while True:
            try: stdout,stderr = child.communicate(timeout=5); break
            except subprocess.TimeoutExpired: guard()
    except BaseException as exc:
        failure = repr(exc)
        if child is not None:
            if child.poll() is None: child.terminate()
            stdout,stderr = child.communicate()
        else: stdout,stderr = b'',str(exc).encode()
        raise
    finally:
        elapsed = time.perf_counter()-start; self.command_seconds += elapsed
        M['atomic'](self.current/(label+'.log'),stderr or b'No stderr')
        save(C/'ENCODE_STAGE.json',{'status':'FAILED' if failure or (child and child.returncode) else 'COMPLETE',
             'label':label,'ffmpeg_pid':child.pid if child else None,'returncode':child.returncode if child else None,
             'elapsed_seconds':elapsed,'error':failure,'stage_directory':str(self.current)})
    assert child.returncode == 0, 'FFmpeg failed; log and partial preserved: ' + label
    guard(); return subprocess.CompletedProcess(command,child.returncode,stdout,stderr)

def result_outputs(result):
    found = {}
    def walk(value):
        if isinstance(value,dict):
            for item in value.get('outputs',[]):
                verify(item); found[item['file']] = item
            for child in value.values(): walk(child)
        elif isinstance(value,list):
            for child in value: walk(child)
    walk(result)
    assert found, 'Completed action without verifiable output pins'
    return list(found.values())

def action(label, operation):
    guard(); preflight(); state('RUNNING_ENCODING' if label != 'validation' else 'VALIDATING',action=label)
    start = time.monotonic(); result = operation(); guard()
    completed_outputs[label] = result_outputs(result)
    timings.append({'action':label,'elapsed_seconds':time.monotonic()-start})
    save(C/('ENCODE_'+label.upper()+'.json'),{'status':'COMPLETE','result':result,'elapsed_seconds':timings[-1]['elapsed_seconds']})
    return result

def final_receipts():
    guard()
    validation = load(R/'render/MEDIA_VALIDATION.json')
    assert validation['status'] == 'PASS' and len(validation['movies']) == 16 and len(validation['images']) == 25
    for item in validation['movies']+validation['images']: verify(item)
    jobs = {}
    for kind,entry in done.items():
        verify(entry); job = load(Path(entry['file']))
        jobs[kind] = {'job_sha256':entry['sha256'],'metadata':job['metadata'],'encoded_sha256':job['sha256'],
                      'render':job['render'],'source_files':job['source_files']}
    save(R/'RENDER_MANIFEST.json',{'schema':'tgl.render.v7','version':VERSION,'parameters':baseline['old_render_parameters'],'jobs':jobs})
    save(C/'MEDIA_VALIDATION.json',validation)
    assert not (C/'DELIVERY_E.json').exists(), 'Original E receipt is immutable'
    save(C/'DELIVERY_E.json',{'status':'MEDIA_VALIDATED_AWAITING_PARENT_PUBLIC_MANIFEST','actor':ACTOR,'task_id':TASK,
         'media_count':16,'image_count':25,'jobs':done,'baseline':pin(BASE),'backup':pin(C/'MEDIA_V401_BACKUP.json'),
         'validation':pin(R/'render/MEDIA_VALIDATION.json'),'render_manifest':pin(R/'RENDER_MANIFEST.json'),
         'audio_binding':pin(C/'MEDIA_AUDIO_BINDING.json'),'assets':pin(R/'render/ASSETS_AUDIT.json'),
         'timings':timings,'namespace_failure_preserved':baseline['negative_history'],'remote_api_calls':0,
         'render_started_by_worker':False,'cost_scope':'Local elapsed/FFmpeg time measured; monetary CPU/energy cost unmeasured.',
         'pending':['Parent final make/public manifest and independent review. No automatic submission.']})

def main():
    global assets
    launch_guard()
    fd = os.open(LOCK,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    os.write(fd,str(os.getpid()).encode()); os.fsync(fd)
    try:
        initialize()
        if (C/'DELIVERY_E.json').exists():
            # Reconcile terminal state, never rewrite the original delivery.
            existing = load(C/'DELIVERY_E.json')
            verify(existing['validation']); verify(existing['render_manifest'])
            assert len(done) == 3 and assets and 'validation' in completed_outputs
            state('COMPLETE'); return
        assert audio_ready(), 'Current reviewed AUDIO_READY required before exports'
        G['jsave'] = save
        M['Pipeline'].run, M['Pipeline'].stage = guarded_run, guarded_stage
        pipe = M['Pipeline'](R,M['FF_DEFAULT'])
        while time.monotonic()-started < 40000:
            guard()
            locks = list((R/'render/.pipeline').glob('*.lock'))
            assert not locks, 'Existing stage lock: reconcile owner before resuming'
            if not assets:
                stills = stills_ready()
                if stills:
                    action('assets',lambda:M['prepare_assets'](pipe,args_for()))
                    save(C/'ASSETS_V402.json',{'status':'COMPLETE','stills':stills,'audit':pin(R/'render/ASSETS_AUDIT.json')})
                    assets = True; state('CHECKPOINT')
            audio = audio_ready(); progressed = False
            for kind in ('film1','film2','loop'):
                if kind in done or (kind in prepared and not audio): continue
                job = candidate(kind)
                if job is None: continue
                args = args_for(None if kind == 'loop' else int(kind[-1]),job)
                if kind == 'loop': action(kind,lambda:M['encode_loop'](pipe,args)); done[kind] = pin(job)
                elif audio: action(kind,lambda:M['encode_film'](pipe,args)); done[kind] = pin(job)
                else: action('prepare_'+kind,lambda:M['prepare_video'](pipe,args)); prepared[kind] = pin(job)
                state('CHECKPOINT'); progressed = True; break
            if len(done) == 3 and assets:
                if 'validation' not in completed_outputs: action('validation',lambda:M['validate_delivery'](pipe,args_for()))
                final_receipts(); state('COMPLETE'); return
            if not progressed: state('WAITING_CURRENT_JOBS_OR_AUDIO',audio_verified=audio); time.sleep(10)
        raise TimeoutError('Worker timeout; no automatic restart')
    except BaseException as exc:
        state('FAILED_STOPPED',error=repr(exc)); raise
    finally:
        os.close(fd); LOCK.unlink()

def self_test():
    global baseline
    names = {'encode_film','encode_loop','prepare_video','reuse_prepared_video','prepare_assets','validate_delivery'}
    tree = ast.parse((R/'cinema/media_v7.py').read_text(encoding='utf-8'))
    fields = {n.attr for fn in tree.body if isinstance(fn,ast.FunctionDef) and fn.name in names
              for n in ast.walk(fn) if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id == 'args'}
    assert not (fields-set(vars(args_for(1,Path('fixture.json')))))
    assert args_for(1).action == 'film' and args_for().action == 'loop'
    baseline = {'source_sha256':'fixture-current'}
    assert job_matches({'metadata':{'source':VERSION,'source_sha256':'fixture-current'}})
    assert not job_matches({'metadata':{'source':'v401','source_sha256':'fixture-current'}})
    assert not job_matches({'metadata':{'source':VERSION,'source_sha256':'fixture-obsolete'}})
    baseline = None
    for path in (R/'cinema/studio.mjs',R/'make_v7.py'):
        text = path.read_text(encoding='utf-8'); assert 'v400' not in text.lower()
        assert 'seal_version' in text and 'seal_pin' in text
        assert 'v401' not in text.lower()
    return {'status':'PASS','actual_api_fields':sorted(fields),'old_version_rejected':True,'old_pin_rejected':True,
            'namespace_action_fixed':True,'dynamic_metadata_no_v400_literal':True,'encoding_executed':False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start-authorized',action='store_true')
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--data-ready',type=Path,default=C/'DATA_READY.json')
    parser.add_argument('--audio-ready',type=Path,default=C/'AUDIO_READY.json')
    parser.add_argument('--audio-dir',type=Path,default=R/'audio')
    options = parser.parse_args()
    if options.self_test: print(json.dumps(self_test()))
    else: main()
