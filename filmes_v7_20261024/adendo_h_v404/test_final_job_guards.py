"""Isolated fixtures for pre-write job admission and observation-to-artifact binding."""
from pathlib import Path
from unittest.mock import patch
import copy, json, tempfile
import final_job_guards as g

H=Path(__file__).resolve().parent
results=[]

def put(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value),encoding='utf-8')

def fixture(base):
    c=base/'c';v=base/'v';c.mkdir();v.mkdir()
    source='fixture-source';closure={str(i):str(i) for i in range(43)}
    baseline={'source':'v404','source_sha256':source,'render_closure':closure}
    put(c/'MEDIA_V404_BASELINE.json',baseline);put(c/'RENDER_INTENT.json',baseline)
    (v/'make_v7.py').write_bytes(b'# fixture only')
    jobs={};rows={};selection={}
    for kind, seconds in g.KINDS.items():
        path=v/'cinema/render/jobs'/f'{kind}_fixture.json'
        raw=path.with_suffix('.h264');raw.parent.mkdir(parents=True,exist_ok=True);raw.write_bytes(kind.encode())
        width,height=(1920,1080) if kind=='loop' else (3840,2160)
        meta={'kind':kind,'source':'v404','source_sha256':source,'fps':60,'duration':seconds,'total':seconds*60,'width':width,'height':height}
        job={'metadata':meta,'file':str(raw),'bytes':raw.stat().st_size,'sha256':g.sha(raw),'source_files':closure,'render':{'encoded':seconds*60}}
        put(path,job);jobs[kind]=g.file_pin(path);selection[kind]=path
        rows[kind]={'job_sha256':g.sha(path),'metadata':meta,'encoded_sha256':job['sha256'],'render':job['render'],'source_files':closure}
    header={'source':'v404','source_sha256':source}
    put(c/'MEDIA_WATCH.json',{**header,'status':'COMPLETE','completed':jobs})
    put(c/'DELIVERY_E.json',{**header,'status':'MEDIA_VALIDATED_AWAITING_PARENT_PUBLIC_MANIFEST','jobs':jobs,'baseline':g.file_pin(c/'MEDIA_V404_BASELINE.json')})
    put(v/'RENDER_MANIFEST.json',{**header,'jobs':rows})
    runtime={'collect_render_sources':lambda unused:closure,'find_job':lambda kind:selection[kind]}
    return c,v,source,runtime,selection

def observations(c,v,source,completed):
    header={'source':'v404','source_sha256':source}
    capture={**header,'status':'PASS_WITH_SCOPE','jobs':completed['jobs'],'render_closure':completed['render_closure']}
    put(c/'PARENT_CAPTURE_AUDIT.json',capture)
    observed={};media=[];public=[]
    for n in (1,2):
        for lang in ('en','pt-BR'):
            suffix='_pt-BR' if lang=='pt-BR' else ''
            p=v/'render'/f'filme{n}_1080p{suffix}.mp4';p.parent.mkdir(exist_ok=True);p.write_bytes(p.name.encode())
            observed[f'film{n}_{lang}']=str(p);media.append(g.file_pin(p))
            public.append({**g.file_pin(p),'path':p.relative_to(v).as_posix()})
    put(v/'PUBLIC_DELIVERY_V7.json',{**header,'public_files':public});put(v.parent/'PUBLIC_DELIVERY_V7.json',header)
    ui={**header,'status':'PASS_OBSERVED_UI','observed_media':observed,'artifact_binding':{'jobs':completed['jobs'],'media':media,'manifests':[g.file_pin(p) for p in [v/'RENDER_MANIFEST.json',v/'PUBLIC_DELIVERY_V7.json',v.parent/'PUBLIC_DELIVERY_V7.json']]}}
    put(c/'FINAL_PLAYER_V404.json',ui)

def mutate_read(path, fn, callback):
    original=g.read
    def changed(p):
        d=original(p)
        if Path(p).resolve()==path.resolve():fn(d)
        return d
    with patch.object(g,'read',changed):callback()

