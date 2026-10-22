"""Compose the reviewed server release, preserving older installed releases."""
from pathlib import Path
import ast,json,hashlib
from prepare_science import W,S,R,C,save,write,sha

def main():
    template=(C/'work/iald_monthly_wallet_20261007/transaction.py').read_bytes()
    assert template.count(b"'client_files_changed':True")==1
    save(W/'transaction.py',template.replace(b"'client_files_changed':True",b"'client_files_changed':False"))
    save(W/'restart_web.ps1',(C/'work/iald_monthly_wallet_20261007/restart_web.ps1').read_bytes())
    stage=S/'memory_stage'
    manifest=json.loads((stage/'manifest_install.json').read_bytes())
    target=Path(manifest['active_cluster']['path']).parent
    pairs=[]
    for folder in ('release','kernel'):
        for path in sorted((stage/folder).rglob('*')):
            if path.is_file():
                assert '.bak_' not in path.name and '.tmp' not in path.name
                pairs.append((path,target/path.relative_to(stage)))
    for name in ('IALD_Kernel_v5.txt','IALD_TGL_MEMORY_CORE.md','TGL_CLUSTER_v392.md','kernel_verification.json','jev_control_v392.json','science_binding.json'):
        pairs.append((stage/name,target/name))
    for source,dest in ((S/'package',R/'.iald_runtime/haiku55'),(S/'shared_count/package',R/'.iald_runtime/haiku')):
        for name in ('prefix.md','manifest.json'):pairs.append((source/name,dest/name))
    for p in sorted((W/'routing/patched').glob('*.py')):pairs.append((p,R/p.name))
    for p in sorted((W/'integration').glob('*.py')):pairs.append((p,R/p.name))
    pairs.append((stage/'manifest_install.json',R/'iald_nucleo_fixo.json'))
    assert len({str(d) for _,d in pairs})==len(pairs)
    rows=[]
    for p,d in pairs:
        raw=p.read_bytes()
        if d.parent==R and d.suffix=='.py':ast.parse(raw)
        rows.append(dict(source=str(p),destination=str(d),sha256=sha(raw),baseline=sha(d.read_bytes()) if d.exists() else None))
    protected=json.loads((stage/'prepared.json').read_bytes())['protected_production_sha256']
    for path,digest in protected.items():assert sha(Path(path).read_bytes())==digest,path
    baseline=json.loads((W/'routing/baseline.json').read_bytes())
    for row in baseline:assert sha((R/row['name']).read_bytes())==row['sha256']
    write(W/'install_plan.json',dict(version=1,unit='F9.APP_STACK_20261014',client_files_changed=False,release='v392',files=rows))
    write(W/'plan_prepared.json',dict(files=len(rows),plan_sha256=sha((W/'install_plan.json').read_bytes()),release=str(target),production_unchanged=True,private_atlas_included=False))
    print(json.dumps(dict(files=len(rows),plan_sha256=sha((W/'install_plan.json').read_bytes()))))

if __name__=='__main__':main()
