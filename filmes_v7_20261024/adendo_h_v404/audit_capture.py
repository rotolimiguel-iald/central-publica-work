"""Verify the single completed capture sequence and recorded coverage masks."""
from context import *
sys.path.insert(0,str(H))
from coverage_validation import validate_samples
import runpy

def main():
 check();stable_seal();assert not (H/'PARENT_CAPTURE_AUDIT.json').exists()
 worker=runpy.run_path(str(H/'media_v404_worker.py'));closure=worker['collect'](V)
 assert closure==read(H/'RENDER_INTENT.json')['render_closure']
 rows={}
 for path in (V/'cinema/render/jobs').glob('*.json'):
  if '.progress.' in path.name:continue
  job=read(path);meta=job.get('metadata',{})
  if meta.get('source')!='v404':continue
  kind=meta['kind'];assert kind in ['film1','film2','loop'] and kind not in rows,'Duplicate/new capture'
  assert meta['source_sha256']==sha(S/'source/um.py') and job['source_files']==closure
  seconds={'film1':224,'film2':360,'loop':16}[kind];dimensions=(1920,1080) if kind=='loop' else (3840,2160)
  assert (meta['width'],meta['height'])==dimensions and meta['duration']==seconds and meta['total']==seconds*60 and job['render']['encoded']==seconds*60
  raw=Path(job['file']);assert raw==path.with_suffix('.h264') and sha(raw)==job['sha256'] and raw.stat().st_size==job['bytes']
  film=read(V/f"data/film{meta['film']}.json");duration=film.get('duration',film.get('total_seconds'))
  coverage=validate_samples(kind,meta,job['render']['samples'],duration)
  rows[kind]={'receipt':pin(path),'stream':pin(raw),'frames':job['render']['encoded'],'elapsed_seconds':job['render']['elapsed_s'],'coverage':coverage,'scene_cpu_submit_seconds':job['render'].get('scene_cpu_submit_seconds'),'overlay_cpu_seconds':job['render'].get('overlay_cpu_seconds'),'cost_scope':job['render'].get('cost_scope')}
 assert set(rows)=={'film1','film2','loop'},'Capture still in progress'
 stable_seal();create(H/'PARENT_CAPTURE_AUDIT.json',{'status':'PASS_WITH_SCOPE','source':'v404','source_sha256':sha(S/'source/um.py'),'jobs':rows,'render_closure':closure,'capture_pipelines':1,'capture_started':pin(H/'BROWSER_CAPTURE_STARTED.json'),'scope':'Exact frame counts, source closure, stream hashes and 1Hz object masks checked. Masks are not a pixel audit or subjective visual rating of encoded MP4 files; monetary compute cost not measured.'})
 print(json.dumps({'status':'PASS_WITH_SCOPE','jobs':{k:v['frames'] for k,v in rows.items()}}))

if __name__=='__main__':main()
