from pathlib import Path
import os,sys,json,hashlib,subprocess,time,datetime,shutil
B=Path(__file__).resolve().parent
A=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\orbital_rotation\attempts\20261016T211651_298033Z")
O=Path(r"C:\IALD\Central de Patentes\work\ordem025\sandbox")
K=Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
LEAN=Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")
def pin(p):return {"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size}
def save(p,v):
 with p.open('xb') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2).encode())
source=B/sys.argv[1]
attempt=B/('attempt_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'));attempt.mkdir()
q=attempt/source.name;shutil.copyfile(source,q)
old=json.loads((A/'RECEIPT.json').read_text(encoding='utf-8-sig'))
cache=json.loads((A/'DEPENDENCY_CACHE.json').read_text(encoding='utf-8-sig'))
checks=[]
for v in json.loads((B/'UNIFIED_DEPENDENCIES.json').read_text(encoding='utf-8')):
 p=Path(v['copy']);h=pin(p)
 if h['sha256']!=v['sha256']:raise RuntimeError('unified changed '+str(p))
 checks.append(h)
for item in cache['copies']:
 p=Path(item['copy']['path']);h=pin(p)
 if h['sha256']!=item['copy']['sha256']:raise RuntimeError('cache changed '+str(p))
 checks.append(h)
# Production dependencies precede the prior O25 copy. Its only changed common
# source is the documented replacement of a comment by the authorized excerpt.
path=str(attempt)+';'+str(B/'unified')+';'+old['LEAN_PATH']
env=dict(os.environ,LEAN_PATH=path)
cmd=[str(LEAN),'-j2','-o',str(q.with_suffix('.olean')),str(q)]
start=datetime.datetime.now(datetime.timezone.utc);ts=time.monotonic()
save(attempt/'START.json',{'start_utc':start.isoformat(),'command':cmd,'LEAN_PATH':path,'source':pin(q),'builder':pin(Path(__file__)),'cache_manifest':pin(A/'DEPENDENCY_CACHE.json'),'dependency_count':len(checks)})
with (attempt/'BUILD.log').open('xb') as f:r=subprocess.run(cmd,cwd=attempt,env=env,stdout=f,stderr=subprocess.STDOUT)
end=datetime.datetime.now(datetime.timezone.utc)
changed=[v['path'] for v in checks if pin(Path(v['path']))['sha256']!=v['sha256']]
log=(attempt/'BUILD.log').read_text(encoding='utf-8',errors='replace')
axioms='\n'.join(l for l in log.splitlines() if 'depends on axioms' in l or 'does not depend on any axioms' in l)
(attempt/'AXIOMS.txt').write_bytes(axioms.encode())
result={'start_utc':start.isoformat(),'end_utc':end.isoformat(),'seconds':time.monotonic()-ts,'command':cmd,'LEAN_PATH':path,'exit_code':r.returncode,'toolchain':subprocess.check_output([str(LEAN),'--version']).decode().strip(),'source':pin(q),'readonly_changed':changed,'artifacts':[pin(attempt/'BUILD.log'),pin(attempt/'AXIOMS.txt')],'axiom_report_count':len(axioms.splitlines()),'contains_sorryAx':'sorryAx' in log,'source_has_sorry':bool(__import__('re').search(r'\bsorry\b',q.read_text(encoding='utf-8')))}
if q.with_suffix('.olean').exists():result['olean']=pin(q.with_suffix('.olean'))
save(attempt/'RESULT.json',result)
print(json.dumps({'attempt':str(attempt),'exit_code':r.returncode,'seconds':result['seconds'],'axiom_report_count':result['axiom_report_count'],'tail':log[-11000:]},ensure_ascii=False))
