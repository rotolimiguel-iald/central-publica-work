"""Authorized offline v400 media worker; no rendering, TTS or public-manifest writes."""
from pathlib import Path
import argparse, datetime, json, os, runpy, subprocess, sys, time

A=Path(__file__).resolve().parent
W=A.parent
R=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
M=runpy.run_path(str(R/'cinema/media_v7.py'))
G=M['encode_film'].__globals__
load,pin,sha=M['load'],M['pin'],M['sha']
save_original=M['jsave']
mission=runpy.run_path(str(W/'mission.py'))
collect=runpy.run_path(str(R/'cinema/render_sources.py'))['collect']
BASE=A/'MEDIA_V400_BASELINE.json'
STATE=A/'MEDIA_WATCH.json'
LOCK=A/'MEDIA_V400_WORKER.lock'
baseline=None
last_state=None
started=time.monotonic()
done={}
prepared={}
timings=[]

def preflight():
    pr=mission['project']()
    task=next(t for t in pr['projection']['active'] if t['id']=='ADENDO_E')
    assert task['status']=='working' and task['lease']['owner']=='codex-video-web'
    check=mission['call']({'operation':'check','actor':{'id':'codex-video-web','kind':'agent'},
        'task_id':'ADENDO_E','lease_id':task['lease']['id'],'expected_revision':pr['receipt']['revision'],
        'projection_sha256':pr['projection_sha256']})
    assert check['ready']
    return check

def verify(p):
    q=Path(p.get('path',p.get('file')))
    assert sha(q)==p['sha256'] and q.stat().st_size==p['bytes'], 'Changed input: '+str(q)

def initialize():
    global baseline
    assert not BASE.exists(), 'Existing run must be reconciled, never duplicated'
    check=preflight()
    ready=load(A/'DATA_READY.json');comparison=load(A/'NUMERIC_COMPARISON.json')
    assert ready['status']=='DATA_READY_FOR_V400_RENDER' and ready['source']=='v400'
    assert ready['scientific_differences']==0 and ready['anchors']>=64
    assert comparison['status']=='PASS_EXACT_SCIENTIFIC_VALUES_UNCHANGED'
    assert comparison['source_sha256']==ready['source_sha256']
    verify(ready['numeric_comparison'])
    frozen=ready['data_pins']+ready['source_pins']+[ready['seal']]
    for p in frozen:verify(p)
    closure=collect(R)
    patch=load(A/'RENDER_METADATA_PATCH.json')
    assert sha(Path(patch['file']))==patch['sha256']
    historical=[]
    for p in [R/'render/MEDIA_WATCH.json',R/'render/MEDIA_VALIDATION.json',R/'render/DELIVERY_E.json',
              R/'RENDER_MANIFEST.json',R/'render/ASSETS_AUDIT.json',R/'audit/DELIVERY_E.json']:
        if p.exists():
            q=A/'media_v399_history'/p.relative_to(R)
            q.parent.mkdir(parents=True,exist_ok=True)
            with q.open('xb') as f:f.write(p.read_bytes())
            assert sha(q)==sha(p)
            historical.append({'original':pin(p),'backup':pin(q)})
    baseline={'source':'v400','source_sha256':ready['source_sha256'],'data_ready':pin(A/'DATA_READY.json'),
              'numeric_comparison':pin(A/'NUMERIC_COMPARISON.json'),'frozen_files':frozen,
              'render_closure':closure,'helper':pin(R/'cinema/media_v7.py'),
              'closure_helper':pin(R/'cinema/render_sources.py'),'worker':pin(Path(__file__)),
              'preflight':check,'historical_receipts':historical,
              'old_render_parameters':load(R/'RENDER_MANIFEST.json')['parameters']}
    save_original(BASE,baseline)

def guard():
    assert collect(R)==baseline['render_closure'], 'STOP: render dependency changed'
    for p in baseline['frozen_files']+[baseline['helper'],baseline['closure_helper'],baseline['worker']]:verify(p)

def save(path,obj):
    if isinstance(obj,dict):
        obj={**obj,'source':'v400','source_sha256':baseline['source_sha256'],'adendo_worker':baseline['worker']}
    save_original(path,obj)

