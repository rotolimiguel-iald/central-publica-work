"""Finalize only the one completed v404 pipeline; preserve original worker receipts."""
from context import *
sys.path.insert(0,str(H))
import subprocess,time
from finalizer_guards import validate_frozen_data,validate_replay,require_current,preserve_render_manifest_before_make,build_render_manifest_link
from current_audio_guard import validate_audio
from final_job_guards import validate_worker_jobs

def main():
 check();stable_seal();source=validate_frozen_data(H,V,N);validate_replay(V,source);validate_audio(H,V,source)
 require_current(read(H/'MEDIA_WATCH.json'),source,{'COMPLETE'})
 assert not (H/'FINAL_MAKE.json').exists(),'Recover prior finalizer, never duplicate'
 jobs=validate_worker_jobs(H,V,source)
 create(H/'PRE_MAKE_JOB_BINDING.json',jobs)
 stage=preserve_render_manifest_before_make(H,V,source)
 before=[pin(N/n) for n in ['um.py','um_absoluto.json','um_absoluto_selo.json']]
 command=[r'C:\Python314\python.exe','-B','-X','utf8',str(V.parent/'make_v7.py'),'--selo',str(N/'um_absoluto_selo.json'),'--finalize-only','--reuse-render','--no-open']
 create(H/'FINAL_MAKE_INTENT.json',{'status':'FINALIZE_ONLY_INTENT','source':'v404','source_sha256':source,'command':command,'media_watch':pin(H/'MEDIA_WATCH.json'),'stage':stage,'job_binding':pin(H/'PRE_MAKE_JOB_BINDING.json')})
 assert validate_worker_jobs(H,V,source)==jobs
 start=time.perf_counter();r=subprocess.run(command,capture_output=True,text=True,encoding='utf-8');elapsed=time.perf_counter()-start
 after=[pin(N/n) for n in ['um.py','um_absoluto.json','um_absoluto_selo.json']]
 stable_seal();validate_frozen_data(H,V,N)
 receipt={'status':'PASS' if r.returncode==0 and before==after else 'FAILED','source':'v404','source_sha256':source,'command':command,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'elapsed_seconds':elapsed,'canonical_before':before,'canonical_after':after,'canonical_unchanged':before==after,'builder':pin(V/'make_v7.py')}
 if receipt['status']=='PASS':
  assert validate_worker_jobs(H,V,source)==jobs
  create(H/'FINAL_RENDER_MANIFEST_LINK.json',build_render_manifest_link(H,V,source,stage));receipt['render_manifest_link']=pin(H/'FINAL_RENDER_MANIFEST_LINK.json');receipt['manifests']=[pin(p) for p in [V/'PUBLIC_DELIVERY_V7.json',V/'RENDER_MANIFEST.json',V.parent/'PUBLIC_DELIVERY_V7.json']]
 create(H/'FINAL_MAKE.json',receipt);print(json.dumps({k:receipt[k] for k in ['status','returncode','stdout','stderr','elapsed_seconds','canonical_unchanged']}));assert receipt['status']=='PASS'

if __name__=='__main__':main()
