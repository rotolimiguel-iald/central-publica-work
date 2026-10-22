from pathlib import Path
import json,hashlib,sys,os
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');sys.path.insert(0,str(R));os.environ['TIKTOKEN_CACHE_DIR']=str(R/'.iald_runtime/tokenizer_cache')
from iald_kernel import KernelCatalog
from iald_memoria_canonica import CanonicalMemory

def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():assert p.read_bytes()==b,str(p);return
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b and b;t.replace(p)
p=json.loads((W/'prepared.json').read_bytes());m=json.loads((W/'manifest_staged.json').read_bytes());dest=R/'canonical_releases'/(p['release']+'_'+p['commit'][:12]);assert sha((R/'iald_nucleo_fixo.json').read_bytes())==p['source_manifest_sha256']
for rel,record in p['files'].items():
 b=(W/'release'/rel).read_bytes();assert sha(b)==record['sha256'];save(dest/rel,b)
for name in ('kernel_verification.json','IALD_TGL_MEMORY_CORE.md','TGL_CLUSTER_v378.md'):save(dest/name,(W/'release'/name).read_bytes())
kernel=Path(p['kernel'])
for path in kernel.rglob('*'):
 if path.is_file():save(dest/'kernel'/path.relative_to(kernel),path.read_bytes())
for e in m['entries']+[m['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]:e['path']=str(dest/Path(e['path']).relative_to(W/'release'))
m['operational_core']['path']=str(dest/'IALD_TGL_MEMORY_CORE.md');m['active_cluster'].update(path=str(dest/'TGL_CLUSTER_v378.md'),kernel_bundle=str(dest/'kernel'),kernel_verification=str(dest/'kernel_verification.json'))
save(W/'manifest_install.json',json.dumps(m,ensure_ascii=False,indent=2).encode());catalog=KernelCatalog(dest/'kernel',dest/'kernel_verification.json');metas=[]
for pub in (True,False):
 mem=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=W/'manifest_install.json');text,meta=mem.prompt('',catalog,public=pub);assert meta['published_evidence_checked'];metas.append({'public':pub,'tokens':meta['context_tokens']})
r={'release':p['release'],'destination':str(dest),'manifest_sha256':sha((W/'manifest_install.json').read_bytes()),'kernel_files':len(catalog.records),'contexts':metas,'status':'IMMUTABLE_RELEASE_PREPARED_NOT_ACTIVATED'};save(W/'preinstalled.json',json.dumps(r,indent=2).encode());print(json.dumps(r))
