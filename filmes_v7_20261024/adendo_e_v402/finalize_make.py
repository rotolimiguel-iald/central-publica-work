"""Close the existing completed render, never generate another one."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
from finalizer_guards import (validate_frozen_data, validate_replay, validate_audio, require_current,
                              preserve_render_manifest_before_make, build_render_manifest_link)
A=Path(__file__).resolve().parent
sys.path.insert(0,str(A.parent));import mission
R=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um');V=R/'delivery_v7';N=R.parent/'Nós'
def read(p):return json.loads(p.read_bytes())
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def pin(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,d):
 b=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
 if p.exists():
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+str(time.time_ns()));bk.write_bytes(old);assert bk.read_bytes()==old
 tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b;os.replace(tmp,p)
source = validate_frozen_data(A, V, N)
validate_replay(V, source)
validate_audio(A, V, source)
require_current(read(A/'MEDIA_WATCH.json'), source, {'COMPLETE'})
p=mission.project();t=next(t for t in p['projection']['active']+p['projection']['settled'] if t['id']=='ADENDO_E_V402')
assert mission.call({'operation':'check',**mission.current('codex-video-v7'),'task_id':'ADENDO_E_V402','lease_id':t['lease']['id'],'max_chars':100000})['ready']
paths=[N/'um.py',N/'um_absoluto.json',N/'um_absoluto_selo.json']
before=[pin(p) for p in paths];h=read(V/'data/hud.json');s=read(N/'um_absoluto_selo.json')
assert s['um_version']==h['seal_version']=='v402' and s['sha256']['um.py']==h['seal_pin']
manifest_stage=preserve_render_manifest_before_make(A, V, source)
cmd=[r'C:\Python314\python.exe','-B','-X','utf8',str(R/'make_v7.py'),'--selo',str(N/'um_absoluto_selo.json'),'--finalize-only','--reuse-render','--no-open']
start=time.perf_counter();r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');elapsed=time.perf_counter()-start
after=[pin(p) for p in paths]
validate_frozen_data(A, V, N)
receipt={'status':'PASS' if r.returncode==0 and before==after else 'FAILED','command':cmd,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'elapsed_seconds':elapsed,'canonical_before':before,'canonical_after':after,'canonical_unchanged':before==after,'builder':pin(V/'make_v7.py'),'source':'v402','source_sha256':h['seal_pin']}
if receipt['status']=='PASS':
 save(A/'FINAL_RENDER_MANIFEST_LINK.json', build_render_manifest_link(A, V, source, manifest_stage))
 receipt['render_manifest_link']=pin(A/'FINAL_RENDER_MANIFEST_LINK.json')
 receipt['manifests']=[pin(p) for p in [V/'PUBLIC_DELIVERY_V7.json',V/'RENDER_MANIFEST.json',R/'PUBLIC_DELIVERY_V7.json']]
save(A/'FINAL_MAKE.json',receipt);print(json.dumps({k:receipt[k] for k in ['status','returncode','stdout','stderr','elapsed_seconds','canonical_unchanged']},ensure_ascii=False))
assert receipt['status']=='PASS'
