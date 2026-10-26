"""Offline completion helper: early film2 mux, validation, then candidate receipt."""
from pathlib import Path
import argparse, json, os, re, runpy, subprocess, sys, time

R=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
W=Path(__file__).resolve().parent
M=runpy.run_path(str(R/'cinema/media_v7.py'))
JOB=R/'cinema/render/jobs/film2_b292404a6f804fa89fe8bb5753d682e2.json'
WEB=['bg_scene.js','bg_demo.html','filmes.html','filmes.css','filmes.mjs','fonts.css','favicon.svg']

def current_web():
    patch=M['load'](W/'CAPTION_WRAP_PATCH.json')
    for entry in patch['changes']:
        assert M['sha'](Path(entry['path']))==entry['sha256'], 'Confirmed web patch changed'
    return [M['pin'](R/'web'/name) for name in WEB]

def ready_h264():
    if not JOB.exists(): return False
    master=R/'render/.pipeline/film2_silent_4k.json'
    small=R/'render/.pipeline/film2_silent_1080p.json'
    if not master.exists() or not small.exists(): return False
    a,b=M['load'](master),M['load'](small)
    return a.get('status')==b.get('status')=='COMPLETE' and a['inputs'][0]['file']==str(JOB) and b['inputs'][0]==a['outputs'][0]

def early_mux_and_validate():
    args=argparse.Namespace(job=JOB,film=2,no_720=True)
    pipe=M['Pipeline'](R,M['FF_DEFAULT'])
    assert M['reuse_prepared_video'](pipe,args,True) is not None
    command=[sys.executable,'-B','-X','utf8',str(R/'cinema/media_v7.py'),'mux-h264','--film','2','--job',str(JOB),'--job-ready','--audio-dir',str(R/'audio'),'--no-720']
    log=R/'render/MUX_H264_FILM2_FINAL.log'
    M['backup'](log)
    with log.open('wb') as stream:
        result=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode==0, 'Early mux failed; logs preserved'
    files=[R/'render/filme2_1080p.mp4',R/'render/filme2_1080p_pt-BR.mp4']
    duration=M['timeline'](R,2)[2]
    def verify(tmp):
        checks=[]
        for file,lang in zip(files,['eng','por']):
            metrics=M['check_mp4'](file,1920,1080,duration,lang,25000000*duration/60)
            result=pipe.run(['-v','error','-xerror','-threads','4','-i',file,'-map','0:v:0','-map','0:a:0','-progress','pipe:1','-nostats','-f','null','-'],file.stem+'_decode')
            frames=re.findall(rb'^frame=(\d+)',result.stdout,re.M)
            assert frames and int(frames[-1])==round(duration*60)
            checks.append({'file':M['pin'](file),'metrics':metrics,'decoded_frames':int(frames[-1])})
        M['jsave'](tmp['receipt'],{'status':'PASS_READY_FOR_PARENT_PLAYER_REVIEW','source_job':M['pin'](JOB),'checks':checks,'video_recoded_for_languages':False,'browser_review_performed':False})
        return {'status':'PASS','decoded_movies':2}
    pipe.stage('film2_final_h264_ui_validation',files+[JOB,R/'render/MUX_H264_FILM2.json'],{'full_decode':True},{'receipt':R/'render/FILM2_FINAL_H264_UI_VALIDATION.json'},verify)
    print('FILM2_H264_EN_PT_READY_FOR_PARENT_PLAYER_REVIEW',flush=True)

