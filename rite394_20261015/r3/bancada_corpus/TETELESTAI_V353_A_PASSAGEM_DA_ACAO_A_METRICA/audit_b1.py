from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys
R=Path(__file__).resolve().parent
K=R/'kernel'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
 assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True)
 q=p.with_name(p.name+'.tmp');q.write_bytes(b)
 assert q.read_bytes()==b and len(b)>0;os.replace(q,p)
attempt=R/'attempts'/sys.argv[1]
run=json.loads((attempt/'run.json').read_text())
assert run['returncode']==0, 'Positive build is required before adversarial probes.'
s=(K/'TGLExt/TheSameBetaReadsThreeFaces.lean').read_text(encoding='utf8')
names=re.findall(r'^theorem (\w+)',s,re.M)
qualified=['TGLExt.'+n if n=='the_same_beta_reads_three_faces' else 'TGLExt.TGLCoupling.'+n for n in names]
qualified=['TGLExt.TGLCoupling','TGLExt.TGLCoupling.alpha']+qualified
env=os.environ.copy();env.pop('LEAN_PATH',None);env.pop('LEAN_SRC_PATH',None)
env['PATH']=str(BIN)+os.pathsep+env['PATH']
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
A=R/'audit'/stamp;A.mkdir(parents=True)
commands=[]
for file in ['TGLExt/AuditSameBeta.lean','../probes/BadReflection.lean','../probes/BadCost.lean']:
 command=[str(BIN/'lake.exe'),'env','lean',str((K/file).resolve())]
 p=subprocess.run(command,cwd=K,env=env,capture_output=True)
 label=Path(file).stem
 put(A/(label+'.stdout.txt'),p.stdout or b'[empty stdout]\n')
 put(A/(label+'.stderr.txt'),p.stderr or b'[empty stderr]\n')
 commands.append(dict(label=label,command=command,returncode=p.returncode,stdout=str(A/(label+'.stdout.txt')),stderr=str(A/(label+'.stderr.txt'))))
 print(label,p.returncode,flush=True)
text=(A/'AuditSameBeta.stdout.txt').read_text(encoding='utf8')
parsed={}
for name,ax in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",text,re.S):
 parsed[name]=[re.sub(r'\.\{[^}]*\}$','',a.strip()) for a in ax.split(',') if a.strip()]
for name in re.findall(r"'([^']+)' does not depend on any axioms",text):parsed[name]=[]
assert set(parsed)==set(qualified),(parsed,qualified)
assert all(set(a)<= {'propext','Classical.choice','Quot.sound'} for a in parsed.values())
assert commands[0]['returncode']==0
for c in commands[1:]:
 assert c['returncode']!=0
 t=Path(c['stdout']).read_text(encoding='utf8')
 assert 'Type mismatch' in t or 'type mismatch' in t,t
 assert 'unknown module' not in t.lower() and 'object file' not in t.lower(),t
custody=json.loads((R/'CUSTODIA_V353_FONTES.json').read_text(encoding='utf8'))
expected_packages={p['name']:p['rev'] for p in json.loads((K/'lake-manifest.json').read_text())['packages']}
package_records=json.loads((R/'DEPENDENCIAS_LAKE_V353.json').read_text())
assert {p['name']:p['head'] for p in package_records}==expected_packages
assert all(p['returncode']==0 for p in package_records)
for f in custody['files']:
 assert sha(K/f['relative'])==f['sha256'],f['relative']
assert sha(R/'um.py')==custody['sha256']
proof_code=re.sub(r'/-.*?-/', '',s,flags=re.S)
proof_code=re.sub(r'--[^\n]*','',proof_code)
assert not re.search(r'\b(sorry|axiom|native_decide|trustCompiler)\b',proof_code)
assert not re.search(r'0\.012|137\.0|ALPHA_FINE|CODATA',proof_code)
data=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),positive_build=str(attempt/'run.json'),
 commands=commands,axioms=parsed,all_trio=True,theorems=len(names),structures=1,defs=1,
 baseline_files_reverified=len(custody['files']),copied_um_unchanged=True,negative_controls_rejected=True,
 package_revisions_verified=expected_packages,
 source=dict(path=str(K/'TGLExt/TheSameBetaReadsThreeFaces.lean'),sha256=sha(K/'TGLExt/TheSameBetaReadsThreeFaces.lean')),
 object=dict(path=str(K/'.lake/build/lib/lean/TGLExt/TheSameBetaReadsThreeFaces.olean'),sha256=sha(K/'.lake/build/lib/lean/TGLExt/TheSameBetaReadsThreeFaces.olean')))
put(R/'AUDITORIA_B1.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(all_trio=True,theorems=len(names),negative_controls_rejected=True,baseline_files=len(custody['files']))))
