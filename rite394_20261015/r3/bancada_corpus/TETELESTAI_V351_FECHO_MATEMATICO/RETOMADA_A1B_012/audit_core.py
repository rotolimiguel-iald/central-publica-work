from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys
R=Path(__file__).resolve().parent;K=R/'k';BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
attempt=R/'core_attempts'/sys.argv[1];run=json.loads((attempt/'run.json').read_text(encoding='utf8'))
assert run['returncode']==0 and run['sources_unchanged_during_build']
for s in run['sources']:assert pin(Path(s['path']))==s
mods=['V351ScalarImaginaryLeftTransport','V351ScalarImaginaryCoreAction'];targets=[]
for mod in mods:
 p=K/'TGLExt'/f'{mod}.lean';s=p.read_text(encoding='utf8');clean=re.sub(r'/-.*?-/', '',s,flags=re.S);clean=re.sub(r'--[^\n]*','',clean)
 assert not re.search(r'\b(sorry|axiom|native_decide|trustCompiler|admit|unsafe)\b',clean)
 for m in re.finditer(r'^theorem (\w+)[\s\S]*?(?= :=)',s,re.M):targets.append(dict(name='TGLV350.Regular.'+m[1],module=mod,line=s[:m.start()].count('\n')+1,statement=m[0],source=pin(p)))
assert len(targets)==5
env=os.environ.copy();env.pop('LEAN_PATH',None);env.pop('LEAN_SRC_PATH',None);env['PATH']=str(BIN)+os.pathsep+env['PATH']
packages=sorted(p for p in (K/'.lake/packages').iterdir() if (p/'.git').exists());env['GIT_CONFIG_COUNT']=str(len(packages))
for i,p in enumerate(packages):env[f'GIT_CONFIG_KEY_{i}']='safe.directory';env[f'GIT_CONFIG_VALUE_{i}']=str(p)
A=R/'audit_core'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True);rows=[]
for s in [K/'TGLExt/AuditA1CoreAction.lean',R/'probes/BadLeftConjugatePhase.lean',R/'probes/BadCoreMissingAdjoint.lean']:
 put(A/s.name,s.read_bytes());cmd=[str(BIN/'lake.exe'),'env','lean',str(s)];p=subprocess.run(cmd,cwd=K,env=env,capture_output=True)
 out=A/(s.stem+'.stdout.txt');err=A/(s.stem+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
 rows.append(dict(label=s.stem,command=cmd,returncode=p.returncode,source=pin(s),stdout=pin(out),stderr=pin(err)));print(s.stem,p.returncode,flush=True)
put(A/'commands.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
text=Path(rows[0]['stdout']['path']).read_text(encoding='utf8');ax={}
for name,s in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",text,re.S):ax[name]=[re.sub(r'\.\{[^}]*\}$','',a.strip()) for a in s.split(',') if a.strip()]
for name in re.findall(r"'([^']+)' does not depend on any axioms",text):ax[name]=[]
assert rows[0]['returncode']==0 and set(ax)=={t['name'] for t in targets} and all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in ax.values())
for row in rows[1:]:
 text=Path(row['stdout']['path']).read_text(encoding='utf8').lower()
 assert row['returncode']!=0 and 'type mismatch' in text and not any(t in text for t in ['unknown identifier','unknown module','object file','timeout'])
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='AUTHOR_STANDALONE_AUDIT_PASS__FULL_TRACE_STILL_OPEN',targets=targets,axioms=ax,all_axioms_allowed=True,new_theorems=5,new_definitions=0,commands=rows,positive_build=pin(attempt/'run.json'),negative_controls_rejected=True,modules=[dict(name=m,source=pin(K/'TGLExt'/f'{m}.lean'),object=pin(K/'.lake/build/lib/lean/TGLExt'/f'{m}.olean')) for m in mods],gate_changed=False,full_trace_constructed=False,dev_objects_used=False)
put(R/'AUDITORIA_ACAO_CORE_A1B.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'));print(json.dumps(dict(new_theorems=5,axioms_allowed=True,negative_controls_rejected=True)))
