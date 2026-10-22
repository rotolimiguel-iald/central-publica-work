from pathlib import Path
from datetime import datetime
import ctypes,hashlib,json,os,subprocess,time
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
OWN=ROOT/'revisao'/'b1_20260914_145853'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):
 b=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8');t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b;os.replace(t,p)
old=OWN/'attempt_01_path_length';old.mkdir(exist_ok=True)
for n in ['run.json','process.json','lake_stdout.txt','lake_stderr.txt','state.json']:
 p=OWN/n;b=p.read_bytes();q=old/n
 if q.exists():assert q.read_bytes()==b
 else:q.write_bytes(b)
lib=ctypes.WinDLL('kernel32',use_last_error=True)
fun=lib.GetShortPathNameW;fun.argtypes=[ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_uint];fun.restype=ctypes.c_uint
buf=ctypes.create_unicode_buffer(32768);assert fun(str(OWN),buf,32768)>0
short=buf.value;assert os.path.samefile(short,str(OWN))
restored=0
src=ROOT/'kernel'/'.lake'/'packages'
for base,dirs,files in os.walk(src):
 rel=Path(base).relative_to(src);dest=OWN/'.lake'/'packages'/rel
 if not os.path.exists('\\\\?\\'+str(dest)):
  os.makedirs('\\\\?\\'+str(dest),exist_ok=True);restored+=1
problem=OWN/'.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/IntegralRepresentation.olean.server.hash'
with open('\\\\?\\'+str(problem),'rb') as f:b=f.read()
save(OWN/'path_diagnosis.json',{'failed_path':str(problem),'length':len(str(problem)),'extended_path_exists':True,'bytes':len(b),'sha256':sha(b),'short_cwd':short,'same_directory':True,'empty_package_directories_restored':restored,'interpretation':'Windows normal-path limit, cache bytes present; no source edits or missing proof'})
env=os.environ.copy()
for k in ['LEAN_PATH','LEAN_SRC_PATH']:env.pop(k,None)
env['PATH']=str(BIN)+os.pathsep+env.get('PATH','')
cmd=[str(BIN/'lake.exe'),'build','TGLExt.TheSameBetaReadsThreeFaces','TGLExt.AuditSameBeta','TGLExt.ReviewSameBeta']
start=time.time()
with (OWN/'lake_stdout.txt').open('wb') as out,(OWN/'lake_stderr.txt').open('wb') as err:
 p=subprocess.Popen(cmd,cwd=short,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
 save(OWN/'process.json',{'pid':p.pid,'command':cmd,'cwd':short,'physical_cwd':str(OWN),'started':datetime.now().astimezone().isoformat(),'lean_path_removed':True})
 print('LAKE_STARTED',p.pid,'short cwd',short,flush=True);rc=p.wait()
run={'returncode':rc,'command':cmd,'cwd':short,'physical_cwd':str(OWN),'elapsed_seconds':time.time()-start,'finished':datetime.now().astimezone().isoformat(),'version':subprocess.check_output([str(BIN/'lean.exe'),'--version']).decode().strip(),'lean_binary_sha256':sha((BIN/'lean.exe').read_bytes()),'lake_binary_sha256':sha((BIN/'lake.exe').read_bytes()),'streams':[],'preparation_history':str(old),'path_diagnosis':str(OWN/'path_diagnosis.json')}
for n in ['lake_stdout.txt','lake_stderr.txt']:
 f=OWN/n;run['streams'].append({'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())})
save(OWN/'run.json',run);save(OWN/'state.json',{'status':'LAKE_FINISHED','returncode':rc,'root':str(OWN)})
print('LAKE_EXIT',rc,flush=True)
raise SystemExit(rc)
