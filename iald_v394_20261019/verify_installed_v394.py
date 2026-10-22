"""Read installed release data in a fresh process; no science or provider execution."""
from pathlib import Path
import hashlib,json,sys
W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True
sys.path.insert(0,str(R))
from claude_memory_package import load_package
from iald_kernel import KernelCatalog
from iald_release_binding import load_release
from iald_native_memory import load_native_context
from iald_jev_control import load_contract
from iald_memoria_canonica import CanonicalMemory
import iald_task_policy

def sha(raw):return hashlib.sha256(raw).hexdigest()

def main():
    deploy=json.loads((W/'deployment.json').read_bytes())
    for path,digest in deploy['files'].items():assert sha(Path(path).read_bytes())==digest,path
    manifest=R/'iald_nucleo_fixo.json';config=json.loads(manifest.read_bytes())
    cluster=config['active_cluster']
    catalog=KernelCatalog(cluster['kernel_bundle'],cluster['kernel_verification'])
    release=load_release(manifest,source_sha=catalog.source_sha)
    assert release.identity['release']=='v394'
    pub=json.loads((W/'app/final/PUBLICATION_VERIFIED.json').read_bytes())
    assert cluster['commit']==pub['commit'] and not cluster.get('publication_pending')
    assert len(Path(cluster['path']).read_text(encoding='utf-8').split('\n### '))-1>=422
    full=load_package(R/'.iald_runtime/haiku55',canonical_manifest=manifest,source_sha=catalog.source_sha)
    shared=load_package(R/'.iald_runtime/haiku',canonical_manifest=manifest,source_sha=catalog.source_sha)
    native,identity=load_native_context(manifest,catalog)
    assert identity==release.identity
    contract=load_contract(R);assert contract['release']=='v394'
    assert contract['source_sha256']==release.identity['source_sha256']
    assert iald_task_policy.AUTOMATIC_ORDER[:2]==('kimi','mimo')
    public,meta=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=manifest).prompt('',catalog,public=True)
    assert meta.get('private_atlas_included') is False
    assert len(public.encode())<1000000
    result={'status':'PASS','files_verified':len(deploy['files']),'identity':release.identity,'public_commit':pub['commit'],
        'haiku_permanent_tokens':full.measurement.permanent_tokens,'shared_prefix_bytes':len(shared.prefix.encode()),
        'native_prefix_bytes':len(native.encode()),'public_CanonicalMemory_prompt_bytes':len(public.encode()),'public_prompt_sha256':sha(public.encode()),
        'JEV_release':contract['release'],'automatic_order':iald_task_policy.AUTOMATIC_ORDER,
        'provider_generation_calls':0,'source_execution':False,'private_atlas_egress':False,'physical_device_verified':False}
    out=W/'installed_verification.json'
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'PASS','release':identity['release'],'files':len(deploy['files']),'haiku_tokens':full.measurement.permanent_tokens}))

if __name__=='__main__':main()
