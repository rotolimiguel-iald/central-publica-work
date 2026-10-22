from pathlib import Path
import subprocess,json,datetime,os,re,hashlib
R=Path(__file__).resolve().parent
plan=json.loads((R/'CONTROLES_AUTORAIS_PLANO.json').read_text(encoding='utf8'))
A=R/'author_controls'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
A.mkdir(parents=True)
rows=[]
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
print(str(A),flush=True)
for item in plan:
 m=item['module']; log=A/(m+'.txt')
 with log.open('wb') as so:
  p=subprocess.run([r'C:\Python314\python.exe','-X','utf8','-B',str(R/'dev_lean.py'),m],cwd=R,stdout=so,stderr=subprocess.STDOUT)
 txt=log.read_text(encoding='utf8')
 run_match=re.search(r'^([^\r\n]+\\attempts\\\d+_\d+_\d+)',txt)
 assert run_match,txt
 run=Path(run_match[1]);res=json.loads((run/'RESULT.json').read_text(encoding='utf8'))
 output=(run/'stdout.txt').read_text(encoding='utf8')
 semantic=any(s in output for s in ['Type mismatch','Application type mismatch','unsolved goals','Tactic `rewrite` failed',"'change' tactic failed"])
 bad_infrastructure=any(s in output for s in ['Unknown identifier','Unknown constant','does not exist','unexpected token','failed to synthesize instance','timeout'])
 ok=p.returncode!=0 and res['source_unchanged'] and semantic and not bad_infrastructure
 rows.append(dict(**item,returncode=p.returncode,semantic_rejection=ok,run=pin(run/'RESULT.json'),log=pin(log),source=pin(R/'src/TGLExt'/(m+'.lean'))))
 print(json.dumps(dict(module=m,semantic_rejection=ok,returncode=p.returncode)),flush=True)
data=dict(controls=rows,all_rejected_semantically=all(r['semantic_rejection'] for r in rows))
p=A/'RESULT.json';b=json.dumps(data,ensure_ascii=False,indent=2).encode('utf8')
t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
print(json.dumps(dict(result=pin(p),all_rejected_semantically=data['all_rejected_semantically'])),flush=True)
raise SystemExit(0 if data['all_rejected_semantically'] else 1)