def state(status,**extra):
    global last_state
    value={'status':status,'completed':done,'prepared':prepared,'timings':timings,**extra}
    signature=json.dumps(value,sort_keys=True)
    if signature!=last_state:
        save(STATE,{**value,'elapsed_seconds':time.monotonic()-started})
        last_state=signature
        print(status,extra,flush=True)

def guarded_run(self,args,label):
    guard()
    assert self.current is not None
    t=time.perf_counter()
    command=[str(self.ff),'-y','-nostdin','-hide_banner',*map(str,args)]
    child=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
    save(A/'ENCODE_STAGE.json',{'status':'RUNNING','label':label,'worker_pid':os.getpid(),
                              'ffmpeg_pid':child.pid,'stage_directory':str(self.current)})
    failure=None
    while True:
        try:
            stdout,stderr=child.communicate(timeout=5)
            break
        except subprocess.TimeoutExpired:
            try:guard()
            except Exception as exc:
                failure=str(exc)
                child.terminate()  # Only this exact FFmpeg child owned by this worker.
                stdout,stderr=child.communicate()
                break
    elapsed=time.perf_counter()-t
    self.command_seconds+=elapsed
    M['atomic'](self.current/(label+'.log'),stderr or b'No stderr')
    save(A/'ENCODE_STAGE.json',{'status':'FAILED' if failure or child.returncode else 'COMPLETE',
                              'label':label,'ffmpeg_pid':child.pid,'returncode':child.returncode,
                              'elapsed_seconds':elapsed,'error':failure,'stage_directory':str(self.current)})
    assert not failure, failure
    assert child.returncode==0, 'FFmpeg failed; partial and log preserved: '+label
    guard()
    return subprocess.CompletedProcess(command,child.returncode,stdout,stderr)

original_stage=M['Pipeline'].stage
def guarded_stage(self,name,inputs,parameters,outputs,work):
    guard()
    def guarded_work(tmp):
        result=work(tmp)
        guard()
        return result
    return original_stage(self,name,inputs+[Path(__file__),BASE],
                          {**parameters,'source':'v400','source_sha256':baseline['source_sha256']},outputs,guarded_work)

def args_for(film=None,job=None):
    return argparse.Namespace(film=film,job=job,root=R,audio_dir=R/'audio',audio_map=None,
        ffmpeg=M['FF_DEFAULT'],no_720=False,vp9_pt=False,poster1_key='gravity',poster2_key='review_240',og_key='review_0')

def stills_ready():
    expected={(1,x['key']) for x in load(R/'data/film1.json')['scenes']}
    old=load(A/'media_v399_history/render/ASSETS_AUDIT.json')
    expected|={(2,s['stage'].removeprefix('asset_film2_')) for s in old['stages'] if s['stage'].startswith('asset_film2_')}
    found={}
    for p in (R/'cinema/render/stills').glob('*.json'):
        if '.bak_' in p.name:continue
        d=load(p);s=d.get('state',{})
        if s.get('source')!='v400' or s.get('source_sha256')!=baseline['source_sha256']:continue
        key=(s.get('film'),s.get('key'))
        if key in expected:
            assert (d['width'],d['height'])==(3840,2160)
            found[key]=(p,d)
    if set(found)!=expected:return None
    for p,d in found.values():
        q=Path(d['file'])
        if not q.is_absolute():q=R/'cinema/render/stills'/q
        assert sha(q)==d['sha256']
    return [pin(p) for p,d in found.values()]

def candidate(kind):
    valid=[]
    for p in (R/'cinema/render/jobs').glob(kind+'_*.json'):
        if '.progress.' in p.name or '.bak_' in p.name:continue
        d=load(p);m=d.get('metadata',{})
        if m.get('source')!='v400' or m.get('source_sha256')!=baseline['source_sha256']:continue
        if d.get('render',{}).get('encoded')!=m.get('total') or not m.get('total'):continue
        assert d['source_files']==baseline['render_closure'], 'Current-version job has different sources'
        M['read_job'](R,p,None if kind=='loop' else int(kind[-1]))
        valid.append(p)
    assert len(valid)<=1, 'Multiple current jobs; explicit selection required'
    return valid[0] if valid else None

def audio_ready():
    d=load(R/'audio/NARRATION_BUILD.json')
    if d.get('status')!='COMPLETED':return False
    if d.get('tts_inflight') is not False or d.get('pending'):return False
    try:
        for f in (1,2):M['audio_inputs'](R,R/'audio',f)
    except (ValueError,KeyError,AssertionError):return False
    return True

