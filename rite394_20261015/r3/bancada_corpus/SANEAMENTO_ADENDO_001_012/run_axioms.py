from support import *
import subprocess, time, re, sys
sys.stdout.reconfigure(encoding='utf-8')
K=ROOT/'kernel';D=ROOT/'checks'/stamp();D.mkdir(parents=True)
def run(label,p):
 cmd=[str(BIN/'lake.exe'),'env','lean',str(p)]
 atomic(D/'sources'/p.name,p.read_bytes())
 before=digest(p);t=time.monotonic();r=subprocess.run(cmd,cwd=K,env=clean_env(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 atomic(D/(label+'.stdout.txt'),r.stdout);atomic(D/(label+'.stderr.txt'),r.stderr)
 row=dict(label=label,source=str(p),source_sha256=before,source_unchanged=before==digest(p),command=cmd,cwd=str(K),returncode=r.returncode,seconds=time.monotonic()-t,stdout=str(D/(label+'.stdout.txt')),stdout_sha256=digest(D/(label+'.stdout.txt')),stderr=str(D/(label+'.stderr.txt')),stderr_sha256=digest(D/(label+'.stderr.txt')))
 record(D/(label+'.run.json'),row)
 print(label,r.returncode,flush=True)
 return row,(r.stdout+r.stderr).decode('utf-8',errors='replace')
audit,text=run('AuditSanitation',K/'TGLExt/AuditSanitation.lean')
allowed={'propext','Classical.choice','Quot.sound'}
axioms={}
for name,ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text,re.S):
 name=re.sub(r'\.\{[^}]*\}','',name);names=[re.sub(r'\.\{[^}]*\}','',a.strip()) for a in ax.replace('\n',' ').split(',') if a.strip()]
 axioms[name]=names
for name in re.findall(r"'([^']+)' does not depend on any axioms",text):axioms[re.sub(r'\.\{[^}]*\}','',name)]=[]
expected=json.loads((ROOT/'ALVOS_AXIOMAS.json').read_text(encoding='utf-8'))['declarations']
missing=sorted(set(expected)-set(axioms));outside={n:a for n,aa in axioms.items() for a in aa if a not in allowed}
ok=audit['returncode']==0 and not missing and not outside and all(n in axioms for n in expected)
record(D/'AXIOMAS.json',dict(run=audit,expected=expected,parsed=axioms,missing=missing,outside_trio=outside,all_audited_within_trio=ok,union=sorted({a for ax in axioms.values() for a in ax})))
record(ROOT/'AXIOMAS_ATUAL.json',dict(directory=str(D),report=str(D/'AXIOMAS.json'),ok=ok))
print('AXIOMS',ok,'missing',missing,'outside',outside,flush=True)
sys.exit(0 if ok else 1)
