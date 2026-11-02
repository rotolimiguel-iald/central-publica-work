"""Bind actual CUA observations to the completed final local artifacts."""
from context import *
sys.path.insert(0,str(H))
from final_job_guards import validate_worker_jobs,validate_observation_bindings

def main():
 check();stable_seal();source=read(H/'SOURCE_CAPTURE.json')['source_sha256']
 raw=read(H/'FINAL_PLAYER_OBSERVATIONS_RAW.json');obs={x['step']:x['value'] for x in raw['observations']}
 for value in obs.values():assert not value.get('error')
 for film,duration in [('film1',224),('film2',360)]:
  value=obs[film+'_ended'];assert value['ended'] and value['paused'] and value['time']==value['duration']==duration
 for step in ['film1_pt_playing','film1_en_playing_zh_half_speed','film2_en_playing','film2_pt_playing']:
  assert not obs[step]['paused'] and obs[step]['time']>0
 assert obs['film1_en_switch']['time']==obs['film1_pt_chapter']['time']==144
 assert abs(obs['film1_en_frame']['time']-144-1/60)<1e-6
 assert abs(obs['film2_pt_switch']['time']-obs['film2_en_playing']['time'])<0.5
 assert not obs['film2_pt_switch']['paused'] and obs['film2_pt_playing']['ready']==4
 assert obs['film2_pt_chapter']['time']==288 and obs['film2_pt_chapter']['paused']
 assert obs['film1_en_playing_zh_half_speed']['rate']==0.5 and obs['film1_en_playing_zh_half_speed']['language']=='zh-Hans'
 assert any(t['language']=='fr' and t['mode']=='showing' for t in obs['film1_fr_caption']['tracks'])
 assert any(t['language']=='en' and t['mode']=='showing' for t in obs['film1_ended']['tracks'])
 assert 'OK · 61/61 comparações' in raw['replayText'] and source in raw['replayText'] and '19 campos documentais fora do recálculo' in raw['replayText']
 assert raw['finalSelection']=={'film':'2','audio':'pt-BR','language':'pt-BR','time':312,'paused':True}
 completed=validate_worker_jobs(H,V,source)
 from urllib.parse import urlparse,unquote
 media={}
 for label,step in [('film1_pt-BR','film1_pt_initial'),('film1_en','film1_en_switch'),('film2_en','film2_en_initial'),('film2_pt-BR','film2_pt_playing')]:
  url=urlparse(obs[step]['src']);assert url.netloc=='127.0.0.1:8797' and url.path.startswith('/render/')
  p=(V/unquote(url.path).lstrip('/')).resolve();assert p.is_relative_to(V.resolve());media[label]=str(p)
 result={'status':'PASS_OBSERVED_UI','source':'v404','source_sha256':source,'url':'http://127.0.0.1:8797/web/filmes.html',
  'raw_observations':pin(H/'FINAL_PLAYER_OBSERVATIONS_RAW.json'),'screenshots':[pin(H/n) for n in ['FINAL_PLAYER_V404.png','FINAL_PLAYER_FRAME_V404.png']],
  'observed_media':media,'artifact_binding':{'jobs':completed['jobs'],'manifests':[pin(p) for p in [V/'PUBLIC_DELIVERY_V7.json',V/'RENDER_MANIFEST.json',V.parent/'PUBLIC_DELIVERY_V7.json']],'media':[pin(Path(p)) for p in media.values()]},
  'observations':raw['observations'],'final_selection':raw['finalSelection'],'replay':'Observed OK61/61 on the integrated page; 34 numeric anchors and19 documentary fields explicitly distinguished.',
  'automation_negatives':raw['automationNegatives'],'limitations':['UI and media state observed through CUA; no subjective audio audition or physical speaker test.','Short playback and both endings observed, not full visual watching of every frame.','Four automation targeting/observation failures preserved; no media error observed.']}
 create(H/'FINAL_PLAYER_V404.json',result);validate_observation_bindings(H,V,source,completed)
 print(json.dumps({'status':result['status'],'media':len(media),'observations':len(raw['observations']),'replay':result['replay']}))

if __name__=='__main__':main()