def action(label,fn):
    guard();preflight();state('RUNNING',action=label)
    t=time.monotonic();result=fn();guard()
    timings.append({'action':label,'elapsed_seconds':time.monotonic()-t})
    save(A/('ENCODE_'+label.upper()+'.json'),{'status':'COMPLETE','result':result,'elapsed_seconds':timings[-1]['elapsed_seconds']})
    return result

def final_receipts():
    guard()
    validation=load(R/'render/MEDIA_VALIDATION.json')
    assert validation['status']=='PASS' and len(validation['movies'])==16 and len(validation['images'])==25
    jobs={}
    for kind,entry in done.items():
        verify(entry);j=load(Path(entry['file']))
        jobs[kind]={'job_sha256':entry['sha256'],'metadata':j['metadata'],'encoded_sha256':j['sha256'],
                    'render':j['render'],'source_files':j['source_files']}
    save(R/'RENDER_MANIFEST.json',{'schema':'tgl.render.v7','version':'v400',
         'parameters':baseline['old_render_parameters'],'jobs':jobs})
    save(A/'MEDIA_VALIDATION.json',validation)
    save(A/'DELIVERY_E.json',{'status':'MEDIA_VALIDATED_AWAITING_PARENT_PUBLIC_MANIFEST',
        'actor':'codex-video-web','task_id':'ADENDO_E','media_count':16,'image_count':25,
        'jobs':done,'baseline':pin(BASE),'validation':pin(R/'render/MEDIA_VALIDATION.json'),
        'render_manifest':pin(R/'RENDER_MANIFEST.json'),'audio_build':pin(R/'audio/NARRATION_BUILD.json'),
        'assets':pin(R/'render/ASSETS_AUDIT.json'),'timings':timings,
        'remote_api_calls':0,'render_started_by_worker':False,'source_edits':False,
        'cost_scope':'Local stage elapsed and FFmpeg times recorded; monetary CPU/energy cost unmeasured.',
        'pending':['Parent final make/public manifest and independent review; no automatic submission.']})

def main():
    fd=os.open(LOCK,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    os.write(fd,str(os.getpid()).encode());os.fsync(fd)
    try:
        initialize()
        G['jsave']=save
        M['Pipeline'].run=guarded_run
        M['Pipeline'].stage=guarded_stage
        pipe=M['Pipeline'](R,M['FF_DEFAULT'])
        assets=False
        while time.monotonic()-started<40000:
            guard()
            locks=list((R/'render/.pipeline').glob('*.lock'))
            if locks:
                state('WAITING_EXISTING_STAGE',locks=[str(p) for p in locks]);time.sleep(10);continue
            if not assets:
                stills=stills_ready()
                if stills:
                    action('assets',lambda:M['prepare_assets'](pipe,args_for()))
                    save(A/'ASSETS_V400.json',{'status':'COMPLETE','stills':stills,'audit':pin(R/'render/ASSETS_AUDIT.json')})
                    assets=True
            progressed=False
            audio=audio_ready()
            for kind in ('film1','film2','loop'):
                if kind in done or (kind in prepared and not audio):continue
                p=candidate(kind)
                if p is None:continue
                a=args_for(None if kind=='loop' else int(kind[-1]),p)
                if kind=='loop':action(kind,lambda:M['encode_loop'](pipe,a));done[kind]=pin(p)
                elif audio:action(kind,lambda:M['encode_film'](pipe,a));done[kind]=pin(p)
                else:action('prepare_'+kind,lambda:M['prepare_video'](pipe,a));prepared[kind]=pin(p)
                progressed=True
                break
            if len(done)==3 and assets:
                action('validation',lambda:M['validate_delivery'](pipe,args_for()))
                final_receipts();state('COMPLETE');return
            if not progressed:
                state('WAITING_CURRENT_JOBS_OR_AUDIO',assets_complete=assets,audio_verified=audio)
                time.sleep(10)
        raise TimeoutError('No automatic restart after timeout')
    except Exception as exc:
        if baseline:state('FAILED_STOPPED',error=str(exc))
        else:save_original(A/'MEDIA_WORKER_START_FAILURE.json',{'status':'FAILED','error':str(exc)})
        raise
    finally:
        os.close(fd);LOCK.unlink()

if __name__=='__main__':main()
