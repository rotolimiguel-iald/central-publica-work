"""Freeze installed bytes and authorize exactly one existing browser capture pipeline."""
from context import *
sys.path.insert(0,str(H))
import runpy,time
import progress
from finalizer_guards import validate_frozen_data,validate_replay
from current_audio_guard import validate_audio

def main():
 pf=check();stable_seal();assert not (H/'RENDER_INTENT.json').exists(),'Recover recorded capture; do not start another'
 assert read(H/'INTEGRATION.json')['status']=='PASS'
 source=validate_frozen_data(H,V,N);validate_replay(V,source);validate_audio(H,V,source)
 review=read(H/'AUDIO_RESULT_REVIEW.json');assert review['status']=='PASS_WITH_SCOPE' and review['actor']=='codex-video-v404-data'
 m=runpy.run_path(str(H/'media_v404_worker.py'))
 from types import SimpleNamespace
 m['main'].__globals__['options']=SimpleNamespace(start_authorized=True,data_ready=H/'MEDIA_DATA_READY.json',audio_ready=H/'MEDIA_AUDIO_READY.json',audio_dir=V/'audio')
 assert m['readiness']() is not None;m['duration_contract']()
 # Verify production plan, compared with the candidate, without synthesis.
 spec=runpy.run_path(str(V/'audio/build_narration.py'))
 live=spec['make_plan'](V,V/'audio/script_templates.json')
 assert live==read(S/'audio/NARRATION_PLAN_v404.json')
 assert live['plan_sha256']==read(V/'audio/NARRATION_BUILD.json')['plan_sha256']
 closure=m['collect'](V);assert len(closure)>=43
 prior=[]
 for p in (V/'cinema/render/jobs').glob('*.json'):
  j=read(p)
  assert j.get('metadata',{}).get('source')!='v404','Existing v404 capture; reconcile before starting'
  if '.progress.' not in p.name:prior.append(pin(p))
 for n in ['MEDIA_WORKER_TESTS.json','MEDIA_READY_CONTRACT_TESTS.json']:
  tests=read(H/n);assert tests['status']=='PASS' and tests['worker']==m['pin'](H/'media_v404_worker.py')
 assert not list((V/'render/.pipeline').glob('*.lock'))
 prepared={'status':'PASS_PREPARED_ONLY','source':'v404','source_sha256':live['seal_pin'],'data_ready':pin(H/'MEDIA_DATA_READY.json'),'audio_ready':pin(H/'MEDIA_AUDIO_READY.json'),'audio_review':pin(H/'AUDIO_RESULT_REVIEW.json'),'integration':pin(H/'INTEGRATION.json'),'worker':pin(H/'media_v404_worker.py'),'backup':pin(H/'MEDIA_V402_BACKUP.json'),'render_closure':closure,'preflight':pf}
 create(H/'MEDIA_PREPARED.json',prepared)
 intent={'status':'INTENT_BEFORE_SINGLE_BROWSER_PIPELINE','source':'v404','source_sha256':live['seal_pin'],'data_ready':pin(H/'MEDIA_DATA_READY.json'),'audio_ready':pin(H/'MEDIA_AUDIO_READY.json'),'numeric_review':pin(H/'PARENT_NUMERIC_REVIEW.json'),'media_prepared':pin(H/'MEDIA_PREPARED.json'),'render_closure':closure,'previous_jobs':prior,'pipeline_url':'http://127.0.0.1:8797/cinema/index.html?pipeline=all','scope':'One capture sequence: film1 224s, film2 360s, loop16s; source unchanged before and after.'}
 create(H/'RENDER_INTENT.json',intent)
 create(H/'MEDIA_GO.json',{'status':'GO','actor':'codex-video-v7','authorization':'explicit_parent_go','authorization_text':'ADENDO H authorizes a single v404 capture after the exact six audio units and scientific comparison. All prerequisite receipts are now bound. No publication by this session.','order':pin(ORDER),'source':'v404','source_sha256':live['seal_pin'],'worker':m['pin'](H/'media_v404_worker.py'),'render_intent':pin(H/'RENDER_INTENT.json'),'data_ready':pin(H/'MEDIA_DATA_READY.json'),'audio_ready':pin(H/'MEDIA_AUDIO_READY.json')})
 m['launch_guard']();stable_seal()
 progress.update('ordem022-v404-single-render-release','v404_single_capture_released','Iniciar uma única captura pelo navegador e recuperar seus IDs; worker codifica após a captura, sem novo pipeline.',[
  {'id':'01a18565-da97-7262-a373-84caaf4a335a:integration-review','status':'completed','evidence':str(H/'INTEGRATION_REVIEW.json')},
  {'id':'01a18564-e297-79e1-83f7-2abc403040bd:audio-result-review','status':'completed','evidence':str(H/'AUDIO_RESULT_REVIEW.json')},
  {'id':'v404-capture-pipeline-adendo-h','kind':'local_render','status':'running','task_id':'ADENDO_H_V404','evidence':str(H/'RENDER_INTENT.json')},
  {'id':'v404-media-worker-adendo-h','kind':'local_encode','status':'running','task_id':'ADENDO_H_V404','evidence':str(H/'MEDIA_GO.json')}])
 print(json.dumps({'status':'GO_SINGLE_CAPTURE','closure_files':len(closure),'source_sha256':live['seal_pin']}))

if __name__=='__main__':main()
