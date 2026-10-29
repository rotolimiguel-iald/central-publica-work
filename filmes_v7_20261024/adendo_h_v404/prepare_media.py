"""Reuse proven export worker; preserve accepted v402 media before replacement."""
from context import *
import ast, shutil

def derive():
 assert not (H/'MEDIA_START.json').exists()
 names={'media_v402_worker.py':'media_v404_worker.py','start_media_v402.py':'start_media_v404.py','test_media_v402_worker.py':'test_media_v404_worker.py','test_media_ready_v402.py':'test_media_ready_v404.py'}
 receipts=[]
 for old,new in names.items():
  text=(E/old).read_text(encoding='utf-8').replace('v402','v404').replace('V402','V404').replace('ADENDO E worker','ADENDO H worker')
  text=text.replace('MEDIA_V401_BACKUP','MEDIA_V402_BACKUP').replace('baseline_manifest_v401','baseline_manifest_v402').replace('media_v401_history','media_v402_history')
  if old=='media_v402_worker.py':
   text=text.replace("TASK, ACTOR, VERSION = 'V404_MEDIA', 'codex-video-web', 'v404'","TASK, ACTOR, VERSION = 'ADENDO_H_V404', 'codex-video-v7', 'v404'")
   text=text.replace("mission, collect = legacy['mission'], legacy['collect']","mission, collect = legacy['mission'], legacy['collect']\nmission['project'] = lambda: mission['call']({'operation':'project','max_chars':450000})")
   text=text.replace("ready['actor'] == 'codex-video-audio'","ready['actor'] == 'codex-video-v404-audio'")
  text=text.replace("'max_chars':100000","'max_chars':450000")
  ast.parse(text);atomic(H/new,text.encode('utf-8'))
  receipts.append({'before':pin(E/old),'after':pin(H/new)})
 create(H/'MEDIA_DERIVATION.json',{'status':'PREPARED_NO_RENDER','files':receipts,'changes':'Source version; history references; parent task/actor; actual audio executor; projection capacity. Worker algorithms unchanged.'})
 print(json.dumps({'status':'MEDIA_DERIVED','files':len(receipts)}))

def backup():
 check();stable_seal()
 assert not (H/'MEDIA_V402_BACKUP.json').exists(),'Recover existing backup receipt'
 manifest=read(V/'PUBLIC_DELIVERY_V7.json');validation=read(V/'render/MEDIA_VALIDATION.json')
 assert manifest['source']==validation['source']=='v402'
 assert len(validation['movies'])==16 and len(validation['images'])==25
 files=set(V/x['path'] for x in manifest['public_files'])
 files|={Path(x['file']) for x in validation['movies']+validation['images']}
 for record in (V/'render/.pipeline').glob('*.json'):
  d=read(record)
  if d.get('status')=='COMPLETE':
   files|={Path(x['file']) for x in d.get('outputs',[]) if Path(x['file']).is_relative_to(V/'render/private') and '_silent.' in x['file']}
 watch=read(E/'MEDIA_WATCH.json');assert watch['status']=='COMPLETE'
 for r in watch['completed'].values():
  p=Path(r['file']);assert pin(p)['sha256']==r['sha256'];files.add(p)
  d=read(p);q=Path(d['file']);q=q if q.is_absolute() else V/'cinema/render/jobs'/q;files.add(q)
 for stage in read(V/'render/ASSETS_AUDIT.json')['stages']:
  files|={Path(x['file']) for x in stage['inputs'] if Path(x['file']).is_relative_to(V/'cinema/render/stills')}
 for folder in ['render','render/.pipeline','web','slides']:
  if folder=='slides' and not (V/folder).exists():continue
  files|={p for p in (V/folder).iterdir() if p.is_file() and '.bak_' not in p.name}
 files|={V/r for r in ['make_v7.py','cinema/studio.mjs','cinema/media_v7.py','cinema/mp4_metrics.py','cinema/render_sources.py','RENDER_MANIFEST.json','PUBLIC_DELIVERY_V7.json']}
 assert all(p.is_relative_to(V) and p.is_file() for p in files)
 need=sum(p.stat().st_size for p in files);assert shutil.disk_usage(H).free>need+(5<<30)
 rows=[]
 for p in sorted(files):
  expected=pin(p);q=H/'media_v402_history'/p.relative_to(V);q.parent.mkdir(parents=True,exist_ok=True)
  if not q.exists():
   tmp=q.with_name(q.name+'.partial');assert not tmp.exists()
   with p.open('rb') as f,tmp.open('xb') as out:shutil.copyfileobj(f,out,4<<20);out.flush();os.fsync(out.fileno())
   assert sha(tmp)==expected['sha256'];os.rename(tmp,q)
  assert sha(q)==expected['sha256'] and pin(p)==expected
  rows.append({'original':expected,'backup':{'file':str(q),'bytes':q.stat().st_size,'sha256':sha(q)}})
 public=[]
 for p,name in [(V/'RENDER_MANIFEST.json','RENDER_MANIFEST.json'),(V/'PUBLIC_DELIVERY_V7.json','PUBLIC_DELIVERY_V7.json'),(V.parent/'PUBLIC_DELIVERY_V7.json','ROOT_PUBLIC_DELIVERY_V7.json')]:
  q=H/'baseline_manifest_v402'/name;atomic(q,p.read_bytes());assert sha(q)==sha(p);public.append(pin(q))
 create(H/'MEDIA_V402_BACKUP.json',{'status':'PASS_PRESERVED_BYTES','source':'v402','target_source':'v404','source_sha256':manifest['source_sha256'],'media_count':16,'image_count':25,'files':rows,'total_bytes':need,'public_baseline':public,'scope':'Byte backup of current accepted media/capture inputs/receipts and public resources. No render or production edits.'})
 print(json.dumps({'status':'PRESERVED','files':len(rows),'bytes':need}))
if __name__=='__main__':{'derive':derive,'backup':backup}[sys.argv[1]]()
