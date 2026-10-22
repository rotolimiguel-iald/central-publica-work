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
pairs=json.loads((ROOT/'CONTROLES_PLANO.json').read_text(encoding='utf-8'))
mode='orphans'
results=[]
for pair in pairs:
 good,gt=run('Good'+pair['label'],Path(pair['good']))
 bad,bt=run('Bad'+pair['label'],Path(pair['bad']))
 reject=bool(bad['returncode']!=0 and 'Type mismatch' in bt and not re.search(r'unknown (?:module|identifier|constant)|unexpected token|failed to synthesize|deterministic.*timeout|no such file|file not found',bt,re.I))
 row=dict(**pair,positive=good,negative=bad,semantic_application_refusal=good['returncode']==0 and reject,scope='Aplicacao do fornecedor a conclusao adulterada; nao teorema geral de falsidade de cada variante.')
 results.append(row)
record(D/'CONTROLES.json',results)
ok=all(x['semantic_application_refusal'] for x in results)
record(ROOT/('CONTROLES_'+mode.upper()+'_ATUAL.json'),dict(directory=str(D),report=str(D/'CONTROLES.json'),ok=ok,expected=len(results),passed=sum(x['semantic_application_refusal'] for x in results)))
print('CONTROLS',ok,sum(x['semantic_application_refusal'] for x in results),'/',len(results),flush=True)
sys.exit(0 if ok else 1)
