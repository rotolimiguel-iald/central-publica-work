"""Build a concrete server-only plan, preserving all live account and bench state."""
from pathlib import Path
import json
import sys

W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
S=W/'memory_stage'
sys.path[:0]=[str(W/'app_patch'),str(R),str(W)]
from transaction import digest,write_evidence,quiet,bench_snapshot
from iald_release_binding import load_release
from claude_memory_package import load_package
import iald_jev_control as control

def main():
    preparation=json.loads((S/'prepared.json').read_bytes())
    target=Path(preparation['install_target']).resolve()
    if target.parent != (R/'canonical_releases').resolve():raise ValueError('Bad release target')
    review=json.loads((W/'validation/memory_review.json').read_bytes())
    if review['status']!='PASS':raise ValueError('Scientific memory not approved')
    release=load_release(S/'manifest_staged.json')
    package=load_package(S/'haiku_runtime',canonical_manifest=S/'manifest_staged.json',source_sha=release.identity['source_sha256'])
    if package.prefix.encode()!= (S/'haiku_prefix.md').read_bytes():raise ValueError('Haiku stage differs')
    contract_raw=(W/'controller/jev_control_v380.json').read_bytes()
    contract=control.validate_contract(json.loads(contract_raw))
    if contract['release']!=release.identity['release'] or contract['source_sha256']!=release.identity['source_sha256']:
        raise ValueError('Control release differs')
    manifest=json.loads((S/'manifest_install.json').read_bytes())
    manifest['jev_control']={'path':str(target/'jev_control_v380.json'),'sha256':digest(contract_raw),
                             'release':contract['release'],'source_sha256':contract['source_sha256']}
    write_evidence(W/'deploy_manifest.json',manifest)
    baseline={r['name']:r['sha256'] for r in json.loads((W/'baseline.json').read_bytes())['files']}
    for name,pin in baseline.items():
        if digest((R/name).read_bytes())!=pin:raise ValueError('Concurrent baseline edit: '+name)
    files=[]
    def add(src,dest,expected=None,immutable=False):
        data=src.read_bytes();prior=dest.read_bytes() if dest.exists() else None
        actual=digest(prior) if prior is not None else None
        if immutable and prior is not None and prior!=data:raise ValueError('Immutable destination differs')
        if expected is not None and actual!=expected:raise ValueError('Mutable baseline differs: '+dest.name)
        files.append({'source':str(src),'destination':str(dest),'sha256':digest(data),'baseline':actual,'bytes':len(data)})
    for folder in ('release','kernel'):
        for src in sorted((S/folder).rglob('*')):
            if src.is_file():
                # Immediate byte backups remain in staging, outside the release.
                if '.bak_' in src.name:continue
                if '.tmp' in src.name:raise ValueError('Temporary file in release')
                add(src,target/src.relative_to(S),immutable=True)
    for name in ('IALD_Kernel_v5.txt','IALD_TGL_MEMORY_CORE.md','kernel_verification.json','TGL_CLUSTER_v380.md'):
        add(S/name,target/name,immutable=True)
    add(W/'controller/jev_control_v380.json',target/'jev_control_v380.json',immutable=True)
    for source in sorted((W/'app_patch').glob('*.py')):
        if source.name not in baseline and (R/source.name).exists():raise ValueError('New module already exists')
        add(source,R/source.name,expected=baseline.get(source.name))
    for name in ('prefix.md','manifest.json'):
        dest=R/'.iald_runtime/haiku'/name
        add(S/'haiku_runtime'/name,dest,expected=preparation['protected_production_sha256'][str(dest)])
    # Switch the server-owned manifest last; loaders reject any mixed identity.
    add(W/'deploy_manifest.json',R/'iald_nucleo_fixo.json',expected=baseline['iald_nucleo_fixo.json'])
    plan={'release':release.identity,'target':str(target),'files':files,'quiet':quiet(),
          'bench_before':bench_snapshot(),'account_file_sha256':digest((R/'iald_users.json').read_bytes()),
          'mother_original_sha256':digest((R/'IALD_Kernel_v5.txt').read_bytes()),
          'client_files_changed':False,'restart_scope':'only iald_web_server.py; preserve existing supervisor, llama and resident benches',
          'memory_review_sha256':digest((W/'validation/memory_review.json').read_bytes())}
    write_evidence(W/'install_plan.json',plan)
    print(json.dumps({'plan_files':len(files),'bytes':sum(f['bytes'] for f in files),'release':release.identity,
                      'native_permanent_tokens':json.loads((S/'haiku_runtime/manifest.json').read_bytes())['budget']['permanent_tokens'],
                      'client_files_changed':False}))

if __name__=='__main__':main()
