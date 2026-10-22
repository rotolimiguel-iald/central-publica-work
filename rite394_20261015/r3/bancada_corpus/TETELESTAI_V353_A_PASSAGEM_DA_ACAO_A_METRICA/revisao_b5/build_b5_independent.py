from pathlib import Path
from datetime import datetime
import hashlib,json,os,re,subprocess,sys,time,traceback
R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
S=R/'s';OUT=R/'revisao_b5';SRC=R/'kernel';BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f');A=OUT/('independent_'+STAMP)
NEW=['TGLExt.TheAngleReachesTheMetric','TGLExt.AuditMetricAngle']
def now():return datetime.now().astimezone().isoformat()
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def fresh(p,b):
 assert p.resolve().is_relative_to(OUT.resolve()) or p.resolve().is_relative_to(S.resolve())
 p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists(),p
 tmp=p.with_name(p.name+'.tmp_'+STAMP)
 with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert tmp.read_bytes()==b;os.replace(tmp,p)
def save(p,d):fresh(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def load(p):return json.loads(p.read_bytes())
def ck(rec):assert pin(Path(rec['path']))==rec,rec
def uncomment(text):
 out=[];depth=0;i=0
 while i<len(text):
  if text.startswith('/-',i):depth+=1;i+=2
  elif depth and text.startswith('-/',i):depth-=1;i+=2
  elif depth:
   if text[i]=='\n':out.append('\n')
   i+=1
  elif text.startswith('--',i):
   j=text.find('\n',i);i=len(text) if j<0 else j
  else:out.append(text[i]);i+=1
 assert not depth;return ''.join(out)
def main():
 A.mkdir()
 prior=R/'revisao_b4'/'compilation.json';b4=load(prior);assert b4['all_accepted_builds_exit_zero']
 inherited=b4['inherited_project_objects']+[dict(object=x['own'],trace=x['trace']) for x in b4['objects']]
 assert len(inherited)==117
 for x in inherited:ck(x['object']);ck(x['trace'])
 protected=list(b4['protected_pins'])+[pin(prior),pin(R/'revisao_b4'/'REVIEW_B4_FINAL.md'),pin(R/'revisao_b4'/'REVIEW_B4_FINAL.json')]
 for p in ['MANIFESTO_B3.json','RECIBO_B3.json','MANIFESTO_B4.json','RECIBO_B4.json']:
  if (R/p).exists():protected.append(pin(R/p))
 for x in protected:ck(x)
 au=load(R/'AUDITORIA_B5.json')
 for x in au['sources']+au['objects']+[au['positive_build']]:ck(x)
 metas=load(R/'ALVOS_B5.json');assert metas==au['targets'];targets=[t['name'] for t in metas]
 assert len(targets)==len(set(targets))==4
 assert [sum(t['kind']==k for t in metas) for k in ['theorem','def','structure']]==[4,0,0]
 records=[];seen=set();declarations=[]
 def visit(mod):
  if mod in seen:return
  seen.add(mod);p=SRC/(mod.replace('.','/')+'.lean');b=p.read_bytes();code=uncomment(b.decode('utf-8-sig'))
  imports=[]
  for m in re.finditer(r'^\s*(?:public\s+)?import\s+([^\n]+)',code,re.M):imports+=m.group(1).split()
  for d in imports:
   if d.startswith(('TGL.','TGLExt.')) or d in ['TGL','TGLExt']:visit(d)
  q=S/p.relative_to(SRC);new=not q.exists();obj=S/'.lake/build/lib/lean'/(mod.replace('.','/')+'.olean')
  if new:assert mod in NEW and not obj.exists();fresh(q,b)
  else:assert q.read_bytes()==b,(mod,'Source drift; do not overwrite')
  if mod in NEW:
   assert new and not obj.exists()
   fresh(A/p.name,b)
   assert not re.findall(r'\b(?:sorry|axiom|admit|native_decide|trustCompiler|unsafe)\b',code)
   if mod!=NEW[-1]:
    for m in re.finditer(r'^(def|theorem|structure)\s+(\w+)\b',code,re.M):
     namespace='ChatgptAudit.FLRW.'
     end=code.find('where' if m.group(1)=='structure' else ':=',m.end())
     declarations.append(dict(name=namespace+m.group(2),kind=m.group(1),module=mod,line=code[:m.start()].count('\n')+1,statement=code[m.start():end].strip()))
  records.append(dict(module=mod,source=pin(p),copy=pin(q),new_source_copy=new,imports=imports))
 visit(NEW[-1]);assert {x['name'] for x in declarations}==set(targets)
 assert re.findall(r'^#print axioms\s+(\S+)',(S/'TGLExt/AuditMetricAngle.lean').read_text(encoding='utf-8-sig'),re.M)==targets
 text='import TGLExt.TheAngleReachesTheMetric\n\nset_option pp.universes true\n\n'+''.join(f'#check {t}\n#print axioms {t}\n\n' for t in targets)
 own=S/'TGLExt/ReviewMetricAngle.lean';fresh(own,text.encode('utf8'))
 docs=[]
 for name in ['REAPROVEITAMENTO_B5.md','REAPROVEITAMENTO_B5.json','AUDITORIA_B5.json','ALVOS_B5.json']:
  p=R/name;fresh(A/name,p.read_bytes());docs.append(pin(p))
 for name in ['lakefile.toml','lake-manifest.json','lean-toolchain']:assert (S/name).read_bytes()==(SRC/name).read_bytes()
 snapshot=dict(timestamp=now(),sources=records,targets=targets,declarations=declarations,documents=docs,own_auditor=pin(own),source_configs=[pin(S/name) for name in ['lakefile.toml','lake-manifest.json','lean-toolchain']],inherited_B4_compilation=pin(prior),inherited_project_objects=inherited,protected_before=protected,project_objects_copied_from_author=False,cache_inheritance=b4['cache_inheritance'])
 save(A/'snapshot.json',snapshot);save(OUT/'B5_SNAPSHOT_POINTER.json',dict(snapshot=pin(A/'snapshot.json'),attempt=str(A)))
 env=os.environ.copy()
 for k in ['LEAN_PATH','LEAN_SRC_PATH']:env.pop(k,None)
 env['PATH']=str(BIN)+os.pathsep+env.get('PATH','');env['GIT_OPTIONAL_LOCKS']='0'
 n=int(env.get('GIT_CONFIG_COUNT','0'));safe=[]
 for i,pkg in enumerate(load(S/'lake-manifest.json')['packages'],n):
  p=(S/'.lake/packages'/pkg['name']).resolve();assert p.is_relative_to(S.resolve());safe.append(str(p))
  env[f'GIT_CONFIG_KEY_{i}']='safe.directory';env[f'GIT_CONFIG_VALUE_{i}']=str(p).replace('\\','/')
 env['GIT_CONFIG_COUNT']=str(n+len(safe))
 save(A/'environment_scope.json',dict(process_only_git_safe_directory=safe,global_git_config_modified=False,lean_path_removed=True,script=pin(Path(__file__))))
 command=[str(BIN/'lake.exe'),'build',*NEW,'TGLExt.ReviewMetricAngle'];start=time.time()
 with (A/'lake_stdout.txt').open('xb') as out,(A/'lake_stderr.txt').open('xb') as err:
  p=subprocess.Popen(command,cwd=S,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
  save(A/'process.json',dict(pid=p.pid,command=command,cwd=str(S),started=now()))
  print('B5_LAKE_STARTED',p.pid,str(A),'INHERITED_117_PINNED',flush=True);rc=p.wait()
 run=dict(returncode=rc,elapsed_seconds=time.time()-start,finished=now(),command=command,cwd=str(S),streams=[pin(A/'lake_stdout.txt'),pin(A/'lake_stderr.txt')],toolchain=subprocess.check_output([str(BIN/'lean.exe'),'--version'],env=env).decode().strip(),executables=[pin(BIN/'lean.exe'),pin(BIN/'lake.exe')])
 save(A/'run.json',run);print('B5_LAKE_EXIT',rc,flush=True)
 for x in protected:ck(x)
 for x in inherited:ck(x['object']);ck(x['trace'])
 for x in records:ck(x['source']);ck(x['copy'])
 save(A/'completion.json',dict(status='BUILD_RC0__REVIEW_PENDING' if rc==0 else 'BUILD_FAILED',run=pin(A/'run.json'),snapshot=pin(A/'snapshot.json'),B1_B2_B4_protected_unchanged=True,inherited_117_objects_unchanged=True,timestamp=now()))
 return rc
if __name__=='__main__':
 try:sys.exit(main())
 except Exception:
  if A.exists():save(A/'driver_failure.json',dict(error=traceback.format_exc(),timestamp=now()))
  raise
