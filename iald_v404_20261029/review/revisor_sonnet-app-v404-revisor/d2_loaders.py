"""Reviewer (sonnet-app-v404-revisor): installed-release loaders in a FRESH process, own code, audit hook (no network / subprocess / writes / secrets).
Prints one JSON object. The runtime modules are imported read-only; nothing is executed against a provider; no Lean / um.py."""
import os,sys,json,hashlib
from pathlib import Path
R=Path(r'C:\IALD\projetos_pyhton\IALD')
os.environ['TIKTOKEN_CACHE_DIR']=str(R/'.iald_runtime'/'tokenizer_cache')
sys.dont_write_bytecode=True
def guard(event,args):
    if event in('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):raise RuntimeError('blocked '+event)
    if event=='open':
        path,mode,flags=args
        if isinstance(path,int):return
        p=Path(os.fsdecode(path)).resolve()
        if p.name in('.env','iald_stack_v7.py','iald_psion_state.json','.iald_secret_key'):raise RuntimeError('secret input forbidden: '+p.name)
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing:raise RuntimeError('write forbidden: '+str(p))
sys.addaudithook(guard)
sys.path.insert(0,str(R))
sha=lambda b:hashlib.sha256(b).hexdigest()
from claude_memory_package import load_package
from iald_kernel import KernelCatalog
from iald_release_binding import load_release
from iald_native_memory import load_native_context
from iald_jev_control import load_contract
from iald_memoria_canonica import CanonicalMemory
manifest=R/'iald_nucleo_fixo.json'
cfg=json.loads(manifest.read_bytes());cl=cfg['active_cluster']
cat=KernelCatalog(cl['kernel_bundle'],cl['kernel_verification'])
rel=load_release(manifest,source_sha=cat.source_sha)
out={'identity':rel.identity,'kernel_sources':len(cat.records),'kernel_source_sha':cat.source_sha}
pk={}
for name in('haiku55','haiku'):
    p=load_package(R/'.iald_runtime'/name,canonical_manifest=manifest,source_sha=cat.source_sha)
    pk[name]={'permanent_tokens':p.measurement.permanent_tokens,'prefix_bytes':len(p.prefix.encode()),'prefix_sha256':sha(p.prefix.encode()),'model':getattr(p.measurement,'model',None)}
out['packages']=pk
native,ident=load_native_context(manifest,cat)
out['native']={'bytes':len(native.encode()),'sha256':sha(native.encode()),'identity_equals_release':ident==rel.identity}
c=load_contract(R);out['jev']={'release':c['release'],'source_sha256':c['source_sha256']}
public,meta=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=manifest).prompt('',cat,public=True)
out['public_prompt']={'bytes':len(public.encode()),'sha256':sha(public.encode()),'private_atlas_included':meta.get('private_atlas_included'),'atlas_marker_in_text':'<ATLAS_CANONICO' in public}
print(json.dumps(out,ensure_ascii=False))
