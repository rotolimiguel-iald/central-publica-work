from pathlib import Path
from datetime import datetime
import hashlib,json,os,subprocess,time
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
OWN=ROOT/'r'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):
 b=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8');t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b;os.replace(t,p)
assert OWN.resolve().is_relative_to(ROOT.resolve())
assert (OWN/'attempt_01_path_length'/'run.json').exists() and (OWN/'attempt_02_short_path'/'run.json').exists()
env=os.environ.copy()
for k in ['LEAN_PATH','LEAN_SRC_PATH']:env.pop(k,None)
env['PATH']=str(BIN)+os.pathsep+env.get('PATH','')
cmd=[str(BIN/'lake.exe'),'build','TGLExt.TheSameBetaReadsThreeFaces','TGLExt.AuditSameBeta','TGLExt.ReviewSameBeta']
start=time.time()
with (OWN/'lake_stdout.txt').open('wb') as out,(OWN/'lake_stderr.txt').open('wb') as err:
 p=subprocess.Popen(cmd,cwd=OWN,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
 save(OWN/'process.json',{'pid':p.pid,'command':cmd,'cwd':str(OWN),'started':datetime.now().astimezone().isoformat(),'lean_path_removed':True})
 save(OWN/'state.json',{'status':'LAKE_RUNNING','pid':p.pid,'root':str(OWN)})
 print('LAKE_STARTED',p.pid,flush=True);rc=p.wait()
run={'returncode':rc,'command':cmd,'cwd':str(OWN),'elapsed_seconds':time.time()-start,'finished':datetime.now().astimezone().isoformat(),'version':subprocess.check_output([str(BIN/'lean.exe'),'--version']).decode().strip(),'lean_binary_sha256':sha((BIN/'lean.exe').read_bytes()),'lake_binary_sha256':sha((BIN/'lake.exe').read_bytes()),'streams':[],'path_remapping':str(ROOT/'revisao'/'B1_BUILD_ROOT_REMAP.json')}
for n in ['lake_stdout.txt','lake_stderr.txt']:
 f=OWN/n;run['streams'].append({'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())})
save(OWN/'run.json',run);save(OWN/'state.json',{'status':'LAKE_FINISHED','returncode':rc,'root':str(OWN)})
print('LAKE_EXIT',rc,flush=True)
raise SystemExit(rc)
