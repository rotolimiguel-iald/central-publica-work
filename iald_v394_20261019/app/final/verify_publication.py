"""Immutable Git/raw and custody checks; no scientific program execution."""
from pathlib import Path
from urllib.parse import quote,unquote,urlparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib,json,subprocess,sys,urllib.request
F=Path(__file__).resolve().parent;A=F.parent;W=A.parent
P=Path(r'C:\IALD\Artigo\the_boundary');R=Path(r'C:\IALD\projetos_pyhton\IALD')
V=W.parent.parent/'vault/originals_copy/um_unificado_v394'
sys.dont_write_bytecode=True;sys.path.insert(0,str(W));import task
assert task.check('app',actor='codex-v394-app-builder')['ready']
sys.path.insert(0,str(A));from prepare_science import save,write,sha
def git(*args):return subprocess.check_output(['git','-c','safe.directory='+P.as_posix(),'-C',str(P),*args])
commit=git('rev-parse','HEAD').decode().strip()
assert commit==git('rev-parse','origin/main').decode().strip()==git('ls-remote','origin','refs/heads/main').decode().split()[0]
tracked=set(git('ls-files','-z').decode().split('\0'))-{''}
assert tracked<=set(git('ls-tree','-r','--name-only','-z',commit).decode().split('\0'))-{''}
baseline=json.loads((R/'iald_nucleo_fixo.json').read_bytes())
mapping={}
for row in baseline['entries']+[baseline['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]:
    rel=unquote('/'.join(urlparse(row['url']).path.split('/')[4:]));assert rel in tracked
    mapping[row.get('id',Path(row['path']).name)]=rel
proof=json.loads((V/'tgl_kernel_proof_manifest.json').read_bytes())
kernel_rel={}
for name in proof['formal_files_sha256']:
    matches=[x for x in tracked if x.endswith('/Lean/tgl_kernel/'+name)];assert len(matches)==1,(name,len(matches))
    kernel_rel[name]=matches[0]
paths=sorted(set(mapping.values())|set(kernel_rel.values()))
command=['git','-c','safe.directory='+P.as_posix(),'-C',str(P),'cat-file','--batch']
proc=subprocess.run(command,input=''.join(commit+':'+p+'\n' for p in paths).encode(),capture_output=True,check=True)
payload={};at=0
for rel in paths:
    end=proc.stdout.index(b'\n',at);header=proc.stdout[at:end].split();assert header[1]==b'blob'
    size=int(header[2]);at=end+1;raw=proc.stdout[at:at+size];at+=size+1
    assert len(raw)==size;payload[rel]=raw
assert at==len(proc.stdout)
stage=F/'science/memory_stage';rows={}
for rel in sorted(set(mapping.values())):
    raw=payload[rel];name=Path(rel).name
    if (V/name).is_file():assert raw==(V/name).read_bytes(),'Custody mismatch '+name
    save(stage/'release'/rel,raw)
    rows[rel]={'sha256':sha(raw),'bytes':len(raw),'custody_checked':(V/name).is_file(),
        'url':'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+commit+'/'+quote(rel,safe='/')}
kernel=[]
for name,rel in kernel_rel.items():
    raw=payload[rel];assert sha(raw)==proof['formal_files_sha256'][name]
    assert raw==(A/'science/memory_stage/kernel'/name).read_bytes()
    save(stage/'kernel'/name,raw)
    kernel.append({'path':name,'git_path':rel,'sha256':sha(raw),'bytes':len(raw)})
assert len(kernel)==1423
save(stage/'kernel/kernel_manifest.json',(A/'science/memory_stage/kernel/kernel_manifest.json').read_bytes())
for name in ('IALD_Kernel_v5.txt','IALD_TGL_MEMORY_CORE.md','kernel_verification.json','jev_control_v394.json'):
    save(stage/name,(A/'science/memory_stage'/name).read_bytes())
http_paths=set(mapping.values())
for entry in baseline['published_evidence']['hypothesis_sources']:http_paths.add(kernel_rel[entry['catalog_path']])
for name in kernel_rel:
    if name=='_check_damming.lean' or Path(name).name in ('TimeGravitonFlow.lean','TimeGravitonKraus.lean','TimeGravitonMatrix.lean','TimeGravitonScalar.lean','RuleQuadraticResidual.lean','TheBinaryReadingAtTheFixedPoint.lean'):
        http_paths.add(kernel_rel[name])
http_paths.update(rel for name,rel in sorted(kernel_rel.items()) if 'F1Fecho394/' in name and name.endswith('.lean') and len(http_paths)<30)
def fetch(rel):
    url='https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+commit+'/'+quote(rel,safe='/')
    request=urllib.request.Request(url,headers={'User-Agent':'IALD-offline-release-verifier'})
    with urllib.request.urlopen(request,timeout=90) as response:
        raw=response.read();status=response.status
    assert raw==payload[rel] and status==200,'HTTP mismatch '+rel
    return {'git_path':rel,'url':url,'status':status,'bytes':len(raw),'sha256':sha(raw),'matches_verified_git_and_local_source':True}
checks=[]
with ThreadPoolExecutor(max_workers=10) as pool:
    futures=[pool.submit(fetch,p) for p in sorted(http_paths)]
    for future in as_completed(futures):checks.append(future.result())
write(F/'PUBLICATION_VERIFIED.json',{'status':'PUBLIC_IMMUTABLE_COMMIT_VERIFIED','commit':commit,
    'head_origin_tracking_and_remote_equal':True,'paths_derived_from_git_ls_files':True,
    'sources':rows,'kernel_files_git_proof_and_staging_equal':kernel,'kernel_count':len(kernel),
    'http_raw_checks':sorted(checks,key=lambda r:r['git_path']),
    'http_scope':'All release document/evidence inputs plus selected hypothesis/new/supplemental formal files. All1423 formal files exhaustively verified in immutable Git against proof and local bundle; no claim every kernel file fetched via HTTP.',
    'source_executed_or_imported':False,'lean_executed':False,'production_changes':0})
print(json.dumps({'status':'PUBLICATION_VERIFIED','commit':commit,'kernel_files_git_verified':len(kernel),'raw_http_sources_verified':len(checks),'public_document_paths':len(rows)}))
