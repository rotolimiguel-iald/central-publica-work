from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def put(p,b):
 assert p.is_relative_to(R) and not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
attempt=R/'attempts/20260914_173309_164705';run=load(attempt/'run.json')
assert run['returncode']==0 and run['sources_unchanged_during_build']
targets=load(R/'ALVOS_RETORNO_A1B.json');names=[t['name'] for t in targets]
env=os.environ.copy();env.pop('LEAN_PATH',None);env.pop('LEAN_SRC_PATH',None);env['PATH']=str(BIN)+os.pathsep+env['PATH']
packages=sorted(p for p in (K/'.lake/packages').iterdir() if (p/'.git').exists())
env['GIT_CONFIG_COUNT']=str(len(packages))
for i,p in enumerate(packages):env[f'GIT_CONFIG_KEY_{i}']='safe.directory';env[f'GIT_CONFIG_VALUE_{i}']=str(p)
A=R/'audit_orphans'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True)
rows=[]
for s in [K/'TGLExt/AuditA1Orphans.lean',R/'probes/BadAntiunitaryPhase.lean',R/'probes/BadImaginaryScaling.lean']:
 put(A/s.name,s.read_bytes());cmd=[str(BIN/'lake.exe'),'env','lean',str(s)]
 p=subprocess.run(cmd,cwd=K,env=env,capture_output=True)
 out=A/(s.stem+'.stdout.txt');err=A/(s.stem+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
 rows.append(dict(label=s.stem,command=cmd,returncode=p.returncode,source=pin(s),stdout=pin(out),stderr=pin(err)))
 print(s.stem,p.returncode,flush=True)
put(A/'commands.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
text=Path(rows[0]['stdout']['path']).read_text(encoding='utf8');ax={}
for name,s in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",text,re.S):
 ax[name]=[re.sub(r'\.\{[^}]*\}$','',a.strip()) for a in s.split(',') if a.strip()]
for name in re.findall(r"'([^']+)' does not depend on any axioms",text):ax[name]=[]
assert set(ax)==set(names) and all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in ax.values())
assert rows[0]['returncode']==0
for row in rows[1:]:
 text=Path(row['stdout']['path']).read_text(encoding='utf8').lower()
 assert row['returncode']!=0 and 'type mismatch' in text
 assert not any(t in text for t in ['unknown identifier','unknown module','object file','timeout'])
records=load(R/'FONTES_REPLAY.json')
for r in records:
 assert pin(Path(r['original']['path']))==r['original']
 assert pin(Path(r['copy']['path']))==r['copy']
modules=[]
for n in sorted({t['module'] for t in targets}):
 s=K/'TGLExt'/f'{n}.lean';c=s.read_text(encoding='utf8');c=re.sub(r'/-.*?-/', '',c,flags=re.S);c=re.sub(r'--[^\n]*','',c)
 assert not re.search(r'\b(sorry|axiom|native_decide|trustCompiler|admit|unsafe)\b',c)
 modules.append(dict(name=n,source=pin(s),object=pin(K/'.lake/build/lib/lean/TGLExt'/f'{n}.olean')))
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='AUTHOR_STANDALONE_AUDIT_PASS__A1B_TRACE_OPEN',positive_build=pin(attempt/'run.json'),
 modules=modules,targets=targets,axioms=ax,all_axioms_allowed=True,existing_theorems=36,existing_definitions=4,new_theorems=0,
 commands=rows,negative_controls_rejected=True,source_copies_reverified=len(records),original_sources_unchanged=True,
 dev_dependencies_used=False,external_package_cache_inherited=True,project_objects_inherited=False,full_trace_constructed=False,
 canonical_written=False,empirical_work=False)
put(R/'AUDITORIA_ORFAOS_A1B.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(existing_targets=len(targets),new_theorems=0,all_axioms_allowed=True,negatives_rejected=True)))
