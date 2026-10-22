"""Verify the layered data-only publication-label correction in a fresh process."""
from pathlib import Path
import hashlib,json,sys
W=Path(__file__).resolve().parent
P=W/'publication_fix'
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True
sys.path.insert(0,str(R))
from claude_memory_package import load_package
from iald_kernel import KernelCatalog
from iald_release_binding import load_release
from iald_native_memory import load_native_context
from iald_jev_control import load_contract
from iald_memoria_canonica import CanonicalMemory

def main():
    old=json.loads((W/'deployment.json').read_bytes())
    new=json.loads((P/'deployment.json').read_bytes())
    effective={**old['files'],**new['files']}
    for path,digest in effective.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    manifest=R/'iald_nucleo_fixo.json';config=json.loads(manifest.read_bytes())
    cluster=config['active_cluster'];catalog=KernelCatalog(cluster['kernel_bundle'],cluster['kernel_verification'])
    release=load_release(manifest,source_sha=catalog.source_sha)
    pub=json.loads((W/'app/final/PUBLICATION_VERIFIED.json').read_bytes())
    assert release.identity['release']=='v394' and cluster['commit']==pub['commit']
    core=Path(config['operational_core']['path']).read_text(encoding='utf-8')
    assert 'commit PUBLICATION_PENDING' not in core and 'publicação pendente; compilador não reexecutado' not in core
    assert pub['commit'] in core
    full=load_package(R/'.iald_runtime/haiku55',canonical_manifest=manifest,source_sha=catalog.source_sha)
    shared=load_package(R/'.iald_runtime/haiku',canonical_manifest=manifest,source_sha=catalog.source_sha)
    for text in (full.prefix,shared.prefix):
        assert 'commit PUBLICATION_PENDING' not in text
        assert pub['commit'] in text
    native,identity=load_native_context(manifest,catalog);assert identity==release.identity
    assert 'commit PUBLICATION_PENDING' not in native
    contract=load_contract(R);assert contract['release']=='v394'
    prefix,meta=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=manifest).prompt('',catalog,public=True)
    assert 'commit PUBLICATION_PENDING' not in prefix and meta['private_atlas_included'] is False
    data={'status':'PASS','files_verified':len(effective),'patch_files_verified':len(new['files']),
        'identity':release.identity,'public_commit':pub['commit'],'haiku_permanent_tokens':full.measurement.permanent_tokens,
        'shared_prefix_bytes':len(shared.prefix.encode()),'native_prefix_bytes':len(native.encode()),
        'public_CanonicalMemory_prompt_bytes':len(prefix.encode()),'public_prompt_sha256':hashlib.sha256(prefix.encode()).hexdigest(),
        'JEV_release':contract['release'],'source_program_executed':False,'provider_generation_calls':0,
        'old_release_preserved':True,'private_atlas_egress':False,'queue_reactivated':False,'physical_device_verified':False}
    with (P/'installed_verification.json').open('x',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'PASS','files':len(effective),'patch_files':len(new['files']),'haiku_tokens':full.measurement.permanent_tokens}))

if __name__=='__main__':main()