def finalize(web):
    watcher=M['load'](R/'render/MEDIA_WATCH.json')
    validation=M['load'](R/'render/MEDIA_VALIDATION.json')
    assert watcher['status']=='COMPLETE' and validation['status']=='PASS'
    assert len(validation['movies'])==16 and len(validation['images'])==25
    assert current_web()==web, 'Web changed after confirmation'
    for item in validation['movies']+validation['images']:
        assert M['pin'](Path(item['file']))=={k:item[k] for k in ('file','bytes','sha256')}
    jobs=[]
    for kind in ('film1','film2','loop'):
        p=watcher['completed'][kind]['job']
        assert M['pin'](Path(p['file']))==p
        M['read_job'](R,Path(p['file']),None if kind=='loop' else int(kind[-1]))
        jobs.append(p)
    for film in (1,2):
        M['audio_inputs'](R,R/'audio',film)
        M['captions'](R,film)
    stages=[]
    for p in (R/'render/.pipeline').glob('*.json'):
        d=M['load'](p)
        if d.get('status')=='COMPLETE' and all(Path(x['file']).is_file() and M['pin'](Path(x['file']))==x for x in d.get('outputs',[])):
            stages.append({k:d.get(k) for k in ('stage','elapsed_seconds','ffmpeg_seconds','cache_hit')})
    report={'status':'MEDIA_WEB_VALIDATED_PUBLIC_MANIFEST_PENDING','media_count':16,'image_count':25,'source_jobs':jobs,'web_files':web,'caption_wrap_patch':M['pin'](W/'CAPTION_WRAP_PATCH.json'),'validation':M['pin'](R/'render/MEDIA_VALIDATION.json'),'audio_build':M['pin'](R/'audio/NARRATION_BUILD.json'),'assets':M['pin'](R/'render/ASSETS_AUDIT.json'),'watcher':M['pin'](R/'render/MEDIA_WATCH.json'),'stage_times':stages,'public_media':[M['pin'](Path(x['file'])) for x in validation['movies'] if Path(x['file']).parent==R/'render'],'private_media':[M['pin'](Path(x['file'])) for x in validation['movies'] if Path(x['file']).parent==R/'render/private'],'pending':['Parent final make: current PUBLIC_DELIVERY_V7.json and RENDER_MANIFEST.json','Bind final manifests, then submit E with codex-video-web actual lease; independent acceptance remains separate'],'remote_api_calls':0,'tts_calls':0,'submission_performed':False,'cost_scope':'Measured local stage wall/FFmpeg time; historical cancelled attempts remain separate; monetary CPU/electricity cost not measured'}
    M['jsave'](R/'render/DELIVERY_E.json',report)
    audit=R/'audit/MEDIA_PIPELINE_BUILD.json';d=M['load'](audit);d['status']=report['status'];d['delivery_E']=M['pin'](R/'render/DELIVERY_E.json');d['delivery_E_submitted']=False;M['jsave'](audit,d)
    print('MEDIA_VALIDATION_16_AND_ASSETS_25_COMPLETE_MANIFEST_PENDING',flush=True)

def main():
    lock=R/'render/E_COMPLETION_WORKER.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode())
    started=time.monotonic();early=False
    try:
        web=current_web()
        M['jsave'](R/'render/E_COMPLETION_WORKER.json',{'status':'WATCHING_CURRENT_FILM2_AND_FULL_VALIDATION','pid':os.getpid(),'web_files_confirmed_by_parent':web,'source':M['pin'](Path(__file__)),'submission_automatic':False})
        while time.monotonic()-started<14400:
            state=M['load'](R/'render/MEDIA_WATCH.json')['status']
            if state in ('FAILED','PAUSED_INTERMEDIATE_VISUAL_REVISION','PAUSED_AWAITING_V399_REANCHOR'):
                raise RuntimeError('Watcher stopped; E withheld: '+state)
            if not early and ready_h264():
                early_mux_and_validate();early=True
            if state=='COMPLETE':
                finalize(web);return
            time.sleep(10)
        raise TimeoutError('Completion timeout; E withheld')
    except Exception as exc:
        M['jsave'](R/'render/E_COMPLETION_FAILURE.json',{'status':'E_WITHHELD','error':str(exc),'elapsed_seconds':time.monotonic()-started})
        raise
    finally:
        os.close(fd);lock.unlink()

if __name__=='__main__': main()
