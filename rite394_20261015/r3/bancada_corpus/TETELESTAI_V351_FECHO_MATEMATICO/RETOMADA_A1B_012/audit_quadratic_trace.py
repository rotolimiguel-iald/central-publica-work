from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys
R=Path(__file__).resolve().parent;K=R/'k'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
attempt=R/'quadratic_trace_attempts'/sys.argv[1]
run=json.loads((attempt/'run.json').read_text(encoding='utf8'))
assert run['returncode']==0 and run['sources_unchanged_during_build']
for row in run['sources']:assert pin(Path(row['path']))==row
targets=[];modules=[];private_count=0
for mod in ['V351QuadraticTrace','V351RegularCoreTraceConstruction']:
 source=K/'TGLExt'/f'{mod}.lean';s=source.read_text(encoding='utf8')
 clean=re.sub(r'/\-.*?\-/','',s,flags=re.S);clean=re.sub(r'--[^\n]*','',clean)
 assert not re.search(r'\b(sorry|axiom|native_decide|trustCompiler|admit|unsafe)\b',clean)
 for m in re.finditer(r'^(def|theorem) (\w+)',s,re.M):
  start=m.start();depth=0;end=None
  for j in range(m.end(),len(s)):
   if depth==0 and (s.startswith(' :=',j) or s.startswith(' where',j)):
    end=j;break
   if s[j] in '([{':depth+=1
   elif s[j] in ')]}':depth-=1
  assert end is not None
  targets.append(dict(kind=m[1],name='TGLV350.Regular.'+m[2],module=mod,line=s[:start].count('\n')+1,statement=s[start:end],source=pin(source)))
 private_count+=len(re.findall(r'^private theorem ',s,re.M))
 assert not re.search(r'^private def ',s,re.M)
 modules.append(dict(name=mod,source=pin(source),object=pin(K/'.lake/build/lib/lean/TGLExt'/f'{mod}.olean')))
assert len(targets)==2 and sum(t['kind']=='theorem' for t in targets)==1 and private_count==6
env=os.environ.copy();env.pop('LEAN_PATH',None);env.pop('LEAN_SRC_PATH',None);env['PATH']=str(BIN)+os.pathsep+env['PATH']
packages=sorted(p for p in (K/'.lake/packages').iterdir() if (p/'.git').exists())
env['GIT_CONFIG_COUNT']=str(len(packages))
for i,p in enumerate(packages):env[f'GIT_CONFIG_KEY_{i}']='safe.directory';env[f'GIT_CONFIG_VALUE_{i}']=str(p)
A=R/'audit_quadratic_trace'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True)
rows=[]
for source in [K/'TGLExt/AuditA1QuadraticTrace.lean',R/'probes/BadQuadraticTraceZeroChanged.lean']:
 put(A/source.name,source.read_bytes());cmd=[str(BIN/'lake.exe'),'env','lean',str(source)]
 p=subprocess.run(cmd,cwd=K,env=env,capture_output=True)
 out=A/(source.stem+'.stdout.txt');err=A/(source.stem+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
 rows.append(dict(label=source.stem,command=cmd,returncode=p.returncode,source=pin(source),stdout=pin(out),stderr=pin(err)))
 print(source.stem,p.returncode,flush=True)
put(A/'commands.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
text=Path(rows[0]['stdout']['path']).read_text(encoding='utf8');axioms={}
for name,body in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",text,re.S):
 axioms[re.sub(r'\.\{[^}]*\}$','',name)]=[re.sub(r'\.\{[^}]*\}$','',a.strip()) for a in body.split(',') if a.strip()]
for name in re.findall(r"'([^']+)' does not depend on any axioms",text):axioms[re.sub(r'\.\{[^}]*\}$','',name)]=[]
assert rows[0]['returncode']==0 and set(axioms)=={t['name'] for t in targets}
assert all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in axioms.values())
negative=Path(rows[1]['stdout']['path']).read_text(encoding='utf8').lower()
assert rows[1]['returncode']!=0 and 'type mismatch' in negative
assert not any(t in negative for t in ['unknown identifier','unknown module','object file','timeout'])
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='AUTHOR_STANDALONE_QUADRATIC_TRACE_PASS__INDEPENDENT_REVIEW_PENDING',
 targets=targets,axioms=axioms,all_axioms_allowed=True,new_theorems=1,new_definitions=1,private_theorems=6,private_definitions=0,
 commands=rows,positive_build=pin(attempt/'run.json'),negative_controls_rejected=True,modules=modules,gate_changed=False,
 core_traciality_proved=True,full_trace_constructed=True,dev_objects_used=False)
put(R/'AUDITORIA_TRACIALIDADE_QUADRATICA_A1B.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(new_theorems=1,new_definitions=1,private_theorems=6,axioms_allowed=True,negative_controls_rejected=True)))
