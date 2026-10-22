from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys
R=Path(__file__).resolve().parent;K=R/'kernel'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_name(p.name+'.tmp');q.write_bytes(b)
    assert q.read_bytes()==b;os.replace(q,p)
attempt=R/'attempts'/sys.argv[1]
run=json.loads((attempt/'run.json').read_text(encoding='utf8'))
assert run['returncode']==0 and run['sources_unchanged_during_build']
for s in run['snapshots']:assert pin(Path(s['path']))['sha256']==s['sha256']
targets=json.loads((R/'ALVOS_B2.json').read_text(encoding='utf8'))
names=[t['name'] for t in targets]
env=os.environ.copy();env.pop('LEAN_PATH',None);env.pop('LEAN_SRC_PATH',None)
env['PATH']=str(BIN)+os.pathsep+env['PATH']
A=R/'audit_B2'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True)
commands=[]
for source in [K/'TGLExt/AuditFLRW.lean',R/'probes_B2/BadFLRW00.lean',R/'probes_B2/BadFLRWLambda.lean']:
    put(A/source.name,source.read_bytes())
    cmd=[str(BIN/'lake.exe'),'env','lean',str(source)]
    p=subprocess.run(cmd,cwd=K,env=env,capture_output=True)
    out=A/(source.stem+'.stdout.txt');err=A/(source.stem+'.stderr.txt')
    put(out,p.stdout);put(err,p.stderr)
    commands.append(dict(command=cmd,label=source.stem,returncode=p.returncode,
        source=pin(source),stdout=pin(out),stderr=pin(err)))
    print(source.stem,p.returncode,flush=True)
put(A/'commands.json',json.dumps(commands,ensure_ascii=False,indent=2).encode('utf8'))
text=(A/'AuditFLRW.stdout.txt').read_text(encoding='utf8')
parsed={}
for name,ax in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",text,re.S):
    parsed[name]=[re.sub(r'\.\{[^}]*\}$','',a.strip()) for a in ax.split(',') if a.strip()]
for name in re.findall(r"'([^']+)' does not depend on any axioms",text):parsed[name]=[]
assert set(parsed)==set(names),(set(parsed)-set(names),set(names)-set(parsed))
assert all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in parsed.values())
assert commands[0]['returncode']==0
for c in commands[1:]:
    s=Path(c['stdout']['path']).read_text(encoding='utf8')
    assert c['returncode']!=0 and 'type mismatch' in s.lower(),s
    assert not any(x in s.lower() for x in ['unknown module','object file','unknown identifier'])
custody=json.loads((R/'CUSTODIA_V353_FONTES.json').read_text(encoding='utf8'))
for f in custody['files']:assert pin(K/f['relative'])['sha256']==f['sha256'],f['relative']
assert pin(R/'um.py')['sha256']==custody['sha256']
sources=[];objects=[]
for name in ['FLRWGeometry','FLRWFieldEquations','AuditFLRW']:
    source=K/'TGLExt'/f'{name}.lean';code=source.read_text(encoding='utf8')
    clean=re.sub(r'/-.*?-/', '',code,flags=re.S);clean=re.sub(r'--[^\n]*','',clean)
    assert not re.search(r'\b(sorry|axiom|native_decide|trustCompiler|admit|unsafe)\b',clean)
    sources.append(pin(source));objects.append(pin(K/'.lake/build/lib/lean/TGLExt'/f'{name}.olean'))
data=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),positive_build=pin(attempt/'run.json'),
    sources=sources,objects=objects,targets=targets,axioms=parsed,all_trio=True,
    theorems=sum(t['kind']=='theorem' for t in targets),defs=sum(t['kind']=='def' for t in targets),
    commands=commands,negative_controls_rejected=True,baseline_files_reverified=len(custody['files']),
    copied_um_unchanged=True,canonical_written=False,empirical_work_performed=False,
    scope='FLRW geometry and conditional Friedmann in the existing general chart; no physical calibration derived')
put(R/'AUDITORIA_B2.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(all_trio=True,theorems=data['theorems'],defs=data['defs'],negative_controls_rejected=True)))
