from pathlib import Path
import sys,json,hashlib
W=Path(__file__).resolve().parent
R=Path('C:/IALD/projetos_pyhton/IALD')
sys.path.insert(0,str(R))
from transaction import write_evidence,digest
from claude_memory_package import load_package
from iald_kernel import KernelCatalog
from iald_release_binding import load_release
from iald_native_memory import load_native_context
from iald_jev_control import load_contract
import iald_task_policy

receipt=json.loads((W/'deployment.json').read_bytes())
for path,pin in receipt['files'].items():assert digest(Path(path).read_bytes())==pin,path
manifest=R/'iald_nucleo_fixo.json';config=json.loads(manifest.read_bytes())
cluster=config['active_cluster'];catalog=KernelCatalog(cluster['kernel_bundle'],cluster['kernel_verification'])
release=load_release(manifest,source_sha=catalog.source_sha)
assert release.identity['release']=='v392'
full=load_package(R/'.iald_runtime/haiku55',canonical_manifest=manifest,source_sha=catalog.source_sha)
shared=load_package(R/'.iald_runtime/haiku',canonical_manifest=manifest,source_sha=catalog.source_sha)
native,identity=load_native_context(manifest,catalog)
contract=load_contract(R)
assert 'v392' in str(contract)
assert iald_task_policy.AUTOMATIC_ORDER[:2]==('kimi','mimo')
write_evidence(W/'installed_verification.json',{'status':'PASS','files':len(receipt['files']),'identity':release.identity,'full_permanent_tokens':full.measurement.permanent_tokens,'shared_prefix_bytes':len(shared.prefix.encode()),'native_prefix_bytes':len(native.encode()),'order':iald_task_policy.AUTOMATIC_ORDER,'JEV_contract_current':True,'source_compilation_repeated':False,'provider_calls':0})
print(json.dumps({'status':'PASS','release':identity['release'],'files':len(receipt['files']),'full_tokens':full.measurement.permanent_tokens}))