def case(label, action, reject=False, ui=False):
    with tempfile.TemporaryDirectory(prefix='job_guard_fixture_',dir=H) as temp:
        c,v,source,runtime,selection=fixture(Path(temp))
        with patch.object(g,'load_make',lambda unused:runtime):
            complete=g.validate_worker_jobs(c,v,source)
            if ui:observations(c,v,source,complete)
            callback=(lambda:g.validate_observation_bindings(c,v,source,complete)) if ui else (lambda:g.validate_worker_jobs(c,v,source))
            try:action(c,v,selection,callback)
            except (AssertionError,KeyError,ValueError,FileNotFoundError) as error:
                assert reject,(label,str(error));outcome='rejected'
            else:
                assert not reject,'Unexpected acceptance: '+label;outcome='accepted'
            results.append({'name':label,'expected':'rejected' if reject else 'accepted','actual':outcome})

case('complete_current_jobs',lambda c,v,s,f:f())
case('worker_lock',lambda c,v,s,f:((c/'MEDIA_V404_WORKER.lock').write_bytes(b'fixture'),f()),True)
case('incomplete_watch',lambda c,v,s,f:mutate_read(c/'MEDIA_WATCH.json',lambda d:d.update(status='RUNNING_ENCODING'),f),True)
case('missing_loop',lambda c,v,s,f:mutate_read(c/'DELIVERY_E.json',lambda d:d['jobs'].pop('loop'),f),True)
case('different_worker_id',lambda c,v,s,f:mutate_read(c/'MEDIA_WATCH.json',lambda d:d['completed']['film1'].update(sha256='wrong'),f),True)
case('old_metadata_source',lambda c,v,s,f:mutate_read(s['film1'],lambda d:d['metadata'].update(source='v402'),f),True)
case('old_metadata_hash',lambda c,v,s,f:mutate_read(s['film1'],lambda d:d['metadata'].update(source_sha256='wrong'),f),True)
case('different_make_selection',lambda c,v,s,f:(s.update(film1=s['film2']),f()),True)
case('raw_stream_altered',lambda c,v,s,f:(s['film1'].with_suffix('.h264').write_bytes(b'altered'),f()),True)
case('duplicate_job',lambda c,v,s,f:(put(s['film1'].with_name('film1_duplicate.json'),g.read(s['film1'])),f()),True)
case('manifest_other_job',lambda c,v,s,f:mutate_read(v/'RENDER_MANIFEST.json',lambda d:d['jobs']['film1'].update(job_sha256='wrong'),f),True)
case('full_observation_binding',lambda c,v,s,f:f(),ui=True)
case('broken_capture_internal_pin',lambda c,v,s,f:mutate_read(c/'PARENT_CAPTURE_AUDIT.json',lambda d:d['jobs']['film1']['receipt'].update(sha256='wrong'),f),True,True)
case('capture_other_job',lambda c,v,s,f:mutate_read(c/'PARENT_CAPTURE_AUDIT.json',lambda d:d['jobs'].update(film1=d['jobs']['film2']),f),True,True)
case('capture_changed_closure',lambda c,v,s,f:mutate_read(c/'PARENT_CAPTURE_AUDIT.json',lambda d:d['render_closure'].update(extra='bad'),f),True,True)
case('missing_UI_binding',lambda c,v,s,f:mutate_read(c/'FINAL_PLAYER_V404.json',lambda d:d.pop('artifact_binding'),f),True,True)
case('broken_UI_media_pin',lambda c,v,s,f:mutate_read(c/'FINAL_PLAYER_V404.json',lambda d:d['artifact_binding']['media'][0].update(sha256='wrong'),f),True,True)
case('UI_other_capture',lambda c,v,s,f:mutate_read(c/'FINAL_PLAYER_V404.json',lambda d:d['artifact_binding']['jobs'].pop('loop'),f),True,True)
case('UI_wrong_language',lambda c,v,s,f:mutate_read(c/'FINAL_PLAYER_V404.json',lambda d:d['observed_media'].update(film1_en=d['observed_media']['film1_pt-BR']),f),True,True)
receipt={'status':'PASS','tests':len(results),'results':results,'scope':'Synthetic temporary fixtures; no production changes, renderer, TTS, network, original science or finalizer executed. Runtime selection mocked; not proof of actual media completion.'}
p=H/'FINAL_JOB_GUARD_CONTROLS.json';assert not p.exists();put(p,receipt)
print(json.dumps({'status':'PASS','tests':len(results)}))
